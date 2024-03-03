from assembler.assert_util import assert_decode


class TestDecodeRST:
    def test_rst(self) -> None:
        assert_decode("rst $0", 0xc7)
        assert_decode("rst $8", 0xcf)
        assert_decode("rst $10", 0xd7)
        assert_decode("rst $18", 0xdf)
        assert_decode("rst $20", 0xe7)
        assert_decode("rst $28", 0xef)
        assert_decode("rst $30", 0xf7)
        assert_decode("rst $38", 0xff)
