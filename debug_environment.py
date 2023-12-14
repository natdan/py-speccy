import os.path

import enum
from typing import Optional, Callable

import time

import pygame
from pygame import Surface, Rect

from gui.hexdump import HexDumpComponent
from gui.registers_component import RegistersComponent
from gui.ui_size import UISize
from gui.box_blue_sf_theme import BoxBlueSFThemeFactory
from gui.components import UIAdapter, Collection
from spectrum.keyboard import Keyboard
from spectrum.spectrum import Spectrum
from spectrum.spectrum_bus_access import ZXSpectrum48ClockAndBusAccess
from spectrum.video import COLORS, TSTATES_PER_INTERRUPT, FULL_SCREEN_WIDTH, FULL_SCREEN_HEIGHT, Video, TSTATES_PER_LINE, TSTATES_RETRACE
from utils.playback import Playback

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

        self.playback = Playback(self.spectrum)

        self.video_clock = pygame.time.Clock()

        self.screen: Optional[Surface] = None
        self.pre_screen: Optional[Surface] = None

        self._state = EmulatorState.RUNNING

        self.spectrum_screen_offset = UISize(10, 30)
        self.spectrum_screen_border_width = 3
        self.spectrum_screen_border_color = (64, 192, 64)

        pygame.init()
        self.font = pygame.font.SysFont("Monaco", 20)
        self.small_font = pygame.font.SysFont("Monaco", 15)
        self.zx_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "gui", "zx-spectrum.ttf"), 14)

        self.ui_adapter = UIAdapter(self.screen, do_init=False)
        self.ui_factory = BoxBlueSFThemeFactory(self.ui_adapter, font=self.font, small_font=self.small_font, antialias=True)

        spectrum_screen_size = self.scaled_spectrum_screen_size()
        self.top_component = Collection(Rect(0, 0, spectrum_screen_size[0], spectrum_screen_size[1]))
        self.ui_adapter.top_component = self.top_component
        self.top_component.add_component(self.ui_factory.label(Rect(5, 5, 0, 0), "State: ", font=self.zx_font))
        self.state_label = self.ui_factory.label(Rect(100, 5, 0, 0), self._state.value, font=self.zx_font)
        self.top_component.add_component(self.state_label)
        self.registers_component = RegistersComponent(
            Rect(
                tuple(self.spectrum_screen_offset + (0, spectrum_screen_size[1] + 10)) + (0, 0)
            ),
            self.ui_factory, self.spectrum.z80,
            self.playback
        )
        self.top_component.add_component(self.registers_component)

        self.memory_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 0)) + (380, 200)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["PC"]
        )
        self.top_component.add_component(self.memory_dump)

        self.stack_pointer_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 205)) + (380, 200)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["SP"]
        )
        self.top_component.add_component(self.stack_pointer_dump)

        self.stack_pointer_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 410)) + (380, 200)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["HL", "IX", "IY"]
        )
        self.top_component.add_component(self.stack_pointer_dump)

        self.key_repeat_method: Optional[Callable] = None
        self.key_repeat_method_key_mods = 0
        self.repeat_timer = 0
        self.current_key_mods = 0
        self.step = 1

        self.show_trace = True

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
            pygame.K_LEFT: self.key_left,
            pygame.K_RIGHT: self.key_right
        }

    def scaled_spectrum_screen_size(self) -> UISize:
        return UISize(FULL_SCREEN_WIDTH * self.ratio, FULL_SCREEN_HEIGHT * self.ratio)

    def init(self) -> None:
        icon = pygame.image.load('icon.png')

        self.screen = pygame.display.set_mode(
            size=self.scaled_spectrum_screen_size() + (410, 130),
            flags=pygame.HWSURFACE | pygame.DOUBLEBUF,
            depth=8)
        self.pre_screen = pygame.surface.Surface(
            size=self.scaled_spectrum_screen_size(),
            flags=pygame.HWSURFACE,
            depth=8)
        self.pre_screen.set_palette(COLORS)

        self.spectrum_screen_border_rect()

        self.update_ui()

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    def spectrum_screen_border_rect(self) -> None:
        pygame.draw.rect(
            self.screen, self.spectrum_screen_border_color,
            tuple(self.spectrum_screen_offset - (self.spectrum_screen_border_width, self.spectrum_screen_border_width))
            + (self.scaled_spectrum_screen_size() + (self.spectrum_screen_border_width * 2, self.spectrum_screen_border_width * 2)),
            width=3)

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
        if self.state != EmulatorState.RUNNING and self.show_trace:
            x_offset = self.spectrum_screen_offset[0]
            y_offset = self.spectrum_screen_offset[1]
            if tstates >= TSTATES_PER_INTERRUPT:
                tstates -= TSTATES_PER_INTERRUPT
            if tstates < FULL_SCREEN_HEIGHT * TSTATES_PER_LINE:
                line = tstates // TSTATES_PER_LINE

                line_tstate = tstates - line * TSTATES_PER_LINE

                line *= self.ratio
                fine_line_state = line_tstate
                line_tstate = (line_tstate // 16) * 16
                if line_tstate < TSTATES_PER_LINE - TSTATES_RETRACE:
                    pygame.draw.line(self.screen, (0, 128, 0),
                                     (x_offset, y_offset + line),
                                     (x_offset + FULL_SCREEN_WIDTH * self.ratio, y_offset + line))

                    pygame.draw.line(self.screen, (128, 255, 128),
                                     (x_offset + line_tstate * 2 * self.ratio, y_offset + line),
                                     (x_offset + (line_tstate * 2 + 16) * self.ratio, y_offset + line))
                else:
                    pygame.draw.line(self.screen, (0, 0, 128),
                                     (x_offset, y_offset + line),
                                     (x_offset + FULL_SCREEN_WIDTH * self.ratio, y_offset + line))
                    beam_position = (TSTATES_PER_LINE - fine_line_state) * FULL_SCREEN_WIDTH * self.ratio / TSTATES_RETRACE
                    pygame.draw.circle(self.screen, (0, 0, 140), (x_offset + beam_position, y_offset + line), 4)
            else:
                pygame.draw.line(self.screen, (0, 0, 128),
                                 (x_offset, y_offset),
                                 (x_offset + FULL_SCREEN_WIDTH * self.ratio, y_offset + FULL_SCREEN_HEIGHT * self.ratio),
                                 width=3)
                retrace_states = TSTATES_PER_INTERRUPT - FULL_SCREEN_HEIGHT * TSTATES_PER_LINE
                beam_position_x = (TSTATES_PER_INTERRUPT - tstates) * FULL_SCREEN_WIDTH * self.ratio / retrace_states
                beam_position_y = (TSTATES_PER_INTERRUPT - tstates) * FULL_SCREEN_HEIGHT * self.ratio / retrace_states
                pygame.draw.circle(self.screen, (0, 0, 140), (x_offset + beam_position_x, y_offset + beam_position_y), 4)

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

    def key_left(self, key_mods: int) -> bool:
        if self.state == EmulatorState.PAUSED:
            if key_mods == 0:
                self.playback.restore_previous()
            elif key_mods & pygame.KMOD_SHIFT != 0:
                self.playback.restore_previous(100)
            return True
        return False

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
            elif self.state != EmulatorState.RUNNING:
                self.ui_adapter.process_event(event)

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
        self.spectrum_screen_border_rect()
        self.ui_adapter.draw(self.screen)
        self.update(self.bus_access.frames, self.bus_access.tstates)

    def run(self) -> None:
        try:
            while True:
                if self.state == EmulatorState.RUNNING:
                    while self.state == EmulatorState.RUNNING:
                        self.spectrum.execute(TSTATES_PER_INTERRUPT)
                        self.process_interrupt()
                    self.playback.record()
                elif self.state == EmulatorState.PAUSED:
                    while self.state == EmulatorState.PAUSED:
                        self.update(self.bus_access.frames, self.bus_access.tstates)
                        self.process_keyboard()
                        self.update_ui()
                elif self.state == EmulatorState.ONE_FRAME:
                    self.spectrum.execute(TSTATES_PER_INTERRUPT)
                    self.playback.record()
                    self.process_interrupt()
                    self.state = EmulatorState.PAUSED
                elif self.state == EmulatorState.STEPPING:
                    while self.step != 0 and self.state == EmulatorState.STEPPING:
                        if self.spectrum.execute_one_instruction():
                            self.process_interrupt()
                        if self.step > 0:
                            self.step -= 1
                        self.playback.record()
                    self.spectrum.update_screen()
                    self.update(self.bus_access.frames, self.bus_access.tstates)
                    self.state = EmulatorState.PAUSED

        except KeyboardInterrupt:
            return
