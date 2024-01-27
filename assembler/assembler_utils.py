

def to_int(s: str, negative: bool = False) -> int:
    if s.endswith("h"):
        value = int(s[:-1], 16)
    elif s.startswith("0x"):
        value = int(s[2:], 16)
    else:
        value = int(s)

    if negative:
        value = - value

    return value
