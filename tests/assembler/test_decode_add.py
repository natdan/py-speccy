from assembler.assert_util import assert_decode


class TestDecodeAdd:
    def test_add(self) -> None:
        assert_decode("add a, b", 0x80)
        assert_decode("add a, c", 0x81)
        assert_decode("add a, d", 0x82)
        assert_decode("add a, e", 0x83)
        assert_decode("add a, h", 0x84)
        assert_decode("add a, l", 0x85)
        assert_decode("add a, a", 0x87)
        assert_decode("add a, 254", 0xc6, 254)
        assert_decode("add a, (hl)", 0x86)
        assert_decode("add a, (ix+123)", 0xdd, 0x86, 123)
        assert_decode("add a, (ix-4)", 0xdd, 0x86, 252)
        assert_decode("add a, (iy+123)", 0xfd, 0x86, 123)
        assert_decode("add a, (iy-123)", 0xfd, 0x86, 133)

    def test_add_hlss(self) -> None:
        assert_decode("add hl, bc", 0x09)
        assert_decode("add hl, de", 0x19)
        assert_decode("add hl, hl", 0x29)
        assert_decode("add hl, sp", 0x39)

    def test_add_ixpp(self) -> None:
        assert_decode("add ix, bc", 0xdd, 0x09)
        assert_decode("add ix, de", 0xdd, 0x19)
        assert_decode("add ix, ix", 0xdd, 0x29)
        assert_decode("add ix, sp", 0xdd, 0x39)

    def test_add_iyrr(self) -> None:
        assert_decode("add iy, bc", 0xfd, 0x09)
        assert_decode("add iy, de", 0xfd, 0x19)
        assert_decode("add iy, iy", 0xfd, 0x29)
        assert_decode("add iy, sp", 0xfd, 0x39)
