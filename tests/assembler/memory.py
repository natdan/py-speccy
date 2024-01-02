from hamcrest import assert_that, is_

from z80.instructions.base import DECODE_MAP


class Memory:
    def __init__(self, *values) -> None:
        self.values = [v for v in values]

    def next_byte(self) -> int:
        byte = self.values[0]
        del self.values[0]
        return byte


def assert_decode(expected: str, *values: int, address=16384) -> None:
    next_byte = Memory(*values).next_byte

    instr_byte = next_byte()
    decoder = DECODE_MAP[instr_byte]

    instruction = decoder.decode(address, instr_byte, next_byte)

    assert_that(instruction.to_str(0), is_(expected))
