from abc import ABC


class MemoryAccess(ABC):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0) -> None:
        self.at_tstates = at_tstates
        self.tstates = tstates
        self.delay = delay

    def __repr__(self) -> str: return f"{self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''}"

    def to_str(self) -> str: return f"{self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''}"


class NoMemoryAccess(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"e{super().__repr__()}"

    def to_str(self) -> str: return f"no access {super().__repr__()}"


class FetchOpcode(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"f{super().__repr__()}"

    def to_str(self) -> str: return f"fetch op {super().__repr__()}"


class PeekB(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"rb{super().__repr__()}"

    def to_str(self) -> str: return f"peekb {super().__repr__()}"


class PokeB(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"wb{super().__repr__()}"

    def to_str(self) -> str: return f"pokeb {super().__repr__()}"


class PeekW(MemoryAccess):
    def __init__(self, at_tstates: int, tstates1: int, tstates2: int, delay1: int = 0, delay2: int = 0):
        super().__init__(at_tstates, tstates1, delay1)
        self.tstates2 = tstates2
        self.delay2 = delay2

    def __repr__(self) -> str:
        return f"rw{self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''},{self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''}"

    def to_str(self) -> str:
        return f"peekw {self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''},{self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''}"


class PokeW(MemoryAccess):
    def __init__(self, at_tstates: int, tstates1: int, tstates2: int, delay1: int = 0, delay2: int = 0):
        super().__init__(at_tstates, tstates1, delay1)
        self.tstates2 = tstates2
        self.delay2 = delay2

    def __repr__(self) -> str:
        return f"ww{self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''},{self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''}"

    def to_str(self) -> str:
        return f"pokew {self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''},{self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''}"


class AddrOnBus(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"a{self.tstates}{''.join(str(d) for d in self.delays)}"

    def to_str(self) -> str:
        return f"addr on bus {self.tstates}{''.join(str(d) for d in self.delays)}"


class InPort(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"i{self.tstates}{''.join(str(d) for d in self.delays)}"

    def to_str(self) -> str:
        return f"in {self.tstates}{''.join(str(d) for d in self.delays)}"


class OutPort(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"o{self.tstates}{''.join(str(d) for d in self.delays)}"

    def to_str(self) -> str:
        return f"out {self.tstates}{''.join(str(d) for d in self.delays)}"
