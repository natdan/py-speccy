from tests.assembler.memory import assert_decode


class TestDecodeSOP:
    def test_and(self) -> None:
        assert_decode("and b", 0xa0)
        assert_decode("and c", 0xa1)
        assert_decode("and d", 0xa2)
        assert_decode("and e", 0xa3)
        assert_decode("and h", 0xa4)
        assert_decode("and l", 0xa5)
        assert_decode("and a", 0xa7)
        assert_decode("and 254", 0xe6, 254)
        assert_decode("and (hl)", 0xa6)
        assert_decode("and (ix+123)", 0xdd, 0xa6, 123)
        assert_decode("and (ix-4)", 0xdd, 0xa6, 252)
        assert_decode("and (iy+123)", 0xfd, 0xa6, 123)
        assert_decode("and (iy-123)", 0xfd, 0xa6, 133)

    def test_or(self) -> None:
        assert_decode("or b", 0xb0)
        assert_decode("or c", 0xb1)
        assert_decode("or d", 0xb2)
        assert_decode("or e", 0xb3)
        assert_decode("or h", 0xb4)
        assert_decode("or l", 0xb5)
        assert_decode("or a", 0xb7)
        assert_decode("or 254", 0xF6, 254)
        assert_decode("or (hl)", 0xb6)
        assert_decode("or (ix+123)", 0xdd, 0xb6, 123)
        assert_decode("or (ix-4)", 0xdd, 0xb6, 252)
        assert_decode("or (iy+123)", 0xfd, 0xb6, 123)
        assert_decode("or (iy-123)", 0xfd, 0xb6, 133)

    def test_xor(self) -> None:
        assert_decode("xor b", 0xa8)
        assert_decode("xor c", 0xa9)
        assert_decode("xor d", 0xaa)
        assert_decode("xor e", 0xab)
        assert_decode("xor h", 0xac)
        assert_decode("xor l", 0xad)
        assert_decode("xor a", 0xaf)
        assert_decode("xor 254", 0xee, 254)
        assert_decode("xor (hl)", 0xae)
        assert_decode("xor (ix+123)", 0xdd, 0xae, 123)
        assert_decode("xor (ix-4)", 0xdd, 0xae, 252)
        assert_decode("xor (iy+123)", 0xfd, 0xae, 123)
        assert_decode("xor (iy-123)", 0xfd, 0xae, 133)

    def test_sub(self) -> None:
        assert_decode("sub b", 0x90)
        assert_decode("sub c", 0x91)
        assert_decode("sub d", 0x92)
        assert_decode("sub e", 0x93)
        assert_decode("sub h", 0x94)
        assert_decode("sub l", 0x95)
        assert_decode("sub a", 0x97)
        assert_decode("sub 254", 0xd6, 254)
        assert_decode("sub (hl)", 0x96)
        assert_decode("sub (ix+123)", 0xdd, 0x96, 123)
        assert_decode("sub (ix-4)", 0xdd, 0x96, 252)
        assert_decode("sub (iy+123)", 0xfd, 0x96, 123)
        assert_decode("sub (iy-123)", 0xfd, 0x96, 133)

    def test_cp(self) -> None:
        assert_decode("cp b", 0xb8)
        assert_decode("cp c", 0xb9)
        assert_decode("cp d", 0xba)
        assert_decode("cp e", 0xbb)
        assert_decode("cp h", 0xbc)
        assert_decode("cp l", 0xbd)
        assert_decode("cp a", 0xbf)
        assert_decode("cp 254", 0xfe, 254)
        assert_decode("cp (hl)", 0xbe)
        assert_decode("cp (ix+123)", 0xdd, 0xbe, 123)
        assert_decode("cp (ix-4)", 0xdd, 0xbe, 252)
        assert_decode("cp (iy+123)", 0xfd, 0xbe, 123)
        assert_decode("cp (iy-123)", 0xfd, 0xbe, 133)