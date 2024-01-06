from abc import ABC


class MemoryAccess(ABC):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0) -> None:
        self.at_tstates = at_tstates
        self.tstates = tstates
        self.delay = delay

    def __repr__(self) -> str: return f"({self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''})"


class NoMemoryAccess(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"E{super().__repr__()}"


class FetchOpcode(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"F{super().__repr__()}"


class PeekB(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"RB{super().__repr__()}"


class PokeB(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, delay: int  = 0):
        super().__init__(at_tstates, tstates, delay)

    def __repr__(self) -> str: return f"WB{super().__repr__()}"


class PeekW(MemoryAccess):
    def __init__(self, at_tstates: int, tstates1: int, tstates2: int, delay1: int = 0, delay2: int = 0):
        super().__init__(at_tstates, tstates1, delay1)
        self.tstates2 = tstates2
        self.delay2 = delay2

    def __repr__(self) -> str:
        return f"RW({self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''} {self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''})"


class PokeW(MemoryAccess):
    def __init__(self, at_tstates: int, tstates1: int, tstates2: int, delay1: int = 0, delay2: int = 0):
        super().__init__(at_tstates, tstates1, delay1)
        self.tstates2 = tstates2
        self.delay2 = delay2

    def __repr__(self) -> str:
        return f"WW({self.tstates}{'+' + str(self.delay) if self.delay > 0 else ''} {self.tstates2}{'+' + str(self.delay2) if self.delay2 > 0 else ''})"


class AddrOnBus(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"A({self.tstates}{''.join(str(d) for d in self.delays)})"


class InPort(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"I({self.tstates}{''.join(str(d) for d in self.delays)})"


class OutPort(MemoryAccess):
    def __init__(self, at_tstates: int, tstates: int, *delays: int):
        super().__init__(at_tstates, tstates, 0)
        self.delays = delays

    def __repr__(self) -> str:
        return f"O({self.tstates}{''.join(str(d) for d in self.delays)})"
