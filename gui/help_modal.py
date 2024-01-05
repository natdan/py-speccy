from typing import Optional, Callable

from pygame import Rect

from gui.components import BaseUIFactory, Panel, BaseLayout, Component, TopDownLayout, LeftRightLayout, ALIGNMENT, UiHint
from gui.text_component import TextComponent


class HelpModal(Panel):
    def __init__(self,
                 rect: Rect,
                 ui_factory: BaseUIFactory,
                 close_modal: Callable[[], None],
                 background_colour=None,
                 decoration: Optional[Component] = None,
                 layout: Optional[BaseLayout] = None,
                 horizontal_decoration_margin: int = 0,
                 vertical_decoration_margin: int = 0
                 ) -> None:
        super().__init__(rect,
                         layout=TopDownLayout(stretch=False) if layout is None else layout,
                         decoration=ui_factory.border(rect) if decoration is None else decoration,
                         background_colour=ui_factory.background_colour if background_colour is None else background_colour,
                         horizontal_decoration_margin=horizontal_decoration_margin,
                         vertical_decoration_margin=vertical_decoration_margin)
        self.ui_factory = ui_factory

        self.help_text = TextComponent(
            self.rect,
            self.ui_factory,
            [
                "ESC - Menu (not working)",
                "F1 - Help (this)",
                "F2 - Pause/Unpause",
                "LEFT/RIGHT - previous/next instruction",
                "SHIFT LEFT/RIGHT - previous/next 100 instructions",
                "ALT LEFT/RIGHT - previous/next frame",
                "CTRL RIGHT - run instruction per instruction",
            ],
        )
        self.help_text.vertical_decoration_margin=5
        self.help_text.horizontal_decoration_margin=5
        self.add_component(self.help_text)

        self.buttons_panel = Panel(
            Rect(0, 0, 100, 16), layout=LeftRightLayout(h_alignment=ALIGNMENT.RIGHT),
            horizontal_decoration_margin=3,
            vertical_decoration_margin=3
        )
        self.buttons_panel.add_component(self.ui_factory.button(
            Rect(0, 0, 50, 20), label=" OK", on_click=close_modal,
            hint=UiHint.LIGHT)
        )
        self.add_component(self.buttons_panel)

        self.redefine_rect(self.rect)

    def redefine_rect(self, rect) -> None:
        super().redefine_rect(rect)
        self.buttons_panel.redefine_rect(
            Rect(self.buttons_panel.rect.x, self.buttons_panel.rect.y,
                 self.help_text.rect.width, 32)
        )
