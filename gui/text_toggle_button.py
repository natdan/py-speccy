from typing import Tuple, Callable

from pygame import Rect

from gui.components import CardsCollection, Button, BaseUIFactory, UiHint


class TextToggleButton(CardsCollection):
    def __init__(self, rect: Rect,
                 ui_factory: BaseUIFactory,
                 on_text: str, on_click_on: Callable[[Button, Tuple[int, int]], None],
                 off_text: str, on_click_off: Callable[[Button, Tuple[int, int]], None],
                 auto_toggle: bool = False,
                 hint: UiHint = UiHint.NORMAL):
        super().__init__(
            rect,
            [
                ("on", ui_factory.text_button(rect, on_text, on_click=self.callback_on, hint=hint)),
                ("off", ui_factory.text_button(rect, off_text, on_click=self.callback_off, hint=hint))
            ])
        self.on_click_on = on_click_on
        self.on_click_off = on_click_off
        self.auto_toggle = auto_toggle
        self.select_card("on")

    def callback_on(self, *_args) -> None:
        if self.auto_toggle:
            self.toggle_off()
        self.on_click_on(*_args)

    def callback_off(self, *_args) -> None:
        if self.auto_toggle:
            self.toggle_on()
        self.on_click_off(*_args)

    def is_toggle_on(self) -> bool:
        return self.selected_card_name == "on"

    def toggle_on(self) -> None:
        self.select_card("on")

    def toggle_off(self) -> None:
        self.select_card("off")

    def toggle(self, toggle: bool) -> None:
        if toggle:
            self.toggle_on()
        else:
            self.toggle_off()
