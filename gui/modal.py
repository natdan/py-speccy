from typing import Optional

from pygame import Rect

from gui.components import Component, Collection


class Modal(Collection):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.modal_component: Optional[Component] = None

    def show_modal(self, component: Component, update_rect: bool = True, center: bool = True) -> None:
        self.modal_component = component
        if center:
            size = component.calculate_size()
            left_margin = (self.rect.width - size[0]) // 2
            top_margin = (self.rect.height - size[1]) // 2
            self.modal_component.redefine_rect(Rect(left_margin, top_margin, size[0], size[1]))
        elif update_rect:
            self.modal_component.redefine_rect(self.rect)

    def hide_modal(self) -> None:
        self.modal_component = None

    def redefine_rect(self, rect) -> None:
        super().redefine_rect(rect)
        if self.modal_component is not None:
            self.modal_component.redefine_rect(rect)

    def mouse_over(self, mouse_pos) -> None:
        if self.modal_component:
            self.modal_component.mouse_over(mouse_pos)
        else:
            super().mouse_over(mouse_pos)

    def mouse_left(self, mouse_pos) -> None:
        if self.modal_component:
            self.modal_component.mouse_left(mouse_pos)
        else:
            super().mouse_over(mouse_pos)

    def mouse_down(self, mouse_pos) -> None:
        if self.modal_component:
            self.modal_component.mouse_down(mouse_pos)
        else:
            super().mouse_over(mouse_pos)

    def mouse_up(self, mouse_pos) -> None:
        if self.modal_component:
            self.modal_component.mouse_up(mouse_pos)
        else:
            super().mouse_over(mouse_pos)

    def draw(self, surface) -> None:
        super().draw(surface)
        if self.modal_component and self.visible:
            self.modal_component.draw(surface)
