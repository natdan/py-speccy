from abc import ABC, abstractmethod
from enum import Enum


class AddrModeElement(ABC):
    @abstractmethod
    def to_str(self, **params) -> str:
        pass


class _R(AddrModeElement):
    rs = {
        0: "b",
        1: "c",
        2: "d",
        3: "e",
        4: "h",
        5: "l",
        7: "a",
    }

    def to_str(self, **params) -> str:
        r = params["r"]
        return self.rs[r]


class _COMMA(AddrModeElement):
    def to_str(self, **params) -> str: return ", "


class _N(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["n"])


class _PHLP(AddrModeElement):
    def to_str(self, **params) -> str: return "(hl)"


class _PIXDP(AddrModeElement):
    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(ix{'+' if d >= 0 else ''}{d})"


class _PIYDP(AddrModeElement):
    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(iy{'+' if d >= 0 else ''}{d})"


class _BIT(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["b"])


class AddrMode(Enum):
    SIMPLE = []
    R = [_R()]
    N = [_N()]
    PHLP = [_PHLP()]
    PIXDP = [_PIXDP()]
    PIYDP = [_PIYDP()]
    BR = [_BIT(), _COMMA(), _R()]
    BPHLP = [_BIT(), _COMMA(), _PHLP()]
    BPIXDP = [_BIT(), _COMMA(), _PIXDP()]
    BPIYDP = [_BIT(), _COMMA(), _PIYDP()]
