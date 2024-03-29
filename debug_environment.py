import os.path

from typing import Optional, Callable

import time

import pygame
from pygame import Surface, Rect

from emulator_state import EmulatorState
from gui.help_modal import HelpModal
from gui.hexdump import HexDumpComponent
from gui.internal_debug_component import InternalDebugComponent
from gui.modal import Modal
from gui.profile_component import ProfileComponent
from gui.registers_component import RegistersComponent
from gui.spectrum_screen import SpectrumScreen
from gui.ui_size import UISize
from gui.box_blue_sf_theme import BoxBlueSFThemeFactory
from gui.components import UIAdapter
from spectrum.keyboard import Keyboard
from spectrum.spectrum import Spectrum
from spectrum.video import COLORS, TSTATES_PER_INTERRUPT, FULL_SCREEN_WIDTH, FULL_SCREEN_HEIGHT, Video
from utils.playback import Playback

CAPTION = "ZX Spectrum 48k Emulator"
KEY_REPEAT_INITIAL_DELAY = 10
KEY_REPEAT_DELAY = 1


class DebugEnvironment:
    def __init__(self, spectrum: Spectrum, show_fps: bool = True) -> None:
        self.show_fps = show_fps

        self.fast = False
        self.max_fps = False

        self._ratio = 2

        self.spectrum = spectrum
        self.video: Video = spectrum.video
        self.keyboard: Keyboard = spectrum.keyboard

        self.playback = Playback(self.spectrum)

        self.video_clock = pygame.time.Clock()

        self.screen: Optional[Surface] = None
        self.pre_screen: Optional[Surface] = None

        self._state = EmulatorState.RUNNING

        self.spectrum_screen_offset = UISize(10, 30)
        self.spectrum_screen_border_width = 3
        self.spectrum_screen_border_color = (64, 192, 64)

        self.screen_size = self.scaled_spectrum_screen_size() + (710, 130)

        pygame.init()
        self.font = pygame.font.SysFont("Monaco", 20)
        self.small_font = pygame.font.SysFont("Monaco", 15)
        self.zx_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "gui", "zx-spectrum.ttf"), 14)

        self.ui_adapter = UIAdapter(self.screen, do_init=False)
        self.ui_factory = BoxBlueSFThemeFactory(self.ui_adapter, font=self.font, small_font=self.small_font, antialias=True)

        spectrum_screen_size = self.scaled_spectrum_screen_size()
        self.top_component = Modal(Rect(0, 0, self.screen_size[0], self.screen_size[1]))
        self.ui_adapter.top_component = self.top_component

        self.spectrum_screen_component = SpectrumScreen(
            Rect(0, 20, spectrum_screen_size[0] + 10, spectrum_screen_size[1] + 10),
            self.pre_screen,
            self.spectrum,
            self.ratio)
        self.top_component.add_component(self.spectrum_screen_component)

        self.top_component.add_component(self.ui_factory.label(Rect(5, 5, 0, 0), "State: ", font=self.zx_font))
        self.state_label = self.ui_factory.label(Rect(100, 5, 0, 0), self._state.value, font=self.zx_font)
        self.state_label.background_colour = (0, 0, 0)
        self.top_component.add_component(self.state_label)
        self.registers_component = RegistersComponent(
            Rect(
                tuple(self.spectrum_screen_offset + (0, spectrum_screen_size[1] + 10)) + (0, 0)
            ),
            self.ui_factory, self.spectrum.z80
        )
        self.top_component.add_component(self.registers_component)
        self.internal_debug_component = InternalDebugComponent(
            Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, spectrum_screen_size[1] + 10)) + (0, 0)
            ),
            self.ui_factory,
            self.playback
        )
        self.top_component.add_component(self.internal_debug_component)

        self._narrow = True
        self.central_column_width = 240 if self._narrow else 380

        self.memory_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 0)) + (self.central_column_width, 200)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["PC"],
            narrow=self._narrow
        )
        self.top_component.add_component(self.memory_dump)

        self.stack_pointer_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 205)) + (self.central_column_width, 200)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["SP"],
            narrow=self._narrow
        )
        self.top_component.add_component(self.stack_pointer_dump)

        self.stack_pointer_dump = HexDumpComponent(Rect(
                tuple(self.spectrum_screen_offset + (spectrum_screen_size[0] + 10, 410)) + (self.central_column_width, 190)
            ),
            self.ui_factory,
            self.spectrum.z80,
            ["HL", "IX", "IY"],
            narrow=self._narrow
        )
        self.top_component.add_component(self.stack_pointer_dump)

        self.profile_component = ProfileComponent(Rect(
                self.memory_dump.rect.right + 10, self.memory_dump.rect.top,
                self.screen_size[0] - self.memory_dump.rect.right - 15, self.screen_size[1] - self.memory_dump.rect.top - 5
            ),
            self.ui_factory,
            self.spectrum.instructions
        )
        self.top_component.add_component(self.profile_component)

        def close_modal(*_) -> None: self.top_component.hide_modal()

        self._help_modal = HelpModal(self.top_component.rect, ui_factory=self.ui_factory, close_modal=close_modal)

        self._key_repeat_method: Optional[Callable] = None
        self._key_repeat_method_key = 0
        self._key_repeat_method_key_mods = 0
        self._key_repeat_timer = 0
        self._current_key_mods = 0
        self._step = 1

        self._show_trace = True

        self._fast_counter = 0
        self._last_frame = 0
        self._last_tstates = 0
        self._last_time = time.time()
        self.spare_time = [0] * 50

        self.key_down_methods: dict[int, Callable[[int, int], bool]] = {
            pygame.K_F1: self.key_help,
            pygame.K_F2: self.key_pause,
            pygame.K_F6: self.key_profile,
            pygame.K_SLASH: self.key_help,
            pygame.K_LEFT: self.key_left,
            pygame.K_RIGHT: self.key_right
        }

    def scaled_spectrum_screen_size(self) -> UISize:
        return UISize(FULL_SCREEN_WIDTH * self.ratio, FULL_SCREEN_HEIGHT * self.ratio)

    def init(self) -> None:
        icon = pygame.image.load('icon.png')

        self.screen = pygame.display.set_mode(
            size=self.screen_size,
            flags=pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
            depth=8)
        self.pre_screen = pygame.surface.Surface(
            size=self.scaled_spectrum_screen_size(),
            flags=pygame.HWSURFACE,
            depth=8)
        self.pre_screen.set_palette(COLORS)

        self.spectrum_screen_component.surface = self.pre_screen

        self.update_ui()

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    @property
    def ratio(self) -> int: return self._ratio

    @ratio.setter
    def ratio(self, ratio: int) -> None:
        self._ratio = ratio
        self.spectrum_screen_component.ratio = ratio

    @property
    def show_trace(self) -> bool: return self._show_trace

    @show_trace.setter
    def show_trace(self, show_trace: bool) -> None:
        self._show_trace = show_trace
        self.spectrum_screen_component.show_trace = show_trace

    @property
    def state(self) -> EmulatorState: return self._state

    @state.setter
    def state(self, state: EmulatorState) -> None:
        self._state = state
        self.state_label.text = state.value
        self.spectrum_screen_component.state = state

    def update(self, frames: int, tstates: int) -> None:
        pygame.transform.scale(self.spectrum.video.zx_screen_with_border, self.scaled_spectrum_screen_size(), self.pre_screen)

        if self.state == EmulatorState.RUNNING:
            self.spectrum_screen_component.draw(self.screen)
            self.state_label.draw(self.screen)

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
        self.video_clock.tick(200 if self.max_fps else 50)

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

    def key_left(self, _: int, key_mods: int) -> bool:
        if self.state == EmulatorState.PAUSED:
            if key_mods & pygame.KMOD_SHIFT != 0:
                self.playback.restore_previous(100)
            else:
                self.playback.restore_previous()

            return True
        return False

    def key_right(self, _: int, key_mods: int) -> bool:
        if self.state == EmulatorState.PAUSED:
            if key_mods & pygame.KMOD_SHIFT != 0:
                self._step = 100
                self.state = EmulatorState.STEPPING
            elif key_mods & pygame.KMOD_CTRL != 0:
                self._step = -1
                self.state = EmulatorState.STEPPING
            elif key_mods & pygame.KMOD_ALT != 0:
                self.state = EmulatorState.ONE_FRAME
            else:
                self._step = 1
                self.state = EmulatorState.STEPPING
            return True
        return False

    def key_profile(self, _: int, _key_mods: int) -> bool:
        if self.state == EmulatorState.PAUSED:
            self.state = EmulatorState.PROFILE
        return False

    def key_help(self, _: int, _key_mods: int) -> bool:
        if self.top_component.modal_component:
            self.top_component.hide_modal()
        else:
            self.top_component.show_modal(self._help_modal, update_rect=False)
        return False

    def key_pause(self, _: int, _key_mods: int) -> bool:
        self.state = EmulatorState.RUNNING if self.state == EmulatorState.PAUSED else EmulatorState.PAUSED
        if self.state == EmulatorState.PAUSED:
            self.playback.reset()
            self.playback.record()
            self.spectrum.profile(TSTATES_PER_INTERRUPT)
            self.playback.restore_first()
            self.profile_component.set_tstates(self.spectrum.bus_access.tstates)
            self.profile_component.redraw()
        return False

    def process_keyboard(self) -> None:
        pygame.event.pump()
        self._current_key_mods = pygame.key.get_mods()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.top_component.modal_component and event.key != pygame.K_F1:
                    self.top_component.hide_modal()

                key_down_method = self.key_down_methods.get(event.key)
                if key_down_method is not None:
                    if key_down_method(event.key, self._current_key_mods):
                        # This method can be repeated after timeout
                        self._key_repeat_method = key_down_method
                        self._key_repeat_method_key_mods = self._current_key_mods
                        self._key_repeat_timer = KEY_REPEAT_INITIAL_DELAY
                        self._key_repeat_method_key = event.key
                    else:
                        self._key_repeat_timer = 0

                if self.state == EmulatorState.RUNNING:
                    self.keyboard.do_key(True, event.key, self._current_key_mods)
            elif event.type == pygame.KEYUP:
                self._key_repeat_timer = 0
                if self.state == EmulatorState.RUNNING:
                    self.keyboard.do_key(False, event.key, self._current_key_mods)
            elif event.type == pygame.QUIT:
                raise KeyboardInterrupt()
            elif event.type == pygame.VIDEORESIZE:
                old_surface = self.screen
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # On the next line, if only part of the window
                # needs to be copied, there's some other options.
                self.screen.blit(old_surface, (0, 0))
                del old_surface
            elif self.state != EmulatorState.RUNNING:
                self.ui_adapter.process_event(event)

        if self._key_repeat_timer > 0:
            self._key_repeat_timer -= 1
            if self._key_repeat_timer == 0:
                self._key_repeat_timer = KEY_REPEAT_DELAY
                self._key_repeat_method(self._key_repeat_method_key, self._key_repeat_method_key_mods)

    def process_interrupt(self) -> None:
        self.spectrum.end_frame()
        self.process_keyboard()
        if self.state != EmulatorState.RUNNING:
            self.update_ui()
        else:
            self.update(self.spectrum.bus_access.frames, self.spectrum.bus_access.tstates)

    def update_ui(self) -> None:
        self.screen.fill((0, 0, 0))
        self.ui_adapter.draw(self.screen)
        self.update(self.spectrum.bus_access.frames, self.spectrum.bus_access.tstates)

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
                        self.profile_component.set_tstates(self.spectrum.bus_access.tstates)
                        self.update_ui()
                        self.process_keyboard()
                elif self.state == EmulatorState.ONE_FRAME:
                    self.spectrum.execute(TSTATES_PER_INTERRUPT)
                    self.playback.reset()
                    self.process_interrupt()
                    self.state = EmulatorState.PAUSED
                # elif self.state == EmulatorState.PROFILE:
                #     self.spectrum.profile(TSTATES_PER_INTERRUPT)
                #     self.playback.reset()
                #     self.process_interrupt()
                #     self.state = EmulatorState.PAUSED
                elif self.state == EmulatorState.STEPPING:
                    while self._step != 0 and self.state == EmulatorState.STEPPING:
                        if self.spectrum.execute_one_instruction():
                            self.process_interrupt()
                        if self._step > 0:
                            self._step -= 1
                        self.playback.record()
                    self.profile_component.set_tstates(self.spectrum.bus_access.tstates)
                    self.spectrum.update_screen()
                    self.update(self.spectrum.bus_access.frames, self.spectrum.bus_access.tstates)
                    self.state = EmulatorState.PAUSED

        except KeyboardInterrupt:
            return
