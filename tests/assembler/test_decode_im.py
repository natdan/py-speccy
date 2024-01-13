from assembler.assert_util import assert_decode


class TestDecodeIM:
    def test_im(self) -> None:
        assert_decode("im 0", 0xed, 0x46)
        assert_decode("im 1", 0xed, 0x56)
        assert_decode("im 2", 0xed, 0x5e)
