"""
Constants used globally in the editor.
"""
from typing import NoReturn, Optional, Union
from game_state.errors import ExitGame
from states import State
import pygame
ColorLike = any

FPS = 60
WINDOW_SIZE = (500, 700)

class Texture(pygame.Surface):
    """ a texture with a hotspot """
    hotspot: tuple[int, int]
    def __init__(self, surface: pygame.Surface, hotspot: tuple[int, int] = (0, 0)):
        super().__init__(surface.get_size())
        self.blit(surface, (0, 0))
        self.hotspot = hotspot

def get_hotspot(surface: pygame.Surface, hotspot: str) -> tuple[int, int]:
    """
    Get the hotspot of a surface with given a string
    + + + + + + + + + + + + + + + + + + +
    + top-left | top-center | top-right +
    +     left | center     |     right +
    + bot-left | bot-center | bot-right +
    + + + + + + + + + + + + + + + + + + +
    """
    match hotspot:
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

def load_image(path: str, hotspot: Optional[Union[tuple[int, int], str]] = None) -> Texture:
    """
    Load an image with a hotspot
    """
    image = pygame.image.load(path)
    if hotspot is None:
        hotspot = (0, 0)
    if isinstance(hotspot, str):
        # pylint: disable=E1111
        hotspot = get_hotspot(image, hotspot)
    # else it is a tuple
    texture = Texture(image, hotspot)
    return texture

class Textures: # create a texture manager? is it worth it?
    """ holds the textures used in the editor """
    button = load_image('textures/save-button.png', hotspot="center") 
    button_selected = load_image('textures/save-button-selected.png', hotspot="center")
    background = load_image('textures/background.png')

def global_event_handler(state: State, event) -> NoReturn:
    """
    global event handler, handles pygame.QUIT and pygame.VIDEORESIZE
    """
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        raise ExitGame()

    if event.type == pygame.VIDEORESIZE:
        width, height = event.size
        default_width, default_height = WINDOW_SIZE
        if width < default_width or width > default_width:
            width = default_width
        if height < default_height or height > default_height:
            height = default_height
        state.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)