from abc import ABC

from enum import Enum, auto


class Rule(ABC):
    def __init__(self) -> None:
        pass


class Token(Enum):
    Comma = auto()
    Register = auto()

    def rule(self) -> 'TokenRule':
        return TokenRule(self)


class TokenRule(Rule):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token = token


class Sequence(Rule):
    def __init__(self, *sequence: Rule) -> None:
        super().__init__()
        self.sequence = sequence
