""" main functionality of the editor """
import pygame
pygame.init()

from typing import Tuple
from game_state.errors import ExitGame, ExitState

from constants import Textures, global_event_handler, FPS, WINDOW_SIZE, get_surface_hotspot
from editor import Editor
from helper import Counter, render_text_with_outline
from states import State, MainEditorStateManager


###

class SlotButton:
    """ A simple button class. """
    image = Textures.button
    image_selected = Textures.button_selected

    def __init__(self, x: int, y: int, text: str = "", font_size = 50):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size

    def get_texture(self, selected: bool):
        """ get the texture of the button based on if the button is selected or not """
        return self.image_selected if selected else self.image

    def change_pos(self, x: int, y: int):
        """ change the position of the button """
        self.x = x
        self.y = y

    def draw(self, window, selected: bool, text: str = ""):
        """ draw the button """
        texture = self.get_texture(selected)
        rect = texture.get_rect()
        rect.x, rect.y = self.x, self.y
        window.blit(texture, rect)
        text = text or self.text
        if text:
            font = pygame.font.Font(None, self.font_size)
            text_surface = render_text_with_outline(text, font, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=self.x + texture.get_width() // 2,
                                              centery=self.y + texture.get_height() // 2)
            window.blit(text_surface, text_rect)


def draw_background(window, image):
    hotspot = get_surface_hotspot(image)
    window.blit(image, (-hotspot.x, -hotspot.y))

class MainMenu(State):
    """ main menu select what save to edit """
    buttons = [SlotButton(100, 100), SlotButton(100, 200), SlotButton(100, 300)]
    current_selection = Counter(0, 0, len(buttons)-1)

    def draw_buttons(self):
        """ Draws the buttons. """
        window = self.window
        for index, button in enumerate(self.buttons):
            is_selected = index == self.current_selection
            button.change_pos(window.get_rect().centerx - button.get_texture(is_selected).get_width() // 2,
                               100 + index * 100)
            button.draw(window, selected=is_selected, text=f"SLOT {index+1}")

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match (event.key):
                        case pygame.K_DOWN:
                            self.current_selection += 1
                        case pygame.K_UP:
                            self.current_selection -= 1
                        case pygame.K_RETURN:
                            self.globals.slot = int(self.current_selection)
                            print("enter been pressed for button", self.current_selection)
                            self.jump_to_state("Editor")
                global_event_handler(self, event)
            draw_background(self.window, Textures.background)
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(FPS)


def main() -> None:
    """ main function holds the main loop of the editor """
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    # Create a basic 500x700 pixel window

    state_manager = MainEditorStateManager(screen)
    state_manager.load_states(MainMenu, Editor)

    state_manager.change_state("MainMenu")
    # Updates the current state to the desired state (screen) we want.

    while True:
        try:
            state_manager.run_state()
            # This is the entry point of our screen manager.
            # This should only be called once at start up.

        except ExitState as change:
            # Stuff you can do right after a state (screen) has been changed
            # i.e. Save player data, pause / resume / change music, etc...

            last_state = change.last_state
            current_state = state_manager.get_current_state()
            print(f"State has changed from: {last_state} to {current_state}")


if __name__ == "__main__":
    try:
        main()
    except ExitGame:
        print("Game has exited successfully")
    except KeyboardInterrupt:
        print("Game has been terminated")
