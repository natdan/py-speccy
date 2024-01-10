class Memory:
    def __init__(self, *values) -> None:
        self.values = [v for v in values]

    def next_byte(self) -> int:
        byte = self.values[0]
        del self.values[0]
        return byte
