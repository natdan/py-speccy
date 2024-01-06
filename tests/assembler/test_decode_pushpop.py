from tests.assembler.memory import assert_decode


class TestDecodePushPop:
    def test_push(self) -> None:
        assert_decode("push bc", 0xc5 + 0 * 16)
        assert_decode("push de", 0xc5 + 1 * 16)
        assert_decode("push hl", 0xc5 + 2 * 16)
        assert_decode("push af", 0xc5 + 3 * 16)
        assert_decode("push ix", 0xdd, 0xe5)
        assert_decode("push iy", 0xfd, 0xe5)

    def test_pop(self) -> None:
        assert_decode("pop bc", 0xc1 + 0 * 16)
        assert_decode("pop de", 0xc1 + 1 * 16)
        assert_decode("pop hl", 0xc1 + 2 * 16)
        assert_decode("pop af", 0xc1 + 3 * 16)
        assert_decode("pop ix", 0xdd, 0xe1)
        assert_decode("pop iy", 0xfd, 0xe1)
