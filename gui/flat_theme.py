from typing import Optional

import pygame.color

from gui.components import Component, BaseUIFactory, Label, ALIGNMENT, UiHint, Button, Panel, BaseLayout, Menu, Image


class ButtonDecoration(Component):
    def __init__(self, colour):
        super(ButtonDecoration, self).__init__(None)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class BorderDecoration(Component):
    def __init__(self, colour):
        super(BorderDecoration, self).__init__(None)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, 1)


class FlatThemeFactory(BaseUIFactory):
    def __init__(self, ui_adapter, font=None, small_font=None, antialias=False,
                 colour=pygame.color.THECOLORS['cyan'],
                 warning_colour=pygame.color.THECOLORS['orange'],
                 error_colour=pygame.color.THECOLORS['red'],
                 disabled_colour=pygame.color.THECOLORS['darkblue'],
                 background_colour=pygame.color.THECOLORS['gray32'],
                 mouse_over_colour=pygame.color.THECOLORS['lightgray'],
                 mouse_over_background_colour=pygame.color.THECOLORS['gray32'],
                 warning_mouse_over_background_colour=pygame.color.THECOLORS['darkorange4'],
                 error_mouse_over_background_colour=pygame.color.THECOLORS['darkred']
                 ):
        super(FlatThemeFactory, self).__init__(ui_adapter,
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
                                               error_mouse_over_background_colour=error_mouse_over_background_colour)

    def setMouseOverColour(self, mouse_over_colour):
        self.mouse_over_colour = mouse_over_colour

    def setBackgroundColour(self, background_colour):
        self.background_colour = background_colour

    def label(self, rect, text, font=None, colour=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, antialias=self._antialias, colour=colour, h_alignment=h_alignment, v_alignment=v_alignment)

    def _disabled_label(self, rect, text, font=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, colour=self.disabled_colour, antialias=self._antialias, h_alignment=h_alignment, v_alignment=v_alignment)

    def image(self, rect, image, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Image(rect, image, h_alignment=h_alignment, v_alignment=v_alignment)

    def button(self, rect, on_click=None, on_hover=None, label=None, disabled_label=None, hint=UiHint.NORMAL):
        background_colour = self.background_colour
        mouse_over_colour = self.mouse_over_colour
        if hint == UiHint.WARNING:
            background_colour = pygame.color.THECOLORS['darkorange3']
            mouse_over_colour = pygame.color.THECOLORS['darkorange']
        elif hint == UiHint.ERROR:
            background_colour = pygame.color.THECOLORS['indianred4']
            mouse_over_colour = pygame.color.THECOLORS['indianred']
        if hint == UiHint.NO_DECORATION:
            return Button(rect, on_click, on_hover, label, disabled_label=disabled_label,
                          background_decoration=ButtonDecoration(background_colour),
                          mouse_over_decoration=ButtonDecoration(mouse_over_colour))
        else:
            return Button(rect, on_click, on_hover, label, disabled_label=disabled_label,
                          background_decoration=ButtonDecoration(background_colour),
                          mouse_over_decoration=ButtonDecoration(mouse_over_colour))

    def panel(self, rect, background_colour=None, layout: Optional[BaseLayout] = None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']
        return Panel(rect, background_colour, decoration=BorderDecoration(self.colour), layout=layout)

    def menu(self, rect, background_colour=None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']
        return Menu(rect, self, background_colour, decoration=BorderDecoration(self.colour))
