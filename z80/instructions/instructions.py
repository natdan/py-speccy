import sys
import inspect

from z80.instructions.base import SOPInstructionDef, Mnemonics, BitOPInstructionDef, MOPInstructionDef

from z80.instructions.base import MNEMONICS_TO_INSTRUCTION


class AND(SOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.AND, 0xa0, 0xe6, 0xa6)


class SUB(SOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SUB, 0x90, 0xd6, 0x96)


class OR(SOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.OR, 0xb0, 0xf6, 0xb6)


class XOR(SOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.XOR, 0xa8, 0xee, 0xae)


class CP(SOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.CP, 0xb8, 0xfe, 0xbe)


class BIT(BitOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.BIT, 0x40, 0x46)


class SET(BitOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SET, 0xC0, 0xC6)


class RES(BitOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RES, 0x80, 0x86)


class RL(MOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RL, 0x80, 0x86)



this_module = sys.modules[__name__]


for _, obj in inspect.getmembers(this_module, lambda member: hasattr(member, "__module__") and member.__module__ == __name__ and inspect.isclass):
    instruction = obj()
    MNEMONICS_TO_INSTRUCTION[instruction.mnemonic] = instruction
    instruction.update_decode_map()
