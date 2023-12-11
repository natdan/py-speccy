from typing import Optional

import pygame

from gui.components import Component, BaseUIFactory, Label, ALIGNMENT, UiHint, Image, Button, BaseLayout, Panel, Menu


class BackgroundChangeDecoration(Component):
    def __init__(self, colour):
        super().__init__(None)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class MenuButtonBackgroundDecoration(Component):
    def __init__(self, colour):
        super().__init__(None)  # Call super constructor to store rectangle
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class ButtonRectangleDecoration(Component):
    def __init__(self, colour, background_colour):
        super().__init__(None)  # Call super constructor to store rectangle
        self.colour = colour
        self.background_colour = background_colour
        self.strip_width = 5
        self.strip_margin = 3
        self.cut_width = 6
        self.cut_margin = 3
        self.cut_size = 15

    def draw(self, surface):
        if self.background_colour is not None:
            pygame.draw.rect(surface, self.background_colour, self.rect)

        x1 = self.rect.x
        x2 = self.rect.right - 1
        y1 = self.rect.y
        y2 = self.rect.bottom - 1
        pygame.draw.rect(surface, self.colour, pygame.Rect(x1, y1, self.strip_width, self.rect.height))
        pygame.draw.line(surface, self.colour, (x1 + self.strip_width + self.strip_margin, y1), (x2 - self.cut_size, y1))
        pygame.draw.line(surface, self.colour, (x2 - self.cut_size, y1), (x2, y1 + self.cut_size))
        pygame.draw.line(surface, self.colour, (x2, y1 + self.cut_size), (x2, y2))
        pygame.draw.line(surface, self.colour, (x2, y2), (x1 + self.strip_margin, y2))
        pygame.draw.line(surface, self.colour, (x1 + self.strip_width + self.strip_margin, y2), (x1 + self.strip_width + self.strip_margin, y1))

        pygame.draw.polygon(surface, self.colour, [
            (x2 - self.cut_size + self.cut_margin, y1),
            (x2 - self.cut_size + self.cut_margin + self.cut_width, y1),
            (x2, y1 + self.cut_size - self.cut_margin - self.cut_width),
            (x2, y1 + self.cut_size - self.cut_margin)
        ])


class BorderDecoration(Component):
    def __init__(self, rect, colour, background_colour=None,
                 horizontal_margin: int = 0,
                 vertical_margin: int = 0):
        super().__init__(rect)  # Call super constructor to store rectangle
        self.colour = colour
        self.background_colour = background_colour
        self.top_left_cut = 8
        self.bottom_right_cut = 5
        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

    def draw(self, surface):
        if self.background_colour is not None:
            pygame.draw.rect(surface, self.background_colour, self.rect)

        x1 = self.rect.x + self.horizontal_margin
        x2 = self.rect.right - 1 - self.horizontal_margin
        y1 = self.rect.y + self.vertical_margin
        y2 = self.rect.bottom - 1 - self.vertical_margin
        # x1 = self.rect.x
        # x2 = self.rect.right - 1
        # y1 = self.rect.y
        # y2 = self.rect.bottom - 1

        pygame.draw.polygon(surface, self.colour, [
            (x1 + self.top_left_cut, y1),
            (x2, y1),
            (x2, y2 - self.bottom_right_cut),
            (x2 - self.bottom_right_cut, y2),
            (x1, y2),
            (x1, y1 + self.top_left_cut)
        ], 1)


class BoxBlueSFThemeFactory(BaseUIFactory):
    def __init__(self, ui_adapter,
                 font=None,
                 small_font=None,
                 antialias=False,
                 colour=pygame.color.THECOLORS['cornflowerblue'],
                 warning_colour=pygame.color.THECOLORS['orange'],
                 error_colour=pygame.color.THECOLORS['red'],
                 disabled_colour=pygame.color.THECOLORS['gray'],
                 background_colour=(0, 0, 0, 255),
                 mouse_over_colour=pygame.color.THECOLORS['yellow'],
                 mouse_over_background_colour=pygame.color.THECOLORS['gray32'],
                 warning_mouse_over_background_colour=pygame.color.THECOLORS['darkorange4'],
                 error_mouse_over_background_colour=pygame.color.THECOLORS['darkred']):
        super().__init__(ui_adapter,
                         font=font,
                         small_font=small_font,
                         antialias=antialias,
                         colour=colour,
                         warning_colour=warning_colour,
                         error_colour=error_colour,
                         disabled_colour=disabled_colour,
                         background_colour=background_colour,
                         mouse_over_colour=mouse_over_colour,
                         mouse_over_background_colour=mouse_over_background_colour,
                         warning_mouse_over_background_colour=warning_mouse_over_background_colour,
                         error_mouse_over_background_colour=error_mouse_over_background_colour
                         )

    def setMouseOverColour(self, mouse_over_colour):
        self.mouse_over_colour = mouse_over_colour

    def setBackgroundColour(self, background_colour):
        self.background_colour = background_colour

    def label(self, rect, text, font=None, colour=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, antialias=self._antialias, colour=colour, h_alignment=h_alignment, v_alignment=v_alignment)

    def _disabled_label(self, rect, text, font=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, antialias=self._antialias, colour=self.disabled_colour, h_alignment=h_alignment, v_alignment=v_alignment)

    def image(self, rect, image, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Image(rect, image, h_alignment=h_alignment, v_alignment=v_alignment)

    def button(self, rect, on_click=None, on_hover=None,
               label=None, disabled_label=None, hint=UiHint.NORMAL):
        colour = self.colour
        background_colour = self.background_colour
        mouse_over_colour = self.mouse_over_colour
        mouse_over_background_colour = self.mouse_over_background_colour
        if hint == UiHint.WARNING:
            colour = self.warning_colour
            background_colour = self.background_colour
            mouse_over_colour = self.warning_colour
            mouse_over_background_colour = self.warning_mouse_over_background_colour
        elif hint == UiHint.ERROR:
            colour = self.error_colour
            background_colour = self.background_colour
            mouse_over_colour = self.error_colour
            mouse_over_background_colour = self.error_mouse_over_background_colour

        if hint == UiHint.NO_DECORATION:
            background_decoration = None
            mouse_over_decoration = BackgroundChangeDecoration(mouse_over_background_colour)
        elif hint == UiHint.LIGHT:
            background_decoration = BorderDecoration(None, colour, background_colour)
            mouse_over_decoration = BorderDecoration(None, mouse_over_colour, mouse_over_background_colour)
        else:
            background_decoration = ButtonRectangleDecoration(colour, background_colour)
            mouse_over_decoration = ButtonRectangleDecoration(mouse_over_colour, mouse_over_background_colour)

        if isinstance(label, str):
            label = self.label(rect, text=label)

        return Button(rect, on_click, on_hover, label, disabled_label=disabled_label,
                      background_decoration=background_decoration,
                      mouse_over_decoration=mouse_over_decoration)

    def panel(self, rect, background_colour=None, layout: Optional[BaseLayout] = None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']

        decoration = None if hint == UiHint.NO_DECORATION else BorderDecoration(rect, self.colour,)  # horizontal_margin=4, vertical_margin=4)
        inner_spacing = 0 if hint == UiHint.NO_DECORATION else 4
        return Panel(rect,
                     background_colour,
                     decoration=decoration,
                     layout=layout,
                     horizontal_decoration_margin=inner_spacing,
                     vertical_decoration_margin=inner_spacing)

    def menu(self, rect, background_colour=None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']
        return Menu(rect, self, background_colour, decoration=BorderDecoration(rect, self.colour))

    def _menu_item_text_button(self, rect, label, callback):
        return self._menu_item_button(rect, self.label(None, label, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE), callback)

    def _menu_item_button(self, rect, label, callback):
        return Button(rect, callback, label=label, mouse_over_decoration=MenuButtonBackgroundDecoration(self.mouse_over_background_colour))

    def border(self, rect, colour=pygame.color.THECOLORS['white']):
        return BorderDecoration(rect, colour)
