""" main functionality of the editor """
import pygame

from typing import Tuple
from game_state.errors import ExitGame, ExitState

from constants import Textures, global_event_handler, FPS, WINDOW_SIZE, get_surface_hotspot
from editor import Editor
from helper import Counter
from states import State, MainEditorStateManager


###

class SlotButton:
    """ A simple button class. """
    image = Textures.button # center (244, 60)
    image_selected = Textures.button_selected

    @classmethod
    def get_texture(cls, selected: bool):
        """ get the texture of the button based on if the button is selected or not """
        return cls.image_selected if selected else cls.image

    @classmethod
    def draw_button_center(cls, window, index: int, selected: bool):
        """ draw button in the center """
        texture = cls.get_texture(selected)
        hotspot = get_surface_hotspot(texture)
        rect = texture.get_rect()
        button_centerx = window.get_rect().centerx - hotspot.x
        button_centery = (window.get_rect().centery - 200) + 100 * index
        rect.x, rect.y = button_centerx, button_centery
        window.blit(texture, rect)

class MainMenu(State):
    """ main menu select what save to edit """
    buttons = [SlotButton, SlotButton, SlotButton]
    current_selection = Counter(0, 0, len(buttons)-1)

    def draw_buttons(self):
        """ Draws the buttons. """
        for index, button in enumerate(self.buttons):
            button.draw_button_center(self.window, index, index == self.current_selection)

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
                            self.manager.globals.slot = int(self.current_selection)
                            print("enter been pressed for button", self.current_selection)
                            self.jump_to_state("Editor")
                global_event_handler(self, event)
            self.window.fill((124, 240, 0))
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
