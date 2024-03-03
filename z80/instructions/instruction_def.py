from abc import ABC, abstractmethod
from typing import Optional

from z80.instructions import AddrMode
from z80.instructions.base import InstructionDecoder, Mnemonics, NEXT_BYTE_CALLBACK, IXY, DECODE_MAP


def read_bytes(instr: int, next_byte: NEXT_BYTE_CALLBACK) -> list[int]:
    b = [instr]
    while True:
        try:
            b.append(next_byte())
            if len(b) == 4:
                return b
        except Exception:
            return b


class InstructionDef(InstructionDecoder):
    def __init__(self, mnemonic: Mnemonics, **addr_mode_code) -> None:
        super().__init__()
        self.mnemonic = mnemonic
        self.addr_mode_code: dict[AddrMode, int] = {AddrMode.from_name(k): v for k, v in addr_mode_code.items()}

    def update_decode_map(self) -> 'InstructionDef':
        for addr_mode in self.addr_mode_code:
            code = self.addr_mode_code[addr_mode]
            addr_mode.update_decode_maps(self, code)
        return self

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        params = params if params is not None else {}
        for addr_mode, code in self.addr_mode_code.items():
            if addr_mode.can_decode(code, instr, ed, ixy):
                params.update(addr_mode.decode(address, code, instr, next_byte))
                if params is not None:
                    return Instruction(0, address, self, addr_mode, **params)

        raise ValueError(f"Cannot decode; {instr}, ixy={ixy}")

    def encode(self, address: int, addr_mode: AddrMode, **params) -> list[int]:
        memory = [0] * (self.size() + addr_mode.size())
        addr_mode.encode(address, self.addr_mode_code[addr_mode], 0, memory, **params)
        return memory

    def size(self) -> int: return 1

    def to_str(self) -> str:
        return self.mnemonic.value


class MemoryDetail(ABC):
    def __init__(self,
                 line: int,
                 address: int) -> None:
        self.line = line
        self.address = address

    @abstractmethod
    def size(self) -> int: pass


class Instruction(MemoryDetail):
    def __init__(self,
                 line: int,
                 address: int,
                 instruction_def: InstructionDef,
                 addr_mode: AddrMode,
                 **params) -> None:
        super().__init__(line, address)
        self.instruction_def = instruction_def
        self.addr_mode = addr_mode
        self.params = params
        self.profile = []
        self.tstates = 0

    def size(self) -> int: return self.instruction_def.size() + self.addr_mode.size()

    def encode(self) -> list[int]:
        return self.instruction_def.encode(self.address, self.addr_mode, **self.params)

    def to_str(self, tab: int = 0) -> str:
        mnemonic = self.instruction_def.to_str() + " "
        l = len(mnemonic)
        if l < tab * 4:
            mnemonic += " " * (tab * 4 - l)
        return f"{mnemonic}{', '.join(a.to_str(**self.params) for a in self.addr_mode.addr_mode_elements)}"


class UnknownInstructionDef(InstructionDef):
    def __init__(self, *code: int) -> None:
        super().__init__(Mnemonics.UNKNOWN)
        self.code = code

    def update_decode_map(self) -> None:
        pass

    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        return Instruction(0, address, self, AddrMode.SIMPLE, **params)

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

    def encode(self, address: int, addr_mode: AddrMode, **params) -> list[int]:
        memory = [0] * (self.size() + addr_mode.size())
        memory[0] = 0xcb
        addr_mode.encode(address, self.addr_mode_code[addr_mode], 1, memory, **params)
        return memory

    def size(self) -> int: return 2


def decode_instruction(address: int, next_byte: NEXT_BYTE_CALLBACK) -> Instruction:
    instr_byte = next_byte()
    if instr_byte in DECODE_MAP:
        decoder = DECODE_MAP[instr_byte]
        return decoder.decode(address, instr_byte, next_byte, False, None)

    return Instruction(0, address, UnknownInstructionDef(*read_bytes(instr_byte, next_byte)), AddrMode.SIMPLE)
