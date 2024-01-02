from abc import ABC
from enum import Enum


class MemoryAccess(ABC):
    pass


class NoMemory(MemoryAccess):
    pass
    # Tn


class _FetchOpcode(MemoryAccess):
    pass
    # mem[PC]
    # PC += 1
    # T4


class _PeekB(MemoryAccess):
    pass
    # mem[x]
    # T3


class _PokeB(MemoryAccess):
    pass
    # mem[x]
    # T3


class _PeekW(MemoryAccess):
    pass
    # mem[x]
    # T3
    # mem[x + 1]
    # T3
    # Total: T6


class _PokeW(MemoryAccess):
    pass
    # mem[x]
    # T3
    # mem[x + 1]
    # T3
    # Total: T6


class AddrOnBus(MemoryAccess):
    pass
    # for i in range(n):
    #     mem[x]
    #     T1
    # Total: Tn


class InPort(MemoryAccess):
    pass
    # port[x]
    # T1
    # for i in range(3):
    #     port[x]
    #     T1
    # Total: T4


class OutPort(MemoryAccess):
    pass
    # port[x]
    # T1
    # for i in range(3):
    #     port[x]
    #     T1
    # Total: T4


class MemoryProfile:
    def __init__(self) -> None:
        pass

