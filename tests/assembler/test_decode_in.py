from assembler.assert_util import assert_decode


class TestDecodeIN:
    def test_in(self) -> None:
        assert_decode("in a, (254)", 0xdb, 254)
        assert_decode("in b, (c)", 0xed, 0x40)
        assert_decode("in c, (c)", 0xed, 0x48)
        assert_decode("in d, (c)", 0xed, 0x50)
        assert_decode("in e, (c)", 0xed, 0x58)
        assert_decode("in h, (c)", 0xed, 0x60)
        assert_decode("in l, (c)", 0xed, 0x68)
        assert_decode("in a, (c)", 0xed, 0x78)
