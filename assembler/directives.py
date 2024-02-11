

class Directive:
    def __init__(self, address: int) -> None:
        self.address = address

    def _to_str(self, directive: str, tab: int = 0) -> str:
        directive = directive + " "
        l = len(directive)
        if l < tab * 4:
            directive += " " * (tab * 4 - l)
        return f"{directive}"

    def to_str(self, tabs: int = 0) -> str:
        return self._to_str("unknown", tabs).strip()


class Org(Directive):
    def __init__(self, address: int) -> None:
        super().__init__(address)

    def to_str(self, tabs: int = 0) -> str:
        return self._to_str("org", tabs) + f"0x{self.address:04x}"


class Label(Directive):
    def __init__(self, label: str) -> None:
        super().__init__(0)
        self.label = label

    def to_str(self, tabs: int = 0) -> str:
        return f"{self.label} ; (0x{self.address:04x})"


class MacroInvocation(Directive):
    def __init__(self, name: str) -> None:
        super().__init__(0)
        self.name = name

    def to_str(self, tabs: int = 0) -> str:
        return f"invoke macro '{self.name}'"
