from assembler.assert_util import assert_decode


class TestDecodeRST:
    def test_rst(self) -> None:
        assert_decode("rst 00h", 0xc7)
        assert_decode("rst 08h", 0xcf)
        assert_decode("rst 10h", 0xd7)
        assert_decode("rst 18h", 0xdf)
        assert_decode("rst 20h", 0xe7)
        assert_decode("rst 28h", 0xef)
        assert_decode("rst 30h", 0xf7)
        assert_decode("rst 38h", 0xff)
