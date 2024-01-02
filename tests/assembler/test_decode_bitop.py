from tests.assembler.memory import assert_decode


class TestDecodeBIT:
    def test_set(self) -> None:
        for b in range(8):
            assert_decode(f"set {b}, b", 0xcb, 0xc0 + b * 8)
            assert_decode(f"set {b}, c", 0xcb, 0xc1 + b * 8)
            assert_decode(f"set {b}, d", 0xcb, 0xc2 + b * 8)
            assert_decode(f"set {b}, e", 0xcb, 0xc3 + b * 8)
            assert_decode(f"set {b}, h", 0xcb, 0xc4 + b * 8)
            assert_decode(f"set {b}, l", 0xcb, 0xc5 + b * 8)
            assert_decode(f"set {b}, a", 0xcb, 0xc7 + b * 8)
            assert_decode(f"set {b}, (hl)", 0xcb, 0xc6 + b * 8)
            assert_decode(f"set {b}, (ix+123)", 0xdd, 0xcb, 123, 0xc6 + b * 8)
            assert_decode(f"set {b}, (ix-4)", 0xdd, 0xcb, 252, 0xc6 + b * 8)
            assert_decode(f"set {b}, (iy+123)", 0xfd, 0xcb, 123, 0xc6 + b * 8)
            assert_decode(f"set {b}, (iy-123)", 0xfd, 0xcb, 133, 0xc6 + b * 8)

    def test_res(self) -> None:
        for b in range(8):
            assert_decode(f"res {b}, b", 0xcb, 0x80 + b * 8)
            assert_decode(f"res {b}, c", 0xcb, 0x81 + b * 8)
            assert_decode(f"res {b}, d", 0xcb, 0x82 + b * 8)
            assert_decode(f"res {b}, e", 0xcb, 0x83 + b * 8)
            assert_decode(f"res {b}, h", 0xcb, 0x84 + b * 8)
            assert_decode(f"res {b}, l", 0xcb, 0x85 + b * 8)
            assert_decode(f"res {b}, a", 0xcb, 0x87 + b * 8)
            assert_decode(f"res {b}, (hl)", 0xcb, 0x86 + b * 8)
            assert_decode(f"res {b}, (ix+123)", 0xdd, 0xcb, 123, 0x86 + b * 8)
            assert_decode(f"res {b}, (ix-4)", 0xdd, 0xcb, 252, 0x86 + b * 8)
            assert_decode(f"res {b}, (iy+123)", 0xfd, 0xcb, 123, 0x86 + b * 8)
            assert_decode(f"res {b}, (iy-123)", 0xfd, 0xcb, 133, 0x86 + b * 8)

    def test_bit(self) -> None:
        for b in range(8):
            assert_decode(f"bit {b}, b", 0xcb, 0x40 + b * 8)
            assert_decode(f"bit {b}, c", 0xcb, 0x41 + b * 8)
            assert_decode(f"bit {b}, d", 0xcb, 0x42 + b * 8)
            assert_decode(f"bit {b}, e", 0xcb, 0x43 + b * 8)
            assert_decode(f"bit {b}, h", 0xcb, 0x44 + b * 8)
            assert_decode(f"bit {b}, l", 0xcb, 0x45 + b * 8)
            assert_decode(f"bit {b}, a", 0xcb, 0x47 + b * 8)
            assert_decode(f"bit {b}, (hl)", 0xcb, 0x46 + b * 8)
            assert_decode(f"bit {b}, (ix+123)", 0xdd, 0xcb, 123, 0x46 + b * 8)
            assert_decode(f"bit {b}, (ix-4)", 0xdd, 0xcb, 252, 0x46 + b * 8)
            assert_decode(f"bit {b}, (iy+123)", 0xfd, 0xcb, 123, 0x46 + b * 8)
            assert_decode(f"bit {b}, (iy-123)", 0xfd, 0xcb, 133, 0x46 + b * 8)
