from io import StringIO

from hamcrest import assert_that, is_, contains_exactly

from assembler.memory import Memory
from expression import Expression, ExprContext
from z80.instructions import DECODE_MAP
from z80_assembler import Z80AssemblerParser


def assert_decode(expected: str, *values: int, address=16384, assert_asm=True) -> None:
    next_byte = Memory(*values).next_byte

    instr_byte = next_byte()
    decoder = DECODE_MAP[instr_byte]

    instruction = decoder.decode(address, instr_byte, next_byte, False, None)

    encoded = instruction.encode()
    assert_that(encoded, contains_exactly(*values))

    assert_that(instruction.to_str(0).strip(), is_(expected))

    assert_that(instruction.size(), is_(len(values)))

    if assert_asm:
        parser = Z80AssemblerParser()
        scanner = Z80AssemblerParser.SCANNER_CLASS()

        string_reader = StringIO("    " + expected + "\n")
        scanner.set_reader(string_reader)
        parser.parse(scanner)

        instruction = parser.instructions[0]

        context = ExprContext()
        for p_key in instruction.params:
            expr = instruction.params[p_key]
            if isinstance(expr, Expression):
                instruction.params[p_key] = expr.evaluate(context)

        assert_that(instruction.to_str(0).strip(), is_(expected))
