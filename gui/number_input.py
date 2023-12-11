from typing import Tuple, Callable, Union, Optional

from pygame import Rect
from pygame.font import Font

from gui.components import Component, Collection, ALIGNMENT, UiHint, LeftRightLayout, BaseUIFactory

Number = Union[int, float]
GetterSetterPair = Tuple[Callable[[], Number], Callable[[Number], None]]


class NumberInputComponent(Collection):

    def __init__(self,
                 rect: Rect,
                 ui_factory: BaseUIFactory,
                 getter_setter_pair: GetterSetterPair,
                 name: str,
                 minimal_value: Optional[Number] = None, maximum_value: Optional[Number] = None,
                 button_font: Optional[Font] = None, value_font: Optional[Font] = None,
                 top_scale: int = 7, bottom_scale: int = 4):

        super().__init__(rect, layout=LeftRightLayout(margin=5))
        self.getter = getter_setter_pair[0]
        self.setter = getter_setter_pair[1]
        self.name = name
        self.minimal_value = minimal_value
        self.maximum_value = maximum_value
        self.button_font = button_font if button_font is not None else ui_factory.font
        self.value_font = value_font if value_font is not None else ui_factory.font
        self.height = 40 if rect is None or rect.height == 0 else rect.height

        self.widths = [self.button_font.size(w)[0] for w in ["<", "<<", ">>", ">"]]
        self.margin = 3

        self.top_scale = top_scale
        self.bottom_scale = bottom_scale
        self.scale = [1]
        p = 0.1
        for _ in range(1, bottom_scale):
            self.scale.insert(0, p)
            p /= 10.0

        p = 10.0
        for _ in range(1, top_scale):
            self.scale.append(p)
            p *= 10.0

        self.add_component(ui_factory.text_button(Rect(rect.x, rect.y, self.widths[0], self.height), "<", self.on_click_minus1, font=self.button_font, hint=UiHint.NO_DECORATION))
        self.add_component(ui_factory.text_button(Rect(rect.x + 34, rect.y, self.widths[1], self.height), "<<", self.on_click_minus01, font=self.button_font, hint=UiHint.NO_DECORATION))
        self.add_component(Component(Rect(0, 0, 5, self.height)))
        self.add_component(ui_factory.label(Rect(rect.x + 112, rect.y, 30, self.height), self.name, v_alignment=ALIGNMENT.MIDDLE, font=self.value_font))

        self.left = ui_factory.label(Rect(rect.x + 100, rect.y, 64, self.height), "", h_alignment=ALIGNMENT.RIGHT, v_alignment=ALIGNMENT.MIDDLE)
        self.right = ui_factory.label(Rect(rect.x + 164, rect.y, 30, self.height), "", h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.MIDDLE)
        self.add_component(self.left)
        self.add_component(self.right)

        self.add_component(ui_factory.text_button(Rect(rect.right - 30 - 34, rect.y, self.widths[2], self.height), ">>", self.on_click_plus01, font=self.button_font, hint=UiHint.NO_DECORATION))
        self.add_component(ui_factory.text_button(Rect(rect.right - 30, rect.y, self.widths[3], self.height), ">", self.on_click_plus1, font=self.button_font, hint=UiHint.NO_DECORATION))

    def redefine_rect(self, rect):
        super(NumberInputComponent, self).redefine_rect(rect)
        # self.rect = rect
        #
        # self.components[3].redefine_rect(Rect(rect.x, rect.y, self.widths[0], self.height))
        # self.components[4].redefine_rect(Rect(self.components[3].rect.right + self.margin, rect.y, self.widths[1], self.height))
        # self.components[5].redefine_rect(Rect(self.components[4].rect.right + self.margin, rect.y, self.widths[2], self.height))
        #
        # self.components[1].redefine_rect(Rect(self.components[5].rect.right + self.margin, rect.y, 64, self.height))
        # self.components[0].redefine_rect(Rect(rect.x + 112, rect.y, 30, self.height))
        # self.components[2].redefine_rect(Rect(rect.x + 164, rect.y, 30, self.height))
        #
        # self.components[6].redefine_rect(Rect(rect.right - 30 - 34 * 2, rect.y, self.widths[3], self.height))
        # self.components[7].redefine_rect(Rect(rect.right - 30 - 34, rect.y, self.widths[4], self.height))
        # self.components[8].redefine_rect(Rect(rect.right - 30, rect.y, self.widths[5], self.height))

    def draw(self, surface):
        value = self.getter()

        if value is not None:
            try:
                if abs(value > 0.1):
                    s = ("   {0:." + str(self.bottom_scale) + "f}").format(value)
                    # s = "{0:.2f}".format(value)
                    i = s.find('.')
                    i = i if i >= 0 else len(s)
                    left = s[0:i + 1]
                    right = s[i + 1:]
                    self.left.text = left
                    self.right.text = right
                    self.left.h_alignment = ALIGNMENT.RIGHT
                else:
                    self.left.text = ("   {0:." + str(self.bottom_scale) + "f}").format(value)
                    self.right.text = ""
                    self.left.h_alignment = ALIGNMENT.LEFT
            except TypeError:
                pass
                # print(f"Cannot handle value {value} it is not a number ({type(value)}")
        else:
            self.left.text = "-"
            self.right.text = ""

        super().draw(surface)

    def set_new_value(self, value) -> bool:
        if self.minimal_value is not None and value < self.minimal_value:
            return False
        if self.maximum_value is not None and value > self.maximum_value:
            return False

        self.setter(value)
        return True

    def on_click_plus1(self, *_args):
        value = self.getter()
        for i in range(1, len(self.scale)):
            if abs(value) < self.scale[i]:
                value += self.scale[i - 1]
                self.set_new_value(value)
                return

        value += self.scale[-1]
        self.set_new_value(value)

    def on_click_minus1(self, *_args):
        value = self.getter()
        for i in range(1, len(self.scale)):
            if abs(value) < self.scale[i]:
                value -= self.scale[i - 1]
                self.set_new_value(value)
                return

        value -= self.scale[-1]
        self.set_new_value(value)

    def on_click_plus01(self, *_args):
        value = self.getter()
        for i in range(2, len(self.scale)):
            if abs(value) < self.scale[i]:
                value += self.scale[i - 2]
                self.set_new_value(value)
                return
        value += self.scale[-2]
        self.set_new_value(value)

    def on_click_minus01(self, *_args):
        value = self.getter()
        for i in range(2, len(self.scale)):
            if abs(value) < self.scale[i]:
                value -= self.scale[i - 2]
                self.set_new_value(value)
                return
        value -= self.scale[-2]
        self.set_new_value(value)
