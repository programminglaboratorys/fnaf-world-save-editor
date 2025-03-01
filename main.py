""" main functionality of the editor """
import pygame

from constants import Textures, global_event_handler, FPS, WINDOW_SIZE
from editor import Editor
from helper import Counter, AttrDict
from states import State, MainEditorStateManager

from typing import Tuple
from game_state.errors import ExitGame, ExitState


###

class Button:
    """ A simple button class. """
    image = Textures.button # center (244, 60)
    image_selected = Textures.button_selected
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

    def change_pos(self, pos: Tuple[int, int]):
        """ change the position of the button """
        self.x, self.y = pos
        self.rect.x, self.rect.y = pos

class MainMenu(State):
    """ main menu select what save to edit """
    current_selection = Counter(0, 0, 2)
    buttons = [ Button((5, 100)),
                Button((5, 200)),
                Button((5, 300))]

    def draw_buttons(self):
        """ Draws the buttons. """
        for index, button in enumerate(self.buttons):
            button_centerx = self.window.get_rect().centerx - 244
            button_centery = self.window.get_rect().centery - (index * 100)
            #print(index,  150 - 60 + (index * 100))
            #print(index, self.window.get_rect().centery, button_centery)
            button.change_pos((button_centerx, button_centery))
            button.draw(self.window, selected = index == self.current_selection)



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
