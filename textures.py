""" Textures and helper functions for textures """
from typing import Optional, Union
from functools import lru_cache
import pygame

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
    match hotspot.lower():
        case "top-left":
            hotspot = (0, 0)
        case "top-center":
            hotspot = (surface.get_width() // 2, 0)
        case "top-right":
            hotspot = (surface.get_width(), 0)
        case "left":
            hotspot = (0, surface.get_height() // 2)
        case "center":
            hotspot = (surface.get_width() // 2, surface.get_height() // 2)
        case "right":
            hotspot = (surface.get_width(), surface.get_height() // 2)
        case "bot-left":
            hotspot = (0, surface.get_height())
        case "bot-center":
            hotspot = (surface.get_width() // 2, surface.get_height())
        case "bot-right":
            hotspot = (surface.get_width(), surface.get_height())
        case _:
            raise ValueError(f"Invalid hotspot: {hotspot}")
    return hotspot

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
    hotspot = get_surface_hotspot(image)
    window.blit(image, (-hotspot.x, -hotspot.y))

class Textures: # create a texture manager? is it worth it?
    """ holds the textures used in the editor """

    button = load_image('textures/save-button.png', hotspot="center")
    button_selected = load_image('textures/save-button-selected.png', hotspot="center")
    background = load_image('textures/background.png')


# TODO: remove _circle_cache, also, try and understand how this code works
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

