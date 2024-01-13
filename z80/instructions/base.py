from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional


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
    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        pass


DECODE_MAP: dict[int, InstructionDecoder] = {}
DECODE_MAP_CB: dict[int, InstructionDecoder] = {}
DECODE_MAP_ED: dict[int, InstructionDecoder] = {}
DECODE_MAP_IDCB: dict[int, InstructionDecoder] = {}
DECODE_MAP_IXY: dict[int, InstructionDecoder] = {}


# MNEMONICS_TO_INSTRUCTION: dict[Mnemonics, InstructionDef] = {}
