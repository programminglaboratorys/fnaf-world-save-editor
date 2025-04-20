"""
Constants used globally in the editor.
"""

import pygame
from game_state.errors import ExitGame

from states import State

ColorLike = any

FPS = 60
EDITOR_DEBUG = True
# 850x530
WINDOW_SIZE = (500, 530)
MAX_WINDOW_SIZE = (850, 530)
MIN_WINDOW_SIZE = (500, 530)


def global_event_handler(state: State, event):
    """
    global event handler, handles pygame.QUIT and pygame.VIDEORESIZE
    """
    if event.type == pygame.WINDOWFOCUSLOST:
        state.focused = False
    elif event.type == pygame.WINDOWFOCUSGAINED:
        state.focused = True
    elif (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_q
    ):
        raise ExitGame()
    elif event.type == pygame.VIDEORESIZE:
        width, height = event.size
        width = min(max(width, MIN_WINDOW_SIZE[0]), MAX_WINDOW_SIZE[0])
        height = min(max(height, MIN_WINDOW_SIZE[1]), MAX_WINDOW_SIZE[1])
        state.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
