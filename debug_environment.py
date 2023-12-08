import os.path

import enum
from typing import Optional, Callable

import time

import pygame
from pygame import Surface, Rect

from gui.registers_gui import RegistersGUI
from gui.ui_size import UISize
from pyros_support_ui.box_blue_sf_theme import BoxBlueSFThemeFactory
from pyros_support_ui.components import UIAdapter, Collection
from spectrum.keyboard import Keyboard
from spectrum.spectrum import Spectrum
from spectrum.spectrum_bus_access import ZXSpectrum48ClockAndBusAccess
from spectrum.video import COLORS, TSTATES_PER_INTERRUPT, FULL_SCREEN_WIDTH, FULL_SCREEN_HEIGHT, Video

CAPTION = "ZX Spectrum 48k Emulator"
KEY_REPEAT_INITIAL_DELAY = 10
KEY_REPEAT_DELAY = 1


class EmulatorState(enum.Enum):
    RUNNING = "RUNNING"
    ONE_FRAME = "ONE FRAME"
    STEPPING = "STEPPING"
    PAUSED = "PAUSED"


class DebugEnvironment:
    def __init__(self, spectrum: Spectrum, show_fps: bool = True) -> None:
        self.show_fps = show_fps
        self.ratio = 2

        self.spectrum = spectrum
        self.video: Video = spectrum.video
        self.keyboard: Keyboard = spectrum.keyboard
        self.bus_access: ZXSpectrum48ClockAndBusAccess = spectrum.bus_access

        self.video_clock = pygame.time.Clock()

        self.screen: Optional[Surface] = None
        self.pre_screen: Optional[Surface] = None

        self._state = EmulatorState.RUNNING

        self.spectrum_screen_offset = UISize(10, 30)
        self.spectrum_screen_border_width = 3
        self.spectrum_screen_border_color = (64, 192, 64)

        pygame.init()
        self.font = pygame.font.SysFont("Monaco", 20)
        self.zx_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "gui", "zx-spectrum.ttf"), 14)

        self.ui_adapter = UIAdapter(self.screen, do_init=False)
        self.ui_factory = BoxBlueSFThemeFactory(self.ui_adapter, font=self.font, antialias=True)
        self.top_component = Collection(self.scaled_spectrum_screen_size())
        self.ui_adapter.top_component = self.top_component
        self.top_component.add_component(self.ui_factory.label(Rect(5, 5, 0, 0), "State: ", font=self.zx_font))
        self.state_label = self.ui_factory.label(Rect(100, 5, 0, 0), self._state.value, font=self.zx_font)
        self.top_component.add_component(self.state_label)
        self.registers = RegistersGUI(
            Rect(
                tuple(self.spectrum_screen_offset + (0, self.scaled_spectrum_screen_size()[1] + 10)) + (0, 0)
            ),
            self.ui_factory, self.spectrum.z80
        )
        self.top_component.add_component(self.registers)

        self.key_repeat_method: Optional[Callable] = None
        self.key_repeat_method_key_mods = 0
        self.repeat_timer = 0
        self.current_key_mods = 0
        self.step = 1

        self.fast = False
        self.show_fps = True
        self.fast = False
        self._fast_counter = 0
        self._last_frame = 0
        self._last_tstates = 0
        self._last_time = time.time()
        self.spare_time = [0] * 50

        self.key_down_methods: dict[int, Callable[[int], bool]] = {
            pygame.K_F1: self.key_pause,
            pygame.K_RIGHT: self.key_right
        }

    def scaled_spectrum_screen_size(self) -> UISize:
        return UISize(FULL_SCREEN_WIDTH * self.ratio, FULL_SCREEN_HEIGHT * self.ratio)

    def init(self) -> None:
        icon = pygame.image.load('icon.png')

        self.screen = pygame.display.set_mode(
            size=self.scaled_spectrum_screen_size() + (200, 130),
            flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
            depth=8)
        self.pre_screen = pygame.surface.Surface(
            size=self.scaled_spectrum_screen_size(),
            flags=pygame.HWSURFACE,
            depth=8)
        self.pre_screen.set_palette(COLORS)

        pygame.draw.rect(
            self.screen, self.spectrum_screen_border_color,
            tuple(self.spectrum_screen_offset - (self.spectrum_screen_border_width, self.spectrum_screen_border_width))
            + (self.scaled_spectrum_screen_size() + (self.spectrum_screen_border_width * 2, self.spectrum_screen_border_width * 2)),
            width=3)

        self.update_ui()

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    @property
    def state(self) -> EmulatorState: return self._state

    @state.setter
    def state(self, state: EmulatorState) -> None:
        self._state = state
        self.state_label.text = state.value
        # if self.state == EmulatorState.RUNNING and self.screen is not None:
        #     self.ui_adapter.draw(self.screen)

    def update(self, frames: int, tstates: int) -> None:
        pygame.transform.scale(self.spectrum.video.zx_screen_with_border, self.scaled_spectrum_screen_size(), self.pre_screen)
        self.screen.blit(self.pre_screen, self.spectrum_screen_offset)

        video_frame = False
        if self.fast:
            if self._fast_counter <= 0:
                self.video_clock.tick(50)
                pygame.display.flip()
                self._fast_counter = 200
                video_frame = True
            self._fast_counter -= 1
        else:
            video_frame = True

        now = time.time()
        self.video_clock.tick(50)

        if video_frame:
            if self.show_fps:
                total_tstates = (frames - self._last_frame) * TSTATES_PER_INTERRUPT + (tstates - self._last_tstates)
                speed = (total_tstates / (TSTATES_PER_INTERRUPT * (now - self._last_time) * 50)) * 100

                self._last_frame = frames
                self._last_tstates = tstates
                self._last_time = now

                time_difference = time.time() - now
                self.spare_time[0:-1] = self.spare_time[1:]
                self.spare_time[-1] = int(time_difference * 100000 / 20)
                spare_time = int(sum(self.spare_time) / len(self.spare_time))

                if self.fast:
                    pygame.display.set_caption(f'{CAPTION} - {self.video_clock.get_fps():.2f} FPS, Speed: {speed:0.1f}%')
                elif self.state == EmulatorState.RUNNING:
                    pygame.display.set_caption(f'{CAPTION} - {self.video_clock.get_fps():.2f} FPS, {spare_time: 4}%')
                else:
                    pygame.display.set_caption(f'{CAPTION} - PAUSED')

            pygame.display.flip()

    def key_right(self, key_mods: int) -> bool:
        if self.state == EmulatorState.PAUSED:
            if key_mods == 0:
                self.step = 1
                self.state = EmulatorState.STEPPING
            elif key_mods & pygame.KMOD_SHIFT != 0:
                self.step = 100
                self.state = EmulatorState.STEPPING
            elif key_mods & pygame.KMOD_CTRL != 0:
                self.step = -1
                self.state = EmulatorState.STEPPING
            elif key_mods & pygame.KMOD_ALT != 0:
                self.state = EmulatorState.ONE_FRAME
            return True
        return False

    def key_pause(self, _key_mods: int) -> bool:
        self.state = EmulatorState.RUNNING if self.state == EmulatorState.PAUSED else EmulatorState.PAUSED
        return False

    def process_keyboard(self) -> None:
        pygame.event.pump()
        self.current_key_mods = pygame.key.get_mods()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_down_method = self.key_down_methods.get(event.key)
                if key_down_method is not None:
                    if key_down_method(self.current_key_mods):
                        # This method can be repeated after timeout
                        self.key_repeat_method = key_down_method
                        self.key_repeat_method_key_mods = self.current_key_mods
                        self.repeat_timer = KEY_REPEAT_INITIAL_DELAY
                    else:
                        self.repeat_timer = 0

                if self.state == EmulatorState.RUNNING:
                    self.keyboard.do_key(True, event.key, self.current_key_mods)
            elif event.type == pygame.KEYUP:
                self.repeat_timer = 0
                if self.state == EmulatorState.RUNNING:
                    self.keyboard.do_key(False, event.key, self.current_key_mods)
            elif event.type == pygame.QUIT:
                raise KeyboardInterrupt()

        if self.repeat_timer > 0:
            self.repeat_timer -= 1
            if self.repeat_timer == 0:
                self.repeat_timer = KEY_REPEAT_DELAY
                self.key_repeat_method(self.key_repeat_method_key_mods)

    def process_interrupt(self) -> None:
        self.spectrum.end_frame()
        self.process_keyboard()
        if self.state != EmulatorState.RUNNING:
            self.update_ui()
        else:
            self.update(self.bus_access.frames, self.bus_access.tstates)

    def update_ui(self) -> None:
        self.screen.fill((0, 0, 0))
        self.ui_adapter.draw(self.screen)
        self.update(self.bus_access.frames, self.bus_access.tstates)

    def run(self) -> None:
        try:
            while True:
                while self.state == EmulatorState.RUNNING:
                    self.spectrum.execute(TSTATES_PER_INTERRUPT)
                    self.process_interrupt()
                while self.state == EmulatorState.PAUSED:
                    self.update(self.bus_access.frames, self.bus_access.tstates)
                    self.process_keyboard()
                    self.update_ui()
                if self.state == EmulatorState.ONE_FRAME:
                    self.spectrum.execute(TSTATES_PER_INTERRUPT)
                    self.process_interrupt()
                    self.state = EmulatorState.PAUSED
                elif self.state == EmulatorState.STEPPING:
                    while self.step != 0 and self.state == EmulatorState.STEPPING:
                        if self.spectrum.execute_one_instruction():
                            self.process_interrupt()
                        if self.step > 0:
                            self.step -= 1
                    self.spectrum.update_video()
                    self.update(self.bus_access.frames, self.bus_access.tstates)
                    self.state = EmulatorState.PAUSED

        except KeyboardInterrupt:
            return
