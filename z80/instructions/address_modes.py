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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr

    def ed(self) -> bool: return False

    def size(self) -> int: return 0

    def relative(self) -> bool: return False

    def param_name(self) -> Optional[str]: return None


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

    def param_name(self) -> Optional[str]: return "r2"

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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["r2"] * 8


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

    def param_name(self) -> Optional[str]: return "r1"

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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["r1"]


class _N(AddrModeElement):

    def param_name(self) -> Optional[str]: return "n"

    def to_str(self, **params) -> str: return str(params["n"])

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"n": next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr
        memory[ptr + 1] = params["n"]

    def size(self) -> int: return 1


class _PHLP(AddrModeElement):
    def to_str(self, **params) -> str: return "(hl)"


class _PIXDP(AddrModeElement):
    def param_name(self) -> Optional[str]: return "d"

    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(ix{'+' if d >= 0 else ''}{d})"

    def ixy(self) -> Optional[IXY]: return IXY.IX

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"d": next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["d"]

    def size(self) -> int: return 2


class _PIYDP(AddrModeElement):
    def param_name(self) -> Optional[str]: return "d"

    def to_str(self, **params) -> str:
        d = params["d"]
        if d > 127: d -= 256
        return f"(iy{'+' if d >= 0 else ''}{d})"

    def ixy(self) -> Optional[IXY]: return IXY.IY

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"d": next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["d"]

    def size(self) -> int: return 2


class _CB_PIXDP(_PIXDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr - 1] = 0xdd
        memory[ptr] = 0xcb
        memory[ptr + 1] = params["d"]
        memory[ptr + 2] = instr

    def size(self) -> int: return 2


class _CB_PIYDP(_PIYDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr - 1] = 0xfd
        memory[ptr] = 0xcb
        memory[ptr + 1] = params["d"]
        memory[ptr + 2] = instr

    def size(self) -> int: return 2


class _CB_BPIXDP(_PIXDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr - 1] = 0xdd
        memory[ptr] = 0xcb
        memory[ptr + 1] = params["d"]
        memory[ptr + 2] = instr + params["b"] * 8

    def size(self) -> int: return 2


class _CB_BPIYDP(_PIYDP):
    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]: return {}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr - 1] = 0xfd
        memory[ptr] = 0xcb
        memory[ptr + 1] = params["d"]
        memory[ptr + 2] = instr + params["b"] * 8

    def size(self) -> int: return 2


class _IX(AddrModeElement):
    def to_str(self, **params) -> str: return "ix"

    def ixy(self) -> Optional[IXY]: return IXY.IX

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr

    def size(self) -> int: return 1


class _IY(AddrModeElement):
    def to_str(self, **params) -> str: return "iy"

    def ixy(self) -> Optional[IXY]: return IXY.IY

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr

    def size(self) -> int: return 1


class _PIXP(_IX):
    def to_str(self, **params) -> str: return "(ix)"

    def ixy(self) -> Optional[IXY]: return IXY.IX

    def size(self) -> int: return 1


class _PIYP(_IY):
    def to_str(self, **params) -> str: return "(iy)"

    def ixy(self) -> Optional[IXY]: return IXY.IY

    def size(self) -> int: return 1


class _BIT(AddrModeElement):
    def param_name(self) -> Optional[str]: return "b"

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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["b"] * 8


class _CD_IXYBIT(AddrModeElement):
    def param_name(self) -> Optional[str]: return "b"

    def to_str(self, **params) -> str: return str(params["b"])

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for b in range(8):
            DECODE_MAP_IDCB[code + b * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"b": (instr & 0x38) // 8}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["b"] * 8

    # Both instances already have IX or IY in address modes
    # def size(self) -> int: return 2


class _CD_IXY(AddrModeElement):
    def param_name(self) -> Optional[str]: return "b"

    def to_str(self, **params) -> str: return str(params["b"])

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        DECODE_MAP_IDCB[code] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr == code

    # Both instances already have IX or IY in address modes
    # def size(self) -> int: return 2


class _NN(AddrModeElement):
    def param_name(self) -> Optional[str]: return "n"

    def to_str(self, **params) -> str: return f"${params['nn']:04x}"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"nn": next_byte() + 256 * next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr
        memory[ptr + 1] = params["nn"] % 256
        memory[ptr + 2] = params["nn"] // 256

    def size(self) -> int: return 2


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

    def param_name(self) -> Optional[str]: return "cc"

    def to_str(self, **params) -> str: return _CC.CC[params["cc"]]

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for cc in range(8):
            DECODE_MAP[code + cc * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"cc": (instr & 0x38) // 8}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["cc"] * 8


class _E(AddrModeElement):
    def param_name(self) -> Optional[str]: return "e"

    def to_str(self, **params) -> str: return f"${params['e']:04x}"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        def calc_relative(e: int) -> int:
            if e > 128:
                return address + 2 - 256 + e
            return address + 2 + e
        return {"e": calc_relative(next_byte())}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        def calc_relative(e: int) -> int:
            delta = e - address - 2
            if delta > 127 or delta < -128:
                raise ValueError(f"Out of range; {delta}")
            if delta < 0:
                delta = 256 + delta
            return delta
        memory[ptr] = instr
        memory[ptr + 1] = calc_relative(params["e"])

    def relative(self) -> bool: return True

    def size(self) -> int: return 1


class _C(AddrModeElement):
    def param_name(self) -> Optional[str]: return "c"

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

    def param_name(self) -> Optional[str]: return "qq"

    def to_str(self, **params) -> str: return _QQ.QQ[params['qq']]

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"qq": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["qq"] * 16


class _DD(AddrModeElement):
    DD = {
        0: "bc",
        1: "de",
        2: "hl",
        3: "sp"
    }

    def param_name(self) -> Optional[str]: return "dd"

    def to_str(self, **params) -> str: return f"{_DD.DD[params['dd']]}"

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"dd": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["dd"] * 16


class _PP(AddrModeElement):
    PP = {
        0: "bc",
        1: "de",
        2: "ix",
        3: "sp"
    }

    def param_name(self) -> Optional[str]: return "pp"

    def to_str(self, **params) -> str: return f"{_PP.PP[params['pp']]}"

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            if ixy:
                DECODE_MAP_IXY[code + r * 16] = decoder
            else:
                DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"pp": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["pp"] * 16


class _RR(AddrModeElement):
    RR = {
        0: "bc",
        1: "de",
        2: "iy",
        3: "sp"
    }

    def param_name(self) -> Optional[str]: return "rr"

    def to_str(self, **params) -> str: return f"{_RR.RR[params['rr']]}"

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"rr": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["rr"] * 16


class _ED_DD(AddrModeElement):
    DD = {
        0: "bc",
        1: "de",
        2: "hl",
        3: "sp"
    }

    def param_name(self) -> Optional[str]: return "dd"

    def to_str(self, **params) -> str: return f"{_DD.DD[params['dd']]}"

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP_ED[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"dd": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xed
        memory[ptr + 1] = instr + params["dd"] * 16

    def ed(self) -> bool: return True

    def size(self) -> int: return 1


class _PDDP(AddrModeElement):
    DD = {
        0: "bc",
        1: "de",
        2: "hl",
        3: "sp"
    }

    def param_name(self) -> Optional[str]: return "dd"

    def to_str(self, **params) -> str: return f"({_DD.DD[params['dd']]})"

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(4):
            DECODE_MAP[code + r * 16] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xcf == code

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"dd": (instr & 0x30) // 16}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["dd"] * 16


class _DE(AddrModeElement):
    def to_str(self, **params) -> str: return "de"


class _HL(AddrModeElement):
    def to_str(self, **params) -> str: return "hl"


class _SP(AddrModeElement):
    def to_str(self, **params) -> str: return "sp"


class _A(AddrModeElement):
    def to_str(self, **params) -> str: return "a"


class _I(AddrModeElement):
    def to_str(self, **params) -> str: return "i"


class _R(AddrModeElement):
    def to_str(self, **params) -> str: return "r"


class _PCP(AddrModeElement):
    def to_str(self, **params) -> str: return "(c)"


class _PBCP(AddrModeElement):
    def to_str(self, **params) -> str: return "(bc)"


class _PDEP(AddrModeElement):
    def to_str(self, **params) -> str: return "(de)"


class _PNNP(AddrModeElement):
    def param_name(self) -> Optional[str]: return "nn"

    def to_str(self, **params) -> str: return f"(${params['nn']:04x})"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"nn": next_byte() + 256 * next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr
        memory[ptr + 1] = params["nn"] % 256
        memory[ptr + 2] = params["nn"] // 256

    def size(self) -> int: return 2


class _PNP(AddrModeElement):
    def param_name(self) -> Optional[str]: return "n"

    def to_str(self, **params) -> str: return f"({params['n']})"

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"n": next_byte()}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr
        memory[ptr + 1] = params["n"]

    def size(self) -> int: return 1


class _PSPP(AddrModeElement):
    def to_str(self, **params) -> str: return "(sp)"


class _AF(AddrModeElement):
    def to_str(self, **params) -> str: return "af"


class _AFp(AddrModeElement):
    def to_str(self, **params) -> str: return "af'"


class _R1R2(AddrModeElement):
    def to_str(self, **params) -> str: return "<R1R2 not_to_be_used>"

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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["r2"] * 8 + params["r1"]


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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["b"] * 8 + params["r1"]


class _RST(AddrModeElement):
    RST = {
        0: "$0",
        1: "$8",
        2: "$10",
        3: "$18",
        4: "$20",
        5: "$28",
        6: "$30",
        7: "$38"
    }

    def param_name(self) -> Optional[str]: return "t"

    def to_str(self, **params) -> str: return f"{_RST.RST[params['t']]}"

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for t in range(8):
            DECODE_MAP[code + t * 8] = decoder

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"t": (instr & 0x38) // 8}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["t"] * 8


class _ED_R2(AddrModeElement):
    rs = {
        0: "b",
        1: "c",
        2: "d",
        3: "e",
        4: "h",
        5: "l",
        7: "a",
    }

    def param_name(self) -> Optional[str]: return "r2"

    def to_str(self, **params) -> str: return self.rs[params["r2"]]

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        for r in range(8):
            if r != 6:
                DECODE_MAP_ED[code + r * 8] = decoder

    def can_decode(self, code: int, instr: int) -> bool:
        return instr & 0xc7 == code and instr & 0x38 != 0x30

    def decode(self, address: int, code: int, instr: int, next_byte: NEXT_BYTE_CALLBACK) -> dict[str, Any]:
        return {"r2": (instr & 0x38) // 8}

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xed
        memory[ptr + 1] = instr + params["r2"] * 8

    def ed(self) -> bool: return True

    def size(self) -> int: return 1


class _ED_SIMPLE(AddrModeElement):
    def to_str(self, **params) -> str: return ""

    def can_decode(self, code: int, instr: int) -> bool:
        return code == instr

    def update_code_maps(self, decoder: InstructionDecoder, code: int, cb: bool = False, ixy: Optional[IXY] = None) -> None:
        DECODE_MAP_ED[code] = decoder

    def ed(self) -> bool: return True

    def size(self) -> int: return 1

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xed
        memory[ptr + 1] = instr


class _IM0(_ED_SIMPLE):
    def to_str(self, **params) -> str: return "0"


class _IM1(_ED_SIMPLE):
    def to_str(self, **params) -> str: return "1"


class _IM2(_ED_SIMPLE):
    def to_str(self, **params) -> str: return "2"


class _IXPP(_PP):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr + params["pp"] * 16


class _IYRR(_RR):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr + params["rr"] * 16


class _CCNN(_NN):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["cc"] * 8
        memory[ptr + 1] = params["nn"] % 256
        memory[ptr + 2] = params["nn"] // 256


class _RN(_N):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["r2"] * 8
        memory[ptr + 1] = params["n"]


class _RPIXDP(_R2):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr + params["r2"] * 8
        memory[ptr + 2] = params["d"]


class _RPIYDP(_R2):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr + params["r2"] * 8
        memory[ptr + 2] = params["d"]


class _PIXDPR(_R1):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr + params["r1"]
        memory[ptr + 2] = params["d"]


class _PIYDPR(_R1):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr + params["r1"]
        memory[ptr + 2] = params["d"]


class _PIXDPN(_N):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["d"]
        memory[ptr + 3] = params["n"]


class _PIYDPN(_N):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["d"]
        memory[ptr + 3] = params["n"]


class _IXNN(_NN):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xdd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["nn"] % 256
        memory[ptr + 3] = params["nn"] // 256


class _IYNN(_NN):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xfd
        memory[ptr + 1] = instr
        memory[ptr + 2] = params["nn"] % 256
        memory[ptr + 3] = params["nn"] // 256


class _DDNN(_DD):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = instr + params["dd"] * 16
        memory[ptr + 1] = params["nn"] % 256
        memory[ptr + 2] = params["nn"] // 256


class _ED_DDNN(_DD):
    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        memory[ptr] = 0xed
        memory[ptr + 1] = instr + params["dd"] * 16
        memory[ptr + 2] = params["nn"] % 256
        memory[ptr + 3] = params["nn"] // 256


_R1 = _R1()
_R2 = _R2()
_N = _N()
_PHLP = _PHLP()
_PIXDP = _PIXDP()
_PIYDP = _PIYDP()
_IX = _IX()
_IY = _IY()
_PIXP = _PIXP()
_PIYP = _PIYP()
_BIT = _BIT()
_NN = _NN()
_CC = _CC()
_E = _E()
_C = _C()
_NC = _NC()
_Z = _Z()
_NZ = _NZ()
_QQ = _QQ()
_DD = _DD()
_SS = _DD
_PP = _PP()
_RR = _RR()
_PDDP = _PDDP()
_DE = _DE()
_HL = _HL()
_SP = _SP()
_A = _A()
_I = _I()
_R = _R()
_PSPP = _PSPP()
_AF = _AF()
_AFp = _AFp()
_PBCP = _PBCP()
_PDEP = _PDEP()
_PNNP = _PNNP()
_PNP = _PNP()

_ED_SIMPLE = _ED_SIMPLE()
_ED_DD = _ED_DD()
_R1R2 = _R1R2()
_BITR1 = _BITR1()
_CD_IXYBIT = _CD_IXYBIT()
_CD_IXY = _CD_IXY()
_CB_PIXDP = _CB_PIXDP()
_CB_PIYDP = _CB_PIYDP()
_ED_R2 = _ED_R2()
_IM0 = _IM0()
_IM1 = _IM1()
_IM2 = _IM2()
_RST = _RST()
_PCP = _PCP()
_IXPP = _IXPP()
_IYRR = _IYRR()
_CB_BPIXDP = _CB_BPIXDP()
_CB_BPIYDP = _CB_BPIYDP()
_CCNN = _CCNN()
_RN = _RN()
_RPIXDP = _RPIXDP()
_RPIYDP = _RPIYDP()
_PIXDPR = _PIXDPR()
_PIYDPR = _PIYDPR()
_PIXDPN = _PIXDPN()
_PIYDPN = _PIYDPN()
_DDNN = _DDNN()
_IXNN = _IXNN()
_IYNN = _IYNN()
_ED_DDNN = _ED_DDNN()


class AddrMode(Enum):
    SIMPLE = [], None, None
    SIMPLE_ED = [], _ED_SIMPLE, _ED_SIMPLE
    R2 = [_R2], _R2, _R2
    R1 = [_R1], _R1, _R1
    RR = [_R2, _R1], _R1R2, _R1R2
    N = [_N], None, _N
    RN = [_R2, _N], _R2, _RN
    IX = [_IX], None, _IX
    IY = [_IY], None, _IY
    PHLP = [_PHLP], None, None
    PIXP = [_PIXP], None, _PIXP
    PIYP = [_PIYP], None, _PIYP
    PIXDP = [_PIXDP], None, _PIXDP
    PIYDP = [_PIYDP], None, _PIYDP
    CBPIXDP = [_CB_PIXDP], _CD_IXY, _CB_PIXDP
    CBPIYDP = [_CB_PIYDP], _CD_IXY, _CB_PIYDP
    BR = [_BIT, _R1], _BITR1, _BITR1
    BPHLP = [_BIT, _PHLP], _BIT, _BIT
    BPIXDP = [_BIT, _CB_PIXDP], _CD_IXYBIT, _CB_BPIXDP
    BPIYDP = [_BIT, _CB_PIYDP], _CD_IXYBIT, _CB_BPIYDP
    NN = [_NN], None, _NN
    CC = [_CC], _CC, _CC
    CCNN = [_CC, _NN], _CC, _CCNN
    E = [_E], None, _E  # Relative
    CE = [_C, _E], None, _E
    NCE = [_NC, _E], None, _E
    ZE = [_Z, _E], None, _E
    NZE = [_NZ, _E], None, _E
    QQ = [_QQ], _QQ, _QQ
    DEHL = [_DE, _HL], None, None
    AFAFp = [_AF, _AFp], None, None
    PSPPHL = [_PSPP, _HL], None, None
    PSPPIX = [_PSPP, _IX], None, _IX
    PSPPIY = [_PSPP, _IY], None, _IY
    RPHLP = [_R2, _PHLP], _R2, _R2
    RPIXDP = [_R2, _PIXDP], _R2, _RPIXDP
    RPIYDP = [_R2, _PIYDP], _R2, _RPIYDP
    PHLPR = [_PHLP, _R1], _R1, _R1
    PIXDPR = [_PIXDP, _R1], _R1, _PIXDPR
    PIYDPR = [_PIYDP, _R1], _R1, _PIYDPR
    PHLPN = [_PHLP, _N], None, _N
    PIXDPN = [_PIXDP, _N], None, _PIXDPN
    PIYDPN = [_PIYDP, _N], None, _PIYDPN
    APBCP = [_A, _PBCP], None, None
    APDEP = [_A, _PDEP], None, None
    APNNP = [_A, _PNNP], None, _NN
    PBCPA = [_PBCP, _A], None, None
    PDEPA = [_PDEP, _A], None, None
    PNNPA = [_PNNP, _A], None, _NN
    AI = [_A, _I], _ED_SIMPLE, _ED_SIMPLE
    AR = [_A, _R], _ED_SIMPLE, _ED_SIMPLE
    IA = [_I, _A], _ED_SIMPLE, _ED_SIMPLE
    RA = [_R, _A], _ED_SIMPLE, _ED_SIMPLE
    DDNN = [_DD, _NN], _DD, _DDNN
    IXNN = [_IX, _NN], None, _IXNN
    IYNN = [_IY, _NN], None, _IYNN
    HLPNNP = [_HL, _PNNP], None, _NN
    DDPNNP = [_DD, _PNNP], _ED_DD, _ED_DDNN  # _ED_DD_NN
    IXPNNP = [_IX, _PNNP], None, _IXNN
    IYPNNP = [_IY, _PNNP], None, _IYNN
    PNNPHL = [_PNNP, _HL], None, _NN
    PNNPDD = [_PNNP, _DD], _ED_DD, _ED_DDNN  # _ED_DD_NN
    PNNPIX = [_PNNP, _IX], None, _IXNN
    PNNPIY = [_PNNP, _IY], None, _IYNN
    SPHL = [_SP, _HL], None, None
    SPIX = [_SP, _IX], None, _IX
    SPIY = [_SP, _IY], None, _IY
    AR1 = [_A, _R1], _R1, _R1
    AN = [_A, _N], None, _N
    APHLP = [_A, _PHLP], None, None
    APIXDP = [_A, _PIXDP], None, _PIXDP
    APIYDP = [_A, _PIYDP], None, _PIYDP
    HLSS = [_HL, _SS], _SS, _SS
    IXPP = [_IX, _PP], _PP, _IXPP
    IYRR = [_IY, _RR], _RR, _IYRR
    SS = [_SS], _SS, _SS
    IM0 = [_IM0], _IM0, _ED_SIMPLE
    IM1 = [_IM1], _IM1, _ED_SIMPLE
    IM2 = [_IM2], _IM2, _ED_SIMPLE
    RST = [_RST], _RST, _RST
    APNP = [_A, _PNP], None, _N
    RPCP = [_R2, _PCP], _ED_R2, _ED_R2
    PNPA = [_PNP, _A], None, _N
    PCPR = [_PCP, _R2], _ED_R2, _ED_R2
    ED_HLSS = [_HL, _SS], _ED_DD, _ED_DD

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, addr_mode_elements: list[AddrModeElement], instr_decoder: Optional[AddrModeElement], instr_encoder: Optional[AddrModeElement]):
        self.addr_mode_elements = addr_mode_elements
        self.instr_decoder = instr_decoder
        self.instr_encoder = instr_encoder

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

    def can_decode(self, code: int, instr: int, ed: bool, ixy: Optional[IXY]):
        return ((self.ixy() == ixy)
                and (self.instr_decoder is None or self.instr_decoder.ed() == ed)
                and (self.instr_decoder.can_decode(code, instr) if self.instr_decoder else (code == instr)))

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

    def encode(self, address: int, instr: int, ptr: int, memory: list[int], **params):
        if self.instr_encoder:
            self.instr_encoder.encode(address, instr, ptr, memory, **params)
        else:
            memory[ptr] = instr

    def size(self) -> int:
        extra = self.instr_decoder.size() if self.instr_decoder is not None and self.instr_decoder not in self.addr_mode_elements else 0
        return sum(map(lambda e: e.size(), self.addr_mode_elements)) + extra

    @classmethod
    def from_name(cls, name: str) -> 'AddrMode':
        for v in cls.__members__.values():
            if v.name.lower() == name.lower():
                return v

        raise KeyError(f"Cannot find '{name}'")
