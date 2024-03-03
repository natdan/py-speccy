from abc import ABC, abstractmethod
from typing import Union

from expression import Expression, ExprContext
from z80.instructions.instruction_def import MemoryDetail


def _to_str(directive: str, tab: int = 0) -> str:
    directive = directive + " "
    l = len(directive)
    if l < tab * 4:
        directive += " " * (tab * 4 - l)
    return f"{directive}"


class Directive(ABC):
    def __init__(self, line: int) -> None:
        self.line = line

    def second_pass(self, context: ExprContext) -> None:
        pass

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("unknown", tabs).strip()


class AddressDirective(Directive):
    def __init__(self, line: int, address: int) -> None:
        super().__init__(line)
        self.address = address
        self.addressed = True


class Org(AddressDirective):
    def __init__(self, line: int, address: Expression) -> None:
        super().__init__(line, 0)
        self.value = address

    def second_pass(self, context: ExprContext) -> None:
        self.address = self.value.evaluate(context)

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("org", tabs) + f"${self.address:04x}"


class Label(AddressDirective):
    def __init__(self, line: int, label: str) -> None:
        super().__init__(line, 0)
        self.label = label[:-1] if label[-1] == ":" else  label

    def to_str(self, tabs: int = 0) -> str:
        return f"{self.label} ; (${self.address:04x})"


class Equ(Directive):
    def __init__(self, line: int, value: Expression) -> None:
        super().__init__(line)
        self.value = value
        self.label = ""

    def second_pass(self, context: ExprContext) -> None:
        if self.label in context.labels:
            raise ValueError(f"Label {self.label} already defined, line {self.line}")
        self.value = self.value.evaluate(context)
        context.labels[self.label] = self.value

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("equ", tabs) + f"${self.value:04x}"


class MemoryDirective(MemoryDetail, ABC):
    def __init__(self, line: int, address: int) -> None:
        super().__init__(line, address)

    def second_pass(self, context: ExprContext) -> None:
        pass

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("unknown", tabs).strip()


class DB(MemoryDirective):
    def __init__(self, line: int) -> None:
        super().__init__(line, 0)
        self.values: list[Union[int, Expression]] = []

    def second_pass(self, context: ExprContext) -> None:
        new_values = []
        for v in self.values:
            v = v.evaluate(context)
            if isinstance(v, str):
                for c in v:
                    new_values.append(ord(c))
            else:
                new_values.append(v)
        self.values = new_values

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("db", tabs) + ",".join(f"${v:02x}" for v in self.values)

    def size(self) -> int: return len(self.values)


class DS(MemoryDirective):
    def __init__(self, line: int) -> None:
        super().__init__(line, 0)
        self.size = 0
        self.value: Union[int, Expression] = 0

    def second_pass(self, context: ExprContext) -> None:
        if isinstance(self.value, Expression):
            self.value = self.value.evaluate(context)

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("ds", tabs) + f"${self.value:02x}" + (
            "" if self.value == 0 else f", {self.value:02x}"
        )

    def size(self) -> int: return self.size


class DW(MemoryDirective):
    def __init__(self, line: int) -> None:
        super().__init__(line, 0)
        self.values: list[Union[int, Expression]] = []

    def second_pass(self, context: ExprContext) -> None:
        self.values = [v.evaluate(context) for v in self.values]

    def to_str(self, tabs: int = 0) -> str:
        return _to_str("dw", tabs) + ",".join(f"${v:04x}" for v in self.values)

    def size(self) -> int: return len(self.values) * 2


class MacroInvocation(Directive):
    def __init__(self, line: int, name: str) -> None:
        super().__init__(line)
        self.name = name

    def to_str(self, tabs: int = 0) -> str:
        return f"invoke macro '{self.name}'"
