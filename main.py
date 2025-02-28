from constants import button_selected_texture, button_texture, exit_handler, FPS
from helper import Counter

from typing import Tuple
from game_state.errors import ExitGame, ExitState
from game_state import StateManager, State

import pygame

###

class Button:
    """ A simple button class. """
    image = button_texture
    image_selected = button_selected_texture
    def __init__(self, pos: Tuple[int, int]):
        self.x, self.y = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
    
    def draw(self, window, *, selected: bool = False):
        """ draw button """
        if selected:
            window.blit(self.image_selected, self.rect)
            return
        window.blit(self.image, self.rect)

class MainMenu(State):
    """ main menu select what save to edit """
    current_selection = Counter(0, 0, 2)
    buttons = [ Button((5, 100)),
                Button((5, 200)),
                Button((5, 300))]

    def draw_buttons(self):
        """ Draws the buttons. """
        for index, button in enumerate(self.buttons):
            button.draw(self.window, selected=index == self.current_selection)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match (event.key):
                        case pygame.K_c:
                            self.manager.change_state(
                            "Editor"
                            )  # Change our state to Editor
                            self.manager.update_state()  # Updates / resets the state.
                        case pygame.K_DOWN:
                            self.current_selection += 1
                        case pygame.K_UP:
                            self.current_selection -= 1
                        case pygame.K_RETURN:
                            print("enter been pressed for button", self.current_selection)
                exit_handler(event)
            self.window.fill((124, 240, 0))
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(FPS)


def main() -> None:
    screen = pygame.display.set_mode((500, 700))
    # Create a basic 500x700 pixel window

    state_manager = StateManager(screen)
    state_manager.load_states(MainMenu)
    # We pass in all the screens that we want to use in our game / app.

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