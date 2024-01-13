from assembler.assert_util import assert_decode


class TestDecodeOUT:
    def test_out(self) -> None:
        assert_decode("out (254), a", 0xd3, 254)
        assert_decode("out (c), b", 0xed, 0x41)
        assert_decode("out (c), c", 0xed, 0x49)
        assert_decode("out (c), d", 0xed, 0x51)
        assert_decode("out (c), e", 0xed, 0x59)
        assert_decode("out (c), h", 0xed, 0x61)
        assert_decode("out (c), l", 0xed, 0x69)
        assert_decode("out (c), a", 0xed, 0x79)
