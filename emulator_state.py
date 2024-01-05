from enum import Enum


class EmulatorState(Enum):
    RUNNING = "RUNNING"
    ONE_FRAME = "ONE FRAME"
    STEPPING = "STEPPING"
    PAUSED = "PAUSED"
