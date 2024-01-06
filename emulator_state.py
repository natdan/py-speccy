from enum import Enum


class EmulatorState(Enum):
    RUNNING = "RUNNING"
    ONE_FRAME = "ONE FRAME"
    PROFILE = "PROFILE"
    STEPPING = "STEPPING"
    PAUSED = "PAUSED"
