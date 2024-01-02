from z80.instructions.grammar import Token, Sequence

from z80.instructions.base import Instruction, Mnemonics


class LDRR(Instruction):
    def __init__(self) -> None:
        super().__init__(
            Mnemonics.LD,
            Sequence(Token.Register.rule(), Token.Comma.rule(), Token.Register.rule())
        )
