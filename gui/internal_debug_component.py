from pygame import Rect

from gui.components import BaseUIFactory, Collection
from utils.playback import Playback
from z80.z80_cpu import Z80CPU


class InternalDebugComponent(Collection):
    def __init__(self, rect: Rect, ui_factory: BaseUIFactory, playback: Playback) -> None:
        super().__init__(rect)
        self.playback = playback
        self.first_row_label = ui_factory.label(Rect(rect.x, rect.y, 0, 0), "")
        self.add_component(self.first_row_label)

    def draw(self, surface) -> None:
        self.first_row_label.text = (
            f"PB:{len(self.playback.backlog):06} "
            f"Top:{self.playback.top:06} "
        )
        super().draw(surface)
