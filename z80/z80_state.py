from typing import Optional

from z80.z80_cpu import Z80CPU


class Z80State:
    def __init__(self, state: Optional[memoryview] = None) -> None:
        self.state = state if state else memoryview(bytearray(32))

    @property
    def regA(self) -> int:
        return self.state[0]

    @regA.setter
    def regA(self, value) -> None:
        self.state[0] = value

    @property
    def regF(self) -> int:
        return self.state[1]

    @regF.setter
    def regF(self, value) -> None:
        self.state[1] = value

    @property
    def regBC(self) -> int:
        return self.state[2] | (self.state[3] << 8)

    @regBC.setter
    def regBC(self, value) -> None:
        self.state[2] = value % 256
        self.state[3] = value // 256

    @property
    def regHL(self) -> int:
        return self.state[4] | (self.state[5] << 8)

    @regHL.setter
    def regHL(self, value) -> None:
        self.state[4] = value % 256
        self.state[5] = value // 256

    @property
    def regPC(self) -> int:
        return self.state[6] | (self.state[7] << 8)

    @regPC.setter
    def regPC(self, value) -> None:
        self.state[6] = value % 256
        self.state[7] = value // 256

    @property
    def regSP(self) -> int:
        return self.state[8] | (self.state[9] << 8)

    @regSP.setter
    def regSP(self, value) -> None:
        self.state[8] = value % 256
        self.state[9] = value // 256

    @property
    def regI(self) -> int:
        return self.state[10]

    @regI.setter
    def regI(self, value) -> None:
        self.state[10] = value

    @property
    def regR(self) -> int:
        return self.state[11]

    @regR.setter
    def regR(self, value) -> None:
        self.state[11] = value & 0xff

    @property
    def extraFlags(self) -> int:
        return self.state[12]

    @extraFlags.setter
    def extraFlags(self, value) -> None:
        self.state[12] = value

    @property
    def regDE(self) -> int:
        return self.state[13] | (self.state[14] << 8)

    @regDE.setter
    def regDE(self, value) -> None:
        self.state[13] = value % 256
        self.state[14] = value // 256

    @property
    def regBCx(self) -> int:
        return self.state[15] | (self.state[16] << 8)

    @regBCx.setter
    def regBCx(self, value) -> None:
        self.state[15] = value % 256
        self.state[16] = value // 256

    @property
    def regDEx(self) -> int:
        return self.state[17] | (self.state[18] << 8)

    @regDEx.setter
    def regDEx(self, value) -> None:
        self.state[17] = value % 256
        self.state[18] = value // 256

    @property
    def regHLx(self) -> int:
        return self.state[19] | (self.state[20] << 8)

    @regHLx.setter
    def regHLx(self, value) -> None:
        self.state[19] = value % 256
        self.state[20] = value // 256

    @property
    def regAx(self) -> int:
        return self.state[21]

    @regAx.setter
    def regAx(self, value) -> None:
        self.state[21] = value

    @property
    def regFx(self) -> int:
        return self.state[22]

    @regFx.setter
    def regFx(self, value) -> None:
        self.state[22] = value

    @property
    def regIY(self) -> int:
        return self.state[23] | (self.state[24] << 8)

    @regIY.setter
    def regIY(self, value) -> None:
        self.state[23] = value % 256
        self.state[24] = value // 256

    @property
    def regIX(self) -> int:
        return self.state[25] | (self.state[26] << 8)

    @regIX.setter
    def regIX(self, value) -> None:
        self.state[25] = value % 256
        self.state[26] = value // 256

    @property
    def ffIFF1(self) -> int:
        return self.state[27]

    @ffIFF1.setter
    def ffIFF1(self, value) -> None:
        self.state[27] = value

    @property
    def ffIFF2(self) -> int:
        return self.state[28]

    @ffIFF2.setter
    def ffIFF2(self, value) -> None:
        self.state[28] = value

    @property
    def modeINT(self) -> int:
        return self.state[29]

    @modeINT.setter
    def modeINT(self, value) -> None:
        self.state[29] = value

    @classmethod
    def create_from(self, z80: Z80CPU, border_colour: int) -> 'Z80State':
        state = Z80State()
        state.regA = z80.regA
        state.regF = z80.get_flags()
        state.regBC = z80.get_reg_BC()
        state.regHL = z80.get_reg_HL()
        state.regPC = z80.regPC
        state.regSP = z80.regSP
        state.regI = z80.regI
        state.regR = z80.regR
        state.extraFlags = z80.regR & 0x80 >> 7 | (border_colour & 0x7) << 1
        state.regDE = z80.get_reg_DE()
        state.regBCx = z80.get_reg_BCx()
        state.regDEx = z80.get_reg_DEx()
        state.regHLx = z80.get_reg_HLx()
        state.regAx = z80.regAx
        state.regFx = z80.regFx
        state.regIY = z80.regIY
        state.regIX = z80.regIX
        state.ffIFF1 = z80.ffIFF1
        state.ffIFF2 = z80.ffIFF2
        state.modeINT = z80.modeINT
        return state

    def update_from(self, z80: Z80CPU, border_colour: int) -> None:
        self.regA = z80.regA
        self.regF = z80.get_flags()
        self.regBC = z80.get_reg_BC()
        self.regHL = z80.get_reg_HL()
        self.regPC = z80.regPC
        self.regSP = z80.regSP
        self.regI = z80.regI
        self.regR = z80.regR
        self.extraFlags = z80.regR & 0x80 >> 7 | (border_colour & 0x7) << 1
        self.regDE = z80.get_reg_DE()
        self.regBCx = z80.get_reg_BCx()
        self.regDEx = z80.get_reg_DEx()
        self.regHLx = z80.get_reg_HLx()
        self.regAx = z80.regAx
        self.regFx = z80.regFx
        self.regIY = z80.regIY
        self.regIX = z80.regIX
        self.ffIFF1 = z80.ffIFF1
        self.ffIFF2 = z80.ffIFF2
        self.modeINT = z80.modeINT

    # Returns border colour
    def restore_to(self, z80: Z80CPU) -> int:
        z80.regA = self.regA
        z80.set_flags(self.regF)
        z80.set_reg_BC(self.regBC)
        z80.set_reg_HL(self.regHL)
        z80.set_reg_PC(self.regPC)
        z80.set_reg_SP(self.regSP)
        z80.regI = self.regI
        z80.regR = self.regR
        z80.set_reg_DE(self.regDE)
        z80.set_reg_BCx(self.regBCx)
        z80.set_reg_DEx(self.regDEx)
        z80.set_reg_HLx(self.regHLx)
        z80.regAx = self.regAx
        z80.regFx = self.regFx
        z80.set_reg_IY(self.regIY)
        z80.set_reg_IX(self.regIX)
        z80.ffIFF1 = self.ffIFF1
        z80.ffIFF2 = self.ffIFF2
        z80.modeINT = self.modeINT

        z80.regR = z80.regR | (self.extraFlags & 0x01) << 7
        return (self.extraFlags & 0x0e) >> 1
