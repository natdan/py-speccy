import sys
import struct

from spectrum.spectrum_ports import SpectrumPorts
from z80.z80 import Z80, IM0, IM1, IM2


# This implementation is from PyZX
# https://github.com/Q-Master/PyZX/blob/master/load.py
class Loader:
    def __init__(self, z80: Z80, ports: SpectrumPorts):
        self.z80 = z80
        self.ports = ports
        self._z80_header = struct.Struct('<BBHHHHBBBHHHHBBHHBBB')
        self._sna_struct = struct.Struct('<BHHHHHHHHHBBHHBB')

    def load_z80(self, name):
        """
        Offset  Length  Description
            ---------------------------
            0       1       A register
            1       1       F register
            2       2       BC register pair (LSB, i.e. C, first)
            4       2       HL register pair
            6       2       Program counter
            8       2       Stack pointer
            10      1       Interrupt register
            11      1       Refresh register (Bit 7 is not significant!)
            12      1       Bit 0  : Bit 7 of the R-register
                            Bit 1-3: Border colour
                            Bit 4  : 1=Basic SamRom switched in
                            Bit 5  : 1=Block of data is compressed
                            Bit 6-7: No meaning
            13      2       DE register pair
            15      2       BC' register pair
            17      2       DE' register pair
            19      2       HL' register pair
            21      1       A' register
            22      1       F' register
            23      2       IY register (Again LSB first)
            25      2       IX register
            27      1       Interrupt flipflop, 0=DI, otherwise EI
            28      1       IFF2 (not particularly important...)
            29      1       Bit 0-1: Interrupt mode (0, 1 or 2)
                            Bit 2  : 1=Issue 2 emulation
                            Bit 3  : 1=Double interrupt frequency
                            Bit 4-5: 1=High video synchronisation
                                     3=Low video synchronisation
                                     0,2=Normal
                            Bit 6-7: 0=Cursor/Protek/AGF joystick
                                     1=Kempston joystick
                                     2=Sinclair 2 Left joystick (or user
                                       defined, for version 3 .z80 files)
                                     3=Sinclair 2 Right joystick
        """
        with open(name, 'rb') as f:
            z80file = f.read()
        mz80file = memoryview(z80file)

        self.z80.regA, regF, regBC, regHL, self.z80.regPC, self.z80.regSP, self.z80.regI, regR, tbyte, regDE, \
            regBCx, regDEx, regHLx, self.z80.regAx, regFx, self.z80.regIY, self.z80.regIX, iff1, iff2, im = self._z80_header.unpack_from(mz80file, 0)
        self.z80.set_flags(regF)
        self.z80.set_reg_BC(regBC)
        self.z80.set_reg_HL(regHL)
        self.z80.set_reg_R(regR)
        self.z80.set_reg_DE(regDE)
        self.z80.set_reg_BCx(regBCx)
        self.z80.set_reg_DEx(regDEx)
        self.z80.set_reg_HLx(regHLx)
        self.z80.set_reg_Fx(regFx)

        if tbyte == 255:
            tbyte = 1

        self.ports.out_port(254, ((tbyte >> 1) % 8))  # border

        if (tbyte % 2) != 0:
            regR = regR | 0x80
        self.z80.set_reg_R(regR)

        compressed = ((tbyte & 0x20) != 0)
        self.z80.ffIFF1 = iff1 != 0
        self.z80.ffIFF2 = iff2 != 0

        im = im & 0x03
        if im == 0:
            self.z80.modeINT = IM0
        elif im == 1:
            self.z80.modeINT = IM1
        else:
            self.z80.modeINT = IM2

        if self.z80.regPC == 0:
            self.load_z80_extended(mz80file[30:])
            return

        # Old format Z80 snapshot
        self.load_z80_block(mz80file[30:], 16384, compressed)

    def load_z80_extended(self, mz80file):
        z80_type, self.z80.regPC, zx_type = struct.unpack_from('<HHB', mz80file, 0)
        print(f'first byte: {z80_type}, PC: {self.z80.regPC}')
        if z80_type == 23:  # V2.01
            print('self.z80 (v201)')
            """
            0 - 48K
            1 - 48K + IF1
            2 - SamRam
            3 - 128K
            4 - 128K + IF1
            """
            if zx_type > 1:
                print(f'self.z80 (v201): unsupported type {zx_type}')
                sys.exit()
        elif z80_type == 54:  # V3.00
            print('Z80 (v300)')
            """
            0 - 48K
            1 - 48K + IF1
            2 - 48K + MGT
            3 - SamRam
            4 - 128K
            5 - 128K + IF1
            6 - 128K + MGT
            """
            if zx_type > 2:
                print(f'Z80 (v300): unsupported type {zx_type}')
                sys.exit()
        elif z80_type == 55:  # V3.01
            print('Z80 (v301)')
            """
            0 - 48K
            1 - 48K + IF1
            2 - 48K + MGT
            3 - SamRam
            4 - 128K
            5 - 128K + IF1
            6 - 128K + MGT
            7 - +3
            """
            if zx_type > 2:
                print(f'Z80 (v300): unsupported type {zx_type}')
                sys.exit()
        else:
            print(f'Z80 (extended): unsupported type {z80_type}')
            sys.exit()
        offset = z80_type + 2
        block_struct = struct.Struct('<HB')
        for _ in range(3):
            length, page = block_struct.unpack_from(mz80file, offset)
            offset += 3
            compressed = True
            if length == 0xffff:
                length = 16384
                compressed = False
            if page == 4:
                addr = 32768
            elif page == 5:
                addr = 49152
            elif page == 8:
                addr = 16384
            else:
                print(f'Z80 (page): out of range {page}')
                sys.exit()
            print(f'Len: {length}, Page: {addr}, Compressed: {compressed}')
            self.load_z80_block(mz80file[offset:offset+length], addr, compressed)
            offset += length

    def load_z80_block(self, data, addr, compressed):
        if compressed:
            blocklen = len(data)
            k = 0
            i = 0
            while k < blocklen:
                tbyte = data[i]
                i += 1
                k += 1
                if tbyte != 0xed:
                    self.z80.memory.pokeb(addr, tbyte)
                    addr += 1
                else:
                    tbyte = data[i]
                    i += 1
                    k += 1
                    if tbyte != 0xed:
                        # TODO: check
                        self.z80.memory.pokeb(addr, 0xed)
                        addr += 1
                        i -= 1
                        k -= 1
                    else:
                        count = data[i]
                        i += 1
                        k += 1
                        tbyte = data[i]
                        i += 1
                        k += 1
                        while count > 0:
                            count -= 1
                            self.z80.memory.pokeb(addr, tbyte)
                            addr += 1
        else:
            self.z80.memory.mem[addr:addr+len(data)] = data[:]

    def load_sna(self, name):
        """
        $00  I
        $01  HL'
        $03  DE'
        $05  BC'
        $07  AF'
        $09  HL
        $0B  DE
        $0D  BC
        $0F  IY
        $11  IX
        $13  IFF2    [Only bit 2 is defined: 1 for EI, 0 for DI]
        $14  R
        $15  AF
        $17  SP
        $19  Interrupt mode: 0, 1 or 2
        $1A  Border colour
        """
        with open(name, 'rb') as f:
            snafile = f.read()
        msnafile = memoryview(snafile)

        self.z80.regI, \
            regHLx, regDEx, regBCx, regAFx, \
            regHL, regDE, regBC, self.z80.regIY, self.z80.regIX, \
            iff2, self.z80.regR, regAF, self.z80.regSP, im, border = self._sna_struct.unpack_from(msnafile, 0)
        self.z80.ffIFF2 = (iff2 & 0b100) != 0
        self.z80.ffIFF1 = self.z80.ffIFF2
        if im == 0:
            self.z80.modeINT = IM0
        elif im == 1:
            self.z80.modeINT = IM1
        else:
            self.z80.modeINT = IM2

        self.z80.set_reg_HLx(regHLx)
        self.z80.set_reg_DEx(regDEx)
        self.z80.set_reg_BCx(regBCx)
        self.z80.set_reg_HL(regHL)
        self.z80.set_reg_DE(regDE)
        self.z80.set_reg_BC(regBC)

        self.z80.set_reg_Fx(regAFx & 0xff)
        self.z80.regAx = (regAFx >> 8) & 0xff

        self.z80.set_flags(regAF & 0xff)
        self.z80.regA = (regAF >> 8) & 0xff

        self.ports.out_port(254, (border % 8))  # border
        self.z80.memory.mem[16384:] = msnafile[27:]

        # self.z80.regPC = self.z80.pop()  # self.z80.poppc()
        self.z80.regPC = 0x72  # JSpeccy's implementation uses RET instruction from the ROM
