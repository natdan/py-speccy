from assembler.assert_util import assert_decode


class TestDecodeADC:
    def test_adc(self) -> None:
        assert_decode("adc a, b", 0x88)
        assert_decode("adc a, c", 0x89)
        assert_decode("adc a, d", 0x8a)
        assert_decode("adc a, e", 0x8b)
        assert_decode("adc a, h", 0x8c)
        assert_decode("adc a, l", 0x8d)
        assert_decode("adc a, a", 0x8f)
        assert_decode("adc a, 254", 0xce, 254)
        assert_decode("adc a, (hl)", 0x8e)
        assert_decode("adc a, (ix+123)", 0xdd, 0x8e, 123)
        assert_decode("adc a, (ix-4)", 0xdd, 0x8e, 252)
        assert_decode("adc a, (iy+123)", 0xfd, 0x8e, 123)
        assert_decode("adc a, (iy-123)", 0xfd, 0x8e, 133)
        assert_decode("adc hl, bc", 0xed, 0x4a)
        assert_decode("adc hl, de", 0xed, 0x5a)
        assert_decode("adc hl, hl", 0xed, 0x6a)
        assert_decode("adc hl, sp", 0xed, 0x7a)
