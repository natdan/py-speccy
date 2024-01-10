from abc import ABC, abstractmethod
from typing import Callable, Optional

from z80.instructions.base import IXY

NEXT_BYTE_CALLBACK = Callable[[], int]


class InstructionDecoder(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def decode(self, address: int, instr: int, next_byte: NEXT_BYTE_CALLBACK, ixy: Optional[IXY] = None, **params) -> 'Instruction':
        pass


