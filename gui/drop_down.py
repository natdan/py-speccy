from functools import partial
from typing import Optional, Callable, List, Tuple

import pygame
from pygame import Rect

from gui.components import BaseUIFactory, Collection


class DropDown(Collection):
    def __init__(self,
                 rect: Optional[Rect],
                 ui_factory: BaseUIFactory,
                 select_method: Optional[Callable] = None,
                 update_activation_button_text: Optional[bool] = True,
                 text: Optional[str] = None,
                 menu_width: int = 200,
                 values: List[Tuple[str, str]] = None,
                 default_value: Optional[str] = None
                 ):
        super().__init__(rect)
        self.menu_width = menu_width

        if text is None and (values is None or len(values) == 0 or len(values[0]) < 2):
            raise ValueError("One of 'text' or 'values' must be populated")

        if text is None:
            text = values[0][1]

        self.select_method = select_method
        self.update_activation_button_text = update_activation_button_text
        self._values = values if values is not None else []

        self.menu = ui_factory.menu(Rect(0, 0, 150, 200), background_colour=pygame.color.THECOLORS['black'])
        self.menu.hide()

        if values is not None:
            for ident, text in values:
                self.menu.add_menu_item(text, callback=partial(self.select_value, ident))

        self.drop_down_activation_button = ui_factory.text_button(self.rect, text, on_click=self.start_drop_down)
        self.add_component(self.drop_down_activation_button)
        if default_value is not None:
            self.select_value(default_value)

    def draw(self, surface):
        super().draw(surface)
        if self.menu.visible:
            self.menu.draw(surface)

    def add_item(self, item_id, item_text):
        self.menu.add_menu_item(item_text, callback=partial(self.select_value, item_id))
        self._values.append((item_id, item_text))

    def start_drop_down(self, button, _=None):
        if self.menu.rect.x != button.rect.x or self.menu.rect.y != button.rect.y:
            self.menu.redefine_rect(Rect(button.rect.x, button.rect.bottom, self.menu_width, 1000))
        self.menu.show()

    def select_value(self, _id, _b=None, _p=None):
        self.menu.hide()
        if self.select_method is not None:
            self.select_method(_id)
        if self.update_activation_button_text:
            self.drop_down_activation_button.label.text = [v for v in self._values if v[0] == _id][0][1]
