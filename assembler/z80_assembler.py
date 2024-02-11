
from typing import TextIO, Optional




from typing import Union
from assembler_utils import to_int
from directives import *
from z80.instructions.instruction_def import Instruction
from z80.instructions.instructions import *
from z80.instructions.address_modes import AddrMode


class Z80AssemblerScanner:

    class Token:
        def __init__(self, s: str, id_: int, line: int, pos: int) -> None:
            self.s = s
            self.id_ = id_
            self.line = line
            self.pos = pos

        def length(self) -> int:
            return len(self.s)

        def __repr__(self) -> str:
            return self.s

    # Class variables 
    BOF_CHAR = -1
    EOF_CHAR = -2
    BOL_CHAR = -3

    TOKEN_WHITESPACE = -1

    def __init__(self, reader: Optional[TextIO] = None):
        self.reader = reader
        self.state = 1
        self.id_ = 0
        self.ok = True
        self.ch = 0

        self.buffer = []
        self.read = []

        self.ptr = 0
        self.line = 1
        self.pos = 0
        self.marked_line = 0
        self.marked_pos = 0
        self.start_line = 0
        self.start_pos = 0
        self.emit_bof = False
        self.emit_eof = False  # Not used
        self.emit_bol = True
        self.emit_eol = True
        self.next_bof = False
        self.next_bol = True
        self.live = True
        if self.emit_bof:
            self.live = False
            self.buffer.append(self.BOF_CHAR)
        if self.emit_bol:
            self.live = False
            self.buffer.append(self.BOL_CHAR)

    def eof_token(self) -> Token:
        return self.Token("EOF", self.TOKEN_EOF, self.line, self.pos)

    def eol_token(self) -> Token:
        return self.Token("EOL", self.TOKEN_EOL, self.line, self.pos)

    def bol_token(self) -> Token:
        return self.Token("BOL", self.TOKEN_BOL, self.line, self.pos)

    def mark(self) -> None:
        if self.live:
            if self.ptr >= len(self.buffer):
                self.buffer = []
            else:
                self.buffer = self.buffer[self.ptr:]
                self.live = False
        else:
            self.buffer = self.buffer[self.ptr:]

        self.ptr = 0
        if self.ptr == len(self.buffer):
            self.live = True
        self.marked_line = self.line
        self.marked_pos = self.pos

    def reset(self) -> None:
        if len(self.buffer) > 0 and self.ptr > 0:
            self.read = self.read[:len(self.read) - self.ptr]
            self.live = False
            self.ptr = 0

        self.line = self.marked_line
        self.pos = self.marked_pos

    def get_next_char(self) -> int:
        if self.live:
            try:
                c = self.reader.read(1)
                if c != "":
                    c = ord(c)
                    self.buffer.append(c)
                    self.ptr += 1
                    if self.emit_bol and c == 10:
                        self.buffer.append(self.BOL_CHAR)
                else:
                    c = self.EOF_CHAR
            except Exception:
                c = self.EOF_CHAR
        else:
            buffer_len = len(self.buffer)
            c = self.buffer[self.ptr]
            self.ptr += 1
            if self.ptr == buffer_len:
                self.live = True
        if c == 10:  # '\n'
            self.pos = 0
            self.line += 1
        else:
            self.pos += 1
        if c != self.EOF_CHAR:
            self.read.append(c)
        return c

    TOKEN_BOF = 0
    TOKEN_EOF = 1
    TOKEN_BOL = 2
    TOKEN_EOL = 3
    # = = 4
    # ; = 5
    # , = 6
    # . = 7
    # ( = 8
    # ) = 9
    # + = 10
    # - = 11
    # adc = 12
    # add = 13
    # and = 14
    # bit = 15
    # call = 16
    # ccf = 17
    # cp = 18
    # cpd = 19
    # cpdr = 20
    # cpi = 21
    # cpir = 22
    # cpl = 23
    # daa = 24
    # dec = 25
    # di = 26
    # djnz = 27
    # ei = 28
    # ex = 29
    # exx = 30
    # halt = 31
    # im = 32
    # in = 33
    # inc = 34
    # ind = 35
    # indr = 36
    # ini = 37
    # inir = 38
    # jp = 39
    # jr = 40
    # ld = 41
    # ldd = 42
    # lddr = 43
    # ldi = 44
    # ldir = 45
    # neg = 46
    # nop = 47
    # or = 48
    # otdr = 49
    # otir = 50
    # out = 51
    # outd = 52
    # outi = 53
    # pop = 54
    # push = 55
    # res = 56
    # ret = 57
    # reti = 58
    # retn = 59
    # rl = 60
    # rla = 61
    # rlc = 62
    # rlca = 63
    # rld = 64
    # rr = 65
    # rra = 66
    # rrc = 67
    # rrca = 68
    # rrd = 69
    # rst = 70
    # sbc = 71
    # scf = 72
    # set = 73
    # sla = 74
    # sra = 75
    # srl = 76
    # sub = 77
    # xor = 78
    # a = 79
    # b = 80
    # c = 81
    # d = 82
    # e = 83
    # h = 84
    # l = 85
    # i = 86
    # r = 87
    # bc = 88
    # de = 89
    # hl = 90
    # ix = 91
    # iy = 92
    # af = 93
    # af' = 94
    # sp = 95
    # nz = 96
    # z = 97
    # nc = 98
    # po = 99
    # pe = 100
    # p = 101
    # m = 102
    # + = 103
    # - = 104
    # * = 105
    # / = 106
    # << = 107
    # >> = 108
    # ~ = 109
    # ! = 110
    # & = 111
    # | = 112
    # && = 113
    # || = 114
    # ? = 115
    # = = 116
    # != = 117
    # > = 118
    # < = 119
    # <= = 120
    # >= = 121
    # mod = 122
    # % = 123
    # shl = 124
    # shr = 125
    # eq = 126
    # ne = 127
    # lt = 128
    # le = 129
    # gt = 130
    # ge = 131
    # $ = 132
    # nul = 133
    # ^ = 134
    # org = 135
    # end = 136
    # None = -1
    # None = -1
    # None = -1
    TOKEN_literal = 140
    # None = -1
    TOKEN_string = 142
    TOKEN_ident = 143
    TOKEN_label = 144
    TOKEN_unsigned_number = 145
    # None = -1
    TOKEN_comments = 147
    #   = -1
    TOKEN_eol = 149
    TOKEN_eof = 150
    TOKEN_bol = 151

    BOF_TOKEN = Token("BOF", TOKEN_BOF, -1, -1)

    def set_reader(self, reader: TextIO) -> None:
        self.reader = reader

    def get_next_token(self) -> Token:
        t = self.get_next_token_state_machine()
        while t.id_ == Z80AssemblerScanner.TOKEN_WHITESPACE:
            t = self.get_next_token_state_machine()
        return t

    def get_next_token_state_machine(self) -> Token:
        self.start_line = self.line
        self.start_pos = self.pos
        self.mark()
        self.read = []
        self.state = 1
        self.id_ = 0
        self.ok = True
        self.ch = 0
        while self.ok:
            self.ch = self.get_next_char()
            # print(f"{self.state}: {self.ch} {chr(self.ch)}
# total nodes: 195
            if self.state == 1:
                if self.ch == -3:
                    self.id_ = self.TOKEN_bol
                    self.mark()
                    self.state = 2
                elif self.ch == -2:
                    self.id_ = self.TOKEN_eof
                    self.mark()
                    self.state = 5
                elif (1 <= self.ch <= 9) or (11 <= self.ch <= 32):
                    self.start_line = self.line
                    self.start_pos = self.pos
                    self.mark()
                    self.read = []
                    self.state = 1
                elif self.ch == 10:
                    self.id_ = self.TOKEN_eol
                    self.mark()
                    self.state = 7
                elif self.ch == 33:
                    self.id_ = 110
                    self.mark()
                    self.state = 8
                elif self.ch == 34:
                    self.state = 10
                elif self.ch == 36:
                    self.id_ = 132
                    self.mark()
                    self.state = 14
                elif self.ch == 37:
                    self.id_ = 123
                    self.mark()
                    self.state = 15
                elif self.ch == 38:
                    self.id_ = 111
                    self.mark()
                    self.state = 16
                elif self.ch == 39:
                    self.state = 18
                elif self.ch == 40:
                    self.id_ = 8
                    self.mark()
                    self.state = 22
                elif self.ch == 41:
                    self.id_ = 9
                    self.mark()
                    self.state = 23
                elif self.ch == 42:
                    self.id_ = 105
                    self.mark()
                    self.state = 24
                elif self.ch == 43:
                    self.id_ = 10
                    self.mark()
                    self.state = 25
                elif self.ch == 44:
                    self.id_ = 6
                    self.mark()
                    self.state = 26
                elif self.ch == 45:
                    self.id_ = 11
                    self.mark()
                    self.state = 27
                elif self.ch == 46:
                    self.id_ = 7
                    self.mark()
                    self.state = 28
                elif self.ch == 47:
                    self.id_ = 106
                    self.mark()
                    self.state = 30
                elif self.ch == 48:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 31
                elif 49 <= self.ch <= 57:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 32
                elif self.ch == 59:
                    self.id_ = 5
                    self.mark()
                    self.state = 36
                elif self.ch == 60:
                    self.id_ = 119
                    self.mark()
                    self.state = 39
                elif self.ch == 61:
                    self.id_ = 4
                    self.mark()
                    self.state = 42
                elif self.ch == 62:
                    self.id_ = 118
                    self.mark()
                    self.state = 43
                elif self.ch == 63:
                    self.id_ = 115
                    self.mark()
                    self.state = 46
                elif (65 <= self.ch <= 66) or (68 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 102) or (self.ch == 107) or (self.ch == 113) or (116 <= self.ch <= 119) or (self.ch == 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 67:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 47
                elif self.ch == 94:
                    self.id_ = 134
                    self.mark()
                    self.state = 52
                elif self.ch == 97:
                    self.id_ = 79
                    self.mark()
                    self.state = 53
                elif self.ch == 98:
                    self.id_ = 80
                    self.mark()
                    self.state = 61
                elif self.ch == 99:
                    self.id_ = 81
                    self.mark()
                    self.state = 65
                elif self.ch == 100:
                    self.id_ = 82
                    self.mark()
                    self.state = 77
                elif self.ch == 101:
                    self.id_ = 83
                    self.mark()
                    self.state = 86
                elif self.ch == 103:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 93
                elif self.ch == 104:
                    self.id_ = 84
                    self.mark()
                    self.state = 96
                elif self.ch == 105:
                    self.id_ = 86
                    self.mark()
                    self.state = 101
                elif self.ch == 106:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 111
                elif self.ch == 108:
                    self.id_ = 85
                    self.mark()
                    self.state = 114
                elif self.ch == 109:
                    self.id_ = 102
                    self.mark()
                    self.state = 122
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 125
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 134
                elif self.ch == 112:
                    self.id_ = 101
                    self.mark()
                    self.state = 146
                elif self.ch == 114:
                    self.id_ = 87
                    self.mark()
                    self.state = 153
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 171
                elif self.ch == 120:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 189
                elif self.ch == 122:
                    self.id_ = 97
                    self.mark()
                    self.state = 192
                elif self.ch == 124:
                    self.id_ = 112
                    self.mark()
                    self.state = 193
                elif self.ch == 126:
                    self.id_ = 109
                    self.mark()
                    self.state = 195
                elif self.ch == self.EOF_CHAR:
                    return self.Token("<eof>", self.TOKEN_EOF, self.start_line, self.start_pos)
                else:
                    self.ok = False
                
            elif self.state == 2:
                if (self.ch == 46) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.state = 3
                else:
                    self.ok = False
                
            elif self.state == 3:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.state = 3
                elif self.ch == 58:
                    self.id_ = self.TOKEN_label
                    self.mark()
                    self.state = 4
                else:
                    self.ok = False
                
            elif self.state == 4:
                self.ok = False
            elif self.state == 5:
                self.ok = False
            elif self.state == 6:
                if self.ch == 10:
                    self.id_ = self.TOKEN_eol
                    self.mark()
                    self.state = 7
                else:
                    self.ok = False
                
            elif self.state == 7:
                self.ok = False
            elif self.state == 8:
                if self.ch == 61:
                    self.id_ = 117
                    self.mark()
                    self.state = 9
                else:
                    self.ok = False
                
            elif self.state == 9:
                self.ok = False
            elif self.state == 10:
                if (32 <= self.ch <= 33) or (35 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 11
                elif self.ch == 34:
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 12
                elif self.ch == 92:
                    self.state = 13
                else:
                    self.ok = False
                
            elif self.state == 11:
                if (32 <= self.ch <= 33) or (35 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 11
                elif self.ch == 34:
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 12
                elif self.ch == 92:
                    self.state = 13
                else:
                    self.ok = False
                
            elif self.state == 12:
                self.ok = False
            elif self.state == 13:
                if (32 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 11
                elif self.ch == 92:
                    self.state = 13
                else:
                    self.ok = False
                
            elif self.state == 14:
                self.ok = False
            elif self.state == 15:
                self.ok = False
            elif self.state == 16:
                if self.ch == 38:
                    self.id_ = 113
                    self.mark()
                    self.state = 17
                else:
                    self.ok = False
                
            elif self.state == 17:
                self.ok = False
            elif self.state == 18:
                if (32 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.state = 19
                elif self.ch == 92:
                    self.state = 21
                else:
                    self.ok = False
                
            elif self.state == 19:
                if self.ch == 39:
                    self.id_ = self.TOKEN_literal
                    self.mark()
                    self.state = 20
                else:
                    self.ok = False
                
            elif self.state == 20:
                self.ok = False
            elif self.state == 21:
                if 32 <= self.ch <= 127:
                    self.state = 19
                else:
                    self.ok = False
                
            elif self.state == 22:
                self.ok = False
            elif self.state == 23:
                self.ok = False
            elif self.state == 24:
                self.ok = False
            elif self.state == 25:
                self.ok = False
            elif self.state == 26:
                self.ok = False
            elif self.state == 27:
                self.ok = False
            elif self.state == 28:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 29:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 30:
                self.ok = False
            elif self.state == 31:
                if 48 <= self.ch <= 57:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 32
                elif (self.ch == 72) or (self.ch == 104):
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 33
                elif self.ch == 120:
                    self.state = 34
                else:
                    self.ok = False
                
            elif self.state == 32:
                if 48 <= self.ch <= 57:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 32
                elif (self.ch == 72) or (self.ch == 104):
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 33
                else:
                    self.ok = False
                
            elif self.state == 33:
                self.ok = False
            elif self.state == 34:
                if (48 <= self.ch <= 57) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 35
                else:
                    self.ok = False
                
            elif self.state == 35:
                if (48 <= self.ch <= 57) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 35
                else:
                    self.ok = False
                
            elif self.state == 36:
                if (1 <= self.ch <= 9) or (11 <= self.ch <= 127):
                    self.state = 37
                elif self.ch == 10:
                    self.id_ = self.TOKEN_comments
                    self.mark()
                    self.state = 38
                else:
                    self.ok = False
                
            elif self.state == 37:
                if (1 <= self.ch <= 9) or (11 <= self.ch <= 127):
                    self.state = 37
                elif self.ch == 10:
                    self.id_ = self.TOKEN_comments
                    self.mark()
                    self.state = 38
                else:
                    self.ok = False
                
            elif self.state == 38:
                self.ok = False
            elif self.state == 39:
                if self.ch == 60:
                    self.id_ = 107
                    self.mark()
                    self.state = 40
                elif self.ch == 61:
                    self.id_ = 120
                    self.mark()
                    self.state = 41
                else:
                    self.ok = False
                
            elif self.state == 40:
                self.ok = False
            elif self.state == 41:
                self.ok = False
            elif self.state == 42:
                self.ok = False
            elif self.state == 43:
                if self.ch == 61:
                    self.id_ = 121
                    self.mark()
                    self.state = 44
                elif self.ch == 62:
                    self.id_ = 108
                    self.mark()
                    self.state = 45
                else:
                    self.ok = False
                
            elif self.state == 44:
                self.ok = False
            elif self.state == 45:
                self.ok = False
            elif self.state == 46:
                self.ok = False
            elif self.state == 47:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 71) or (73 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 72:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 48
                else:
                    self.ok = False
                
            elif self.state == 48:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 81) or (83 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 82:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 49
                else:
                    self.ok = False
                
            elif self.state == 49:
                if self.ch == 40:
                    self.state = 50
                elif (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 50:
                if 48 <= self.ch <= 57:
                    self.state = 51
                else:
                    self.ok = False
                
            elif self.state == 51:
                if self.ch == 41:
                    self.id_ = self.TOKEN_literal
                    self.mark()
                    self.state = 20
                elif 48 <= self.ch <= 57:
                    self.state = 51
                else:
                    self.ok = False
                
            elif self.state == 52:
                self.ok = False
            elif self.state == 53:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (self.ch == 101) or (103 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 54
                elif self.ch == 102:
                    self.id_ = 93
                    self.mark()
                    self.state = 57
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 59
                else:
                    self.ok = False
                
            elif self.state == 54:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 12
                    self.mark()
                    self.state = 55
                elif self.ch == 100:
                    self.id_ = 13
                    self.mark()
                    self.state = 56
                else:
                    self.ok = False
                
            elif self.state == 55:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 56:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 57:
                if self.ch == 39:
                    self.id_ = 94
                    self.mark()
                    self.state = 58
                elif (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 58:
                self.ok = False
            elif self.state == 59:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 14
                    self.mark()
                    self.state = 60
                else:
                    self.ok = False
                
            elif self.state == 60:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 61:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 88
                    self.mark()
                    self.state = 62
                elif self.ch == 105:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 63
                else:
                    self.ok = False
                
            elif self.state == 62:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 63:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 116:
                    self.id_ = 15
                    self.mark()
                    self.state = 64
                else:
                    self.ok = False
                
            elif self.state == 64:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 65:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (100 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 66
                elif self.ch == 99:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 69
                elif self.ch == 112:
                    self.id_ = 18
                    self.mark()
                    self.state = 71
                else:
                    self.ok = False
                
            elif self.state == 66:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 67
                else:
                    self.ok = False
                
            elif self.state == 67:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 108:
                    self.id_ = 16
                    self.mark()
                    self.state = 68
                else:
                    self.ok = False
                
            elif self.state == 68:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 69:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 101) or (103 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 102:
                    self.id_ = 17
                    self.mark()
                    self.state = 70
                else:
                    self.ok = False
                
            elif self.state == 70:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 71:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 19
                    self.mark()
                    self.state = 72
                elif self.ch == 105:
                    self.id_ = 21
                    self.mark()
                    self.state = 74
                elif self.ch == 108:
                    self.id_ = 23
                    self.mark()
                    self.state = 76
                else:
                    self.ok = False
                
            elif self.state == 72:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 20
                    self.mark()
                    self.state = 73
                else:
                    self.ok = False
                
            elif self.state == 73:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 74:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 22
                    self.mark()
                    self.state = 75
                else:
                    self.ok = False
                
            elif self.state == 75:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 76:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 77:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 100) or (102 <= self.ch <= 104) or (107 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 78
                elif self.ch == 101:
                    self.id_ = 89
                    self.mark()
                    self.state = 80
                elif self.ch == 105:
                    self.id_ = 26
                    self.mark()
                    self.state = 82
                elif self.ch == 106:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 83
                else:
                    self.ok = False
                
            elif self.state == 78:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 24
                    self.mark()
                    self.state = 79
                else:
                    self.ok = False
                
            elif self.state == 79:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 80:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 25
                    self.mark()
                    self.state = 81
                else:
                    self.ok = False
                
            elif self.state == 81:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 82:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 83:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 84
                else:
                    self.ok = False
                
            elif self.state == 84:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 122:
                    self.id_ = 27
                    self.mark()
                    self.state = 85
                else:
                    self.ok = False
                
            elif self.state == 85:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 86:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 104) or (106 <= self.ch <= 109) or (111 <= self.ch <= 112) or (114 <= self.ch <= 119) or (121 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 105:
                    self.id_ = 28
                    self.mark()
                    self.state = 87
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 88
                elif self.ch == 113:
                    self.id_ = 126
                    self.mark()
                    self.state = 90
                elif self.ch == 120:
                    self.id_ = 29
                    self.mark()
                    self.state = 91
                else:
                    self.ok = False
                
            elif self.state == 87:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 88:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 136
                    self.mark()
                    self.state = 89
                else:
                    self.ok = False
                
            elif self.state == 89:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 90:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 91:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 119) or (121 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 120:
                    self.id_ = 30
                    self.mark()
                    self.state = 92
                else:
                    self.ok = False
                
            elif self.state == 92:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 93:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 100) or (102 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 101:
                    self.id_ = 131
                    self.mark()
                    self.state = 94
                elif self.ch == 116:
                    self.id_ = 130
                    self.mark()
                    self.state = 95
                else:
                    self.ok = False
                
            elif self.state == 94:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 95:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 96:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 97
                elif self.ch == 108:
                    self.id_ = 90
                    self.mark()
                    self.state = 100
                else:
                    self.ok = False
                
            elif self.state == 97:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 98
                else:
                    self.ok = False
                
            elif self.state == 98:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 116:
                    self.id_ = 31
                    self.mark()
                    self.state = 99
                else:
                    self.ok = False
                
            elif self.state == 99:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 100:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 101:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 108) or (111 <= self.ch <= 119) or (self.ch == 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 109:
                    self.id_ = 32
                    self.mark()
                    self.state = 102
                elif self.ch == 110:
                    self.id_ = 33
                    self.mark()
                    self.state = 103
                elif self.ch == 120:
                    self.id_ = 91
                    self.mark()
                    self.state = 109
                elif self.ch == 121:
                    self.id_ = 92
                    self.mark()
                    self.state = 110
                else:
                    self.ok = False
                
            elif self.state == 102:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 103:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 34
                    self.mark()
                    self.state = 104
                elif self.ch == 100:
                    self.id_ = 35
                    self.mark()
                    self.state = 105
                elif self.ch == 105:
                    self.id_ = 37
                    self.mark()
                    self.state = 107
                else:
                    self.ok = False
                
            elif self.state == 104:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 105:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 36
                    self.mark()
                    self.state = 106
                else:
                    self.ok = False
                
            elif self.state == 106:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 107:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 38
                    self.mark()
                    self.state = 108
                else:
                    self.ok = False
                
            elif self.state == 108:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 109:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 110:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 111:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (self.ch == 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 112:
                    self.id_ = 39
                    self.mark()
                    self.state = 112
                elif self.ch == 114:
                    self.id_ = 40
                    self.mark()
                    self.state = 113
                else:
                    self.ok = False
                
            elif self.state == 112:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 113:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 114:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (102 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 41
                    self.mark()
                    self.state = 115
                elif self.ch == 101:
                    self.id_ = 129
                    self.mark()
                    self.state = 120
                elif self.ch == 116:
                    self.id_ = 128
                    self.mark()
                    self.state = 121
                else:
                    self.ok = False
                
            elif self.state == 115:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 42
                    self.mark()
                    self.state = 116
                elif self.ch == 105:
                    self.id_ = 44
                    self.mark()
                    self.state = 118
                else:
                    self.ok = False
                
            elif self.state == 116:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 43
                    self.mark()
                    self.state = 117
                else:
                    self.ok = False
                
            elif self.state == 117:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 118:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 45
                    self.mark()
                    self.state = 119
                else:
                    self.ok = False
                
            elif self.state == 119:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 120:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 121:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 122:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 110) or (112 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 123
                else:
                    self.ok = False
                
            elif self.state == 123:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 122
                    self.mark()
                    self.state = 124
                else:
                    self.ok = False
                
            elif self.state == 124:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 125:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (self.ch == 100) or (102 <= self.ch <= 110) or (112 <= self.ch <= 116) or (118 <= self.ch <= 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 98
                    self.mark()
                    self.state = 126
                elif self.ch == 101:
                    self.id_ = 127
                    self.mark()
                    self.state = 127
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 129
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 131
                elif self.ch == 122:
                    self.id_ = 96
                    self.mark()
                    self.state = 133
                else:
                    self.ok = False
                
            elif self.state == 126:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 127:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 102) or (104 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 103:
                    self.id_ = 46
                    self.mark()
                    self.state = 128
                else:
                    self.ok = False
                
            elif self.state == 128:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 129:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 112:
                    self.id_ = 47
                    self.mark()
                    self.state = 130
                else:
                    self.ok = False
                
            elif self.state == 130:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 131:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 108:
                    self.id_ = 133
                    self.mark()
                    self.state = 132
                else:
                    self.ok = False
                
            elif self.state == 132:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 133:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 134:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (self.ch == 115) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 48
                    self.mark()
                    self.state = 135
                elif self.ch == 116:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 137
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 142
                else:
                    self.ok = False
                
            elif self.state == 135:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 102) or (104 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 103:
                    self.id_ = 135
                    self.mark()
                    self.state = 136
                else:
                    self.ok = False
                
            elif self.state == 136:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 137:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 138
                elif self.ch == 105:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 140
                else:
                    self.ok = False
                
            elif self.state == 138:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 49
                    self.mark()
                    self.state = 139
                else:
                    self.ok = False
                
            elif self.state == 139:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 140:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 50
                    self.mark()
                    self.state = 141
                else:
                    self.ok = False
                
            elif self.state == 141:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 142:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 116:
                    self.id_ = 51
                    self.mark()
                    self.state = 143
                else:
                    self.ok = False
                
            elif self.state == 143:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 100:
                    self.id_ = 52
                    self.mark()
                    self.state = 144
                elif self.ch == 105:
                    self.id_ = 53
                    self.mark()
                    self.state = 145
                else:
                    self.ok = False
                
            elif self.state == 144:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 145:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 146:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 100) or (102 <= self.ch <= 110) or (112 <= self.ch <= 116) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 101:
                    self.id_ = 100
                    self.mark()
                    self.state = 147
                elif self.ch == 111:
                    self.id_ = 99
                    self.mark()
                    self.state = 148
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 150
                else:
                    self.ok = False
                
            elif self.state == 147:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 148:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 112:
                    self.id_ = 54
                    self.mark()
                    self.state = 149
                else:
                    self.ok = False
                
            elif self.state == 149:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 150:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 114) or (116 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 151
                else:
                    self.ok = False
                
            elif self.state == 151:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 103) or (105 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 104:
                    self.id_ = 55
                    self.mark()
                    self.state = 152
                else:
                    self.ok = False
                
            elif self.state == 152:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 153:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 100) or (102 <= self.ch <= 107) or (109 <= self.ch <= 113) or (116 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 101:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 154
                elif self.ch == 108:
                    self.id_ = 60
                    self.mark()
                    self.state = 159
                elif self.ch == 114:
                    self.id_ = 65
                    self.mark()
                    self.state = 164
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 169
                else:
                    self.ok = False
                
            elif self.state == 154:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 114) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 115:
                    self.id_ = 56
                    self.mark()
                    self.state = 155
                elif self.ch == 116:
                    self.id_ = 57
                    self.mark()
                    self.state = 156
                else:
                    self.ok = False
                
            elif self.state == 155:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 156:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 104) or (106 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 105:
                    self.id_ = 58
                    self.mark()
                    self.state = 157
                elif self.ch == 110:
                    self.id_ = 59
                    self.mark()
                    self.state = 158
                else:
                    self.ok = False
                
            elif self.state == 157:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 158:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 159:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 61
                    self.mark()
                    self.state = 160
                elif self.ch == 99:
                    self.id_ = 62
                    self.mark()
                    self.state = 161
                elif self.ch == 100:
                    self.id_ = 64
                    self.mark()
                    self.state = 163
                else:
                    self.ok = False
                
            elif self.state == 160:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 161:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 63
                    self.mark()
                    self.state = 162
                else:
                    self.ok = False
                
            elif self.state == 162:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 163:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 164:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 66
                    self.mark()
                    self.state = 165
                elif self.ch == 99:
                    self.id_ = 67
                    self.mark()
                    self.state = 166
                elif self.ch == 100:
                    self.id_ = 69
                    self.mark()
                    self.state = 168
                else:
                    self.ok = False
                
            elif self.state == 165:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 166:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 68
                    self.mark()
                    self.state = 167
                else:
                    self.ok = False
                
            elif self.state == 167:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 168:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 169:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 116:
                    self.id_ = 70
                    self.mark()
                    self.state = 170
                else:
                    self.ok = False
                
            elif self.state == 170:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 171:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 97) or (self.ch == 100) or (102 <= self.ch <= 103) or (105 <= self.ch <= 107) or (109 <= self.ch <= 111) or (self.ch == 113) or (115 <= self.ch <= 116) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 98:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 172
                elif self.ch == 99:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 174
                elif self.ch == 101:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 176
                elif self.ch == 104:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 178
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 181
                elif self.ch == 112:
                    self.id_ = 95
                    self.mark()
                    self.state = 183
                elif self.ch == 114:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 184
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 187
                else:
                    self.ok = False
                
            elif self.state == 172:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 99:
                    self.id_ = 71
                    self.mark()
                    self.state = 173
                else:
                    self.ok = False
                
            elif self.state == 173:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 174:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 101) or (103 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 102:
                    self.id_ = 72
                    self.mark()
                    self.state = 175
                else:
                    self.ok = False
                
            elif self.state == 175:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 176:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 116:
                    self.id_ = 73
                    self.mark()
                    self.state = 177
                else:
                    self.ok = False
                
            elif self.state == 177:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 178:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 108:
                    self.id_ = 124
                    self.mark()
                    self.state = 179
                elif self.ch == 114:
                    self.id_ = 125
                    self.mark()
                    self.state = 180
                else:
                    self.ok = False
                
            elif self.state == 179:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 180:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 181:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 74
                    self.mark()
                    self.state = 182
                else:
                    self.ok = False
                
            elif self.state == 182:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 183:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 184:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 97:
                    self.id_ = 75
                    self.mark()
                    self.state = 185
                elif self.ch == 108:
                    self.id_ = 76
                    self.mark()
                    self.state = 186
                else:
                    self.ok = False
                
            elif self.state == 185:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 186:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 187:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 97) or (99 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 98:
                    self.id_ = 77
                    self.mark()
                    self.state = 188
                else:
                    self.ok = False
                
            elif self.state == 188:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 189:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 110) or (112 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 190
                else:
                    self.ok = False
                
            elif self.state == 190:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                elif self.ch == 114:
                    self.id_ = 78
                    self.mark()
                    self.state = 191
                else:
                    self.ok = False
                
            elif self.state == 191:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 192:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 193:
                if self.ch == 124:
                    self.id_ = 114
                    self.mark()
                    self.state = 194
                else:
                    self.ok = False
                
            elif self.state == 194:
                self.ok = False
            elif self.state == 195:
                self.ok = False
            if self.id_ == 0 and self.ch == 0:
                return self.eof_token()

        self.reset()
        s = "".join(chr(c) for c in self.read if c > 0)
        if self.id_ == self.TOKEN_EOL:
            if self.emit_bol: self.next_bol = True
        elif self.id_ == self.TOKEN_literal:
            c = ' '
            if s.startswith("CHR("):
                try:
                    c = chr(int(s[4:-1]))
                except Exception:
                    pass
            elif s.startswith("'\\"):
                c = s[2]
            else:
                c = s[1]
            return Token(c, self.TOKEN_literal, self.start_line, self.start_pos)
        elif self.id_ == self.TOKEN_string:
            i = s.find('\\')
            if i > 0:
                l = 0
                sb = ""
                while i > 0:
                    sb += s[l:i]
                    sb += s[i + 1]
                    l = i + 2
                    i = s.find('\\', l)
                s = sb
            return Token(s[1:-1], self.TOKEN_string, self.start_line, self.start_pos)
        return self.Token("".join(chr(c) for c in self.read if c > 0), self.id_, self.start_line, self.start_pos)


Token = Z80AssemblerScanner.Token


class ParserError(Exception):
    def __init__(self, s: Optional[str] = None, t: Optional[Token] = None, nt: Optional[Token] = None, expected: Optional[str] = None, e: Optional[Exception] = None) -> None:
        super().__init__(self.create_message(t, nt, expected) if t is not None else s, e)
        self.line = -1 if t is None else t.line
        self.pos = -1 if t is None else t.pos
        self.raw_message = "" if expected is None else f"expected {expected}"

    @staticmethod
    def create_message(t: Token, nt: Optional[Token] = None, expected: Optional[str] = None) -> str:
        res = ""
        if nt is not None and nt != t and nt is not t:
            res += f"Error after '{t}' ({t.id_})"
            res += f" at '{nt}' ({t.id_})"
        else:
            res += f"Error at/after '{t}' ({t.id_})"

        res += f"[{t.line}, {t.pos}]"
        if expected is not None and len(expected) > 0:
            res += f" expected {expected}"

        return res


class Z80AssemblerParser:

    SCANNER_CLASS = Z80AssemblerScanner

    def __init__(self) -> None:
        self.scanner: Optional[Z80AssemblerScanner] = None
        self.t: Token = Z80AssemblerScanner.BOF_TOKEN
        self.nt: Token = self.t
        self.id_ = 0

        self.string = ""

        self.instructions: list[Union[Instruction, Directive]] = []
        self.value: Optional[Union[int, str]] = None
        self.reg = 0
        self._cc = 0

    def parse(self, scanner) -> None:
        self.scanner = scanner
        self.next()
        self.z80()

    def next(self) -> None:
        self.t = self.nt
        self.nt = self.scanner.get_next_token()
        self.id_ = self.nt.id_

    # z80<> = {(.k=1.) label CODE|bol [(.k=1.) instruction|directive|macro_invocation] (.k=1.) comments|eol|eof} eof
    def z80(self):
        while (self.id_ == Z80AssemblerScanner.TOKEN_label) or (self.id_ == Z80AssemblerScanner.TOKEN_bol):
            if self.id_ == Z80AssemblerScanner.TOKEN_label:
                if self.id_ == Z80AssemblerScanner.TOKEN_label:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\":\"")
                self.instructions.append(Label(self.t.s)) 
            elif self.id_ == Z80AssemblerScanner.TOKEN_bol:
                if self.id_ == Z80AssemblerScanner.TOKEN_bol:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="bol")
            else:
                raise ParserError(t=self.t, expected="ident,eof")
            if (12 <= self.id_ <= 78) or (135 <= self.id_ <= 136) or (self.id_ == Z80AssemblerScanner.TOKEN_ident):
                if 12 <= self.id_ <= 78:
                    self.instruction()
                elif 135 <= self.id_ <= 136:
                    self.directive()
                elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
                    self.macro_invocation()
                else:
                    raise ParserError(t=self.t, expected="'-','adc','add','and','bit','call','ccf','cp','cpd','cpdr','cpi','cpir','cpl','daa','dec','di','djnz','ei','ex','exx','halt','im','in','inc','ind','indr','ini','inir','jp','jr','ld','ldd','lddr','ldi','ldir','neg','nop','or','otdr','otir','out','outd','outi','pop','push','res','ret','reti','retn','rl','rla','rlc','rlca','rld','rr','rra','rrc','rrca','rrd','rst','sbc','scf','set','sla','sra','srl','sub','^','org',string")
            if self.id_ == Z80AssemblerScanner.TOKEN_comments:
                if self.id_ == Z80AssemblerScanner.TOKEN_comments:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\";\"")
            elif self.id_ == Z80AssemblerScanner.TOKEN_eol:
                if self.id_ == Z80AssemblerScanner.TOKEN_eol:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="eol")
            elif self.id_ == Z80AssemblerScanner.TOKEN_eof:
                if self.id_ == Z80AssemblerScanner.TOKEN_eof:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="eof")
            else:
                raise ParserError(t=self.t, expected="allbuteol,whitespace,eol")
        if self.id_ == Z80AssemblerScanner.TOKEN_eof:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="eof")

    # instruction<> = (.k=1.) adc adc_op|add add_op|and s_op|bit bit_op|call call_op|ccf CODE|cp s_op|cpd CODE|cpdr CODE
    #    |cpi CODE|cpir CODE|cpl CODE|daa CODE|dec incdec|di CODE|djnz relative CODE|ei CODE|ex ex_op|exx CODE|halt CODE
    #    |im im_op|in in_op|inc incdec|ind CODE|indr CODE|ini CODE|inir CODE|jp jp_op|jr jr_op|ld ld_op|ldd CODE|lddr CO
    #    DE|ldi CODE|ldir CODE|neg CODE|nop CODE|or s_op|otdr CODE|otir CODE|out out_op|outd CODE|outi CODE|pop pop_op|p
    #    ush pop_op|res bit_op|ret ret_op|reti CODE|retn CODE|rl m_op|rla CODE|rlc m_op|rlca CODE|rld CODE|rr m_op|rra C
    #    ODE|rrc m_op|rrca CODE|rrd CODE|rst immediate CODE|sbc sbc_op|scf CODE|set bit_op|sla m_op|sra m_op|srl m_op|su
    #    b s_op|xor s_op
    def instruction(self):
        if self.id_ == 12:
            if self.id_ == 12:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"adc\"")
            self.adc_op()
        elif self.id_ == 13:
            if self.id_ == 13:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"add\"")
            self.add_op()
        elif self.id_ == 14:
            if self.id_ == 14:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"and\"")
            self.s_op(AND())
        elif self.id_ == 15:
            if self.id_ == 15:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bit\"")
            self.bit_op(BIT())
        elif self.id_ == 16:
            if self.id_ == 16:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"call\"")
            self.call_op()
        elif self.id_ == 17:
            if self.id_ == 17:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ccf\"")
            self.instructions.append(Instruction(0, CCF, AddrMode.SIMPLE)) 
        elif self.id_ == 18:
            if self.id_ == 18:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cp\"")
            self.s_op(CP())
        elif self.id_ == 19:
            if self.id_ == 19:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpd\"")
            self.instructions.append(Instruction(0, CPD, AddrMode.SIMPLE)) 
        elif self.id_ == 20:
            if self.id_ == 20:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpdr\"")
            self.instructions.append(Instruction(0, CPDR, AddrMode.SIMPLE)) 
        elif self.id_ == 21:
            if self.id_ == 21:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpi\"")
            self.instructions.append(Instruction(0, CPI, AddrMode.SIMPLE)) 
        elif self.id_ == 22:
            if self.id_ == 22:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpir\"")
            self.instructions.append(Instruction(0, CPIR, AddrMode.SIMPLE)) 
        elif self.id_ == 23:
            if self.id_ == 23:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpl\"")
            self.instructions.append(Instruction(0, CPL, AddrMode.SIMPLE)) 
        elif self.id_ == 24:
            if self.id_ == 24:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"daa\"")
            self.instructions.append(Instruction(0, DAA, AddrMode.SIMPLE)) 
        elif self.id_ == 25:
            if self.id_ == 25:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"dec\"")
            self.incdec(DEC())
        elif self.id_ == 26:
            if self.id_ == 26:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"di\"")
            self.instructions.append(Instruction(0, DI, AddrMode.SIMPLE)) 
        elif self.id_ == 27:
            if self.id_ == 27:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"djnz\"")
            self.relative()
            self.instructions.append(Instruction(0, DJNZ(), AddrMode.E, e=self.value)) 
        elif self.id_ == 28:
            if self.id_ == 28:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ei\"")
            self.instructions.append(Instruction(0, EI, AddrMode.SIMPLE)) 
        elif self.id_ == 29:
            if self.id_ == 29:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ex\"")
            self.ex_op()
        elif self.id_ == 30:
            if self.id_ == 30:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"exx\"")
            self.instructions.append(Instruction(0, EXX, AddrMode.SIMPLE)) 
        elif self.id_ == 31:
            if self.id_ == 31:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"halt\"")
            self.instructions.append(Instruction(0, HALT, AddrMode.SIMPLE)) 
        elif self.id_ == 32:
            if self.id_ == 32:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"im\"")
            self.im_op()
        elif self.id_ == 33:
            if self.id_ == 33:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"in\"")
            self.in_op()
        elif self.id_ == 34:
            if self.id_ == 34:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"inc\"")
            self.incdec(INC())
        elif self.id_ == 35:
            if self.id_ == 35:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ind\"")
            self.instructions.append(Instruction(0, IND, AddrMode.SIMPLE)) 
        elif self.id_ == 36:
            if self.id_ == 36:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"indr\"")
            self.instructions.append(Instruction(0, INDR, AddrMode.SIMPLE)) 
        elif self.id_ == 37:
            if self.id_ == 37:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ini\"")
            self.instructions.append(Instruction(0, INI, AddrMode.SIMPLE)) 
        elif self.id_ == 38:
            if self.id_ == 38:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"inir\"")
            self.instructions.append(Instruction(0, INIR, AddrMode.SIMPLE)) 
        elif self.id_ == 39:
            if self.id_ == 39:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"jp\"")
            self.jp_op()
        elif self.id_ == 40:
            if self.id_ == 40:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"jr\"")
            self.jr_op()
        elif self.id_ == 41:
            if self.id_ == 41:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ld\"")
            self.ld_op()
        elif self.id_ == 42:
            if self.id_ == 42:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldd\"")
            self.instructions.append(Instruction(0, LDD, AddrMode.SIMPLE)) 
        elif self.id_ == 43:
            if self.id_ == 43:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"lddr\"")
            self.instructions.append(Instruction(0, LDDR, AddrMode.SIMPLE)) 
        elif self.id_ == 44:
            if self.id_ == 44:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldi\"")
            self.instructions.append(Instruction(0, LDI, AddrMode.SIMPLE)) 
        elif self.id_ == 45:
            if self.id_ == 45:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldir\"")
            self.instructions.append(Instruction(0, LDIR, AddrMode.SIMPLE)) 
        elif self.id_ == 46:
            if self.id_ == 46:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"neg\"")
            self.instructions.append(Instruction(0, NEG, AddrMode.SIMPLE)) 
        elif self.id_ == 47:
            if self.id_ == 47:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nop\"")
            self.instructions.append(Instruction(0, NOP, AddrMode.SIMPLE)) 
        elif self.id_ == 48:
            if self.id_ == 48:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"or\"")
            self.s_op(OR())
        elif self.id_ == 49:
            if self.id_ == 49:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"otdr\"")
            self.instructions.append(Instruction(0, OTDR, AddrMode.SIMPLE)) 
        elif self.id_ == 50:
            if self.id_ == 50:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"otir\"")
            self.instructions.append(Instruction(0, OTIR, AddrMode.SIMPLE)) 
        elif self.id_ == 51:
            if self.id_ == 51:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"out\"")
            self.out_op()
        elif self.id_ == 52:
            if self.id_ == 52:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"outd\"")
            self.instructions.append(Instruction(0, OUTD, AddrMode.SIMPLE)) 
        elif self.id_ == 53:
            if self.id_ == 53:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"outi\"")
            self.instructions.append(Instruction(0, OUTI, AddrMode.SIMPLE)) 
        elif self.id_ == 54:
            if self.id_ == 54:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"pop\"")
            self.pop_op(POP())
        elif self.id_ == 55:
            if self.id_ == 55:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"push\"")
            self.pop_op(PUSH())
        elif self.id_ == 56:
            if self.id_ == 56:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"res\"")
            self.bit_op(RES())
        elif self.id_ == 57:
            if self.id_ == 57:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ret\"")
            self.ret_op()
        elif self.id_ == 58:
            if self.id_ == 58:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"reti\"")
            self.instructions.append(Instruction(0, RETI, AddrMode.SIMPLE)) 
        elif self.id_ == 59:
            if self.id_ == 59:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"retn\"")
            self.instructions.append(Instruction(0, RETN, AddrMode.SIMPLE)) 
        elif self.id_ == 60:
            if self.id_ == 60:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rl\"")
            self.m_op(RL())
        elif self.id_ == 61:
            if self.id_ == 61:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rla\"")
            self.instructions.append(Instruction(0, RLA, AddrMode.SIMPLE)) 
        elif self.id_ == 62:
            if self.id_ == 62:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rlc\"")
            self.m_op(RLC())
        elif self.id_ == 63:
            if self.id_ == 63:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rlca\"")
            self.instructions.append(Instruction(0, RLCA, AddrMode.SIMPLE)) 
        elif self.id_ == 64:
            if self.id_ == 64:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rld\"")
            self.instructions.append(Instruction(0, RLD, AddrMode.SIMPLE)) 
        elif self.id_ == 65:
            if self.id_ == 65:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rr\"")
            self.m_op(RR())
        elif self.id_ == 66:
            if self.id_ == 66:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rra\"")
            self.instructions.append(Instruction(0, RRA, AddrMode.SIMPLE)) 
        elif self.id_ == 67:
            if self.id_ == 67:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrc\"")
            self.m_op(RRC())
        elif self.id_ == 68:
            if self.id_ == 68:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrca\"")
            self.instructions.append(Instruction(0, RRCA, AddrMode.SIMPLE)) 
        elif self.id_ == 69:
            if self.id_ == 69:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrd\"")
            self.instructions.append(Instruction(0, RRD, AddrMode.SIMPLE)) 
        elif self.id_ == 70:
            if self.id_ == 70:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rst\"")
            self.immediate()
            if self.value in [0x00, 0x08, 0x10, 0x18, 0x20, 0x28, 0x30, 0x38]:
                self.instructions.append(Instruction(0, RST(), AddrMode.RST, t=self.value // 8))
            else:
                ParserError(t=self.t, nt=self.nt, expected="\"00h\", \"08h\", \"10h\", \"18h\", \"20h\", \"28h\", \"30h\", \"38h\"")
        elif self.id_ == 71:
            if self.id_ == 71:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sbc\"")
            self.sbc_op()
        elif self.id_ == 72:
            if self.id_ == 72:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"scf\"")
            self.instructions.append(Instruction(0, SCF, AddrMode.SIMPLE)) 
        elif self.id_ == 73:
            if self.id_ == 73:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"set\"")
            self.bit_op(SET())
        elif self.id_ == 74:
            if self.id_ == 74:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sla\"")
            self.m_op(SLA())
        elif self.id_ == 75:
            if self.id_ == 75:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sra\"")
            self.m_op(SRA())
        elif self.id_ == 76:
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"srl\"")
            self.m_op(SRL())
        elif self.id_ == 77:
            if self.id_ == 77:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sub\"")
            self.s_op(SUB())
        elif self.id_ == 78:
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"xor\"")
            self.s_op(XOR())
        else:
            raise ParserError(t=self.t, expected="'-','adc','add','and','bit','call','ccf','cp','cpd','cpdr','cpi','cpir','cpl','daa','dec','di','djnz','ei','ex','exx','halt','im','in','inc','ind','indr','ini','inir','jp','jr','ld','ldd','lddr','ldi','ldir','neg','nop','or','otdr','otir','out','outd','outi','pop','push','res','ret','reti','retn','rl','rla','rlc','rlca','rld','rr','rra','rrc','rrca','rrd','rst','sbc','scf','set','sla','sra','srl','sub'")

    # directive<> = (.k=1.) org unsigned_number CODE|end
    def directive(self):
        if self.id_ == 135:
            if self.id_ == 135:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"org\"")
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            self.instructions.append(Org(to_int(self.t.s))) 
        elif self.id_ == 136:
            if self.id_ == 136:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"end\"")
        else:
            raise ParserError(t=self.t, expected="'^','org'")

    # macro_invocation<> = ident CODE
    def macro_invocation(self):
        if self.id_ == Z80AssemblerScanner.TOKEN_ident:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="ident")
        self.instructions.append(MacroInvocation(self.t.s)) 

    # ld_op<> = (.k=1.) ( (.k=1.) hl ) , (.k=1.) register CODE|immediate CODE|ix number_with_sign ) , CODE (.k=1.) regis
    #    ter CODE|immediate CODE|iy number_with_sign ) , CODE (.k=1.) register CODE|immediate CODE|bc ) , a CODE|de ) , 
    #    a CODE|addr16 ) , (.k=1.) a CODE|hl CODE|ix CODE|iy CODE|dd CODE|sp , (.k=1.) hl CODE|ix CODE|iy CODE|( addr16 
    #    ) CODE|immediate CODE|dd , (.k=1.) ( addr16 ) CODE|immediate CODE|ix , (.k=1.) ( addr16 ) CODE|immediate CODE|i
    #    y , (.k=1.) ( addr16 ) CODE|immediate CODE|i , a CODE|r , a CODE|a , (.k=1.) i CODE|r CODE|( (.k=1.) bc CODE|de
    #     CODE|hl CODE|ix number_with_sign CODE|iy number_with_sign CODE|addr16 CODE )|register CODE|immediate CODE|regi
    #    ster , CODE (.k=1.) register CODE|immediate CODE|( (.k=1.) hl CODE|ix number_with_sign CODE|iy number_with_sign
    #     CODE )
    def ld_op(self):
        if self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if 79 <= self.id_ <= 85:
                    self.register()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PHLPR, r1=self.reg)) 
                elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.immediate()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PHLPN, n=self.value)) 
                else:
                    raise ParserError(t=self.t, expected="')','+','xor','a','b','c','d','e','h',string,label")
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.number_with_sign()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                d = self.value 
                if 79 <= self.id_ <= 85:
                    self.register()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PIXDPR, r1=self.reg, d=d)) 
                elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.immediate()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PIXDPN, n=self.value, d=d)) 
                else:
                    raise ParserError(t=self.t, expected="')','+','xor','a','b','c','d','e','h',string,label")
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.number_with_sign()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                d = self.value 
                if 79 <= self.id_ <= 85:
                    self.register()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PIYDPR, r1=self.reg, d=d)) 
                elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.immediate()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PIYDPN, n=self.value, d=d)) 
                else:
                    raise ParserError(t=self.t, expected="')','+','xor','a','b','c','d','e','h',string,label")
            elif self.id_ == 88:
                if self.id_ == 88:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 79:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.PBCPA)) 
            elif self.id_ == 89:
                if self.id_ == 89:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 79:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.PDEPA)) 
            elif (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.addr16()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 79:
                    if self.id_ == 79:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.PNNPA, nn=self.value)) 
                elif self.id_ == 90:
                    if self.id_ == 90:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.PNNPHL, nn=self.value)) 
                elif self.id_ == 91:
                    if self.id_ == 91:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.PNNPIX, nn=self.value)) 
                elif self.id_ == 92:
                    if self.id_ == 92:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.PNNPIY, nn=self.value)) 
                elif (88 <= self.id_ <= 90) or (self.id_ == 95):
                    self.dd()
                    self.instructions.append(Instruction(0, LD(), AddrMode.PNNPDD, dd=self.reg, nn=self.value)) 
                else:
                    raise ParserError(t=self.t, expected="'xor','r','bc','de','hl','ix','af''")
            else:
                raise ParserError(t=self.t, expected="'r','bc','de','hl','ix',string,label")
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.SPHL)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.SPIX)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.SPIY)) 
            elif self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.DDPNNP, dd=3, nn=self.value))  # sp=3 
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.DDNN, dd=3, nn=self.value))  # sp=3 
            else:
                raise ParserError(t=self.t, expected="'.',')','+','de','hl','ix',string,label")
        elif (88 <= self.id_ <= 90) or (self.id_ == 95):
            self.dd()
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.reg == 2:
                    self.instructions.append(Instruction(0, LD(), AddrMode.HLPNNP, nn=self.value))
                else:
                    self.instructions.append(Instruction(0, LD(), AddrMode.DDPNNP, dd=self.reg, nn=self.value))
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.DDNN, dd=self.reg, nn=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'.',')','+',string,label")
        elif self.id_ == 91:
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.IXPNNP, nn=self.value)) 
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.IXNN, nn=self.value))  # sp=3 
            else:
                raise ParserError(t=self.t, expected="'.',')','+',string,label")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.IYPNNP, nn=self.value)) 
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.IYNN, nn=self.value))  # sp=3 
            else:
                raise ParserError(t=self.t, expected="'.',')','+',string,label")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"i\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            self.instructions.append(Instruction(0, LD(), AddrMode.IA)) 
        elif self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"r\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            self.instructions.append(Instruction(0, LD(), AddrMode.RA)) 
        elif self.id_ == 79:
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 86:
                if self.id_ == 86:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"i\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.AI)) 
            elif self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"r\"")
                self.instructions.append(Instruction(0, LD(), AddrMode.AR)) 
            elif self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.APBCP)) 
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.APDEP)) 
                elif self.id_ == 90:
                    if self.id_ == 90:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPHLP, r2=7))  # a=7 
                elif self.id_ == 91:
                    if self.id_ == 91:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    self.number_with_sign()
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPIXDP, r2=7, d=self.value))  # a=7 
                elif self.id_ == 92:
                    if self.id_ == 92:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    self.number_with_sign()
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPIYDP, r2=7, d=self.value))  # a=7 
                elif (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.addr16()
                    self.instructions.append(Instruction(0, LD(), AddrMode.APNNP, nn=self.value)) 
                else:
                    raise ParserError(t=self.t, expected="'r','bc','de','hl','ix',string,label")
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            elif 79 <= self.id_ <= 85:
                self.register()
                self.instructions.append(Instruction(0, LD(), AddrMode.RR, r1=self.reg, r2=7))   # a = 7
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.RN, n=self.value, r2=7))   # a = 7
            else:
                raise ParserError(t=self.t, expected="'.',')','+','xor','a','b','c','d','e','h','l','i',string,label")
        elif 79 <= self.id_ <= 85:
            self.register()
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            reg = self.reg 
            if 79 <= self.id_ <= 85:
                self.register()
                self.instructions.append(Instruction(0, LD(), AddrMode.RR, r1=self.reg, r2=reg)) 
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, LD(), AddrMode.RN, n=self.value, r2=reg)) 
            elif self.id_ == 8:
                if self.id_ == 8:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                if self.id_ == 90:
                    if self.id_ == 90:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPHLP, r2=reg)) 
                elif self.id_ == 91:
                    if self.id_ == 91:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    self.number_with_sign()
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPIXDP, r2=reg, d=self.value)) 
                elif self.id_ == 92:
                    if self.id_ == 92:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    self.number_with_sign()
                    self.instructions.append(Instruction(0, LD(), AddrMode.RPIYDP, r2=reg, d=self.value)) 
                else:
                    raise ParserError(t=self.t, expected="'de','hl','ix'")
                if self.id_ == 9:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            else:
                raise ParserError(t=self.t, expected="'.',')','+','xor','a','b','c','d','e','h',string,label")
        else:
            raise ParserError(t=self.t, expected="'.','xor','a','b','c','d','e','h','l','i','r','bc','de','hl','ix','af''")

    # add_op<> = (.k=1.) hl , ss CODE|ix , pp CODE|iy , rr CODE|a_op
    def add_op(self):
        if self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
            self.instructions.append(Instruction(0, ADD(), AddrMode.ED_HLSS, dd=self.reg)) 
        elif self.id_ == 91:
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.pp()
            self.instructions.append(Instruction(0, ADD(), AddrMode.IXPP, pp=self.reg)) 
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.rr()
            self.instructions.append(Instruction(0, ADD(), AddrMode.IYRR, rr=self.reg)) 
        elif self.id_ == 79:
            self.a_op(ADD())
        else:
            raise ParserError(t=self.t, expected="'xor','de','hl','ix'")

    # adc_op<> = (.k=1.) hl , ss CODE|a_op
    def adc_op(self):
        if self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
            self.instructions.append(Instruction(0, ADC(), AddrMode.ED_HLSS, dd=self.reg)) 
        elif self.id_ == 79:
            self.a_op(ADC())
        else:
            raise ParserError(t=self.t, expected="'xor','de'")

    # sbc_op<> = (.k=1.) hl , ss CODE|a_op
    def sbc_op(self):
        if self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
            self.instructions.append(Instruction(0, SBC(), AddrMode.ED_HLSS, dd=self.reg)) 
        elif self.id_ == 79:
            self.a_op(SBC())
        else:
            raise ParserError(t=self.t, expected="'xor','de'")

    # call_op<> = (.k=1.) cc , addr16 CODE|addr16 CODE
    def call_op(self):
        if (self.id_ == 81) or (96 <= self.id_ <= 102):
            self.cc()
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.addr16()
            self.instructions.append(Instruction(0, CALL(), AddrMode.CCNN, cc=self._cc, nn=self.value)) 
        elif (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.addr16()
            self.instructions.append(Instruction(0, CALL(), AddrMode.NN, nn=self.value)) 
        else:
            raise ParserError(t=self.t, expected="'b','sp','nz','z','nc','po','pe','p',string,label")

    # jp_op<> = (.k=1.) ( (.k=1.) hl CODE|ix CODE|iy CODE )|cc , addr16 CODE|addr16 CODE
    def jp_op(self):
        if self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, JP(), AddrMode.PHLP)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.instructions.append(Instruction(0, JP(), AddrMode.PIXP)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.instructions.append(Instruction(0, JP(), AddrMode.PIYP)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif (self.id_ == 81) or (96 <= self.id_ <= 102):
            self.cc()
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.addr16()
            self.instructions.append(Instruction(0, JP(), AddrMode.CCNN, cc=self._cc, nn=self.value)) 
        elif (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.addr16()
            self.instructions.append(Instruction(0, JP(), AddrMode.NN, nn=self.value)) 
        else:
            raise ParserError(t=self.t, expected="'.','b','sp','nz','z','nc','po','pe','p',string,label")

    # jr_op<> = (.k=1.) nz , relative CODE|z , relative CODE|nc , relative CODE|c , relative CODE|relative CODE
    def jr_op(self):
        if self.id_ == 96:
            if self.id_ == 96:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nz\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
            self.instructions.append(Instruction(0, JR(), AddrMode.NZE, e=self.value)) 
        elif self.id_ == 97:
            if self.id_ == 97:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"z\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
            self.instructions.append(Instruction(0, JR(), AddrMode.ZE, e=self.value)) 
        elif self.id_ == 98:
            if self.id_ == 98:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nc\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
            self.instructions.append(Instruction(0, JR(), AddrMode.NCE, e=self.value)) 
        elif self.id_ == 81:
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
            self.instructions.append(Instruction(0, JR(), AddrMode.CE, e=self.value)) 
        elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.relative()
            self.instructions.append(Instruction(0, JR(), AddrMode.E, e=self.value)) 
        else:
            raise ParserError(t=self.t, expected="')','+','b','sp','nz','z',string,label")

    # out_op<> = ( (.k=1.) c ) , register CODE|immediate ) , a CODE
    def out_op(self):
        if self.id_ == 8:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
        if self.id_ == 81:
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.register()
            self.instructions.append(Instruction(0, OUT(), AddrMode.PCPR, n=self.value, r2=self.reg)) 
        elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            self.instructions.append(Instruction(0, OUT(), AddrMode.PNPA, n=self.value)) 
        else:
            raise ParserError(t=self.t, expected="')','+','b',string,label")

    # in_op<> = (.k=1.) a , ( (.k=1.) c CODE|immediate CODE )|register , ( c ) CODE
    def in_op(self):
        if self.id_ == 79:
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 81:
                if self.id_ == 81:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
                self.instructions.append(Instruction(0, IN(), AddrMode.RPCP, r2=7))  # a = 7 
            elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
                self.instructions.append(Instruction(0, IN(), AddrMode.APNP, n=self.value)) 
            else:
                raise ParserError(t=self.t, expected="')','+','b',string,label")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif 79 <= self.id_ <= 85:
            self.register()
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            self.instructions.append(Instruction(0, IN(), AddrMode.RPCP, r2=self.reg)) 
        else:
            raise ParserError(t=self.t, expected="'xor','a','b','c','d','e','h'")

    # ex_op<> = (.k=1.) de , hl CODE|af , af' CODE|( sp ) , (.k=1.) hl CODE|ix CODE|iy CODE
    def ex_op(self):
        if self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            self.instructions.append(Instruction(0, EX(), AddrMode.DEHL)) 
        elif self.id_ == 93:
            if self.id_ == 93:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 94:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af'\"")
            self.instructions.append(Instruction(0, EX(), AddrMode.AFAFp)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, EX(), AddrMode.PSPPHL)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.instructions.append(Instruction(0, EX(), AddrMode.PSPPIX)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.instructions.append(Instruction(0, EX(), AddrMode.PSPPIY)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
        else:
            raise ParserError(t=self.t, expected="'.','bc','iy'")

    # pop_op<op: InstructionDef> = (.k=1.) qq CODE|ix CODE|iy CODE
    def pop_op(self, op: InstructionDef):
        if (88 <= self.id_ <= 90) or (self.id_ == 93):
            self.qq()
            self.instructions.append(Instruction(0, op, AddrMode.QQ, qq=self.reg)) 
        elif self.id_ == 91:
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            self.instructions.append(Instruction(0, op, AddrMode.IX)) 
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            self.instructions.append(Instruction(0, op, AddrMode.IY)) 
        else:
            raise ParserError(t=self.t, expected="'r','bc','de','hl','ix','iy'")

    # ret_op<> = [cc CODE] CODE
    def ret_op(self):
        has_cc = False 
        if (self.id_ == 81) or (96 <= self.id_ <= 102):
            self.cc()
            has_cc = True 
        if has_cc:
            self.instructions.append(Instruction(0, RET(), AddrMode.CC, cc=self._cc))
        else:
            self.instructions.append(Instruction(0, RET(), AddrMode.SIMPLE))

    # im_op<> = unsigned_number CODE
    def im_op(self):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        if self.t.s == "0":
            self.instructions.append(Instruction(0, IM(), AddrMode.IM0))
        elif self.t.s == "1":
            self.instructions.append(Instruction(0, IM(), AddrMode.IM1))
        elif self.t.s == "2":
            self.instructions.append(Instruction(0, IM(), AddrMode.IM2))
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="0, 1 or 2")

    # a_op<op: InstructionDef> = a , (.k=1.) register CODE|immediate CODE|( (.k=1.) hl CODE|(.k=1.) ix CODE|iy CODE numb
    #    er_with_sign CODE )
    def a_op(self, op: InstructionDef):
        if self.id_ == 79:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        if self.id_ == 6:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
        if 79 <= self.id_ <= 85:
            self.register()
            self.instructions.append(Instruction(0, op, AddrMode.AR1, r1=self.reg)) 
        elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
            self.instructions.append(Instruction(0, op, AddrMode.AN, n=self.value)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, op, AddrMode.APHLP)) 
            elif 91 <= self.id_ <= 92:
                if self.id_ == 91:
                    if self.id_ == 91:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    addr_mode = AddrMode.APIXDP 
                elif self.id_ == 92:
                    if self.id_ == 92:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    addr_mode = AddrMode.APIYDP 
                else:
                    raise ParserError(t=self.t, expected="'hl','ix'")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, addr_mode, d=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'.',')','+','xor','a','b','c','d','e','h',string,label")

    # s_op<op: InstructionDef> = (.k=1.) register CODE|immediate CODE|( (.k=1.) hl CODE|ix number_with_sign CODE|iy numb
    #    er_with_sign CODE )
    def s_op(self, op: InstructionDef):
        if 79 <= self.id_ <= 85:
            self.register()
            self.instructions.append(Instruction(0, op, AddrMode.R1, r1=self.reg)) 
        elif (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
            self.instructions.append(Instruction(0, op, AddrMode.N, n=self.value)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, op, AddrMode.PHLP)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIXDP, d=self.value)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIYDP, d=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'.',')','+','xor','a','b','c','d','e','h',string,label")

    # m_op<op: InstructionDef> = (.k=1.) register CODE|( (.k=1.) hl CODE|ix number_with_sign CODE|iy number_with_sign CO
    #    DE )
    def m_op(self, op: InstructionDef):
        if 79 <= self.id_ <= 85:
            self.register()
            self.instructions.append(Instruction(0, op, AddrMode.R1, r1=self.reg)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, op, AddrMode.PHLP)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIXDP, d=self.value)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIYDP, d=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'.','xor','a','b','c','d','e','h'")

    # incdec<op: InstructionDef> = (.k=1.) register CODE|( (.k=1.) hl CODE|ix number_with_sign CODE|iy number_with_sign 
    #    CODE )|ss CODE|ix CODE|iy CODE
    def incdec(self, op: InstructionDef):
        if 79 <= self.id_ <= 85:
            self.register()
            self.instructions.append(Instruction(0, op, AddrMode.R1, r1=self.reg)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, op, AddrMode.PHLP)) 
            elif self.id_ == 91:
                if self.id_ == 91:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIXDP, d=self.value)) 
            elif self.id_ == 92:
                if self.id_ == 92:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, AddrMode.PIYDP, d=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif (88 <= self.id_ <= 90) or (self.id_ == 95):
            self.ss()
            self.instructions.append(Instruction(0, op, AddrMode.SS, dd=self.reg)) 
        elif self.id_ == 91:
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            self.instructions.append(Instruction(0, op, AddrMode.IX)) 
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            self.instructions.append(Instruction(0, op, AddrMode.IY)) 
        else:
            raise ParserError(t=self.t, expected="'.','xor','a','b','c','d','e','h','r','bc','de','hl','ix','af''")

    # bit_op<op: InstructionDef> = unsigned_number CODE , (.k=1.) register CODE|( (.k=1.) hl CODE|(.k=1.) ix CODE|iy COD
    #    E number_with_sign CODE )
    def bit_op(self, op: InstructionDef):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        bit = int(self.t.s) 
        if self.id_ == 6:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
        if 79 <= self.id_ <= 85:
            self.register()
            self.instructions.append(Instruction(0, op, AddrMode.BR, b=bit, r1=self.reg)) 
        elif self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 90:
                if self.id_ == 90:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                self.instructions.append(Instruction(0, op, AddrMode.BPHLP, b=bit, r1=self.reg)) 
            elif 91 <= self.id_ <= 92:
                if self.id_ == 91:
                    if self.id_ == 91:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    addr_mode = AddrMode.BPIXDP 
                elif self.id_ == 92:
                    if self.id_ == 92:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    addr_mode = AddrMode.BPIYDP 
                else:
                    raise ParserError(t=self.t, expected="'hl','ix'")
                self.number_with_sign()
                self.instructions.append(Instruction(0, op, addr_mode, b=bit, d=self.value)) 
            else:
                raise ParserError(t=self.t, expected="'de','hl','ix'")
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'.','xor','a','b','c','d','e','h'")

    # addr16<> = (.k=1.) unsigned_number CODE|ident CODE
    def addr16(self):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            self.value = to_int(self.t.s, False) 
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
            self.value = self.t.s 
        else:
            raise ParserError(t=self.t, expected="string,label")

    # relative<> = (.k=1.) signed_number|ident CODE
    def relative(self):
        if (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.signed_number()
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
            self.value = self.t.s 
        else:
            raise ParserError(t=self.t, expected="')','+',string,label")

    # immediate<> = (.k=1.) signed_number|ident CODE
    def immediate(self):
        if (10 <= self.id_ <= 11) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.signed_number()
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
            self.value = self.t.s 
        else:
            raise ParserError(t=self.t, expected="')','+',string,label")

    # register<> = (.k=1.) a CODE|b CODE|c CODE|d CODE|e CODE|h CODE|l CODE
    def register(self):
        if self.id_ == 79:
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            self.reg = 7 
        elif self.id_ == 80:
            if self.id_ == 80:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"b\"")
            self.reg = 0 
        elif self.id_ == 81:
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            self.reg = 1 
        elif self.id_ == 82:
            if self.id_ == 82:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"d\"")
            self.reg = 2 
        elif self.id_ == 83:
            if self.id_ == 83:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"e\"")
            self.reg = 3 
        elif self.id_ == 84:
            if self.id_ == 84:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"h\"")
            self.reg = 4 
        elif self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"l\"")
            self.reg = 5 
        else:
            raise ParserError(t=self.t, expected="'xor','a','b','c','d','e','h'")

    # cc<> = (.k=1.) nz CODE|z CODE|nc CODE|c CODE|po CODE|pe CODE|p CODE|m CODE
    def cc(self):
        if self.id_ == 96:
            if self.id_ == 96:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nz\"")
            self._cc = 0 
        elif self.id_ == 97:
            if self.id_ == 97:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"z\"")
            self._cc = 1 
        elif self.id_ == 98:
            if self.id_ == 98:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nc\"")
            self._cc = 2 
        elif self.id_ == 81:
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            self._cc = 3 
        elif self.id_ == 99:
            if self.id_ == 99:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"po\"")
            self._cc = 4 
        elif self.id_ == 100:
            if self.id_ == 100:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"pe\"")
            self._cc = 5 
        elif self.id_ == 101:
            if self.id_ == 101:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"p\"")
            self._cc = 6 
        elif self.id_ == 102:
            if self.id_ == 102:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"m\"")
            self._cc = 7 
        else:
            raise ParserError(t=self.t, expected="'b','sp','nz','z','nc','po','pe','p'")

    # qq<> = (.k=1.) bc CODE|de CODE|hl CODE|af CODE
    def qq(self):
        if self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
            self.reg = 0 
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            self.reg = 1 
        elif self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            self.reg = 2 
        elif self.id_ == 93:
            if self.id_ == 93:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af\"")
            self.reg = 3 
        else:
            raise ParserError(t=self.t, expected="'r','bc','de','iy'")

    # ss<> = (.k=1.) bc CODE|de CODE|hl CODE|sp CODE
    def ss(self):
        if self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
            self.reg = 0 
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            self.reg = 1 
        elif self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            self.reg = 2 
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            self.reg = 3 
        else:
            raise ParserError(t=self.t, expected="'r','bc','de','af''")

    # pp<> = (.k=1.) bc CODE|de CODE|ix CODE|sp CODE
    def pp(self):
        if self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
            self.reg = 0 
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            self.reg = 1 
        elif self.id_ == 91:
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            self.reg = 2 
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            self.reg = 3 
        else:
            raise ParserError(t=self.t, expected="'r','bc','hl','af''")

    # rr<> = (.k=1.) bc CODE|de CODE|iy CODE|sp CODE
    def rr(self):
        if self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
            self.reg = 0 
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            self.reg = 1 
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            self.reg = 2 
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            self.reg = 3 
        else:
            raise ParserError(t=self.t, expected="'r','bc','ix','af''")

    # dd<> = (.k=1.) bc CODE|de CODE|hl CODE|sp CODE
    def dd(self):
        if self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
            self.reg = 0 
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            self.reg = 1 
        elif self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            self.reg = 2 
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            self.reg = 3 
        else:
            raise ParserError(t=self.t, expected="'r','bc','de','af''")

    # number_with_sign<> = (.k=1.) + CODE|- CODE unsigned_number CODE
    def number_with_sign(self):
        if self.id_ == 10:
            if self.id_ == 10:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
            negative = False 
        elif self.id_ == 11:
            if self.id_ == 11:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
            negative = True 
        else:
            raise ParserError(t=self.t, expected="')','+'")
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        self.value = to_int(self.t.s, negative) 

    # signed_number<> = [(.k=1.) +|- CODE] unsigned_number CODE
    def signed_number(self):
        negative = False 
        if 10 <= self.id_ <= 11:
            if self.id_ == 10:
                if self.id_ == 10:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
            elif self.id_ == 11:
                if self.id_ == 11:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                negative = True 
            else:
                raise ParserError(t=self.t, expected="')','+'")
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        self.value = to_int(self.t.s, negative) 

    # expr<> = and_test {|| and_test}
    def expr(self):
        self.and_test()
        while self.id_ == 114:
            if self.id_ == 114:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"||\"")
            self.and_test()

    # and_test<> = not_test {&& not_test}
    def and_test(self):
        self.not_test()
        while self.id_ == 113:
            if self.id_ == 113:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"&&\"")
            self.not_test()

    # not_test<> = (.k=1.) ! not_test|comparison
    def not_test(self):
        if self.id_ == 110:
            if self.id_ == 110:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"!\"")
            self.not_test()
        elif (self.id_ == 8) or (10 <= self.id_ <= 11) or (self.id_ == 109) or (self.id_ == Z80AssemblerScanner.TOKEN_ident) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            self.comparison()
        else:
            raise ParserError(t=self.t, expected="'.',')','+','>>','~',string,label")

    # comparison<> = or_expr {comp_op or_expr}
    def comparison(self):
        self.or_expr()
        while (self.id_ == 4) or (117 <= self.id_ <= 121) or (126 <= self.id_ <= 131):
            self.comp_op()
            self.or_expr()

    # comp_op<> = (.k=1.) (.k=1.) lt|<|(.k=1.) gt|>|(.k=1.) eq|=|(.k=1.) ge|>=|(.k=1.) le|<=|(.k=1.) ne|!=
    def comp_op(self):
        if (self.id_ == 119) or (self.id_ == 128):
            if self.id_ == 128:
                if self.id_ == 128:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"lt\"")
            elif self.id_ == 119:
                if self.id_ == 119:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"<\"")
            else:
                raise ParserError(t=self.t, expected="'>','ne'")
        elif (self.id_ == 118) or (self.id_ == 130):
            if self.id_ == 130:
                if self.id_ == 130:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"gt\"")
            elif self.id_ == 118:
                if self.id_ == 118:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\">\"")
            else:
                raise ParserError(t=self.t, expected="'!=','le'")
        elif (self.id_ == 4) or (self.id_ == 126):
            if self.id_ == 126:
                if self.id_ == 126:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"eq\"")
            elif self.id_ == 4:
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"=\"")
            else:
                raise ParserError(t=self.t, expected="EOL,'shr'")
        elif (self.id_ == 121) or (self.id_ == 131):
            if self.id_ == 131:
                if self.id_ == 131:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ge\"")
            elif self.id_ == 121:
                if self.id_ == 121:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\">=\"")
            else:
                raise ParserError(t=self.t, expected="'<=','gt'")
        elif (self.id_ == 120) or (self.id_ == 129):
            if self.id_ == 129:
                if self.id_ == 129:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"le\"")
            elif self.id_ == 120:
                if self.id_ == 120:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"<=\"")
            else:
                raise ParserError(t=self.t, expected="'<','lt'")
        elif (self.id_ == 117) or (self.id_ == 127):
            if self.id_ == 127:
                if self.id_ == 127:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ne\"")
            elif self.id_ == 117:
                if self.id_ == 117:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"!=\"")
            else:
                raise ParserError(t=self.t, expected="'=','eq'")
        else:
            raise ParserError(t=self.t, expected="EOL,'=','!=','>','<','<=','shr','eq','ne','lt','le','gt'")

    # or_expr<> = xor_expr {(.k=1.) or|| xor_expr}
    def or_expr(self):
        self.xor_expr()
        while (self.id_ == 48) or (self.id_ == 112):
            if self.id_ == 48:
                if self.id_ == 48:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"or\"")
            elif self.id_ == 112:
                if self.id_ == 112:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"|\"")
            else:
                raise ParserError(t=self.t, expected="'nop','&'")
            self.xor_expr()

    # xor_expr<> = and_expr {^ and_expr}
    def xor_expr(self):
        self.and_expr()
        while self.id_ == 134:
            if self.id_ == 134:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"^\"")
            self.and_expr()

    # and_expr<> = shift_expr {(.k=1.) and|& shift_expr}
    def and_expr(self):
        self.shift_expr()
        while (self.id_ == 14) or (self.id_ == 111):
            if self.id_ == 14:
                if self.id_ == 14:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"and\"")
            elif self.id_ == 111:
                if self.id_ == 111:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"&\"")
            else:
                raise ParserError(t=self.t, expected="'add','!'")
            self.shift_expr()

    # shift_expr<> = arith_expr {(.k=1.) <<|>> arith_expr}
    def shift_expr(self):
        self.arith_expr()
        while 107 <= self.id_ <= 108:
            if self.id_ == 107:
                if self.id_ == 107:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"<<\"")
            elif self.id_ == 108:
                if self.id_ == 108:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\">>\"")
            else:
                raise ParserError(t=self.t, expected="'/','<<'")
            self.arith_expr()

    # arith_expr<> = term {(.k=1.) +|- term}
    def arith_expr(self):
        self.term()
        while 10 <= self.id_ <= 11:
            if self.id_ == 10:
                if self.id_ == 10:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
            elif self.id_ == 11:
                if self.id_ == 11:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
            else:
                raise ParserError(t=self.t, expected="')','+'")
            self.term()

    # term<> = factor {(.k=1.) *|/ factor}
    def term(self):
        self.factor()
        while 105 <= self.id_ <= 106:
            if self.id_ == 105:
                if self.id_ == 105:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"*\"")
            elif self.id_ == 106:
                if self.id_ == 106:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"/\"")
            else:
                raise ParserError(t=self.t, expected="'-','*'")
            self.factor()

    # factor<> = {(.k=1.) +|-|~ factor} atom
    def factor(self):
        while (10 <= self.id_ <= 11) or (self.id_ == 109):
            if self.id_ == 10:
                if self.id_ == 10:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
            elif self.id_ == 11:
                if self.id_ == 11:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
            elif self.id_ == 109:
                if self.id_ == 109:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"~\"")
            else:
                raise ParserError(t=self.t, expected="')','+','>>'")
            self.factor()
        self.atom()

    # atom<> = (.k=1.) ( expr )|ident|unsigned_number
    def atom(self):
        if self.id_ == 8:
            if self.id_ == 8:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            self.expr()
            if self.id_ == 9:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
        elif self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        else:
            raise ParserError(t=self.t, expected="'.',string,label")


if __name__ == "__main__":
    import sys
    from buLL.parser.toolkit import Toolkit
    t = Toolkit.create(Z80AssemblerParser())
    t.set_args(*sys.argv[1:])
    t.process()
