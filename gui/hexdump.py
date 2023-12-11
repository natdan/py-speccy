import functools

import pygame
from typing import Optional

from pygame import Rect, Surface

from gui.components import BaseUIFactory, Collection, LeftRightLayout, TopDownLayout, ALIGNMENT, UiHint, BorderDecoration, Component
from z80.z80 import Z80

SEPARATOR_HEIGHT = 3


class HexDumpComponent(Collection):
    def __init__(self, rect: Rect, ui_factory: BaseUIFactory, z80: Z80, registers: list[str]) -> None:
        super().__init__(rect)
        self._ui_factory = ui_factory
        self.z80 = z80
        self.last_memory_address = -1
        self.selected_register_name = registers[0]
        self._surface: Optional[Surface] = None
        self.top_line_height = self._ui_factory.small_font.get_linesize()
        self.line_height = self._ui_factory.small_font.get_linesize()
        self.header = Collection(Rect(0, 0, rect.width, self.line_height), layout=LeftRightLayout())
        self.header_label = ui_factory.label(Rect(0, 0, 30, self.line_height), registers[0], font=ui_factory.small_font)
        self.header.add_component(self.header_label)
        self.add_component(self.header)
        self.register_selection = Collection(
            Rect(0, 0, rect.width - self.header_label.rect.width, self.line_height),
            layout=LeftRightLayout(4, h_alignment=ALIGNMENT.RIGHT))
        self.header.add_component(self.register_selection)
        if len(registers) > 1:
            for register_name in registers:
                def select_register(name: str, *_args) -> None:
                    self.selected_register_name = name
                    self._surface = None

                button_rect = Rect(rect.x, rect.y, 34, rect.height)
                register_button = ui_factory.button(
                    button_rect,
                    on_click=functools.partial(select_register, register_name),
                    label=self._ui_factory.label(button_rect, " " + register_name, font=self._ui_factory.small_font),
                    hint=UiHint.NO_DECORATION
                )
                register_button.background_decoration = BorderDecoration(None, self._ui_factory.colour)
                self.register_selection.add_component(register_button)
        self.lines = Collection(rect, layout=TopDownLayout())
        self.lines_offset = self.line_height + SEPARATOR_HEIGHT * 2
        self.redefine_rect(rect)

    def redefine_rect(self, rect: Rect) -> None:
        super().redefine_rect(rect)

        local_rect = Rect(0, 0, rect.width, rect.height)

        self.header.redefine_rect(Rect(rect.x, rect.y, rect.width, self.top_line_height))

        self.lines.redefine_rect(Rect(local_rect.x, local_rect.y + self.lines_offset, local_rect.width, local_rect.height - self.top_line_height - self.lines_offset))

        number_of_lines = (local_rect.height - self.line_height - SEPARATOR_HEIGHT * 2) // self.line_height
        while len(self.lines.components) > number_of_lines:
            del self.lines.components[-1]

        while len(self.lines.components) < number_of_lines:
            y = self.header.rect.height + SEPARATOR_HEIGHT * 2 + len(self.lines.components) * self.line_height
            self.lines.add_component(
                self._ui_factory.label(
                    Rect(local_rect.x, y, local_rect.width, self.line_height),
                    "---------------",
                    font=self._ui_factory.small_font
                ))

    def _get_register_value(self) -> int:
        value = getattr(self.z80, "reg" + self.selected_register_name, None)
        if value is None:
            value = getattr(self.z80, "get_reg_" + self.selected_register_name)()
        return value

    def _render(self) -> Surface:
        def byte_to_char(b: int) -> str:
            if 32 <= b < 128:
                return chr(b)
            return "."
        if self._surface is None:
            self._surface = Surface((self.rect.width, self.rect.height), flags=pygame.HWSURFACE)
        else:
            self._surface.fill(self._ui_factory.background_colour)
        middle_line = len(self.lines.components) // 2
        register_value = self._get_register_value()
        addr = register_value - middle_line * 8

        middle_mine_rect = self.lines.components[middle_line].rect
        pygame.draw.rect(self._surface, (64, 64, 64),
                         (0, middle_mine_rect.y, middle_mine_rect.left, middle_mine_rect.height))

        line = 0
        for a in range(addr, addr + len(self.lines.components) * 8, 8):
            if 0 <= a < 65536 - 8:
                text = f"0x{a:04x}: " + \
                    ",".join([f"{self.z80.memory.peekb(a + i):02x}" for i in range(8)]) + \
                    " |" + "".join([byte_to_char(self.z80.memory.peekb(a + i)) for i in range(8)]) + "|"
                self.lines.components[line].text = text
            else:
                self.lines.components[line].text = ""
            line += 1

        pygame.draw.rect(self._surface, (64, 64, 64),
                         (0, middle_mine_rect.y, middle_mine_rect.width, middle_mine_rect.height))

        # self.header.draw(self._surface)
        self.lines.draw(self._surface)

        pygame.draw.rect(self._surface, self._ui_factory.colour,
                         (0, self.lines_offset - SEPARATOR_HEIGHT, self.rect.right, 3))

        self.last_memory_address = addr
        return self._surface

    def draw(self, surface) -> None:
        if self._surface is None or self.last_memory_address != self._get_register_value():
            self._surface = self._render()
        surface.blit(self._surface, (self.rect.x, self.rect.y))
        self.header.draw(surface)
