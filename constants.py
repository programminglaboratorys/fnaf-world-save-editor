from typing import NoReturn
from game_state.errors import ExitGame
import pygame
ColorLike = any


FPS = 60
button_texture = pygame.image.load('save-button.png') # create a texture manager? is it worth it?
button_selected_texture = pygame.image.load('save-button-selected.png')

def exit_handler(event) -> NoReturn:
    """
    Handles exit events for the game.

    This function is responsible for handling events that signal the termination
    of the game. If the event type is `pygame.QUIT`, it raises an `ExitGame` 
    exception to facilitate a clean exit from the game loop.

    Args:
        event: The event object that contains information about the current event.

    Raises:
        ExitGame: If the event type is `pygame.QUIT`, indicating a request to quit the game.
    """
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        raise ExitGame()
