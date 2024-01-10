from typing import Optional

import sys
import inspect

from z80.instructions import AddrMode
from z80.instructions.instruction_def import Mnemonics, InstructionDef, DECODE_MAP, DECODE_MAP_IXY, NEXT_BYTE_CALLBACK, Instruction, IXY, CBInstructionDef


class AND(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.AND,
                         R1=0xa0,
                         N=0xe6,
                         PHLP=0xa6,
                         PIXDP=0xa6,
                         PIYDP=0xa6)


class SUB(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SUB,
                         R1=0x90,
                         N=0xd6,
                         PHLP=0x96,
                         PIXDP=0x96,
                         PIYDP=0x96)


class OR(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.OR,
                         R1=0xb0,
                         N=0xf6,
                         PHLP=0xb6,
                         PIXDP=0xb6,
                         PIYDP=0xb6)


class XOR(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.XOR,
                         R1=0xa8,
                         N=0xee,
                         PHLP=0xae,
                         PIXDP=0xae,
                         PIYDP=0xae)


class CP(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.CP,
                         R1=0xb8,
                         N=0xfe,
                         PHLP=0xbe,
                         PIXDP=0xbe,
                         PIYDP=0xbe)


class BIT(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.BIT,
                         BR=0x40,
                         BPHLP=0x46,
                         BPIXDP=0x46,
                         BPIYDP=0x46)


class SET(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SET,
                         BR=0xc0,
                         BPHLP=0xc6,
                         BPIXDP=0xc6,
                         BPIYDP=0xc6)


class RES(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RES,
                         BR=0x80,
                         BPHLP=0x86,
                         BPIXDP=0x86,
                         BPIYDP=0x86)


class INC(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.INC,
                         R2=0x04,
                         PHLP=0x34,
                         PIXDP=0x34,
                         PIYDP=0x34)


class DEC(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.DEC,
                         R2=0x05,
                         PHLP=0x35,
                         PIXDP=0x35,
                         PIYDP=0x35)


class RL(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RL,
                         R1=0x10,
                         PHLP=0x16,
                         CBPIXDP=0x16,
                         CBPIYDP=0x16)


class RR(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RR,
                         R1=0x18,
                         PHLP=0x1e,
                         CBPIXDP=0x1e,
                         CBPIYDP=0x1e)


class RRC(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.RRC,
                         R1=0x08,
                         PHLP=0x0e,
                         CBPIXDP=0x0e,
                         CBPIYDP=0x0e)


class SLA(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SLA,
                         R1=0x20,
                         PHLP=0x26,
                         CBPIXDP=0x26,
                         CBPIYDP=0x26)


class SRA(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SRA,
                         R1=0x28,
                         PHLP=0x2e,
                         CBPIXDP=0x2e,
                         CBPIYDP=0x2e)


class SRL(CBInstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.SRL,
                         R1=0x38,
                         PHLP=0x3e,
                         CBPIXDP=0x3e,
                         CBPIYDP=0x3e)


InstructionDef(Mnemonics.CCF, SIMPLE=0x3f).update_decode_map()
InstructionDef(Mnemonics.CPL, SIMPLE=0x2f).update_decode_map()
InstructionDef(Mnemonics.DAA, SIMPLE=0x27).update_decode_map()
InstructionDef(Mnemonics.DI, SIMPLE=0xf3).update_decode_map()
InstructionDef(Mnemonics.EI, SIMPLE=0xfb).update_decode_map()
InstructionDef(Mnemonics.EXX, SIMPLE=0xd9).update_decode_map()
InstructionDef(Mnemonics.RLA, SIMPLE=0x17).update_decode_map()
InstructionDef(Mnemonics.RLCA, SIMPLE=0x07).update_decode_map()
InstructionDef(Mnemonics.RRA, SIMPLE=0x1f).update_decode_map()
InstructionDef(Mnemonics.RRCA, SIMPLE=0x0f).update_decode_map()
InstructionDef(Mnemonics.SCF, SIMPLE=0x37).update_decode_map()

InstructionDef(Mnemonics.CPD, SIMPLE_ED=0xa9).update_decode_map()
InstructionDef(Mnemonics.CPDR, SIMPLE_ED=0xb9).update_decode_map()
InstructionDef(Mnemonics.CPI, SIMPLE_ED=0xa1).update_decode_map()
InstructionDef(Mnemonics.CPIR, SIMPLE_ED=0xb1).update_decode_map()
InstructionDef(Mnemonics.IND, SIMPLE_ED=0xaa).update_decode_map()
InstructionDef(Mnemonics.INDR, SIMPLE_ED=0xba).update_decode_map()
InstructionDef(Mnemonics.INI, SIMPLE_ED=0xa2).update_decode_map()
InstructionDef(Mnemonics.INIR, SIMPLE_ED=0xb2).update_decode_map()
InstructionDef(Mnemonics.LDD, SIMPLE_ED=0xa8).update_decode_map()
InstructionDef(Mnemonics.LDDR, SIMPLE_ED=0xb8).update_decode_map()
InstructionDef(Mnemonics.LDI, SIMPLE_ED=0xa0).update_decode_map()
InstructionDef(Mnemonics.LDIR, SIMPLE_ED=0xb0).update_decode_map()
InstructionDef(Mnemonics.NEG, SIMPLE_ED=0x44).update_decode_map()
InstructionDef(Mnemonics.OTDR, SIMPLE_ED=0xbb).update_decode_map()
InstructionDef(Mnemonics.OUTD, SIMPLE_ED=0xab).update_decode_map()
InstructionDef(Mnemonics.OUTI, SIMPLE_ED=0xa3).update_decode_map()
InstructionDef(Mnemonics.RETI, SIMPLE_ED=0x4d).update_decode_map()
InstructionDef(Mnemonics.RETN, SIMPLE_ED=0x45).update_decode_map()
InstructionDef(Mnemonics.RLD, SIMPLE_ED=0x6f).update_decode_map()
InstructionDef(Mnemonics.RRD, SIMPLE_ED=0x67).update_decode_map()


class HALT(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.HALT, SIMPLE=0x76)


class NOP(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.NOP, SIMPLE=0x00)


class JP(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.JP,
                         NN=0xc3,
                         CCNN=0xc2,
                         PHLP=0xe9,
                         PIXP=0xe9,
                         PIYP=0xe9)


class JR(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.JR,
                         E=0x18,
                         CE=0x38,
                         NCE=0x30,
                         ZE=0x28,
                         NZE=0x20)


class DJNZ(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.DJNZ,
                         E=0x10)


class PushInstructionDef(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.PUSH,
                         QQ=0xc5,
                         IX=0xe5,
                         IY=0xe5)


class PopInstructionDef(InstructionDef):
    def __init__(self) -> None:
        super().__init__(Mnemonics.POP,
                         QQ=0xc1,
                         IX=0xe1,
                         IY=0xe1)


class EX(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.EX,
                         DEHL=0xeb,
                         AFAFp=0x08,
                         PSPPHL=0xe3,
                         PSPPIX=0xe3,
                         PSPPIY=0xe3)


class RET(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.RET,
                         SIMPLE=0xc9,
                         CC=0xc0)


class LD(InstructionDef):
    def __init__(self):
        super().__init__(Mnemonics.LD,
                         RR=0x40,
                         RN=0x06,
                         RPHLP=0x46,
                         RPIXDP=0x46,
                         RPIYDP=0x46,
                         PHLPR=0x70,
                         PIXDPR=0x70,
                         PIYDPR=0x70)


this_module = sys.modules[__name__]


for _, obj in inspect.getmembers(this_module, lambda member: hasattr(member, "__module__") and member.__module__ == __name__ and inspect.isclass):
    instruction = obj()
    # MNEMONICS_TO_INSTRUCTION[instruction.mnemonic] = instruction
    instruction.update_decode_map()
