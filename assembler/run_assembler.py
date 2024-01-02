
from z80 import Z80AssemblerParser

parser = Z80AssemblerParser()
scanner = Z80AssemblerParser.SCANNER_CLASS()

with open("test-asm.asm", "r") as f:
    scanner.set_reader(f)
    parser.parse(scanner)

