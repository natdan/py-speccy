from assembler.assert_util import assert_decode


class TestDecodeLd:
    def test_ld_rr(self) -> None:
        assert_decode("ld b, b", 0x40)
        assert_decode("ld b, c", 0x41)
        assert_decode("ld b, d", 0x42)
        assert_decode("ld b, e", 0x43)
        assert_decode("ld b, h", 0x44)
        assert_decode("ld b, l", 0x45)
        assert_decode("ld b, a", 0x47)

        assert_decode("ld c, b", 0x48)
        assert_decode("ld c, c", 0x49)
        assert_decode("ld c, d", 0x4a)
        assert_decode("ld c, e", 0x4b)
        assert_decode("ld c, h", 0x4c)
        assert_decode("ld c, l", 0x4d)
        assert_decode("ld c, a", 0x4f)

        assert_decode("ld d, b", 0x50)
        assert_decode("ld d, c", 0x51)
        assert_decode("ld d, d", 0x52)
        assert_decode("ld d, e", 0x53)
        assert_decode("ld d, h", 0x54)
        assert_decode("ld d, l", 0x55)
        assert_decode("ld d, a", 0x57)

        assert_decode("ld e, b", 0x58)
        assert_decode("ld e, c", 0x59)
        assert_decode("ld e, d", 0x5a)
        assert_decode("ld e, e", 0x5b)
        assert_decode("ld e, h", 0x5c)
        assert_decode("ld e, l", 0x5d)
        assert_decode("ld e, a", 0x5f)

        assert_decode("ld h, b", 0x60)
        assert_decode("ld h, c", 0x61)
        assert_decode("ld h, d", 0x62)
        assert_decode("ld h, e", 0x63)
        assert_decode("ld h, h", 0x64)
        assert_decode("ld h, l", 0x65)
        assert_decode("ld h, a", 0x67)

        assert_decode("ld l, b", 0x68)
        assert_decode("ld l, c", 0x69)
        assert_decode("ld l, d", 0x6a)
        assert_decode("ld l, e", 0x6b)
        assert_decode("ld l, h", 0x6c)
        assert_decode("ld l, l", 0x6d)
        assert_decode("ld l, a", 0x6f)

        assert_decode("ld a, b", 0x78)
        assert_decode("ld a, c", 0x79)
        assert_decode("ld a, d", 0x7a)
        assert_decode("ld a, e", 0x7b)
        assert_decode("ld a, h", 0x7c)
        assert_decode("ld a, l", 0x7d)
        assert_decode("ld a, a", 0x7f)

    def test_ld_rn(self) -> None:
        assert_decode("ld b, 1", 0x06, 1)
        assert_decode("ld c, 2", 0x0e, 2)
        assert_decode("ld d, 3", 0x16, 3)
        assert_decode("ld e, 4", 0x1e, 4)
        assert_decode("ld h, 5", 0x26, 5)
        assert_decode("ld l, 6", 0x2e, 6)
        assert_decode("ld a, 7", 0x3e, 7)

    def test_ld_rphlp(self) -> None:
        assert_decode("ld b, (hl)", 0x46)
        assert_decode("ld c, (hl)", 0x4e)
        assert_decode("ld d, (hl)", 0x56)
        assert_decode("ld e, (hl)", 0x5e)
        assert_decode("ld h, (hl)", 0x66)
        assert_decode("ld l, (hl)", 0x6e)
        assert_decode("ld a, (hl)", 0x7e)

    def test_ld_rpixp(self) -> None:
        assert_decode("ld b, (ix+1)", 0xdd, 0x46, 1)
        assert_decode("ld c, (ix+2)", 0xdd, 0x4e, 2)
        assert_decode("ld d, (ix+3)", 0xdd, 0x56, 3)
        assert_decode("ld e, (ix+4)", 0xdd, 0x5e, 4)
        assert_decode("ld h, (ix+5)", 0xdd, 0x66, 5)
        assert_decode("ld l, (ix+6)", 0xdd, 0x6e, 6)
        assert_decode("ld a, (ix+7)", 0xdd, 0x7e, 7)

    def test_ld_rpiyp(self) -> None:
        assert_decode("ld b, (iy+1)", 0xfd, 0x46, 1)
        assert_decode("ld c, (iy+2)", 0xfd, 0x4e, 2)
        assert_decode("ld d, (iy+3)", 0xfd, 0x56, 3)
        assert_decode("ld e, (iy+4)", 0xfd, 0x5e, 4)
        assert_decode("ld h, (iy+5)", 0xfd, 0x66, 5)
        assert_decode("ld l, (iy+6)", 0xfd, 0x6e, 6)
        assert_decode("ld a, (iy+7)", 0xfd, 0x7e, 7)

    def test_ld_phlpr(self) -> None:
        # assert_decode("ld (hl), b", 0x70)
        assert_decode("ld (hl), c", 0x71)
        assert_decode("ld (hl), d", 0x72)
        assert_decode("ld (hl), e", 0x73)
        assert_decode("ld (hl), h", 0x74)
        assert_decode("ld (hl), l", 0x75)
        assert_decode("ld (hl), a", 0x77)

    def test_ld_pixpr(self) -> None:
        assert_decode("ld (ix+1), b", 0xdd, 0x70, 1)
        assert_decode("ld (ix+2), c", 0xdd, 0x71, 2)
        assert_decode("ld (ix+3), d", 0xdd, 0x72, 3)
        assert_decode("ld (ix+4), e", 0xdd, 0x73, 4)
        assert_decode("ld (ix+5), h", 0xdd, 0x74, 5)
        assert_decode("ld (ix+6), l", 0xdd, 0x75, 6)
        assert_decode("ld (ix+7), a", 0xdd, 0x77, 7)

    def test_ld_piypr(self) -> None:
        assert_decode("ld (iy+1), b", 0xfd, 0x70, 1)
        assert_decode("ld (iy+2), c", 0xfd, 0x71, 2)
        assert_decode("ld (iy+3), d", 0xfd, 0x72, 3)
        assert_decode("ld (iy+4), e", 0xfd, 0x73, 4)
        assert_decode("ld (iy+5), h", 0xfd, 0x74, 5)
        assert_decode("ld (iy+6), l", 0xfd, 0x75, 6)
        assert_decode("ld (iy+7), a", 0xfd, 0x77, 7)
