from pygame import Rect

from gui.components import BaseUIFactory, Collection
from utils.playback import Playback
from z80.z80 import Z80


class RegistersComponent(Collection):
    def __init__(self, rect: Rect, ui_factory: BaseUIFactory, z80: Z80, playback: Playback) -> None:
        super().__init__(rect)
        self.playback = playback
        self.z80 = z80
        self.first_row_label = ui_factory.label(Rect(rect.x, rect.y, 0, 0), "")
        self.second_row_label = ui_factory.label(Rect(rect.x, rect.y + 25, 0, 0), "")
        self.third_row_label = ui_factory.label(Rect(rect.x, rect.y + 50, 0, 0), "")
        self.add_component(self.first_row_label)
        self.add_component(self.second_row_label)
        self.add_component(self.third_row_label)

    def draw(self, surface) -> None:
        self.first_row_label.text = (
            f"T:{self.z80.bus_access.tstates:06} "
            f"PC:{self.z80.regPC:04x} "
            f"SP:{self.z80.regSP:04x} "
            f"OP:{self.z80.bus_access.memory.peekb(self.z80.regPC):02x}({self.z80.bus_access.memory.peekb(self.z80.regPC):03d}) "
            f"PS:{len(self.playback.backlog):06} "
            f"T:{self.playback.top:06} "
        )
        self.second_row_label.text = (
            f"A:{self.z80.regA:02x} "
            f"HL:{self.z80.get_reg_HL():04x} "
            f"BC:{self.z80.get_reg_BC():04x} "
            f"DE:{self.z80.get_reg_DE():04x} "
            f"IX:{self.z80.regIX:04x} "
            f"IY:{self.z80.regIY:04x} "
        )
        self.third_row_label.text = (
            f"F:{self.z80.get_flags():02x} "
            f"C:{(1 if self.z80.carryFlag else 0)} "
            f"N:{1 if self.z80.is_add_sub_flag() else 0} "
            f"PV:{1 if self.z80.is_par_over_flag() else 0} "
            f"3:{1 if self.z80.is_bit3_flag() else 0} "
            f"H:{1 if self.z80.is_half_carry_flag() else 0} "
            f"5:{1 if self.z80.is_bit5_flag() else 0} "
            f"Z:{1 if self.z80.is_zero_flag() else 0} "
            f"S:{1 if self.z80.is_sign_flag() else 0} "
            f"IFF1:{1 if self.z80.ffIFF1 else 0} "
            f"IFF2:{1 if self.z80.ffIFF2 else 0} ")
            # f"Mem: 0x{self.z80.regPC:04x}: "
            # f"{self.z80.memory.peekb(self.z80.regPC):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 1):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 2):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 3):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 4):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 5):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 6):02x}, "
            # f"{self.z80.memory.peekb(self.z80.regPC + 7):02x}")
        super().draw(surface)
