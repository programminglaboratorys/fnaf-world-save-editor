"""a module for resources like fonts and images"""

# pylint: disable=too-few-public-methods
import pygame

from graphics.textures import load_image

from .helper import instantiate

CHARACTER_TEXTURES_PATH = "textures/characters/"
Surface = pygame.Surface


class LazyAttributes:
    """
    A class that loads attributes lazily when they are accessed
    """

    _loaded_attributes = {}

    def __getattribute__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        attr = super().__getattribute__(name)
        if callable(attr):
            # print("attribute", name, "value", attr, flush=True)
            if name not in self._loaded_attributes:
                self._loaded_attributes[name] = attr()
            return self._loaded_attributes[name]
        return attr


@instantiate()
class FontBank(LazyAttributes):
    """A class that loads fonts lazily when they are accessed"""

    arialnb_font: pygame.font.Font = lambda _: pygame.font.Font(
        "textures/fonts/ARIALNB.TTF", 30
    )
    lcd_font: pygame.font.Font = lambda _: pygame.font.Font(
        "textures/fonts/LcdSolid.ttf", 20
    )


# pylint: disable=unnecessary-lambda-assignment
@instantiate()
class Textures(LazyAttributes):
    """holds the textures used in the editor"""

    button: Surface = lambda _: load_image("textures/save-button.png", hotspot="center")
    button_selected: Surface = lambda _: load_image(
        "textures/save-button-selected.png", hotspot="center"
    )
    # TODO: make a default texture for characters
    freddy: Surface = lambda _: load_image(
        "textures/characters/freddy.png", hotspot=(125, 220)
    )
    background: Surface = lambda _: load_image("textures/background.png", convert=True)
