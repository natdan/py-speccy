from typing import Optional

import pygame
from pygame import Surface, Rect

from gui.components import Collection, BaseUIFactory, TopDownLayout, LeftRightLayout
from z80.instructions import Instruction

SEPARATOR_HEIGHT = 3


class ProfileComponent(Collection):
    def __init__(self, rect: Optional[Rect], ui_factory: BaseUIFactory, instructions: list[Instruction]) -> None:
        super().__init__(rect)
        self._ui_factory = ui_factory
        self._surface: Optional[Surface] = None
        self.instructions = instructions
        self.tstates = 0
        self.top_line_height = self._ui_factory.small_font.get_linesize()
        self.line_height = self._ui_factory.small_font.get_linesize()
        self.header = Collection(Rect(0, 0, rect.width, self.line_height), layout=LeftRightLayout())
        self.header_label = ui_factory.label(Rect(0, 0, 30, self.line_height), "Profile", font=ui_factory.small_font)
        self.header.add_component(self.header_label)
        self.add_component(self.header)
        self.lines = Collection(rect, layout=TopDownLayout())
        self.lines_offset = self.line_height + SEPARATOR_HEIGHT * 2
        self.profile = Collection(rect, layout=TopDownLayout())
        self.redefine_rect(rect)

    def set_tstates(self, tstates: int) -> None:
        if self.tstates != tstates:
            self.tstates = tstates
            self._surface = self._render()

    def redefine_rect(self, rect: Rect) -> None:
        super().redefine_rect(rect)

        local_rect = Rect(0, 0, rect.width, rect.height)

        self.header.redefine_rect(Rect(rect.x, rect.y, rect.width, self.top_line_height))

        self.lines.redefine_rect(Rect(
            local_rect.x, local_rect.y + self.lines_offset,
            local_rect.width, local_rect.height - self.top_line_height - self.lines_offset - 6 * self.line_height - SEPARATOR_HEIGHT * 2)
        )

        self.profile.redefine_rect(Rect(
            local_rect.x, self.lines.rect.bottom,
            local_rect.width, local_rect.height - self.lines.rect.height - self.lines_offset)
        )

        def update_lines(component: Collection) -> None:
            number_of_lines = (component.rect.height - self.line_height - SEPARATOR_HEIGHT * 2) // self.line_height
            while len(component.components) > number_of_lines:
                del component.components[-1]

            while len(component.components) < number_of_lines:
                y = component.rect.y + len(component.components) * self.line_height
                component.add_component(
                    self._ui_factory.label(
                        Rect(local_rect.x, y, local_rect.width, self.line_height),
                        "",
                        font=self._ui_factory.small_font
                    ))

        update_lines(self.lines)
        update_lines(self.profile)

    def _render(self) -> Surface:
        error = False
        found = False
        selected_index = 0
        while selected_index < len(self.instructions) and not error and not found:
            if self.tstates == self.instructions[selected_index].tstates:
                found = True
            elif self.tstates < self.instructions[selected_index].tstates:
                error = True
            selected_index += 1

        if self._surface is None:
            self._surface = Surface((self.rect.width, self.rect.height), flags=pygame.HWSURFACE)
        else:
            self._surface.fill(self._ui_factory.background_colour)

        middle_line = len(self.lines.components) // 2

        if not found:
            for i in range(len(self.lines.components)):
                self.lines.components[i].text = ""
            # self.lines.components[middle_line].text = "Error profiling"
            # self.lines.components[middle_line + 1].text = f"my: {self.tstates}"
            # if 0 <= selected_index < len(self.instructions):
            #     self.lines.components[middle_line + 2].text = f"found: {self.instructions[selected_index].tstates}"
            # else:
            #     self.lines.components[middle_line + 2].text = f"len={len(self.instructions)}"
            #     self.lines.components[middle_line + 3].text = f"selected_index={selected_index}"
            #     if selected_index == len(self.instructions) and len(self.instructions) > 0:
            #         self.lines.components[middle_line + 4].text = f"last_tstates={self.instructions[selected_index - 1].tstates}"
        else:
            line_index = selected_index - middle_line - 1

            for i in range(len(self.lines.components)):
                if line_index < 0 or line_index >= len(self.instructions):
                    self.lines.components[i].text = ""
                else:
                    instruction = self.instructions[line_index]
                    s = instruction.to_str(2)
                    l = len(s)
                    if l < 19:
                        s += " " * (19 - l)

                    has_delay = any(p for p in instruction.profile if p.delay > 0)
                    # self.lines.components[i].text = f"0x{instruction.address:04x} ({instruction.tstates:05d}): {s} {'*' if has_delay else ''}{' '.join(str(p) for p in instruction.profile)}"
                    self.lines.components[i].text = f"0x{instruction.address:04x}: {s}"

                line_index += 1

            middle_mine_rect = self.lines.components[middle_line].rect
            pygame.draw.rect(self._surface, (64, 64, 64),
                             (middle_mine_rect.x, middle_mine_rect.y, middle_mine_rect.width, middle_mine_rect.height))

            instruction = self.instructions[selected_index]
            for i in range(len(self.profile.components)):
                if i < len(instruction.profile):
                    self.profile.components[i].text = instruction.profile[i].to_str()
                else:
                    self.profile.components[i].text = ""

        self.lines.draw(self._surface)
        self.profile.draw(self._surface)

        pygame.draw.rect(self._surface, self._ui_factory.colour, (0, self.lines_offset - SEPARATOR_HEIGHT, self.rect.right, 3))

        pygame.draw.rect(self._surface, self._ui_factory.colour, (self.profile.rect.x, self.profile.rect.y - SEPARATOR_HEIGHT, self.profile.rect.width, 1))

        return self._surface

    def redraw(self) -> None:
        self._surface = self._render()

    def draw(self, surface) -> None:
        if self._surface is None:
            self._surface = self._render()
        surface.blit(self._surface, (self.rect.x, self.rect.y))
        self.header.draw(surface)
