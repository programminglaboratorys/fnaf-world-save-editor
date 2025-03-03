""" Textures and helper functions for textures """
from typing import Optional, Union
from functools import lru_cache
from helper import subtract_vectors
import pygame
import glob
class TVector2(tuple):
    """ 2D vector """
    @property
    def x(self):
        """ x component of the vector """
        return self[0]

    @property
    def y(self):
        """ y component of the vector """
        return self[1]

    def __repr__(self):
        return f"TVector2(x={self.x}, y={self.y})"

_textures_hotspot_table: dict[pygame.Surface, TVector2] = {}

def get_hotspot_from_string(surface: pygame.Surface, hotspot: str) -> tuple[int, int]:
    """
    Get the hotspot of a surface with given a string
    + + + + + + + + + + + + + + + + + + +
    + top-left | top-center | top-right +
    +     left | center     |     right +
    + bot-left | bot-center | bot-right +
    + + + + + + + + + + + + + + + + + + +
    """
    rect = surface.get_rect()
    try:
        return getattr(rect, hotspot)
    except AttributeError:
        raise ValueError(f"Invalid hotspot: {hotspot}") from None

def load_image(path: str, hotspot: Optional[Union[tuple[int, int], str]] = None) -> pygame.Surface:
    """
    Load an image with a hotspot
    """
    image = pygame.image.load(path)
    if hotspot is None:
        hotspot = (0, 0)
    if isinstance(hotspot, str):
        hotspot = get_hotspot_from_string(image, hotspot)
    # else it is a tuple
    _textures_hotspot_table[image] = TVector2(hotspot)
    return image

def get_surface_hotspot(surface: pygame.Surface) -> Optional[TVector2]:
    """ get the hotspot of a surface """
    return _textures_hotspot_table.get(surface)

def draw_background(window, image):
    """
    Draws a background image with a hotspot.
    The image is placed such that the position is at (0, 0) in the window.
    """
    hotspot = get_surface_hotspot(image)
    window.blit(image, (-hotspot.x, -hotspot.y))

class Textures: # create a texture manager? is it worth it?
    """ holds the textures used in the editor """

    button = load_image('textures/save-button.png', hotspot="center")
    button_selected = load_image('textures/save-button-selected.png', hotspot="center")
    freddy = load_image('textures/characters/freddy.png', hotspot=(125, 220))
    background = load_image('textures/background.png')


@lru_cache
def _circlepoints(r):
    x, y, e = r, 0, 1 - r
    points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render_text_with_outline(text: str, font: pygame.Font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=2):
    """
    Render text with an outline
    """
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(int(round(opx))):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf
