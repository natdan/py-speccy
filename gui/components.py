from enum import Enum, auto
from typing import Tuple, List, Optional

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from gui.ui_size import UISize


class ALIGNMENT(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


class Component:
    def __init__(self, rect: Optional[Rect]):
        self.rect: Optional[Rect] = rect
        self.mouse_is_over = False
        self.font: Optional[Font] = None
        self._visible = True

    def _font(self) -> Optional[Font]:
        if self.font is None:
            self.font = pygame.font.SysFont('Arial', 30)
        return self.font

    @property
    def visible(self) -> bool: return self._visible

    @visible.setter
    def visible(self, visible: bool): self._visible = visible

    def draw(self, surface) -> None:
        pass

    def calculate_size(self) -> UISize:
        return UISize(self.rect.width, self.rect.height)

    def redefine_rect(self, rect: Rect) -> None:
        self.rect = rect

    def mouse_over(self, mouse_pos: Tuple[int, int]) -> None:
        self.mouse_is_over = True

    def mouse_left(self, mouse_pos: Tuple[int, int]) -> None:
        self.mouse_is_over = False

    def mouse_down(self, mouse_pos: Tuple[int, int]) -> None:
        pass

    def mouse_up(self, mouse_pos: Tuple[int, int]) -> None:
        pass

    def size(self) -> Tuple[int, int]:
        return self.rect.width, self.rect.height

    def key_down(self, code: str) -> bool:
        return False

    def key_up(self, code: str) -> bool:
        return False


class BaseLayout:
    def __init__(self) -> None:
        pass

    def arrange(self, rect: Rect, components: List[Component]):
        for component in components:
            component.redefine_rect(rect)


class TopDownLayout(BaseLayout):
    def __init__(self, margin: int = 0, stretch: bool = False):
        super().__init__()
        self.margin = margin
        self.stretch = stretch

    def arrange(self, rect: Rect, components: List[Component]) -> None:
        y = rect.y
        for component in components:
            component_size = component.calculate_size()
            height = component_size.height
            # if component.rect is not None and component.rect.height != 0:
            #     height = component.rect.height
            # else:
            #     height = (rect.height - self.margin * (len(components) - 1)) // len(components)
            component.redefine_rect(Rect(rect.x, y, rect.width if self.stretch else component_size.width, height))
            y += self.margin + component.rect.height


class LeftRightLayout(BaseLayout):
    def __init__(self, margin: int = 0, h_alignment: ALIGNMENT = ALIGNMENT.LEFT):
        super().__init__()
        self.margin = margin
        self.h_alignment = h_alignment

    def arrange(self, rect: Rect, components: List[Component]) -> None:
        filled_in_space = False
        x = rect.x
        for component in components:
            if component.rect is not None and component.rect.width != 0:
                width = component.rect.width
            else:
                width = rect.width - self.margin * (len(components) - 1)
                filled_in_space = True
            component.redefine_rect(Rect(x, rect.y, width, rect.height))
            x += self.margin + width
        if not filled_in_space and self.h_alignment != ALIGNMENT.LEFT:
            offset = 0
            if self.h_alignment == ALIGNMENT.RIGHT:
                offset = rect.width - (x - rect.x) - 1
            elif self.h_alignment == ALIGNMENT.CENTER:
                offset = (rect.width - (x - rect.x) - 1) // 2
            for component in components:
                if component.rect is not None:
                    component.rect.x = component.rect.x + offset


class Collection(Component):
    def __init__(self, rect, layout: Optional[BaseLayout] = None, components: List[Component] = ()):
        super().__init__(rect)  # Call super constructor to store rectable
        self.components: List[Component] = []
        self.layout = layout
        self._selected_component: Optional[Component] = None
        for component in components:
            self.add_component(component)

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def remove_component(self, component: Component) -> None:
        i = self.components.index(component)
        if i > 0:
            del self.components[i]

    def draw(self, surface) -> None:
        for component in self.components:
            if component.visible:
                component.draw(surface)

    def calculate_size(self) -> UISize:
        if self.layout:
            self.layout.arrange(self.rect, self.components)

        max_width = 0
        max_height = 0

        for component in self.components:
            component_rect = component.rect
            if component_rect.right > max_width: max_width = component_rect.right
            if component_rect.bottom > max_height: max_height = component_rect.bottom

        return UISize(max_width - self.rect.x, max_height - self.rect.y)

    def find_component(self, pos) -> Optional[Component]:
        for component in reversed(self.components):
            rect = component.rect
            if component.visible and rect is not None and rect.collidepoint(pos):
                return component
        return None

    def redefine_rect(self, rect) -> None:
        self.rect = rect
        if self.layout is not None:
            self.layout.arrange(rect, self.components)
        else:
            for component in self.components:
                component.redefine_rect(rect)

    def mouse_over(self, mouse_pos) -> None:
        self.mouse_is_over = True
        component = self.find_component(mouse_pos)
        if component != self._selected_component and self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)
        if component is not None:
            component.mouse_over(mouse_pos)
            self._selected_component = component

    def mouse_left(self, mouse_pos) -> None:
        self.mouse_is_over = False
        if self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)

    def mouse_down(self, mouse_pos) -> None:
        component = self.find_component(mouse_pos)
        if component != self._selected_component and self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)
        if component is not None:
            component.mouse_down(mouse_pos)
            self._selected_component = component

    def mouse_up(self, mouse_pos) -> None:
        if self._selected_component is not None:
            self._selected_component.mouse_up(mouse_pos)
            if not self._selected_component.rect.collidepoint(mouse_pos):
                # we released button outside of component - it would be nice to let it know mouse is not inside of it any more
                self._selected_component.mouse_left(mouse_pos)
        component = self.find_component(mouse_pos)
        if component is not None:
            # we released mouse over some other component - now it is turn for it to receive mouse over
            component.mouse_over(mouse_pos)


class Panel(Collection):
    def __init__(self, rect: Rect,
                 background_colour=None,
                 decoration: Optional[Component] = None,
                 layout: Optional[BaseLayout] = None,
                 horizontal_decoration_margin: int = 0,
                 vertical_decoration_margin: int = 0):
        super().__init__(rect, layout=layout)
        self.bacground_colour = background_colour
        self.decoration = decoration
        self.horizontal_decoration_margin = horizontal_decoration_margin
        self.vertical_decoration_margin = vertical_decoration_margin

    def redefine_rect(self, rect):
        super().redefine_rect(Rect(rect.left + self.horizontal_decoration_margin,
                                   rect.top + self.vertical_decoration_margin,
                                   rect.width - self.horizontal_decoration_margin * 2,
                                   rect.height - self.vertical_decoration_margin * 2))
        self.rect = rect
        if self.decoration is not None:
            self.decoration.redefine_rect(rect)

    def draw(self, surface):
        if self.bacground_colour is not None:
            pygame.draw.rect(surface, self.bacground_colour, self.rect)
        if self.decoration is not None:
            self.decoration.draw(surface)
        super().draw(surface)

    def calculate_size(self) -> UISize:
        width, height = super().calculate_size()

        return UISize(width + self.horizontal_decoration_margin * 2, height + self.vertical_decoration_margin * 2)


class Menu(Panel):
    def __init__(self, rect, ui_factory, background_colour=None, decoration=None):
        super(Menu, self).__init__(ui_factory.ui_adapter.screen.get_rect())
        self.draw_rect = rect
        self.ui_factory = ui_factory
        self.bacground_colour = background_colour
        self.decoration = decoration
        self.menu_items = []
        self.visible = False
        self._key_selected = -1

    def redefine_rect(self, rect):
        self.draw_rect = rect
        self.rect = self.ui_factory.ui_adapter.screen.get_rect()
        self.calculate_rect_size()
        if self.decoration is not None:
            self.decoration.redefine_rect(self.draw_rect)

    def draw(self, surface):
        if self.bacground_colour is not None:
            pygame.draw.rect(surface, self.bacground_colour, self.draw_rect)
        if self._key_selected >= 0:
            for i in range(len(self.menu_items)):
                item = self.menu_items[i]

                item.mouse_is_over = i == self._key_selected

        super(Panel, self).draw(surface)
        if self.decoration is not None:
            self.decoration.draw(surface)

    def mouse_down(self, mouse_pos):
        if not self.draw_rect.collidepoint(mouse_pos):
            self.hide()
        else:
            super(Menu, self).mouse_over(mouse_pos)

    def show(self):
        self.visible = True
        self._clean_key_selected()

    def hide(self):
        self.visible = False
        self._clean_key_selected()

    def size(self):
        return self.draw_rect.width, self.draw_rect.height

    def _clean_key_selected(self):
        for item in self.menu_items:
            item.mouse_is_over = False

    def calculate_rect_size(self):
        max_x = 0
        y = 5
        for item in self.menu_items:
            item.redefine_rect(Rect(self.draw_rect.x, y + self.draw_rect.y, self.draw_rect.width, item.rect.height))
            y += item.rect.height
            max_x = item.rect.width if item.rect.width > max_x else max_x
        y += 5
        max_x += 10
        self.draw_rect.height = y
        self.draw_rect.width = max_x

    def add_menu_item(self, label, callback=None, height=30):
        component = self.ui_factory.menu_item(Rect(0, 0, 0, height), label, callback)
        self.menu_items.append(component)
        self.add_component(component)
        self.calculate_rect_size()

    def clear_menu_items(self):
        del self.menu_items[:]
        del self.components[:]
        self._key_selected = -1

    def key_down(self, code):
        if len(self.menu_items) > 0:
            if code == pygame.K_UP:
                if self._key_selected <= 0:
                    self._key_selected = len(self.menu_items) - 1
                else:
                    self._key_selected -= 1
                return True

            if code == pygame.K_DOWN:
                self._key_selected += 1
                if self._key_selected >= len(self.menu_items):
                    self._key_selected = 0
                return True

            if code == pygame.K_RETURN or code == pygame.K_KP_ENTER or code == pygame.K_SPACE:
                item = self.menu_items[self._key_selected]
                if isinstance(item, Button):
                    item.on_click(item, None)
                return True

        return False

    def key_up(self, code):
        return False


class CardsCollection(Collection):
    def __init__(self, rect, initial_cards: List[Tuple[str, Component]] = ()):
        super(CardsCollection, self).__init__(rect)
        self.cards = {}
        self.selected_card_name = None
        self.selected_card_component = None

        for name, component in initial_cards:
            self.add_card(name, component)

    def add_card(self, name, component) -> None:
        self.cards[name] = component
        component._visible = False
        super(CardsCollection, self).add_component(component)

    def card_component(self, name) -> Optional[Component]:
        return self.cards[name]

    def select_card(self, name) -> None:
        if name in self.cards:
            if self.selected_card_component is not None:
                self.selected_card_component.visible = False
            self.selected_card_component = self.cards[name]
            self.selected_card_component.visible = True
            self.selected_card_name = name
            return self.selected_card_component
        return None

    def selected_card_name(self):
        return self.selected_card_name

    def mouse_over(self, mouse_pos):
        self.selected_card_component.mouse_over(mouse_pos)

    def mouse_left(self, mouse_pos):
        self.selected_card_component.mouse_left(mouse_pos)

    def mouse_down(self, mouse_pos):
        self.selected_card_component.mouse_down(mouse_pos)

    def mouse_up(self, mouse_pos):
        self.selected_card_component.mouse_up(mouse_pos)

    def key_down(self, code: str) -> bool:
        return self.selected_card_component.key_down(code)

    def key_up(self, code: str) -> bool:
        return self.selected_card_component.key_up(code)


class Image(Component):
    def __init__(self, rect, surface, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP):
        super(Image, self).__init__(rect)  # Call super constructor to store rectable
        self._surface = surface
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment

    def getImage(self):
        return self._surface

    def setImage(self, surface):
        self._surface = surface

    def draw(self, surface):
        if self._surface is not None:
            x = self.rect.x
            y = self.rect.y

            if self.h_alignment == ALIGNMENT.CENTER:
                x = self.rect.centerx - self._surface.get_width() // 2
            elif self.h_alignment == ALIGNMENT.RIGHT:
                x = self.rect.right - self._surface.get_width()

            if self.v_alignment == ALIGNMENT.MIDDLE:
                y = self.rect.centery - self._surface.get_height() // 2
            elif self.v_alignment == ALIGNMENT.BOTTOM:
                y = self.rect.bottom - self._surface.get_height()

            surface.blit(self._surface, (x, y))


class Label(Image):
    def __init__(self,
                 rect: Rect,
                 text: str,
                 colour=None,
                 background_colour=None,
                 font=None,
                 antialias=True,
                 h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP):
        super(Label, self).__init__(rect, None, h_alignment, v_alignment)  # Call super constructor to store rectable
        self._text = text
        self.font = font
        self._colour = colour if colour is not None else pygame.color.THECOLORS['white']
        self._background_colour = background_colour
        self.antialias = antialias

    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        if self._text != text:
            self._text = text
            self.invalidate_surface()

    @property
    def colour(self): return self._colour

    @colour.setter
    def colour(self, colour) -> None:
        self._colour = colour
        self.invalidate_surface()

    @property
    def background_colour(self): return self._background_colour

    @background_colour.setter
    def background_colour(self, background_colour) -> None:
        self._background_colour = background_colour
        self.invalidate_surface()

    def invalidate_surface(self) -> None:
        self._surface: Optional[Surface] = None

    def create_rect(self) -> None:
        if self._surface is None:
            self.create_surface()
        surface_size = self.calculate_size()
        self.rect = Rect(0, 0, surface_size[0], surface_size[1])

    def calculate_size(self) -> UISize:
        if self._surface is None:
            self.create_surface()
        surface_size = self._surface.get_size()
        return UISize(surface_size[0], surface_size[1])

    def create_surface(self) -> Surface:
        if self._surface is None:
            self._surface = self._font().render(self._text, self.antialias, self.colour)
            if self._background_colour:
                new_surface = Surface(self._surface.get_size())
                new_surface.fill(self._background_colour)
                new_surface.blit(self._surface, (0, 0))
                self._surface = new_surface
        return self._surface

    def draw(self, surface):
        if self._surface is None:
            self.create_surface()

        super(Label, self).draw(surface)


class Button(Component):
    def __init__(self,
                 rect,
                 on_click=None,
                 on_hover=None,
                 label=None,
                 disabled_label=None,
                 background_decoration=None,
                 mouse_over_decoration=None):
        super(Button, self).__init__(rect)  # Call super constructor to store rectable
        self.on_click = on_click
        self.on_hover = on_hover
        self._label = label
        self._disabled_label = disabled_label
        self.background_decoration = background_decoration
        self.mouse_over_decoration = mouse_over_decoration
        self.redefine_rect(rect)
        self._enabled = True

    @property
    def label(self) -> Component: return self._label

    @label.setter
    def label(self, label: Component):
        self._label = label
        self._label.redefine_rect(self.rect)

    @property
    def disabled_label(self) -> Component: return self._disabled_label

    @disabled_label.setter
    def disabled_label(self, label: Component):
        self._disabled_label = label
        self._disabled_label.redefine_rect(self.rect)

    def redefine_rect(self, rect):
        super(Button, self).redefine_rect(rect)
        if self._label is not None:
            self._label.redefine_rect(rect)  # set label's position to buttons
        if self._disabled_label is not None:
            self._disabled_label.redefine_rect(rect)  # set label's position to buttons
        if self.background_decoration is not None:
            self.background_decoration.redefine_rect(rect)
        if self.mouse_over_decoration is not None:
            self.mouse_over_decoration.redefine_rect(rect)

    def draw(self, surface):
        if self.mouse_is_over and self._enabled:
            if self.mouse_over_decoration is not None:
                self.mouse_over_decoration.draw(surface)
        else:
            if self.background_decoration is not None:
                self.background_decoration.draw(surface)

        if not self._enabled and self._disabled_label is not None:
            self._disabled_label.draw(surface)
        elif self._label is not None:  # this way 'label' can be anything - text, image or something custom drawn
            self._label.draw(surface)

    def mouse_up(self, mouse_pos):
        if self._enabled and self.rect.collidepoint(mouse_pos) and self.on_click is not None:
            self.on_click(self, mouse_pos)

    @property
    def enabled(self) -> bool: return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool): self._enabled = enabled


class UIAdapter:
    def __init__(self, screen=None, screen_size=None, freq: int = 30, do_init: bool = True):
        self._screen = screen
        self.screen_size = None if screen_size is None else screen_size
        self._top_component = None
        self.mouse_is_down = False
        self.freq = freq
        self.frameclock = pygame.time.Clock()
        if self.screen is None and do_init:
            self.init()

    def init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.screen_size)

    @property
    def screen(self): return self._screen

    @property
    def top_component(self) -> Component: return self._top_component

    @top_component.setter
    def top_component(self, top_component): self._top_component = top_component

    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_moved(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_down(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_up(mouse_pos)

    def mouse_moved(self, mouse_pos):
        if self.top_component is not None:
            self.top_component.mouse_over(mouse_pos)

    def mouse_down(self, mouse_pos):
        self.mouse_is_down = True
        if self.top_component is not None:
            self.top_component.mouse_down(mouse_pos)

    def mouse_up(self, mouse_pos):
        self.mouse_is_down = False
        if self.top_component is not None:
            self.top_component.mouse_up(mouse_pos)

    def draw(self, surface):
        if self.top_component is not None:
            self.top_component.draw(surface)

    def frame_end(self):
        pygame.display.flip()
        self.frameclock.tick(self.freq)


class UiHint(Enum):
    NO_DECORATION = auto()
    LIGHT = auto()
    NORMAL = auto()
    WARNING = auto()
    ERROR = auto()


class BorderDecoration(Component):
    def __init__(self, rect, colour):
        super(BorderDecoration, self).__init__(rect)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, 1)


class BaseUIFactory:
    def __init__(self, ui_adapter, font=None, small_font=None, antialias=False,
                 colour=None, warning_colour=None, error_colour=None,
                 disabled_colour=None, background_colour=None,
                 mouse_over_colour=None,
                 mouse_over_background_colour=None,
                 warning_mouse_over_background_colour=None,
                 error_mouse_over_background_colour=None):
        self._ui_adapter = ui_adapter
        self._font = font if font is not None else pygame.font.SysFont('Arial', 14)
        self._small_font = small_font if small_font is not None else pygame.font.SysFont('Arial', 9)
        self._antialias = antialias
        self.colour = colour if colour is not None else pygame.color.THECOLORS['white']
        self.warning_colour = warning_colour if warning_colour else pygame.color.THECOLORS['orange']
        self.error_colour = error_colour if error_colour else pygame.color.THECOLORS['red']
        self.disabled_colour = disabled_colour if disabled_colour is not None else pygame.color.THECOLORS['gray']
        self.background_colour = background_colour if background_colour is not None else pygame.color.THECOLORS['black']
        self.mouse_over_colour = mouse_over_colour
        self.mouse_over_background_colour = mouse_over_background_colour if mouse_over_background_colour else pygame.color.THECOLORS['gray32']
        self.warning_mouse_over_background_colour = warning_mouse_over_background_colour if warning_mouse_over_background_colour else pygame.color.THECOLORS['darkorange4'],
        self.error_mouse_over_background_colour = error_mouse_over_background_colour if error_mouse_over_background_colour else pygame.color.THECOLORS['darkred']

    @property
    def ui_adapter(self) -> UIAdapter: return self._ui_adapter

    @property
    def font(self) -> Font: return self._font

    @property
    def small_font(self) -> Font: return self._small_font

    def label(self, rect, text, font=None, colour=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL) -> Label:
        # noinspection PyTypeChecker
        return None

    def _disabled_label(self, rect, text, font=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL) -> Label:
        # noinspection PyTypeChecker
        return None

    def image(self, rect, image, hint=UiHint.NORMAL) -> Image:
        # noinspection PyTypeChecker
        return None

    def button(self, rect, on_click=None, on_hover=None,
               label=None,
               disabled_label=None,
               hint=UiHint.NORMAL) -> Button:
        # noinspection PyTypeChecker
        return None

    def text_button(self, rect, text, on_click=None, on_hover=None, hint=UiHint.NORMAL, font=None) -> Button:
        return self.button(rect, on_click, on_hover,
                           self.label(None, text, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE, font=font),
                           disabled_label=self._disabled_label(None, text, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE, font=font),
                           hint=hint)

    def panel(self, rect, background_colour=None, layout: Optional[BaseLayout] = None, hint=UiHint.NORMAL) -> Panel:
        # noinspection PyTypeChecker
        return None

    def menu(self, rect, background_colour=None, hint=UiHint.NORMAL) -> Menu:
        # noinspection PyTypeChecker
        return None

    def _menu_item_text_button(self, rect, label, callback) -> Button:
        return self._menu_item_button(self, rect, self.label(None, label, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE))

    def _menu_item_button(self, rect, label, callback) -> Button:
        return Button(rect, callback, label=label)

    def menu_item(self, rect, label, callback) -> Component:
        if isinstance(label, str):
            component = self._menu_item_text_button(rect, label, callback)
        elif isinstance(label, Label):
            component = self._menu_item_button(rect, label, callback)
        else:
            component = label

        return component

    def border(self, rect, colour=pygame.color.THECOLORS['white']) -> BorderDecoration:
        return BorderDecoration(rect, colour)
