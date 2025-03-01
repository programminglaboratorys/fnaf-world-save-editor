"""
Constants used globally in the editor.
"""
import pygame

from typing import Optional, Union
from game_state.errors import ExitGame
from states import State

ColorLike = any

FPS = 60
WINDOW_SIZE = (500, 700)
MAX_WINDOW_SIZE = (500, 700)
MIN_WINDOW_SIZE = (500, 700)

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

class Textures: # create a texture manager? is it worth it?
    """ holds the textures used in the editor """

    button = load_image('textures/save-button.png', hotspot="center")
    button_selected = load_image('textures/save-button-selected.png', hotspot="center")
    background = load_image('textures/background.png')

def global_event_handler(state: State, event):
    """
    global event handler, handles pygame.QUIT and pygame.VIDEORESIZE
    """
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        raise ExitGame()
    return
    if event.type == pygame.VIDEORESIZE:
        width, height = event.size
        default_width, default_height = WINDOW_SIZE
        if width < default_width or width > default_width:
            width = default_width
        if height < default_height or height > default_height:
            height = default_height
        state.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)