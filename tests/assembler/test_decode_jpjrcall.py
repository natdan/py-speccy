from assembler.assert_util import assert_decode


class TestDecodeJPJRCALL:
    def test_jp(self) -> None:
        assert_decode("jp $1234", 0xc3, 0x34, 0x12)
        assert_decode("jp nz, $1110", 0xc2 + 0 * 8, 0x10, 0x11)
        assert_decode("jp z, $2211", 0xc2 + 1 * 8, 0x11, 0x22)
        assert_decode("jp nc, $3312", 0xc2 + 2 * 8, 0x12, 0x33)
        assert_decode("jp c, $4413", 0xc2 + 3 * 8, 0x13, 0x44)
        assert_decode("jp po, $5514", 0xc2 + 4 * 8, 0x14, 0x55)
        assert_decode("jp pe, $6615", 0xc2 + 5 * 8, 0x15, 0x66)
        assert_decode("jp p, $7716", 0xc2 + 6 * 8, 0x16, 0x77)
        assert_decode("jp m, $8817", 0xc2 + 7 * 8, 0x17, 0x88)
        assert_decode("jp (hl)", 0xe9)
        assert_decode("jp (ix)", 0xdd, 0xe9)
        assert_decode("jp (iy)", 0xfd, 0xe9)

    def test_jr(self) -> None:
        assert_decode("jr $4036", 0x18, 0x34)
        assert_decode("jr c, $4012", 0x38, 0x10)
        assert_decode("jr nc, $4000",  0x30, 0xfe)
        assert_decode("jr z, $3fff", 0x28, 0xfd)
        assert_decode("jr nz, $4015",  0x20, 0x13)

    def test_djnz(self) -> None:
        assert_decode("djnz $4036", 0x10, 0x34)
        assert_decode("djnz $4000",  0x10, 0xfe)

    def test_call(self) -> None:
        assert_decode("call $1234", 0xcd, 0x34, 0x12)
        assert_decode("call nz, $1110", 0xc4 + 0 * 8, 0x10, 0x11)
        assert_decode("call z, $2211",  0xc4 + 1 * 8, 0x11, 0x22)
        assert_decode("call nc, $3312", 0xc4 + 2 * 8, 0x12, 0x33)
        assert_decode("call c, $4413",  0xc4 + 3 * 8, 0x13, 0x44)
        assert_decode("call po, $5514", 0xc4 + 4 * 8, 0x14, 0x55)
        assert_decode("call pe, $6615", 0xc4 + 5 * 8, 0x15, 0x66)
        assert_decode("call p, $7716",  0xc4 + 6 * 8, 0x16, 0x77)
        assert_decode("call m, $8817",  0xc4 + 7 * 8, 0x17, 0x88)

