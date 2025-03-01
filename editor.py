import pygame
from states import State
from constants import FPS, global_event_handler

"""
pressed = py.key.get_pressed()
if pressed[py.K_RSHIFT] or pressed[py.K_LSHIFT] and ch in src:
    ch = dest[src.index(ch)]
"""

class Editor(State):
    """ the main editor interface for fnaf world """
    go_back: bool = False
    def run(self) -> None:
        """ Editor mainloop """
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        while True:
            for event in pygame.event.get():
                global_event_handler(self, event)
            if self.go_back:
                self.jump_to_state("MainMenu")
            self.window.fill((100, 149, 237))  # Cornflower Blue
            # draw the current slot
            text = font.render(str(self.manager.globals.slot), 1, (255, 255, 255))
            textpos = text.get_rect(centerx=self.window.get_rect().centerx, centery=self.window.get_rect().centery)
            self.window.blit(text, textpos)

            pygame.display.flip()
            self.clock.tick(FPS)
