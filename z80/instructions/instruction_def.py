from abc import ABC
from typing import Optional

from z80.instructions import AddrMode
from z80.instructions.base import InstructionDecoder, Mnemonics, NEXT_BYTE_CALLBACK, IXY, DECODE_MAP, DECODE_MAP_ED, DECODE_MAP_IXY, DECODE_MAP_CB, DECODE_MAP_IDCB


class InstructionDef(InstructionDecoder):
    def __init__(self, mnemonic: Mnemonics, **addr_mode_code) -> None:
        super().__init__()
        self.mnemonic = mnemonic
        self.addr_mode_code: dict[AddrMode, int] = {AddrMode.from_name(k): v for k, v in addr_mode_code.items()}

    def update_decode_map(self) -> None:
        for addr_mode in self.addr_mode_code:
            code = self.addr_mode_code[addr_mode]
            addr_mode.update_decode_maps(self, code)

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        params = params if params is not None else {}
        for addr_mode, code in self.addr_mode_code.items():
            if addr_mode.ixy() == ixy and addr_mode.can_decode(code, instr):
                params.update(addr_mode.decode(address, code, instr, next_byte))
                if params is not None:
                    return Instruction(address, self, addr_mode, **params)

        raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")

    def to_str(self) -> str:
        return self.mnemonic.value


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
        return f"{mnemonic}{''.join(a.to_str(**self.params) for a in self.addr_mode.addr_mode_elements)}"


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


class CBInstructionDef(InstructionDef):
    def __init__(self, mnemonic: Mnemonics, **addr_mode_code) -> None:
        super().__init__(mnemonic, **addr_mode_code)
        self.mnemonic = mnemonic
        self.addr_mode_code: dict[AddrMode, int] = {AddrMode.from_name(k): v for k, v in addr_mode_code.items()}

    def update_decode_map(self) -> None:
        for addr_mode in self.addr_mode_code:
            code = self.addr_mode_code[addr_mode]
            addr_mode.update_decode_maps(self, code, cb=True)


def decode_instruction(address: int, next_byte: NEXT_BYTE_CALLBACK) -> Instruction:
    instr_byte = next_byte()
    if instr_byte in DECODE_MAP:
        decoder = DECODE_MAP[instr_byte]
    else:
        return Instruction(address, UnknownInstructionDef(instr_byte), AddrMode.SIMPLE)

    instruction = decoder.decode(address, instr_byte, next_byte)
    return instruction
