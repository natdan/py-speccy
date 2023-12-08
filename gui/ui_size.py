from typing import Union


class UISize(tuple):
    def __new__(self, width, height):
        return tuple.__new__(UISize, (width, height))

    def __init__(self, *args, **kwargs) -> None:
        self.width = 0
        self.height = 0

        if len(args) == 2:
            self.width = args[0]
            self.height = args[1]
        elif len(args) == 1:
            self.width = args[0][0]
            self.height = args[0][1]

        if "width" in kwargs:
            self.width = kwargs["width"]
        if "height" in kwargs:
            self.height = kwargs["height"]

    def __getitem__(self, item: int) -> Union[int, float]:
        if item == 0:
            return self.width
        elif item == 1:
            return self.height

        raise KeyError(item)

    def __setitem__(self, key: int, value: Union[int, float]):
        if key == 0:
            self.width = value
        elif key == 1:
            self.height = value
        raise KeyError(key)

    def __iter__(self) -> Union[int, float]:
        yield self.width
        yield self.height

    def __add__(self, other) -> 'UISize':
        return UISize(self.width + other[0], self.height + other[1])

    def __sub__(self, other) -> 'UISize':
        return UISize(self.width - other[0], self.height - other[1])

    def __repr__(self) -> str:
        return f"({self.width}, {self.height})"
