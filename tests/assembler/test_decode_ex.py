from assembler.assert_util import assert_decode


class TestDecodeEx:
    def test_ex(self) -> None:
        assert_decode("ex de, hl", 0xeb)
        assert_decode("ex af, af'", 0x08)
        assert_decode("ex (sp), hl", 0xe3)
        assert_decode("ex (sp), ix", 0xdd, 0xe3)
        assert_decode("ex (sp), iy", 0xfd, 0xe3)
