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

    def to_str(self, **params) -> str: return self.rs[params["r"]]


class _R1(AddrModeElement):
    rs = {
        0: "b",
        1: "c",
        2: "d",
        3: "e",
        4: "h",
        5: "l",
        7: "a",
    }

    def to_str(self, **params) -> str: return self.rs[params["r1"]]


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


class _IX(AddrModeElement):
    def to_str(self, **params) -> str: return "ix"


class _IY(AddrModeElement):
    def to_str(self, **params) -> str: return "iy"


class _PIXP(AddrModeElement):
    def to_str(self, **params) -> str: return "(ix)"


class _PIYP(AddrModeElement):
    def to_str(self, **params) -> str: return "(iy)"


class _PIYDP(AddrModeElement):
    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(iy{'+' if d >= 0 else ''}{d})"


class _BIT(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["b"])


class _NN(AddrModeElement):
    def to_str(self, **params) -> str: return f"0x{params['nn']:04x}"


class _CC(AddrModeElement):
    CC = {
        0: "nz",
        1: "z",
        2: "nc",
        3: "c",
        4: "po",
        5: "pe",
        6: "p",
        7: "m"
    }
    def to_str(self, **params) -> str: return _CC.CC[params["cc"]]


class _E(AddrModeElement):
    def to_str(self, **params) -> str: return f"0x{params['e']:04x}"


class _C(AddrModeElement):
    def to_str(self, **params) -> str: return "c"


class _NC(AddrModeElement):
    def to_str(self, **params) -> str: return "nc"


class _Z(AddrModeElement):
    def to_str(self, **params) -> str: return "z"


class _NZ(AddrModeElement):
    def to_str(self, **params) -> str: return "nz"


class _QQ(AddrModeElement):
    QQ = {
        0: "bc",
        1: "de",
        2: "hl",
        3: "af"
    }
    def to_str(self, **params) -> str: return _QQ.QQ[params["qq"]]


class _DE(AddrModeElement):
    def to_str(self, **params) -> str: return "de"


class _HL(AddrModeElement):
    def to_str(self, **params) -> str: return "hl"


class _PSPP(AddrModeElement):
    def to_str(self, **params) -> str: return "(sp)"


class _AF(AddrModeElement):
    def to_str(self, **params) -> str: return "af"


class _AFp(AddrModeElement):
    def to_str(self, **params) -> str: return "af'"


class AddrMode(Enum):
    SIMPLE = []
    R = [_R()]
    RR = [_R(), _COMMA(), _R1()]
    N = [_N()]
    RN = [_R(), _COMMA(), _N()]
    IX = [_IX()]
    IY = [_IY()]
    PHLP = [_PHLP()]
    PIXP = [_PIXP()]
    PIYP = [_PIYP()]
    PIXDP = [_PIXDP()]
    PIYDP = [_PIYDP()]
    BR = [_BIT(), _COMMA(), _R()]
    BPHLP = [_BIT(), _COMMA(), _PHLP()]
    BPIXDP = [_BIT(), _COMMA(), _PIXDP()]
    BPIYDP = [_BIT(), _COMMA(), _PIYDP()]
    NN = [_NN()]
    CC = [_CC()]
    CCNN = [_CC(), _COMMA(), _NN()]
    E = [_E()]  # Relative
    CE = [_C(), _COMMA(), _E()]
    NCE = [_NC(), _COMMA(), _E()]
    ZE = [_Z(), _COMMA(), _E()]
    NZE = [_NZ(), _COMMA(), _E()]
    QQ = [_QQ()]
    DEHL = [_DE(), _COMMA(), _HL()]
    AFAFp = [_AF(), _COMMA(), _AFp()]
    SPHL = [_PSPP(), _COMMA(), _HL()]
    SPIX = [_PSPP(), _COMMA(), _IX()]
    SPIY = [_PSPP(), _COMMA(), _IY()]
    RPHLP = [_R(), _COMMA(), _PHLP()]
    RPIXDP = [_R(), _COMMA(), _PIXDP()]
    RPIYDP = [_R(), _COMMA(), _PIYDP()]
    PHLPR = [_PHLP(), _COMMA(), _R()]
    PIXDPR = [_PIXDP(), _COMMA(), _R()]
    PIYDPR = [_PIYDP(), _COMMA(), _R()]
