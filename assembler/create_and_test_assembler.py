
from buLL.bull_parser import BullParser
from buLL.parser.toolkit import Toolkit
from directives import Org, Label
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

with open("test-asm.asm", "r") as f:
    scanner.set_reader(f)
    parser.parse(scanner)

pc = 0
print("------------------------------------------------------")
for instruction in parser.instructions:
    if isinstance(instruction, Instruction):
        instruction.address = pc
        pc += instruction.size()
    elif isinstance(instruction, Org):
        pc = instruction.address
    elif isinstance(instruction, Label):
        instruction.address = pc

print("------------------------------------------------------")
for instruction in parser.instructions:
    if isinstance(instruction, Instruction):
        print(f"0x{instruction.address:04x}            {instruction.to_str(2).strip()}")
    else:
        print(f"          {instruction.to_str(2)}")
