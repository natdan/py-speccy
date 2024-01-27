from io import StringIO

from hamcrest import assert_that, is_

from assembler.memory import Memory
from z80.instructions import DECODE_MAP
from z80_assembler import Z80AssemblerParser


def assert_decode(expected: str, *values: int, address=16384, assert_asm=True) -> None:
    next_byte = Memory(*values).next_byte

    instr_byte = next_byte()
    decoder = DECODE_MAP[instr_byte]

    instruction = decoder.decode(address, instr_byte, next_byte, False, None)

    assert_that(instruction.to_str(0).strip(), is_(expected))

    if assert_asm:
        parser = Z80AssemblerParser()
        scanner = Z80AssemblerParser.SCANNER_CLASS()

        string_reader = StringIO("    " + expected + "\n")
        scanner.set_reader(string_reader)
        parser.parse(scanner)

        instruction = parser.instructions[0]
        assert_that(instruction.to_str(0).strip(), is_(expected))
