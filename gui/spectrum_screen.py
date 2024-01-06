import pygame
from pygame import Rect, Surface

from emulator_state import EmulatorState
from gui.components import Component
from gui.ui_size import UISize
from spectrum.spectrum import Spectrum
from spectrum.video import FULL_SCREEN_WIDTH, TSTATES_VERTICAL_RETRACE, FULL_SCREEN_HEIGHT, TSTATES_PER_LINE, TSTATES_HORIZONTAL_RETRACE, TSTATES_LEFT_BORDER, TSTATES_PER_INTERRUPT


MARGIN = 6


class SpectrumScreen(Component):
    def __init__(self, rect: Rect, surface: Surface, spectrum: Spectrum, ratio: int) -> None:
        super().__init__(rect)
        self._surface = surface
        self.ratio = ratio
        self.spectrum = spectrum
        self.show_trace = True
        self.state = EmulatorState.RUNNING
        self._spectrum_screen_border_width = 3
        self._spectrum_screen_border_color = (64, 192, 64)
        if self._surface is not None:
            self._surface_size = UISize(self._surface.get_size()[0], self._surface.get_size()[1])
            self.redefine_rect(rect)

    @property
    def surface(self) -> Surface: return self._surface

    @surface.setter
    def surface(self, surface: Surface) -> None:
        self._surface = surface
        self._surface_size = UISize(self._surface.get_size()[0], self._surface.get_size()[1])
        self.redefine_rect(self.rect)

    def redefine_rect(self, rect: Rect) -> None:
        self.rect = Rect(rect.x, rect.y, self._surface_size[0] + MARGIN * 2, self._surface_size[1] + MARGIN * 2)

    def draw(self, surface) -> None:
        x = self.rect.x + MARGIN
        y = self.rect.y + MARGIN

        if self.state != EmulatorState.RUNNING:
            border_width = self._spectrum_screen_border_width
            pygame.draw.rect(
                surface, self._spectrum_screen_border_color,
                Rect(
                    x - border_width, y - border_width,
                    self._surface_size[0] + border_width * 2, self._surface_size[1] + border_width * 2
                ),
                width=3)

        surface.blit(self.surface, (x, y))
        if self.state != EmulatorState.RUNNING and self.show_trace:
            tstates = self.spectrum.bus_access.tstates
            if tstates >= TSTATES_PER_INTERRUPT:
                tstates -= TSTATES_PER_INTERRUPT

            if TSTATES_VERTICAL_RETRACE <= tstates:
                local_ts = tstates - TSTATES_VERTICAL_RETRACE + TSTATES_LEFT_BORDER  # to correct for where the border happens
                line = local_ts // TSTATES_PER_LINE
                line_tstate = local_ts - line * TSTATES_PER_LINE

                line *= self.ratio
                fine_line_state = line_tstate
                line_tstate = (line_tstate // 16) * 16
                if line_tstate < TSTATES_PER_LINE - TSTATES_HORIZONTAL_RETRACE:
                    pygame.draw.line(surface, (0, 128, 0),
                                     (x, y + line),
                                     (x + FULL_SCREEN_WIDTH * self.ratio, y + line))

                    pygame.draw.line(surface, (128, 255, 128),
                                     (x + line_tstate * 2 * self.ratio, y + line),
                                     (x + (line_tstate * 2 + 16) * self.ratio, y + line))
                else:
                    pygame.draw.line(surface, (0, 0, 128),
                                     (x, y + line),
                                     (x + FULL_SCREEN_WIDTH * self.ratio, y + line))
                    beam_position = (TSTATES_PER_LINE - fine_line_state) * FULL_SCREEN_WIDTH * self.ratio / TSTATES_HORIZONTAL_RETRACE
                    pygame.draw.circle(surface, (0, 0, 140), (x + beam_position, y + line), 4)
            else:
                pygame.draw.line(surface, (0, 0, 128),
                                 (x, y),
                                 (x + FULL_SCREEN_WIDTH * self.ratio, y + FULL_SCREEN_HEIGHT * self.ratio),
                                 width=3)
                beam_position_x = (TSTATES_VERTICAL_RETRACE - tstates) * FULL_SCREEN_WIDTH * self.ratio / TSTATES_VERTICAL_RETRACE
                beam_position_y = (TSTATES_VERTICAL_RETRACE - tstates) * FULL_SCREEN_HEIGHT * self.ratio / TSTATES_VERTICAL_RETRACE
                pygame.draw.circle(surface, (0, 0, 140), (x + beam_position_x, y + beam_position_y), 4)
