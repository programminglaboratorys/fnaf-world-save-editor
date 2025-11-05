"""main functionality of the editor"""

# pylint: disable=all
# append the script directory to the path
import os

os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# pylint: enable=all

from threading import Thread

import pygame

# load states
from editor import Editor
from test import Test

#

from graphics import draw_background, render_text_with_outline
from states import MainEditorStateManager, State
from utils.constants import PLAYGROUND_MODE, EDITOR_DEBUG, FPS, WINDOW_SIZE, global_event_handler
from utils.helper import Counter
from utils.resources import Textures, FontBank


class SlotButton:
    """a simple button class."""

    image = Textures.button
    image_selected = Textures.button_selected

    def __init__(self, x: int, y: int, text: str = "", font_size=50):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size

    def get_texture(self, selected: bool):
        """get the texture of the button based on if the button is selected or not"""
        return self.image_selected if selected else self.image

    def change_pos(self, x: int, y: int):
        """change the position of the button"""
        self.x = x
        self.y = y

    def draw(self, window: pygame.Surface, selected: bool, text: str = ""):
        """draw the button"""
        texture: pygame.Surface = self.get_texture(selected)
        rect = texture.get_rect()
        rect.x, rect.y = self.x, self.y
        window.blit(texture, rect)
        text = text or self.text
        if text:
            font = pygame.font.Font(None, self.font_size)
            text_surface = render_text_with_outline(text, font, (255, 255, 255))
            text_rect = text_surface.get_rect(
                centerx=self.x + texture.get_width() // 2,
                centery=self.y + texture.get_height() // 2,
            )
            window.blit(text_surface, text_rect)


class MainMenu(State):
    """main menu select what save to edit"""

    update: bool = True
    buttons = [SlotButton(100, 100), SlotButton(100, 200), SlotButton(100, 300)]
    current_selection = Counter(0, 0, len(buttons) - 1)

    def draw_buttons(self):
        """Draws the buttons."""
        window = self.window
        for index, button in enumerate(self.buttons):
            is_selected = index == self.current_selection
            button.change_pos(
                window.get_rect().centerx
                - button.get_texture(is_selected).get_width() // 2,
                100 + index * 100,
            )
            button.draw(window, selected=is_selected, text=f"SLOT {index+1}")

    def load_and_jump(self, state="Editor"):

        # TODO: load in a thread and
        # create a loading frame, spinning fredbear animation?
        # sad animation when failure to load save file

        self.save.read(
            os.path.join(
                os.getenv("APPDATA"),
                "MMFApplications",
                f"fnafwr{self.globals.slot+1}",
            )
        )
        #print(list(self.save["fnafw"].keys()))
        self.jump_to_state(state)

    def on_setup(self):
        self.update = True
        #if PLAYGROUND_MODE:
        #    self.load_and_jump("Test")
        #if EDITOR_DEBUG:
        #    self.load_and_jump()
        
        return super().on_setup()
    def process_event(self, event: pygame.event.Event):
            if event.type == pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_DOWN:
                        self.current_selection += 1
                    case pygame.K_UP:
                        self.current_selection -= 1
                    case pygame.K_RETURN:
                        self.globals.slot = int(self.current_selection)
                        print(
                            "enter been pressed for button", self.current_selection
                        )
                        self.load_and_jump()
                self.update = True
            if event.type == pygame.VIDEORESIZE:
                self.update = True

    def process_update(self, deltatime) -> None:
        if not self.update:  # avoid using cpu/gpu power when not needed
            return
        draw_background(self.window, Textures.background)
        self.draw_buttons()
        self.update = False
        pygame.display.flip()



def main() -> None:
    """main function holds the main loop of the editor"""
    pygame.init()
    pygame.display.set_caption("FNaF World Save Editor")
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    # Create a basic 500x700 pixel window

    state_manager = MainEditorStateManager(screen)
    state_manager.load_states(MainMenu, Editor)
    lcd_font_size = 20

    state_manager.change_state("MainMenu")
    # Updates the current state to the desired state (screen) we want.
    clock = pygame.Clock()
    while state_manager.is_running:
       dt = clock.tick(FPS)

       for event in pygame.event.get():
             state_manager.current_state.process_event(event)
             global_event_handler(state_manager.current_state, event)

       state_manager.current_state.process_update(dt)

    print("Game has exited successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Game has been terminated")
