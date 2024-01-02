
from typing import TextIO, Optional


from typing import Optional



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
    EOF_CHAR = -1

    TOKEN_WHITESPACE = -1
    TOKEN_BOF = -2
    TOKEN_EOF = 1
    BOF_TOKEN = Token("BOF", TOKEN_BOF, -1, -1)

    def __init__(self, reader: Optional[TextIO] = None):
        self.reader = reader
        self.state = 1
        self.id_ = 0
        self.ok = True
        self.ch = 0

        self.buffer = ""
        self.read = ""

        self.ptr = 0
        self.live = True
        self.line = 1
        self.pos = 0
        self.marked_line = 0
        self.marked_pos = 0
        self.start_line = 0
        self.start_pos = 0

    def eof_token(self) -> Token:
        return self.Token("EOF", self.TOKEN_EOF, self.line, self.pos)

    def mark(self) -> None:
        if self.live:
            if len(self.buffer) > 0:
                self.buffer = ""
        else:
            self.buffer = self.buffer[self.ptr:]

        self.ptr = 0
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
                    self.buffer += c
                    self.ptr += 1
                    c = ord(c)
                else:
                    c = self.EOF_CHAR
            except Exception:
                c = self.EOF_CHAR
        else:
            buffer_len = len(self.buffer)
            c = ord(self.buffer[self.ptr])
            self.ptr += 1
            if self.ptr == buffer_len:
                self.live = True
        if c == 10:  # '\n'
            self.pos = 0
            self.line += 1
        else:
            self.pos += 1
        if c != self.EOF_CHAR:
            self.read += chr(c)
        return c

    TOKEN_eof = 1
    TOKEN_eol = 101
    TOKEN_literal = 104
    TOKEN_string = 106
    TOKEN_ident = 107
    TOKEN_unsigned_number = 108
    TOKEN_comments = 110

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
        self.read = ""
        self.state = 1
        self.id_ = 0
        self.ok = True
        self.ch = 0
        while self.ok:
            self.ch = self.get_next_char()
            # print(f"{self.state}: {self.ch} {chr(self.ch)}
# total nodes: 152
            if self.state == 1:
                if (1 <= self.ch <= 9) or (11 <= self.ch <= 32):
                    self.start_line = self.line
                    self.start_pos = self.pos
                    self.mark()
                    self.read = ""
                    self.state = 1
                elif self.ch == 10:
                    self.id_ = self.TOKEN_eol
                    self.mark()
                    self.state = 3
                elif self.ch == 34:
                    self.state = 4
                elif self.ch == 39:
                    self.state = 8
                elif self.ch == 40:
                    self.id_ = 6
                    self.mark()
                    self.state = 12
                elif self.ch == 41:
                    self.id_ = 7
                    self.mark()
                    self.state = 13
                elif self.ch == 43:
                    self.id_ = 8
                    self.mark()
                    self.state = 14
                elif self.ch == 44:
                    self.id_ = 4
                    self.mark()
                    self.state = 15
                elif self.ch == 45:
                    self.id_ = 9
                    self.mark()
                    self.state = 16
                elif self.ch == 46:
                    self.id_ = 5
                    self.mark()
                    self.state = 17
                elif 48 <= self.ch <= 57:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 19
                elif self.ch == 59:
                    self.id_ = 3
                    self.mark()
                    self.state = 21
                elif self.ch == 61:
                    self.id_ = 2
                    self.mark()
                    self.state = 24
                elif (65 <= self.ch <= 66) or (68 <= self.ch <= 90) or (self.ch == 95) or (102 <= self.ch <= 103) or (self.ch == 107) or (self.ch == 113) or (116 <= self.ch <= 119) or (self.ch == 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 67:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 25
                elif self.ch == 97:
                    self.id_ = 76
                    self.mark()
                    self.state = 30
                elif self.ch == 98:
                    self.id_ = 77
                    self.mark()
                    self.state = 38
                elif self.ch == 99:
                    self.id_ = 78
                    self.mark()
                    self.state = 42
                elif self.ch == 100:
                    self.id_ = 79
                    self.mark()
                    self.state = 53
                elif self.ch == 101:
                    self.id_ = 80
                    self.mark()
                    self.state = 62
                elif self.ch == 104:
                    self.id_ = 81
                    self.mark()
                    self.state = 66
                elif self.ch == 105:
                    self.id_ = 83
                    self.mark()
                    self.state = 71
                elif self.ch == 106:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 81
                elif self.ch == 108:
                    self.id_ = 82
                    self.mark()
                    self.state = 84
                elif self.ch == 109:
                    self.id_ = 100
                    self.mark()
                    self.state = 90
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 91
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 98
                elif self.ch == 112:
                    self.id_ = 99
                    self.mark()
                    self.state = 109
                elif self.ch == 114:
                    self.id_ = 84
                    self.mark()
                    self.state = 116
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 134
                elif self.ch == 120:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 149
                elif self.ch == 122:
                    self.id_ = 94
                    self.mark()
                    self.state = 152
                elif self.ch == self.EOF_CHAR:
                    return self.Token("<eof>", self.TOKEN_EOF, self.start_line, self.start_pos)
                else:
                    self.ok = False
                
            elif self.state == 2:
                self.ok = False
            elif self.state == 3:
                self.ok = False
            elif self.state == 4:
                if (32 <= self.ch <= 33) or (35 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 5
                elif self.ch == 34:
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 6
                elif self.ch == 92:
                    self.state = 7
                else:
                    self.ok = False
                
            elif self.state == 5:
                if (32 <= self.ch <= 33) or (35 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 5
                elif self.ch == 34:
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 6
                elif self.ch == 92:
                    self.state = 7
                else:
                    self.ok = False
                
            elif self.state == 6:
                self.ok = False
            elif self.state == 7:
                if (32 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.id_ = self.TOKEN_string
                    self.mark()
                    self.state = 5
                elif self.ch == 92:
                    self.state = 7
                else:
                    self.ok = False
                
            elif self.state == 8:
                if (32 <= self.ch <= 91) or (93 <= self.ch <= 127):
                    self.state = 9
                elif self.ch == 92:
                    self.state = 11
                else:
                    self.ok = False
                
            elif self.state == 9:
                if self.ch == 39:
                    self.id_ = self.TOKEN_literal
                    self.mark()
                    self.state = 10
                else:
                    self.ok = False
                
            elif self.state == 10:
                self.ok = False
            elif self.state == 11:
                if 32 <= self.ch <= 127:
                    self.state = 9
                else:
                    self.ok = False
                
            elif self.state == 12:
                self.ok = False
            elif self.state == 13:
                self.ok = False
            elif self.state == 14:
                self.ok = False
            elif self.state == 15:
                self.ok = False
            elif self.state == 16:
                self.ok = False
            elif self.state == 17:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 18:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 19:
                if 48 <= self.ch <= 57:
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 19
                elif (self.ch == 72) or (self.ch == 104):
                    self.id_ = self.TOKEN_unsigned_number
                    self.mark()
                    self.state = 20
                else:
                    self.ok = False
                
            elif self.state == 20:
                self.ok = False
            elif self.state == 21:
                if (1 <= self.ch <= 9) or (11 <= self.ch <= 127):
                    self.state = 22
                elif self.ch == 10:
                    self.id_ = self.TOKEN_comments
                    self.mark()
                    self.state = 23
                else:
                    self.ok = False
                
            elif self.state == 22:
                if (1 <= self.ch <= 9) or (11 <= self.ch <= 127):
                    self.state = 22
                elif self.ch == 10:
                    self.id_ = self.TOKEN_comments
                    self.mark()
                    self.state = 23
                else:
                    self.ok = False
                
            elif self.state == 23:
                self.ok = False
            elif self.state == 24:
                self.ok = False
            elif self.state == 25:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 71) or (73 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 72:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 26
                else:
                    self.ok = False
                
            elif self.state == 26:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 81) or (83 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 82:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 27
                else:
                    self.ok = False
                
            elif self.state == 27:
                if self.ch == 40:
                    self.state = 28
                elif (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 28:
                if 48 <= self.ch <= 57:
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 29:
                if self.ch == 41:
                    self.id_ = self.TOKEN_literal
                    self.mark()
                    self.state = 10
                elif 48 <= self.ch <= 57:
                    self.state = 29
                else:
                    self.ok = False
                
            elif self.state == 30:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (self.ch == 101) or (103 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 31
                elif self.ch == 102:
                    self.id_ = 90
                    self.mark()
                    self.state = 34
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 36
                else:
                    self.ok = False
                
            elif self.state == 31:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 10
                    self.mark()
                    self.state = 32
                elif self.ch == 100:
                    self.id_ = 11
                    self.mark()
                    self.state = 33
                else:
                    self.ok = False
                
            elif self.state == 32:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 33:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 34:
                if self.ch == 39:
                    self.id_ = 91
                    self.mark()
                    self.state = 35
                elif (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 35:
                self.ok = False
            elif self.state == 36:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = 12
                    self.mark()
                    self.state = 37
                else:
                    self.ok = False
                
            elif self.state == 37:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 38:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 85
                    self.mark()
                    self.state = 39
                elif self.ch == 105:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 40
                else:
                    self.ok = False
                
            elif self.state == 39:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 40:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 116:
                    self.id_ = 13
                    self.mark()
                    self.state = 41
                else:
                    self.ok = False
                
            elif self.state == 41:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 42:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (100 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 43
                elif self.ch == 99:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 46
                elif self.ch == 112:
                    self.id_ = 16
                    self.mark()
                    self.state = 48
                else:
                    self.ok = False
                
            elif self.state == 43:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 44
                else:
                    self.ok = False
                
            elif self.state == 44:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 108:
                    self.id_ = 14
                    self.mark()
                    self.state = 45
                else:
                    self.ok = False
                
            elif self.state == 45:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 46:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 101) or (103 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 102:
                    self.id_ = 15
                    self.mark()
                    self.state = 47
                else:
                    self.ok = False
                
            elif self.state == 47:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 48:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = 17
                    self.mark()
                    self.state = 49
                elif self.ch == 105:
                    self.id_ = 19
                    self.mark()
                    self.state = 51
                else:
                    self.ok = False
                
            elif self.state == 49:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 18
                    self.mark()
                    self.state = 50
                else:
                    self.ok = False
                
            elif self.state == 50:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 51:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 20
                    self.mark()
                    self.state = 52
                else:
                    self.ok = False
                
            elif self.state == 52:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 53:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 100) or (102 <= self.ch <= 104) or (107 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 54
                elif self.ch == 101:
                    self.id_ = 86
                    self.mark()
                    self.state = 56
                elif self.ch == 105:
                    self.id_ = 23
                    self.mark()
                    self.state = 58
                elif self.ch == 106:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 59
                else:
                    self.ok = False
                
            elif self.state == 54:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 21
                    self.mark()
                    self.state = 55
                else:
                    self.ok = False
                
            elif self.state == 55:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 56:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 22
                    self.mark()
                    self.state = 57
                else:
                    self.ok = False
                
            elif self.state == 57:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 58:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 59:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 110:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 60
                else:
                    self.ok = False
                
            elif self.state == 60:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 122:
                    self.id_ = 24
                    self.mark()
                    self.state = 61
                else:
                    self.ok = False
                
            elif self.state == 61:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 62:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 104) or (106 <= self.ch <= 119) or (121 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 105:
                    self.id_ = 25
                    self.mark()
                    self.state = 63
                elif self.ch == 120:
                    self.id_ = 26
                    self.mark()
                    self.state = 64
                else:
                    self.ok = False
                
            elif self.state == 63:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 64:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 119) or (121 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 120:
                    self.id_ = 27
                    self.mark()
                    self.state = 65
                else:
                    self.ok = False
                
            elif self.state == 65:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 66:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 67
                elif self.ch == 108:
                    self.id_ = 87
                    self.mark()
                    self.state = 70
                else:
                    self.ok = False
                
            elif self.state == 67:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 68
                else:
                    self.ok = False
                
            elif self.state == 68:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 116:
                    self.id_ = 28
                    self.mark()
                    self.state = 69
                else:
                    self.ok = False
                
            elif self.state == 69:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 70:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 71:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 108) or (111 <= self.ch <= 119) or (self.ch == 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 109:
                    self.id_ = 29
                    self.mark()
                    self.state = 72
                elif self.ch == 110:
                    self.id_ = 30
                    self.mark()
                    self.state = 73
                elif self.ch == 120:
                    self.id_ = 88
                    self.mark()
                    self.state = 79
                elif self.ch == 121:
                    self.id_ = 89
                    self.mark()
                    self.state = 80
                else:
                    self.ok = False
                
            elif self.state == 72:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 73:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 31
                    self.mark()
                    self.state = 74
                elif self.ch == 100:
                    self.id_ = 32
                    self.mark()
                    self.state = 75
                elif self.ch == 105:
                    self.id_ = 34
                    self.mark()
                    self.state = 77
                else:
                    self.ok = False
                
            elif self.state == 74:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 75:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 33
                    self.mark()
                    self.state = 76
                else:
                    self.ok = False
                
            elif self.state == 76:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 77:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 35
                    self.mark()
                    self.state = 78
                else:
                    self.ok = False
                
            elif self.state == 78:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 79:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 80:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 81:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (self.ch == 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 112:
                    self.id_ = 36
                    self.mark()
                    self.state = 82
                elif self.ch == 114:
                    self.id_ = 37
                    self.mark()
                    self.state = 83
                else:
                    self.ok = False
                
            elif self.state == 82:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 83:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 84:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = 38
                    self.mark()
                    self.state = 85
                else:
                    self.ok = False
                
            elif self.state == 85:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = 39
                    self.mark()
                    self.state = 86
                elif self.ch == 105:
                    self.id_ = 41
                    self.mark()
                    self.state = 88
                else:
                    self.ok = False
                
            elif self.state == 86:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 40
                    self.mark()
                    self.state = 87
                else:
                    self.ok = False
                
            elif self.state == 87:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 88:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 42
                    self.mark()
                    self.state = 89
                else:
                    self.ok = False
                
            elif self.state == 89:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 90:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 91:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (self.ch == 100) or (102 <= self.ch <= 110) or (112 <= self.ch <= 121):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 95
                    self.mark()
                    self.state = 92
                elif self.ch == 101:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 93
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 95
                elif self.ch == 122:
                    self.id_ = 93
                    self.mark()
                    self.state = 97
                else:
                    self.ok = False
                
            elif self.state == 92:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 93:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 102) or (104 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 103:
                    self.id_ = 43
                    self.mark()
                    self.state = 94
                else:
                    self.ok = False
                
            elif self.state == 94:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 95:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 112:
                    self.id_ = 44
                    self.mark()
                    self.state = 96
                else:
                    self.ok = False
                
            elif self.state == 96:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 97:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 98:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (self.ch == 115) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 45
                    self.mark()
                    self.state = 99
                elif self.ch == 116:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 100
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 105
                else:
                    self.ok = False
                
            elif self.state == 99:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 100:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 101
                elif self.ch == 105:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 103
                else:
                    self.ok = False
                
            elif self.state == 101:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 46
                    self.mark()
                    self.state = 102
                else:
                    self.ok = False
                
            elif self.state == 102:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 103:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 47
                    self.mark()
                    self.state = 104
                else:
                    self.ok = False
                
            elif self.state == 104:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 105:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 116:
                    self.id_ = 48
                    self.mark()
                    self.state = 106
                else:
                    self.ok = False
                
            elif self.state == 106:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 99) or (101 <= self.ch <= 104) or (106 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 100:
                    self.id_ = 49
                    self.mark()
                    self.state = 107
                elif self.ch == 105:
                    self.id_ = 50
                    self.mark()
                    self.state = 108
                else:
                    self.ok = False
                
            elif self.state == 107:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 108:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 109:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 100) or (102 <= self.ch <= 110) or (112 <= self.ch <= 116) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 101:
                    self.id_ = 98
                    self.mark()
                    self.state = 110
                elif self.ch == 111:
                    self.id_ = 97
                    self.mark()
                    self.state = 111
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 113
                else:
                    self.ok = False
                
            elif self.state == 110:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 111:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 111) or (113 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 112:
                    self.id_ = 51
                    self.mark()
                    self.state = 112
                else:
                    self.ok = False
                
            elif self.state == 112:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 113:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 114) or (116 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 114
                else:
                    self.ok = False
                
            elif self.state == 114:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 103) or (105 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 104:
                    self.id_ = 52
                    self.mark()
                    self.state = 115
                else:
                    self.ok = False
                
            elif self.state == 115:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 116:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 100) or (102 <= self.ch <= 107) or (109 <= self.ch <= 113) or (116 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 101:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 117
                elif self.ch == 108:
                    self.id_ = 57
                    self.mark()
                    self.state = 122
                elif self.ch == 114:
                    self.id_ = 62
                    self.mark()
                    self.state = 127
                elif self.ch == 115:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 132
                else:
                    self.ok = False
                
            elif self.state == 117:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 114) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 115:
                    self.id_ = 53
                    self.mark()
                    self.state = 118
                elif self.ch == 116:
                    self.id_ = 54
                    self.mark()
                    self.state = 119
                else:
                    self.ok = False
                
            elif self.state == 118:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 119:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 104) or (106 <= self.ch <= 109) or (111 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 105:
                    self.id_ = 55
                    self.mark()
                    self.state = 120
                elif self.ch == 110:
                    self.id_ = 56
                    self.mark()
                    self.state = 121
                else:
                    self.ok = False
                
            elif self.state == 120:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 121:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 122:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 58
                    self.mark()
                    self.state = 123
                elif self.ch == 99:
                    self.id_ = 59
                    self.mark()
                    self.state = 124
                elif self.ch == 100:
                    self.id_ = 61
                    self.mark()
                    self.state = 126
                else:
                    self.ok = False
                
            elif self.state == 123:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 124:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 60
                    self.mark()
                    self.state = 125
                else:
                    self.ok = False
                
            elif self.state == 125:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 126:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 127:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 98) or (101 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 63
                    self.mark()
                    self.state = 128
                elif self.ch == 99:
                    self.id_ = 64
                    self.mark()
                    self.state = 129
                elif self.ch == 100:
                    self.id_ = 66
                    self.mark()
                    self.state = 131
                else:
                    self.ok = False
                
            elif self.state == 128:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 129:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 65
                    self.mark()
                    self.state = 130
                else:
                    self.ok = False
                
            elif self.state == 130:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 131:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 132:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 116:
                    self.id_ = 67
                    self.mark()
                    self.state = 133
                else:
                    self.ok = False
                
            elif self.state == 133:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 134:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 97) or (self.ch == 100) or (102 <= self.ch <= 107) or (109 <= self.ch <= 111) or (self.ch == 113) or (115 <= self.ch <= 116) or (118 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 98:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 135
                elif self.ch == 99:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 137
                elif self.ch == 101:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 139
                elif self.ch == 108:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 141
                elif self.ch == 112:
                    self.id_ = 92
                    self.mark()
                    self.state = 143
                elif self.ch == 114:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 144
                elif self.ch == 117:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 147
                else:
                    self.ok = False
                
            elif self.state == 135:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 98) or (100 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 99:
                    self.id_ = 68
                    self.mark()
                    self.state = 136
                else:
                    self.ok = False
                
            elif self.state == 136:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 137:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 101) or (103 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 102:
                    self.id_ = 69
                    self.mark()
                    self.state = 138
                else:
                    self.ok = False
                
            elif self.state == 138:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 139:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 115) or (117 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 116:
                    self.id_ = 70
                    self.mark()
                    self.state = 140
                else:
                    self.ok = False
                
            elif self.state == 140:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 141:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 71
                    self.mark()
                    self.state = 142
                else:
                    self.ok = False
                
            elif self.state == 142:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 143:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 144:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (98 <= self.ch <= 107) or (109 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 97:
                    self.id_ = 72
                    self.mark()
                    self.state = 145
                elif self.ch == 108:
                    self.id_ = 73
                    self.mark()
                    self.state = 146
                else:
                    self.ok = False
                
            elif self.state == 145:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 146:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 147:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (self.ch == 97) or (99 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 98:
                    self.id_ = 74
                    self.mark()
                    self.state = 148
                else:
                    self.ok = False
                
            elif self.state == 148:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 149:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 110) or (112 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 111:
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 150
                else:
                    self.ok = False
                
            elif self.state == 150:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 113) or (115 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                elif self.ch == 114:
                    self.id_ = 75
                    self.mark()
                    self.state = 151
                else:
                    self.ok = False
                
            elif self.state == 151:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            elif self.state == 152:
                if (self.ch == 46) or (48 <= self.ch <= 57) or (65 <= self.ch <= 90) or (self.ch == 95) or (97 <= self.ch <= 122):
                    self.id_ = self.TOKEN_ident
                    self.mark()
                    self.state = 18
                else:
                    self.ok = False
                
            
            if self.id_ == 0 and self.ch == 0:
                return self.eof_token()

        self.reset()
        s = self.read
        if self.id_ == self.TOKEN_literal:
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
        return self.Token(self.read, self.id_, self.start_line, self.start_pos)
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



    def parse(self, scanner) -> None:
        self.scanner = scanner
        self.next()
        self.z80()

    def next(self) -> None:
        self.t = self.nt
        self.nt = self.scanner.get_next_token()
        self.id_ = self.nt.id_

    # z80<> = {[instruction] (.k=1.) comments|eol} eof
    def z80(self):
        while (10 <= self.id_ <= 75) or (self.id_ == Z80AssemblerScanner.TOKEN_eol) or (self.id_ == Z80AssemblerScanner.TOKEN_comments):
            if 10 <= self.id_ <= 75:
                self.instruction()
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
            else:
                raise ParserError(t=self.t, expected="eol,comments")
        if self.id_ == Z80AssemblerScanner.TOKEN_eof:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="eof")

    # instruction<> = (.k=1.) adc adc_op|add add_op|and s_op|bit bit_op|call call_op|ccf|cp s_op|cpd|cpdr|cpi|cpir|daa|d
    #    ec m_op|di|djnz relative|ei|ex ex_op|exx|halt|im im_op|in in_op|inc m_op|ind|indr|ini|inir|jp jp_op|jr jr_op|ld
    #     ld_op|ldd|lddr|ldi|ldir|neg|nop|or s_op|otdr|otir|out out_op|outd|outi|pop pop_op|push pop_op|res bit_op|ret r
    #    et_op|reti|retn|rl m_op|rla|rlc m_op|rlca|rld|rr m_op|rra|rrc m_op|rrca|rrd|rst immediate|sbc sbc_op|scf|set bi
    #    t_op|sla m_op|sra m_op|srl m_op|sub s_op|xor s_op
    def instruction(self):
        if self.id_ == 10:
            if self.id_ == 10:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"adc\"")
            self.adc_op()
        elif self.id_ == 11:
            if self.id_ == 11:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"add\"")
            self.add_op()
        elif self.id_ == 12:
            if self.id_ == 12:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"and\"")
            self.s_op("and")
        elif self.id_ == 13:
            if self.id_ == 13:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bit\"")
            self.bit_op("bit")
        elif self.id_ == 14:
            if self.id_ == 14:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"call\"")
            self.call_op()
        elif self.id_ == 15:
            if self.id_ == 15:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ccf\"")
        elif self.id_ == 16:
            if self.id_ == 16:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cp\"")
            self.s_op("cp")
        elif self.id_ == 17:
            if self.id_ == 17:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpd\"")
        elif self.id_ == 18:
            if self.id_ == 18:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpdr\"")
        elif self.id_ == 19:
            if self.id_ == 19:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpi\"")
        elif self.id_ == 20:
            if self.id_ == 20:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"cpir\"")
        elif self.id_ == 21:
            if self.id_ == 21:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"daa\"")
        elif self.id_ == 22:
            if self.id_ == 22:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"dec\"")
            self.m_op("dec")
        elif self.id_ == 23:
            if self.id_ == 23:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"di\"")
        elif self.id_ == 24:
            if self.id_ == 24:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"djnz\"")
            self.relative()
        elif self.id_ == 25:
            if self.id_ == 25:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ei\"")
        elif self.id_ == 26:
            if self.id_ == 26:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ex\"")
            self.ex_op()
        elif self.id_ == 27:
            if self.id_ == 27:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"exx\"")
        elif self.id_ == 28:
            if self.id_ == 28:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"halt\"")
        elif self.id_ == 29:
            if self.id_ == 29:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"im\"")
            self.im_op()
        elif self.id_ == 30:
            if self.id_ == 30:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"in\"")
            self.in_op()
        elif self.id_ == 31:
            if self.id_ == 31:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"inc\"")
            self.m_op("inc")
        elif self.id_ == 32:
            if self.id_ == 32:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ind\"")
        elif self.id_ == 33:
            if self.id_ == 33:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"indr\"")
        elif self.id_ == 34:
            if self.id_ == 34:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ini\"")
        elif self.id_ == 35:
            if self.id_ == 35:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"inir\"")
        elif self.id_ == 36:
            if self.id_ == 36:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"jp\"")
            self.jp_op()
        elif self.id_ == 37:
            if self.id_ == 37:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"jr\"")
            self.jr_op()
        elif self.id_ == 38:
            if self.id_ == 38:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ld\"")
            self.ld_op()
        elif self.id_ == 39:
            if self.id_ == 39:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldd\"")
        elif self.id_ == 40:
            if self.id_ == 40:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"lddr\"")
        elif self.id_ == 41:
            if self.id_ == 41:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldi\"")
        elif self.id_ == 42:
            if self.id_ == 42:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ldir\"")
        elif self.id_ == 43:
            if self.id_ == 43:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"neg\"")
        elif self.id_ == 44:
            if self.id_ == 44:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nop\"")
        elif self.id_ == 45:
            if self.id_ == 45:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"or\"")
            self.s_op("or")
        elif self.id_ == 46:
            if self.id_ == 46:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"otdr\"")
        elif self.id_ == 47:
            if self.id_ == 47:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"otir\"")
        elif self.id_ == 48:
            if self.id_ == 48:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"out\"")
            self.out_op()
        elif self.id_ == 49:
            if self.id_ == 49:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"outd\"")
        elif self.id_ == 50:
            if self.id_ == 50:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"outi\"")
        elif self.id_ == 51:
            if self.id_ == 51:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"pop\"")
            self.pop_op("pop")
        elif self.id_ == 52:
            if self.id_ == 52:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"push\"")
            self.pop_op("push")
        elif self.id_ == 53:
            if self.id_ == 53:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"res\"")
            self.bit_op("res")
        elif self.id_ == 54:
            if self.id_ == 54:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ret\"")
            self.ret_op()
        elif self.id_ == 55:
            if self.id_ == 55:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"reti\"")
        elif self.id_ == 56:
            if self.id_ == 56:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"retn\"")
        elif self.id_ == 57:
            if self.id_ == 57:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rl\"")
            self.m_op("rl")
        elif self.id_ == 58:
            if self.id_ == 58:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rla\"")
        elif self.id_ == 59:
            if self.id_ == 59:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rlc\"")
            self.m_op("rlc")
        elif self.id_ == 60:
            if self.id_ == 60:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rlca\"")
        elif self.id_ == 61:
            if self.id_ == 61:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rld\"")
        elif self.id_ == 62:
            if self.id_ == 62:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rr\"")
            self.m_op("rr")
        elif self.id_ == 63:
            if self.id_ == 63:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rra\"")
        elif self.id_ == 64:
            if self.id_ == 64:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrc\"")
            self.m_op("rrc")
        elif self.id_ == 65:
            if self.id_ == 65:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrca\"")
        elif self.id_ == 66:
            if self.id_ == 66:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rrd\"")
        elif self.id_ == 67:
            if self.id_ == 67:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"rst\"")
            self.immediate()
        elif self.id_ == 68:
            if self.id_ == 68:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sbc\"")
            self.sbc_op()
        elif self.id_ == 69:
            if self.id_ == 69:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"scf\"")
        elif self.id_ == 70:
            if self.id_ == 70:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"set\"")
            self.bit_op("set")
        elif self.id_ == 71:
            if self.id_ == 71:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sla\"")
            self.m_op("sla")
        elif self.id_ == 72:
            if self.id_ == 72:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sra\"")
            self.m_op("sra")
        elif self.id_ == 73:
            if self.id_ == 73:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"srl\"")
            self.m_op("srl")
        elif self.id_ == 74:
            if self.id_ == 74:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sub\"")
            self.s_op("sub")
        elif self.id_ == 75:
            if self.id_ == 75:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"xor\"")
            self.s_op("xor")
        else:
            raise ParserError(t=self.t, expected="'adc','add','and','bit','call','ccf','cp','cpd','cpdr','cpi','cpir','daa','dec','di','djnz','ei','ex','exx','halt','im','in','inc','ind','indr','ini','inir','jp','jr','ld','ldd','lddr','ldi','ldir','neg','nop','or','otdr','otir','out','outd','outi','pop','push','res','ret','reti','retn','rl','rla','rlc','rlca','rld','rr','rra','rrc','rrca','rrd','rst','sbc','scf','set','sla','sra','srl','sub','xor'")

    # ld_op<> = (.k=1.) ( (.k=1.) hl ) , (.k=1.) a|register|immediate|(.k=1.) ix|iy (.k=1.) +|- unsigned_number ) , (.k=
    #    1.) a|register|immediate|bc ) , a|de ) , a|addr16 ) , (.k=1.) a|hl|ix|iy|dd|sp , (.k=1.) hl|ix|iy|( addr16 )|im
    #    mediate|dd , (.k=1.) ( addr16 )|immediate|ix , (.k=1.) ( addr16 )|immediate|iy , (.k=1.) ( addr16 )|immediate|i
    #     , a|r , a|a , (.k=1.) i|r|( (.k=1.) bc|de|addr16 )|register , (.k=1.) register|immediate|( (.k=1.) hl|(.k=1.) 
    #    ix|iy (.k=1.) +|- unsigned_number )
    def ld_op(self):
        if self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 76:
                    if self.id_ == 76:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                elif 76 <= self.id_ <= 82:
                    self.register()
                elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.immediate()
                else:
                    raise ParserError(t=self.t, expected="'+','-','a','b','c','d','e','h','l',ident,unsigned_number")
            elif 88 <= self.id_ <= 89:
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                else:
                    raise ParserError(t=self.t, expected="'ix','iy'")
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
                if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 76:
                    if self.id_ == 76:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                elif 76 <= self.id_ <= 82:
                    self.register()
                elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                    self.immediate()
                else:
                    raise ParserError(t=self.t, expected="'+','-','a','b','c','d','e','h','l',ident,unsigned_number")
            elif self.id_ == 85:
                if self.id_ == 85:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 76:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            elif self.id_ == 86:
                if self.id_ == 86:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 76:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            elif Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number:
                self.addr16()
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
                if self.id_ == 4:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
                if self.id_ == 76:
                    if self.id_ == 76:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
                elif self.id_ == 87:
                    if self.id_ == 87:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                elif self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                elif (85 <= self.id_ <= 87) or (self.id_ == 92):
                    self.dd()
                else:
                    raise ParserError(t=self.t, expected="'a','bc','de','hl','ix','iy','sp'")
            else:
                raise ParserError(t=self.t, expected="'bc','de','hl','ix','iy',ident,unsigned_number")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif self.id_ == 88:
                if self.id_ == 88:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            elif self.id_ == 89:
                if self.id_ == 89:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            elif self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
            else:
                raise ParserError(t=self.t, expected="'(','+','-','hl','ix','iy',ident,unsigned_number")
        elif (85 <= self.id_ <= 87) or (self.id_ == 92):
            self.dd()
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
            else:
                raise ParserError(t=self.t, expected="'(','+','-',ident,unsigned_number")
        elif self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
            else:
                raise ParserError(t=self.t, expected="'(','+','-',ident,unsigned_number")
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                self.addr16()
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
            else:
                raise ParserError(t=self.t, expected="'(','+','-',ident,unsigned_number")
        elif self.id_ == 83:
            if self.id_ == 83:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"i\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        elif self.id_ == 84:
            if self.id_ == 84:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"r\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        elif self.id_ == 76:
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 83:
                if self.id_ == 83:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"i\"")
            elif self.id_ == 84:
                if self.id_ == 84:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"r\"")
            elif self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                if self.id_ == 85:
                    if self.id_ == 85:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
                elif self.id_ == 86:
                    if self.id_ == 86:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
                elif Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.addr16()
                else:
                    raise ParserError(t=self.t, expected="'bc','de',ident,unsigned_number")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            else:
                raise ParserError(t=self.t, expected="'(','i','r'")
        elif 76 <= self.id_ <= 82:
            self.register()
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if 76 <= self.id_ <= 82:
                self.register()
            elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
                self.immediate()
            elif self.id_ == 6:
                if self.id_ == 6:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
                if self.id_ == 87:
                    if self.id_ == 87:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
                elif 88 <= self.id_ <= 89:
                    if self.id_ == 88:
                        if self.id_ == 88:
                            self.next()
                        else:
                            raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                    elif self.id_ == 89:
                        if self.id_ == 89:
                            self.next()
                        else:
                            raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                    else:
                        raise ParserError(t=self.t, expected="'ix','iy'")
                    if self.id_ == 8:
                        if self.id_ == 8:
                            self.next()
                        else:
                            raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                    elif self.id_ == 9:
                        if self.id_ == 9:
                            self.next()
                        else:
                            raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                    else:
                        raise ParserError(t=self.t, expected="'+','-'")
                    if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
                else:
                    raise ParserError(t=self.t, expected="'hl','ix','iy'")
                if self.id_ == 7:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            else:
                raise ParserError(t=self.t, expected="'(','+','-','a','b','c','d','e','h','l',ident,unsigned_number")
        else:
            raise ParserError(t=self.t, expected="'(','a','b','c','d','e','h','l','i','r','bc','de','hl','ix','iy','sp'")

    # add_op<> = (.k=1.) hl , ss|ix , pp|iy , rr|a_op
    def add_op(self):
        if self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
        elif self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.pp()
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.rr()
        elif self.id_ == 76:
            self.a_op("add")
        else:
            raise ParserError(t=self.t, expected="'a','hl','ix','iy'")

    # adc_op<> = (.k=1.) hl , ss|a_op
    def adc_op(self):
        if self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
        elif self.id_ == 76:
            self.a_op("adc")
        else:
            raise ParserError(t=self.t, expected="'a','hl'")

    # sbc_op<> = (.k=1.) hl , ss|a_op
    def sbc_op(self):
        if self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.ss()
        elif self.id_ == 76:
            self.a_op("sbc")
        else:
            raise ParserError(t=self.t, expected="'a','hl'")

    # call_op<> = (.k=1.) cc , addr16|addr16
    def call_op(self):
        if (self.id_ == 78) or (93 <= self.id_ <= 95) or (97 <= self.id_ <= 100):
            self.cc()
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.addr16()
        elif Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number:
            self.addr16()
        else:
            raise ParserError(t=self.t, expected="'c','nz','z','nc','po','pe','p','m',ident,unsigned_number")

    # jp_op<> = (.k=1.) ( (.k=1.) hl|ix|iy )|cc , addr16|addr16
    def jp_op(self):
        if self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif self.id_ == 88:
                if self.id_ == 88:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            elif self.id_ == 89:
                if self.id_ == 89:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif (self.id_ == 78) or (93 <= self.id_ <= 95) or (97 <= self.id_ <= 100):
            self.cc()
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.addr16()
        elif Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number:
            self.addr16()
        else:
            raise ParserError(t=self.t, expected="'(','c','nz','z','nc','po','pe','p','m',ident,unsigned_number")

    # jr_op<> = (.k=1.) nz , relative|z , relative|nc , relative|c , relative|relative
    def jr_op(self):
        if self.id_ == 93:
            if self.id_ == 93:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nz\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
        elif self.id_ == 94:
            if self.id_ == 94:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"z\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nc\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
        elif self.id_ == 78:
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.relative()
        elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
            self.relative()
        else:
            raise ParserError(t=self.t, expected="'+','-','c','nz','z','nc',ident,unsigned_number")

    # out_op<> = ( (.k=1.) c ) , register|immediate ) , a
    def out_op(self):
        if self.id_ == 6:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
        if self.id_ == 78:
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            self.register()
        elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        else:
            raise ParserError(t=self.t, expected="'+','-','c',ident,unsigned_number")

    # in_op<> = (.k=1.) a , ( immediate )|register , ( c )
    def in_op(self):
        if self.id_ == 76:
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            self.immediate()
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        elif 76 <= self.id_ <= 82:
            self.register()
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'a','b','c','d','e','h','l'")

    # ex_op<> = (.k=1.) de , hl|af , af'|( sp ) , (.k=1.) hl|ix|iy
    def ex_op(self):
        if self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
        elif self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 91:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af'\"")
        elif self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
            if self.id_ == 4:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif self.id_ == 88:
                if self.id_ == 88:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
            elif self.id_ == 89:
                if self.id_ == 89:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
        else:
            raise ParserError(t=self.t, expected="'(','de','af'")

    # pop_op<op: str> = (.k=1.) qq|ix|iy
    def pop_op(self, op: str):
        if (85 <= self.id_ <= 87) or (self.id_ == 90):
            self.qq()
        elif self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','hl','ix','iy','af'")

    # ret_op<> = [cc]
    def ret_op(self):
        if (self.id_ == 78) or (93 <= self.id_ <= 95) or (97 <= self.id_ <= 100):
            self.cc()

    # im_op<> = unsigned_number
    def im_op(self):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")

    # a_op<op: str> = a , (.k=1.) register|immediate|( (.k=1.) hl|(.k=1.) ix|iy (.k=1.) +|- unsigned_number )
    def a_op(self, op: str):
        if self.id_ == 76:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        if self.id_ == 4:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
        if 76 <= self.id_ <= 82:
            self.register()
        elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
        elif self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif 88 <= self.id_ <= 89:
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                else:
                    raise ParserError(t=self.t, expected="'ix','iy'")
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
                if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'(','+','-','a','b','c','d','e','h','l',ident,unsigned_number")

    # s_op<op: str> = (.k=1.) register|immediate|( (.k=1.) hl|(.k=1.) ix|iy (.k=1.) +|- unsigned_number )
    def s_op(self, op: str):
        if 76 <= self.id_ <= 82:
            self.register()
        elif (8 <= self.id_ <= 9) or (Z80AssemblerScanner.TOKEN_ident <= self.id_ <= Z80AssemblerScanner.TOKEN_unsigned_number):
            self.immediate()
        elif self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif 88 <= self.id_ <= 89:
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                else:
                    raise ParserError(t=self.t, expected="'ix','iy'")
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
                if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'(','+','-','a','b','c','d','e','h','l',ident,unsigned_number")

    # m_op<op: str> = (.k=1.) register|( (.k=1.) hl|(.k=1.) ix|iy (.k=1.) +|- unsigned_number )
    def m_op(self, op: str):
        if 76 <= self.id_ <= 82:
            self.register()
        elif self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif 88 <= self.id_ <= 89:
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                else:
                    raise ParserError(t=self.t, expected="'ix','iy'")
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
                if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'(','a','b','c','d','e','h','l'")

    # bit_op<op: str> = unsigned_number , (.k=1.) register|( (.k=1.) hl|(.k=1.) ix|iy (.k=1.) +|- unsigned_number )
    def bit_op(self, op: str):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        if self.id_ == 4:
            self.next()
        else:
            raise ParserError(t=self.t, nt=self.nt, expected="\",\"")
        if 76 <= self.id_ <= 82:
            self.register()
        elif self.id_ == 6:
            if self.id_ == 6:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"(\"")
            if self.id_ == 87:
                if self.id_ == 87:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
            elif 88 <= self.id_ <= 89:
                if self.id_ == 88:
                    if self.id_ == 88:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
                elif self.id_ == 89:
                    if self.id_ == 89:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
                else:
                    raise ParserError(t=self.t, expected="'ix','iy'")
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
                if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                    self.next()
                else:
                    raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
            else:
                raise ParserError(t=self.t, expected="'hl','ix','iy'")
            if self.id_ == 7:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\")\"")
        else:
            raise ParserError(t=self.t, expected="'(','a','b','c','d','e','h','l'")

    # addr16<> = (.k=1.) unsigned_number|ident
    def addr16(self):
        if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
        else:
            raise ParserError(t=self.t, expected="ident,unsigned_number")

    # relative<> = (.k=1.) [(.k=1.) +|-] unsigned_number|ident
    def relative(self):
        if (8 <= self.id_ <= 9) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            if 8 <= self.id_ <= 9:
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
        else:
            raise ParserError(t=self.t, expected="'+','-',ident,unsigned_number")

    # immediate<> = (.k=1.) [(.k=1.) +|-] unsigned_number|ident
    def immediate(self):
        if (8 <= self.id_ <= 9) or (self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number):
            if 8 <= self.id_ <= 9:
                if self.id_ == 8:
                    if self.id_ == 8:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"+\"")
                elif self.id_ == 9:
                    if self.id_ == 9:
                        self.next()
                    else:
                        raise ParserError(t=self.t, nt=self.nt, expected="\"-\"")
                else:
                    raise ParserError(t=self.t, expected="'+','-'")
            if self.id_ == Z80AssemblerScanner.TOKEN_unsigned_number:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"H\"")
        elif self.id_ == Z80AssemblerScanner.TOKEN_ident:
            if self.id_ == Z80AssemblerScanner.TOKEN_ident:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="ident")
        else:
            raise ParserError(t=self.t, expected="'+','-',ident,unsigned_number")

    # register<> = (.k=1.) a|b|c|d|e|h|l
    def register(self):
        if self.id_ == 76:
            if self.id_ == 76:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"a\"")
        elif self.id_ == 77:
            if self.id_ == 77:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"b\"")
        elif self.id_ == 78:
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
        elif self.id_ == 79:
            if self.id_ == 79:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"d\"")
        elif self.id_ == 80:
            if self.id_ == 80:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"e\"")
        elif self.id_ == 81:
            if self.id_ == 81:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"h\"")
        elif self.id_ == 82:
            if self.id_ == 82:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"l\"")
        else:
            raise ParserError(t=self.t, expected="'a','b','c','d','e','h','l'")

    # cc<> = (.k=1.) nz|z|nc|c|po|pe|p|m
    def cc(self):
        if self.id_ == 93:
            if self.id_ == 93:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nz\"")
        elif self.id_ == 94:
            if self.id_ == 94:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"z\"")
        elif self.id_ == 95:
            if self.id_ == 95:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"nc\"")
        elif self.id_ == 78:
            if self.id_ == 78:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"c\"")
        elif self.id_ == 97:
            if self.id_ == 97:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"po\"")
        elif self.id_ == 98:
            if self.id_ == 98:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"pe\"")
        elif self.id_ == 99:
            if self.id_ == 99:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"p\"")
        elif self.id_ == 100:
            if self.id_ == 100:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"m\"")
        else:
            raise ParserError(t=self.t, expected="'c','nz','z','nc','po','pe','p','m'")

    # qq<> = (.k=1.) bc|de|hl|af
    def qq(self):
        if self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
        elif self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
        elif self.id_ == 90:
            if self.id_ == 90:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"af\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','hl','af'")

    # ss<> = (.k=1.) bc|de|hl|sp
    def ss(self):
        if self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
        elif self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','hl','sp'")

    # pp<> = (.k=1.) bc|de|ix|sp
    def pp(self):
        if self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
        elif self.id_ == 88:
            if self.id_ == 88:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"ix\"")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','ix','sp'")

    # rr<> = (.k=1.) bc|de|iy|sp
    def rr(self):
        if self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
        elif self.id_ == 89:
            if self.id_ == 89:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"iy\"")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','iy','sp'")

    # dd<> = (.k=1.) bc|de|hl|sp
    def dd(self):
        if self.id_ == 85:
            if self.id_ == 85:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"bc\"")
        elif self.id_ == 86:
            if self.id_ == 86:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"de\"")
        elif self.id_ == 87:
            if self.id_ == 87:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"hl\"")
        elif self.id_ == 92:
            if self.id_ == 92:
                self.next()
            else:
                raise ParserError(t=self.t, nt=self.nt, expected="\"sp\"")
        else:
            raise ParserError(t=self.t, expected="'bc','de','hl','sp'")


if __name__ == "__main__":
    import sys
    from buLL.parser.toolkit import Toolkit
    t = Toolkit.create(Z80AssemblerParser())
    t.set_args(*sys.argv[1:])
    t.process()
