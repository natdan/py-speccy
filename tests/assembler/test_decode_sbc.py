from assembler.assert_util import assert_decode


class TestDecodeSBC:
    def test_and(self) -> None:
        assert_decode("sbc a, b", 0x98)
        assert_decode("sbc a, c", 0x99)
        assert_decode("sbc a, d", 0x9a)
        assert_decode("sbc a, e", 0x9b)
        assert_decode("sbc a, h", 0x9c)
        assert_decode("sbc a, l", 0x9d)
        assert_decode("sbc a, a", 0x9f)
        assert_decode("sbc a, 254", 0xde, 254)
        assert_decode("sbc a, (hl)", 0x9e)
        assert_decode("sbc a, (ix+123)", 0xdd, 0x9e, 123)
        assert_decode("sbc a, (ix-4)", 0xdd, 0x9e, 252)
        assert_decode("sbc a, (iy+123)", 0xfd, 0x9e, 123)
        assert_decode("sbc a, (iy-123)", 0xfd, 0x9e, 133)
