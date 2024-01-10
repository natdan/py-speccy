from hamcrest import assert_that, is_

from assembler.memory import Memory
from z80.instructions import DECODE_MAP


def assert_decode(expected: str, *values: int, address=16384) -> None:
    next_byte = Memory(*values).next_byte

    instr_byte = next_byte()
    decoder = DECODE_MAP[instr_byte]

    instruction = decoder.decode(address, instr_byte, next_byte)

    assert_that(instruction.to_str(0).strip(), is_(expected))
