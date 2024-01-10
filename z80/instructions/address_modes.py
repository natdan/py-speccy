from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

from z80.instructions.base import DECODE_MAP, InstructionDecoder, NEXT_BYTE_CALLBACK, IXY, DECODE_MAP_IXY, DECODE_MAP_CB, DECODE_MAP_IDCB, DECODE_MAP_ED


class AddrModeElement(ABC):
    @abstractmethod
    def to_str(self, **params) -> str:
        pass

    def ixy(self) -> Optional[IXY]: return None

    def can_decode(self, code: int, instr: int) -> bool: return False

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        pass

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {}


class _COMMA(AddrModeElement):
    def to_str(self, **params) -> str: return ", "


class _R2(AddrModeElement):
    rs = {
        0: "b",
        1: "c",
        2: "d",
        3: "e",
        4: "h",
        5: "l",
        7: "a",
    }

    def to_str(self, **params) -> str: return self.rs[params["r2"]]

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(8):
            if r != 6:
                if cb:
                    DECODE_MAP_CB[code + r * 8] = decoder
                elif ixy:
                    DECODE_MAP_IXY[code + r * 8] = decoder
                else:
                    DECODE_MAP[code + r * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code and instr & 0x38 != 0x30

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"r2": (instr & 0x38) // 8}


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

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(8):
            if r != 6:
                if cb:
                    DECODE_MAP_CB[code + r] = decoder
                elif ixy:
                    DECODE_MAP_IXY[code + r] = decoder
                else:
                    DECODE_MAP[code + r] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xf8 == code and instr & 0x07 != 6

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"r1": instr & 0x07}


class _N(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["n"])

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"n": next_byte()}


class _PHLP(AddrModeElement):
    def to_str(self, **params) -> str: return "(hl)"


class _PIXDP(AddrModeElement):
    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(ix{'+' if d >= 0 else ''}{d})"

    def ixy(self) -> Optional[IXY]: return IXY.IX

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"d": next_byte()}


class _PIYDP(AddrModeElement):
    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(iy{'+' if d >= 0 else ''}{d})"

    def ixy(self) -> Optional[IXY]: return IXY.IY

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"d": next_byte()}


class _CB_PIXDP(_PIXDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}


class _CB_PIYDP(_PIYDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}


class _IX(AddrModeElement):
    def to_str(self, **params) -> str: return "ix"

    def ixy(self) -> Optional[IXY]: return IXY.IX


class _IY(AddrModeElement):
    def to_str(self, **params) -> str: return "iy"

    def ixy(self) -> Optional[IXY]: return IXY.IY


class _PIXP(AddrModeElement):
    def to_str(self, **params) -> str: return "(ix)"

    def ixy(self) -> Optional[IXY]: return IXY.IX


class _PIYP(AddrModeElement):
    def to_str(self, **params) -> str: return "(iy)"

    def ixy(self) -> Optional[IXY]: return IXY.IY


class _BIT(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["b"])

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for b in range(8):
            if cb:
                DECODE_MAP_CB[code + b * 8] = decoder
            else:
                DECODE_MAP[code + b * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"b": (instr & 0x38) // 8}


class _CD_IXYBIT(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["b"])

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for b in range(8):
            DECODE_MAP_IDCB[code + b * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"b": (instr & 0x38) // 8}


class _CD_IXY(AddrModeElement):
    def to_str(self, **params) -> str: return str(params["b"])

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        DECODE_MAP_IDCB[code] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr == code


class _NN(AddrModeElement):
    def to_str(self, **params) -> str: return f"0x{params['nn']:04x}"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"nn": next_byte() + 256 * next_byte()}


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

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for cc in range(8):
            DECODE_MAP[code + cc * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"cc": (instr & 0x38) // 8}


class _E(AddrModeElement):
    def to_str(self, **params) -> str: return f"0x{params['e']:04x}"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        def calc_relative(e: int) -> int:
            if e > 128:
                return address + 2 - 256 + e
            return address + 2 + e
        return {"e": calc_relative(next_byte())}


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

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool: return True

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"qq": (instr & 0x30) // 16}


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


class _RR(AddrModeElement):
    def to_str(self, **params) -> str: return "<RR not_to_be_used>"

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc0 == code and instr & 0x38 != 0x30 and instr & 0x07 != 6

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r1 in range(8):
            if r1 != 6:
                for r2 in range(8):
                    if r2 != 6:
                        if cb:
                            DECODE_MAP_CB[code + r2 * 8 + r1] = decoder
                        else:
                            DECODE_MAP[code + r2 * 8 + r1] = decoder

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"r2": (instr & 0x38) // 8, "r1": instr & 0x07}


class _BITR1(AddrModeElement):
    def to_str(self, **params) -> str: return "<BITR not_to_be_used>"

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc0 == code and instr & 0x07 != 6

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for b in range(8):
            for r1 in range(8):
                if r1 != 6:
                    if cb:
                        DECODE_MAP_CB[code + b * 8 + r1] = decoder
                    else:
                        DECODE_MAP[code + b * 8 + r1] = decoder

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"b": (instr & 0x38) // 8, "r1": instr & 0x07}


class _ED_SIMPLE(AddrModeElement):
    def to_str(self, **params) -> str: return ""

    def can_decode(self, code: int, instr: int) -> bool:
        return instr == instr

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None: \
        DECODE_MAP_ED[code] = decoder


_COMMA = _COMMA()
_R1 = _R1()
_R2 = _R2()
_N = _N()
_PHLP = _PHLP()
_PIXDP = _PIXDP()
_IX = _IX()
_IY = _IY()
_PIXP = _PIXP()
_PIYP = _PIYP()
_PIYDP = _PIYDP()
_BIT = _BIT()
_NN = _NN()
_CC = _CC()
_E = _E()
_C = _C()
_NC = _NC()
_Z = _Z()
_NZ = _NZ()
_QQ = _QQ()
_DE = _DE()
_HL = _HL()
_PSPP = _PSPP()
_AF = _AF()
_AFp = _AFp()

_ED_SIMPLE = _ED_SIMPLE()
_RR = _RR()
_BITR1 = _BITR1()
_CD_IXYBIT = _CD_IXYBIT()
_CD_IXY = _CD_IXY()
_CB_PIXDP = _CB_PIXDP()
_CB_PIYDP = _CB_PIYDP()


class AddrMode(Enum):
    SIMPLE = [], None
    SIMPLE_ED = [], _ED_SIMPLE
    R2 = [_R2], _R2
    R1 = [_R1], _R1
    RR = [_R2, _COMMA, _R1], _RR
    N = [_N], None
    RN = [_R2, _COMMA, _N], _R2
    IX = [_IX], None
    IY = [_IY], None
    PHLP = [_PHLP], None
    PIXP = [_PIXP], None
    PIYP = [_PIYP], None
    PIXDP = [_PIXDP], None
    PIYDP = [_PIYDP], None
    CBPIXDP = [_CB_PIXDP], _CD_IXY
    CBPIYDP = [_CB_PIYDP], _CD_IXY
    BR = [_BIT, _COMMA, _R1], _BITR1
    BPHLP = [_BIT, _COMMA, _PHLP], _BIT
    BPIXDP = [_BIT, _COMMA, _CB_PIXDP], _CD_IXYBIT
    BPIYDP = [_BIT, _COMMA, _CB_PIYDP], _CD_IXYBIT
    NN = [_NN], None
    CC = [_CC], _CC
    CCNN = [_CC, _COMMA, _NN], _CC
    E = [_E], None  # Relative
    CE = [_C, _COMMA, _E], None
    NCE = [_NC, _COMMA, _E], None
    ZE = [_Z, _COMMA, _E], None
    NZE = [_NZ, _COMMA, _E], None
    QQ = [_QQ], _QQ
    DEHL = [_DE, _COMMA, _HL], None
    AFAFp = [_AF, _COMMA, _AFp], None
    PSPPHL = [_PSPP, _COMMA, _HL], None
    PSPPIX = [_PSPP, _COMMA, _IX], None
    PSPPIY = [_PSPP, _COMMA, _IY], None
    RPHLP = [_R2, _COMMA, _PHLP], _R2
    RPIXDP = [_R2, _COMMA, _PIXDP], _R2
    RPIYDP = [_R2, _COMMA, _PIYDP], _R2
    PHLPR = [_PHLP, _COMMA, _R1], _R1
    PIXDPR = [_PIXDP, _COMMA, _R1], _R1
    PIYDPR = [_PIYDP, _COMMA, _R1], _R1

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, addr_mode_elements: list[AddrModeElement], instr_decoder: Optional[AddrModeElement]):
        self.addr_mode_elements = addr_mode_elements
        self.instr_decoder = instr_decoder

    def ixy(self) -> Optional[IXY]:
        return next((ixy for ixy in map(lambda x: x.ixy(), self.addr_mode_elements) if ixy is not None), None)

    def update_decode_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False) -> None:
        ixy = self.ixy()

        if self.instr_decoder:
            self.instr_decoder.update_code_maps(decoder, code, cb, ixy)
        else:
            if cb:
                DECODE_MAP_CB[code] = decoder
            elif ixy is not None:
                DECODE_MAP_IXY[code] = decoder
            else:
                DECODE_MAP[code] = decoder

    def can_decode(self, code: int, instr: int):
        return self.instr_decoder.can_decode(code, instr) if self.instr_decoder else (code == instr)

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        res = {}
        for addr_mode_el in self.addr_mode_elements:
            r = addr_mode_el.decode(address, code, instr, next_byte)
            if r is not None:
                if res is None:
                    res = r
                else:
                    res.update(r)

        return res

    @classmethod
    def from_name(cls, name: str) -> 'AddrMode':
        for v in cls.__members__.values():
            if v.name.lower() == name.lower():
                return v

        raise KeyError(f"Cannot find '{name}'")
