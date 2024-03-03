from abc import ABC
from enum import Enum
from typing import Callable, Union, Optional

from z80.instructions import Instruction


class ExprContext:
    def __init__(self) -> None:
        self.labels: dict[str, Union[int, Expression]] = {}
        self.current_instruction: Optional[Instruction] = None

    def add_label(self, name: str, value: Union[int, 'Expression']) -> None:
        self.labels[name] = value

    def evaluate(self, label: str) -> Union[int, 'Expression']:
        if label in self.labels:
            return self.labels[label]
        raise KeyError(f"Not defined {label}")


class Expression(ABC):
    def __init__(self) -> None:
        pass

    def evaluate(self, context: ExprContext) -> Union[int, str]:
        raise ValueError(f"Not implemented on {type(self)}")


class NumberExpression(Expression):
    def __init__(self, number: int) -> None:
        super().__init__()
        self.number = number

    def evaluate(self, context: ExprContext) -> int:
        return self.number

    def __repr__(self) -> str:
        return str(self.number)


class StringExpression(Expression):
    def __init__(self, s: str) -> None:
        super().__init__()
        self.s = s

    def evaluate(self, context: ExprContext) -> str:
        return self.s

    def __repr__(self) -> str:
        return self.s


class LabelExpression(Expression):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def evaluate(self, context: ExprContext) -> int:
        return context.evaluate(self.label)

    def __repr__(self) -> str:
        return str(self.label)


class InstructionAddressExpression(Expression):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, context: ExprContext) -> int:
        return context.current_instruction.address

    def __repr__(self) -> str: return "$"


class BinaryOperator(Enum):
    ADD = "+", lambda left, right: left + right
    SUB = "-", lambda left, right: left - right
    MUL = "*", lambda left, right: left * right
    DIV = "/", lambda left, right: left // right

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, op: str, expr: Callable[[int, int], int]) -> None:
        self.op = op
        self.expr = expr


class BinaryOperation(Expression):
    def __init__(self, op: BinaryOperator, left: Expression, right: Expression) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self, context: ExprContext) -> int:
        return self.op.expr(self.left.evaluate(context), self.right.evaluate(context))

    def __repr__(self) -> str:
        return f"({self.left} {self.op.op} {self.right})"
