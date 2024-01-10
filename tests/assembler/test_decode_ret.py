from assembler.assert_util import assert_decode


class TestDecodeRet:
    def test_ret(self) -> None:
        assert_decode("ret", 0xc9)
        assert_decode("ret nz", 0xc0 + 0 * 8)
        assert_decode("ret z", 0xc0 + 1 * 8)
        assert_decode("ret nc", 0xc0 + 2 * 8)
        assert_decode("ret c", 0xc0 + 3 * 8)
        assert_decode("ret po", 0xc0 + 4 * 8)
        assert_decode("ret pe", 0xc0 + 5 * 8)
        assert_decode("ret p", 0xc0 + 6 * 8)
        assert_decode("ret m", 0xc0 + 7 * 8)
        assert_decode("reti", 0xed, 0x4d)
        assert_decode("retn", 0xed, 0x45)
