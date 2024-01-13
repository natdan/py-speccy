from typing import Optional

from z80.instructions.base import IX_CODE, IY_CODE, CB_CODE, ED_CODE, IXY, NEXT_BYTE_CALLBACK

from z80.instructions.address_modes import AddrMode
from z80.instructions.base import InstructionDecoder
from z80.instructions.base import DECODE_MAP, DECODE_MAP_CB, DECODE_MAP_ED, DECODE_MAP_IXY, DECODE_MAP_IDCB

import z80.instructions.instructions
from z80.instructions.instruction_def import Instruction, UnknownInstructionDef, read_bytes


class IXYInstructionDecoder(InstructionDecoder):
    def __init__(self, ixy: IXY) -> None:
        super().__init__()
        self.ixy = ixy

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_IXY:
            return DECODE_MAP_IXY[instr].decode(address, instr, next_byte, ed, self.ixy)

        return Instruction(address, UnknownInstructionDef(prefix, *read_bytes(instr, next_byte)), AddrMode.SIMPLE)


class CBInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, _ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_CB:
            return DECODE_MAP_CB[instr].decode(address, instr, next_byte, False, ixy)

        return Instruction(address, UnknownInstructionDef(prefix, *read_bytes(instr, next_byte)), AddrMode.SIMPLE)


class EDInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        instr = next_byte()
        if instr in DECODE_MAP_ED:
            return DECODE_MAP_ED[instr].decode(address, instr, next_byte, True, ixy)

        return Instruction(address, UnknownInstructionDef(prefix, *read_bytes(instr, next_byte)), AddrMode.SIMPLE)


class IXYCBInstructionDecoder(InstructionDecoder):
    def __init__(self) -> None:
        super().__init__()

    def decode(self, address: int, prefix: int, next_byte: NEXT_BYTE_CALLBACK, ed: bool, ixy: Optional[IXY], **params) -> 'Instruction':
        displacement = next_byte()
        instr = next_byte()
        if instr in DECODE_MAP_IDCB:
            return DECODE_MAP_IDCB[instr].decode(address, instr, next_byte, False, ixy, d=displacement)

        return Instruction(address, UnknownInstructionDef(prefix, *read_bytes(instr, next_byte)), AddrMode.SIMPLE)


DECODE_MAP[IX_CODE] = IXYInstructionDecoder(IXY.IX)
DECODE_MAP[IY_CODE] = IXYInstructionDecoder(IXY.IY)
DECODE_MAP[CB_CODE] = CBInstructionDecoder()
DECODE_MAP[ED_CODE] = EDInstructionDecoder()
DECODE_MAP_IXY[CB_CODE] = IXYCBInstructionDecoder()
