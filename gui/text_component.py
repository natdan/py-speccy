from typing import Optional

from pygame import Rect

from gui.components import BaseUIFactory, TopDownLayout, Panel


class TextComponent(Panel):
    def __init__(self,
                 rect: Rect,
                 ui_factory: BaseUIFactory,
                 lines: list[str]) -> None:
        super().__init__(rect,
                         layout=TopDownLayout(stretch=False))
        self.ui_factory = ui_factory
        for line in lines:
            label = ui_factory.label(None, line)
            label.create_rect()
            self.add_component(label)

        self.redefine_rect(rect)
