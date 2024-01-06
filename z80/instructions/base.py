from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional

from z80.instructions.address_modes import AddrMode

CB_CODE = 0xcb
ED_CODE = 0xed
IX_CODE = 0xdd
IY_CODE = 0xfd


class Mnemonics(Enum):
    UNKNOWN = "unknown"
    ADC = "adc"
    ADD = "add"
    AND = "and"
    BIT = "bit"
    CALL = "call"
    CCF = "ccf"
    CP = "cp"
    CPD = "cpd"
    CPDR = "cpdr"
    CPI = "cpi"
    CPIR = "cpir"
    CPL = "cpl"
    DAA = "daa"
    DEC = "dec"
    DI = "di"
    DJNZ = "djnz"
    EI = "ei"
    EX = "ex"
    EXX = "exx"
    HALT = "halt"
    IM = "im"
    IN = "in"
    INC = "inc"
    IND = "ind"
    INDR = "indr"
    INI = "ini"
    INIR = "inir"
    JP = "jp"
    JR = "jr"
    LD = "ld"
    LDD = "ldd"
    LDDR = "lddr"
    LDI = "ldi"
    LDIR = "ldir"
    NEG = "neg"
    NOP = "nop"
    OR = "or"
    OTDR = "otdr"
    OTIR = "otir"
    OUT = "out"
    OUTD = "outd"
    OUTI = "outi"
    POP = "pop"
    PUSH = "push"
    RES = "res"
    RET = "ret"
    RETI = "reti"
    RETN = "retn"
    RL = "rl"
    RLA = "rla"
    RLC = "rlc"
    RLCA = "rlca"
    RLD = "rld"
    RR = "rr"
    RRA = "rra"
    RRC = "rrc"
    RRCA = "rrca"
    RRD = "rrd"
    RST = "rst"
    SBC = "sbc"
    SCF = "scf"
    SET = "set"
    SLA = "sla"
    SRA = "sra"
    SRL = "srl"
    SUB = "sub"
    XOR = "xor"

    @classmethod
    def from_string(cls, s: str):
        for v in cls.__members__.values():
            if v.value == s.lower():
                return v

        raise KeyError


class IXY(Enum):
    IX = "ix"
    IY = "iy"


NEXT_BYTE_CALLBACK = Callable[[], int]


class InstructionDecoder(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        pass


DECODE_MAP: dict[int, InstructionDecoder] = {}
DECODE_MAP_CB: dict[int, InstructionDecoder] = {}
DECODE_MAP_ED: dict[int, InstructionDecoder] = {}
DECODE_MAP_IDCB: dict[int, InstructionDecoder] = {}
DECODE_MAP_IXY: dict[int, InstructionDecoder] = {}


class InstructionDef(InstructionDecoder, ABC):
    def __init__(self, mnemonic: Mnemonics) -> None:
        super().__init__()
        self.mnemonic = mnemonic

    @abstractmethod
    def update_decode_map(self) -> None:
        pass

    def to_str(self) -> str:
        return self.mnemonic.value


MNEMONICS_TO_INSTRUCTION: dict[Mnemonics, InstructionDef] = {}


class IXYInstructionDecoder(InstructionDecoder):
    def __init__(self, ixy: IXY) -> None:
        super().__init__()
        self.ixy = ixy

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_IXY:
            return DECODE_MAP_IXY[instr].decode(address, instr, next_byte, self.ixy)

        return Instruction(address, UnknownInstructionDef(prefix, instr), AddrMode.SIMPLE)


class CBInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_CB:
            return DECODE_MAP_CB[instr].decode(address, instr, next_byte, ixy)

        return Instruction(address, UnknownInstructionDef(prefix, instr), AddrMode.SIMPLE)


class EDInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_ED:
            return DECODE_MAP_ED[instr].decode(address, instr, next_byte, ixy)

        return Instruction(address, UnknownInstructionDef(prefix, instr), AddrMode.SIMPLE)


class IXYCBInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        displacement = next_byte()
        instr = next_byte()
        if instr in DECODE_MAP_IDCB:
            return DECODE_MAP_IDCB[instr].decode(address, instr, next_byte, ixy, d=displacement)

        return Instruction(address, UnknownInstructionDef(prefix, instr), AddrMode.SIMPLE)


DECODE_MAP[IX_CODE] = IXYInstructionDecoder(IXY.IX)
DECODE_MAP[IY_CODE] = IXYInstructionDecoder(IXY.IY)
DECODE_MAP[CB_CODE] = CBInstructionDecoder()
DECODE_MAP[ED_CODE] = EDInstructionDecoder()
DECODE_MAP_IXY[CB_CODE] = IXYCBInstructionDecoder()


class Instruction:
    def __init__(self,
                 address: int,
                 instruction_def: InstructionDef,
                 addr_mode: AddrMode,
                 **params) -> None:
        self.address = address
        self.instruction_def = instruction_def
        self.addr_mode = addr_mode
        self.params = params
        self.profile = []
        self.tstates = 0

    def to_str(self, tab: int = 0) -> str:
        mnemonic = self.instruction_def.to_str() + " "
        l = len(mnemonic)
        if l < tab * 4:
            mnemonic += " " * (tab * 4 - l)
        return f"{mnemonic}{''.join(a.to_str(**self.params) for a in self.addr_mode.value)}"


class SimpleInstructionDef(InstructionDef):
    def __init__(self, mnemonics: Mnemonics, code: int) -> None:
        super().__init__(mnemonics)
        self.code = code

    def update_decode_map(self) -> None:
        DECODE_MAP[self.code] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        return Instruction(address, self, AddrMode.SIMPLE, **params)


class SimpleEDInstructionDef(InstructionDef):
    def __init__(self, mnemonics: Mnemonics, code: int) -> None:
        super().__init__(mnemonics)
        self.code = code

    def update_decode_map(self) -> None:
        DECODE_MAP_ED[self.code] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        return Instruction(address, self, AddrMode.SIMPLE, **params)


class UnknownInstructionDef(InstructionDef):
    def __init__(self, *code: int) -> None:
        super().__init__(Mnemonics.UNKNOWN)
        self.code = code

    def update_decode_map(self) -> None:
        pass

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        return Instruction(address, self, AddrMode.SIMPLE, **params)

    def to_str(self) -> str:
        s = " ".join(f"{c:02x}" for c in self.code)
        return f"unknown({s})"


class SOPInstructionDef(InstructionDef, ABC):
    def __init__(self,
                 mnemonic: Mnemonics,
                 reg_op: int,
                 n_op: int,
                 hl_op: int) -> None:
        super().__init__(mnemonic)
        self.reg_op = reg_op
        self.n_op = n_op
        self.hl_op = hl_op

    def update_decode_map(self) -> None:
        for r in range(8):
            if r != 6:
                DECODE_MAP[self.reg_op + r] = self
        DECODE_MAP[self.n_op] = self
        DECODE_MAP[self.hl_op] = self
        DECODE_MAP_IXY[self.hl_op] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if instr == self.n_op:
            return Instruction(address, self, AddrMode.N, n=next_byte(), **params)
        elif ixy:
            return Instruction(address, self, AddrMode.PIXDP if ixy == IXY.IX else AddrMode.PIYDP, d=next_byte(), **params)
        elif instr == self.hl_op:
            return Instruction(address, self, AddrMode.PHLP, **params)
        elif instr & 0xF8 == self.reg_op:
            return Instruction(address, self, AddrMode.R, r=instr & 0x7, **params)
        elif ixy:
            return Instruction(address, self, AddrMode.PIXDP if ixy == IXY.IX else AddrMode.PIYDP, n=next_byte(), **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class MOPInstructionDef(InstructionDef, ABC):
    def __init__(self,
                 mnemonic: Mnemonics,
                 reg_op: int,
                 hl_op: int) -> None:
        super().__init__(mnemonic)
        self.reg_op = reg_op
        self.hl_op = hl_op

    def update_decode_map(self) -> None:
        for r in range(8):
            if r != 6:
                DECODE_MAP[self.reg_op + r * 8] = self
        DECODE_MAP[self.hl_op] = self
        DECODE_MAP_IXY[self.hl_op] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.PIXDP if ixy == IXY.IX else AddrMode.PIYDP, d=next_byte(), **params)
        elif instr == self.hl_op:
            return Instruction(address, self, AddrMode.PHLP, **params)
        elif instr & self.reg_op == self.reg_op:
            return Instruction(address, self, AddrMode.R, r=(instr & 0x38) // 8, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class PushPopInstructionDef(InstructionDef, ABC):
    def __init__(self,
                 mnemonic: Mnemonics,
                 qq_op: int,
                 hl_op: int) -> None:
        super().__init__(mnemonic)
        self.qq_op = qq_op
        self.hl_op = hl_op

    def update_decode_map(self) -> None:
        for r in range(4):
            DECODE_MAP[self.qq_op + r * 16] = self
        DECODE_MAP_IXY[self.hl_op] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.IX if ixy == IXY.IX else AddrMode.IY, **params)
        elif instr & self.qq_op == self.qq_op:
            return Instruction(address, self, AddrMode.QQ, qq=(instr & 0x30) // 16, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class CBMOPInstructionDef(InstructionDef, ABC):
    def __init__(self,
                 mnemonic: Mnemonics,
                 reg_op: int,
                 hl_op: int) -> None:
        super().__init__(mnemonic)
        self.reg_op = reg_op
        self.hl_op = hl_op

    def update_decode_map(self) -> None:
        for r in range(8):
            if r != 6:
                DECODE_MAP_CB[self.reg_op + r] = self
        DECODE_MAP_CB[self.hl_op] = self
        DECODE_MAP_IDCB[self.hl_op] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.PIXDP if ixy == IXY.IX else AddrMode.PIYDP, **params)
        elif instr == self.hl_op:
            return Instruction(address, self, AddrMode.PHLP, **params)
        elif instr & 0xF8 == self.reg_op:
            return Instruction(address, self, AddrMode.R, r=instr & 0x7, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


class BitOPInstructionDef(InstructionDef, ABC):
    def __init__(self,
                 mnemonic: Mnemonics,
                 reg_op: int,
                 hl_op: int) -> None:
        super().__init__(mnemonic)
        self.reg_op = reg_op
        self.hl_op = hl_op

    def update_decode_map(self) -> None:
        for b in range(8):
            for r in range(8):
                DECODE_MAP_CB[self.reg_op + b * 8 + r] = self
            DECODE_MAP_CB[self.hl_op + b * 8] = self
            DECODE_MAP_IDCB[self.hl_op + b * 8] = self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> Instruction:
        if ixy:
            return Instruction(address, self, AddrMode.BPIXDP if ixy == IXY.IX else AddrMode.BPIYDP, b=(instr & 0x38) // 8, **params)
        elif instr & 0xC7 == self.hl_op:
            return Instruction(address, self, AddrMode.BPHLP, b=(instr & 0x38) // 8, **params)
        elif instr & 0xC0 == self.reg_op:
            return Instruction(address, self, AddrMode.BR, b=(instr & 0x38) // 8, r=instr & 0x7, **params)
        else:
            raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")


def decode_instruction(address: int, next_byte: NEXT_BYTE_CALLBACK) -> Instruction:
    instr_byte = next_byte()
    if instr_byte in DECODE_MAP:
        decoder = DECODE_MAP[instr_byte]
    else:
        return Instruction(address, UnknownInstructionDef(instr_byte), AddrMode.SIMPLE)

    instruction = decoder.decode(address, instr_byte, next_byte)
    return instruction
