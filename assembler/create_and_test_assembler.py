import os
from typing import cast

from assembler_utils import second_pass, assembler_output
from buLL.bull_parser import BullParser
from buLL.parser.toolkit import Toolkit
from directives import Org, Label, Equ, AddressDirective, MemoryDirective
from z80.instructions import Instruction

args = "-vv --one-file z80-assembler.grammar"


toolkit1 = Toolkit.create(parser=BullParser())
toolkit1.set_filename("z80-assembler.grammar")
toolkit1.out_path = "."
toolkit1.generate_scanner = True
toolkit1.generate_parser = True
toolkit1.verbose_level = 2
toolkit1.one_file = True
toolkit1.process()

from z80_assembler import Z80AssemblerParser

parser = Z80AssemblerParser()
scanner = Z80AssemblerParser.SCANNER_CLASS()

test_filename = os.environ.get("TEST_FILE", "test-asm.asm")

with open(test_filename, "r") as f:
    scanner.set_reader(f)
    parser.parse(scanner)


second_pass(parser.instructions)
# pc = 0
# print("------------------------------------------------------")
# for instruction in parser.instructions:
#     if isinstance(instruction, Instruction):
#         instruction.address = pc
#         pc += instruction.size()
#     elif isinstance(instruction, Org):
#         pc = instruction.address
#     elif isinstance(instruction, Label):
#         instruction.address = pc

print("------------------------------------------------------")
assembler_output(parser.instructions)

print()