from assembler.assert_util import assert_decode


class TestDecodeSimple:
    def test_simple(self) -> None:
        assert_decode(f"ccf", 0x3f)
        assert_decode(f"scf", 0x37)
        assert_decode(f"cpl", 0x2f)
        assert_decode(f"daa", 0x27)
        assert_decode(f"di", 0xf3)
        assert_decode(f"ei", 0xfb)
        assert_decode(f"exx", 0xd9)
        assert_decode(f"rla", 0x17)
        assert_decode(f"rlca", 0x07)
        assert_decode(f"rra", 0x1f)
        assert_decode(f"rrca", 0x0f)

    def test_simple_ed(self) -> None:
        assert_decode(f"cpd", 0xed, 0xa9)
        assert_decode(f"cpdr", 0xed, 0xb9)
        assert_decode(f"cpi", 0xed, 0xa1)
        assert_decode(f"cpir", 0xed, 0xb1)
        assert_decode(f"ind", 0xed, 0xaa)
        assert_decode(f"indr", 0xed, 0xba)
        assert_decode(f"ini", 0xed, 0xa2)
        assert_decode(f"inir", 0xed, 0xb2)
        assert_decode(f"ldd", 0xed, 0xa8)
        assert_decode(f"lddr", 0xed, 0xb8)
        assert_decode(f"ldi", 0xed, 0xa0)
        assert_decode(f"ldir", 0xed, 0xb0)
        assert_decode(f"neg", 0xed, 0x44)
        assert_decode(f"outd", 0xed, 0xab)
        assert_decode(f"otdr", 0xed, 0xbb)
        assert_decode(f"otir", 0xed, 0xb3)
        assert_decode(f"reti", 0xed, 0x4d)
        assert_decode(f"retn", 0xed, 0x45)
        assert_decode(f"rrd", 0xed, 0x67)

