from typing import Optional

import sys
import inspect

from z80.instructions import AddrMode
from z80.instructions.base import SOPInstructionDef, Mnemonics, BitOPInstructionDef, CBMOPInstructionDef, SimpleInstructionDef, SimpleEDInstructionDef, InstructionDef, DECODE_MAP, DECODE_MAP_IXY, NEXT_BYTE_CALLBACK, Instruction, IXY, MOPInstructionDef, PushPopInstructionDef

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


class INC(MOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.INC, 0x04, 0x34)


class DEC(MOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.DEC, 0x05, 0x35)


class RL(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RL, 0x10, 0x16)


class RR(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RR, 0x18, 0x1e)


class RRC(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RRC, 0x08, 0x0e)


class SLA(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SLA, 0x20, 0x26)


class SRA(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SRA, 0x28, 0x2e)


class SRL(CBMOPInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SRL, 0x38, 0x3e)


SimpleInstructionDef(Mnemonics.CCF, 0x3f).update_decode_map()
SimpleEDInstructionDef(Mnemonics.CPD, 0xa9).update_decode_map()
SimpleEDInstructionDef(Mnemonics.CPDR, 0xb9).update_decode_map()
SimpleEDInstructionDef(Mnemonics.CPI, 0xa1).update_decode_map()
SimpleEDInstructionDef(Mnemonics.CPIR, 0xb1).update_decode_map()
SimpleInstructionDef(Mnemonics.CPL, 0x2f).update_decode_map()
SimpleInstructionDef(Mnemonics.DAA, 0x27).update_decode_map()
SimpleInstructionDef(Mnemonics.DI, 0xf3).update_decode_map()
SimpleInstructionDef(Mnemonics.EI, 0xfb).update_decode_map()
SimpleInstructionDef(Mnemonics.EXX, 0xd9).update_decode_map()
SimpleEDInstructionDef(Mnemonics.IND, 0xaa).update_decode_map()
SimpleEDInstructionDef(Mnemonics.INDR, 0xba).update_decode_map()
SimpleEDInstructionDef(Mnemonics.INI, 0xa2).update_decode_map()
SimpleEDInstructionDef(Mnemonics.INIR, 0xb2).update_decode_map()
SimpleEDInstructionDef(Mnemonics.LDD, 0xa8).update_decode_map()
SimpleEDInstructionDef(Mnemonics.LDDR, 0xb8).update_decode_map()
SimpleEDInstructionDef(Mnemonics.LDI, 0xa0).update_decode_map()
SimpleEDInstructionDef(Mnemonics.LDIR, 0xb0).update_decode_map()
SimpleEDInstructionDef(Mnemonics.NEG, 0x44).update_decode_map()
SimpleEDInstructionDef(Mnemonics.OTDR, 0xbb).update_decode_map()
SimpleEDInstructionDef(Mnemonics.OUTD, 0xab).update_decode_map()
SimpleEDInstructionDef(Mnemonics.OUTI, 0xa3).update_decode_map()
SimpleEDInstructionDef(Mnemonics.RETI, 0x4d).update_decode_map()
SimpleEDInstructionDef(Mnemonics.RETN, 0x45).update_decode_map()
SimpleInstructionDef(Mnemonics.RLA, 0x17).update_decode_map()
SimpleInstructionDef(Mnemonics.RLCA, 0x07).update_decode_map()
SimpleEDInstructionDef(Mnemonics.RLD, 0x6f).update_decode_map()
SimpleInstructionDef(Mnemonics.RRA, 0x1f).update_decode_map()
SimpleInstructionDef(Mnemonics.RRCA, 0x0f).update_decode_map()
SimpleEDInstructionDef(Mnemonics.RRD, 0x67).update_decode_map()
SimpleInstructionDef(Mnemonics.SCF, 0x37).update_decode_map()


class HALT(SimpleInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.HALT, 0x76)


class NOP(SimpleInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.NOP, 0x00)


class JP(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.JP)

    def update_decode_map(self) -> None:
        DECODE_MAP[0xc3] = self
        DECODE_MAP[0xe9] = self
        DECODE_MAP_IXY[0xe9] = self
        for cc in range(8):
            DECODE_MAP[0xc2 + cc * 8] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.PIXP if ixy == IXY.IX else AddrMode.PIYP, **params)
        elif instr == 0xe9:
            return Instruction(address, self, AddrMode.PHLP, **params)
        elif instr == 0xc3:
            return Instruction(address, self, AddrMode.NN, nn=next_byte() + 256 * next_byte(), **params)
        elif instr & 0xc2 == 0xc2:
            return Instruction(address, self, AddrMode.CCNN, cc=(instr & 0x38) // 8, nn=next_byte() + 256 * next_byte(), **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class JR(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.JR)

    def update_decode_map(self) -> None:
        DECODE_MAP[0x18] = self
        DECODE_MAP[0x38] = self
        DECODE_MAP[0x30] = self
        DECODE_MAP[0x28] = self
        DECODE_MAP[0x20] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        def calc_relative(e: int) -> int:
            if e > 128:
                return  + address + 2 - 256 + e
            return address + 2 + e

        if instr == 0x18:
            return Instruction(address, self, AddrMode.E, e=calc_relative(next_byte()), **params)
        elif instr == 0x38:
            return Instruction(address, self, AddrMode.CE, e=calc_relative(next_byte()), **params)
        elif instr == 0x30:
            return Instruction(address, self, AddrMode.NCE, e=calc_relative(next_byte()), **params)
        elif instr == 0x28:
            return Instruction(address, self, AddrMode.ZE, e=calc_relative(next_byte()), **params)
        elif instr == 0x20:
            return Instruction(address, self, AddrMode.NZE, e=calc_relative(next_byte()), **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class DJNZ(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.DJNZ)

    def update_decode_map(self) -> None:
        DECODE_MAP[0x10] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        def calc_relative(e: int) -> int:
            if e > 128:
                return  + address + 2 - 256 + e
            return address + 2 + e

        if instr == 0x10:
            return Instruction(address, self, AddrMode.E, e=calc_relative(next_byte()), **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class PushInstructionDef(PushPopInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.PUSH, 0xc5, 0xe5)


class PopInstructionDef(PushPopInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.POP, 0xc1, 0xe1)


class EX(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.EX)

    def update_decode_map(self) -> None:
        DECODE_MAP[0xeb] = self
        DECODE_MAP[0x08] = self
        DECODE_MAP[0xe3] = self
        DECODE_MAP_IXY[0xe3] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.SPIX if ixy == ixy.IX else AddrMode.SPIY, **params)
        elif instr == 0xeb:
            return Instruction(address, self, AddrMode.DEHL, **params)
        elif instr == 0x08:
            return Instruction(address, self, AddrMode.AFAFp, **params)
        elif instr == 0xe3:
            return Instruction(address, self, AddrMode.SPHL, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class RET(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.RET)

    def update_decode_map(self) -> None:
        DECODE_MAP[0xc9] = self
        for cc in range(8):
            DECODE_MAP[0xc0 + cc * 8] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if instr == 0xc9:
            return Instruction(address, self, AddrMode.SIMPLE, **params)
        elif instr & 0xc0 == 0xc0:
            return Instruction(address, self, AddrMode.CC, cc=(instr & 0x38) // 8, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


this_module = sys.modules[__name__]


for _, obj in inspect.getmembers(this_module, lambda member: hasattr(member, "__module__") and member.__module__ == __name__ and inspect.isclass):
    instruction = obj()
    MNEMONICS_TO_INSTRUCTION[instruction.mnemonic] = instruction
    instruction.update_decode_map()
