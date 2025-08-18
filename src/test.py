"""test frame mainaly to test new ui components or new features in the fly without to mess other states code"""

import glob
import json
import os

import pygame

from components.animate import AnimatatedObject, Animation
from components.characterbox import CharacterBox
from graphics import draw_background
from graphics.textures import load_image
from states import State
from utils.constants import FPS, global_event_handler, MAX_WINDOW_SIZE
from utils.helper import add_vectors, quick_load, subtract_vectors
from utils.resources import FontBank, Textures


class Test(State):
    """a Test Frame, can be also considered a Playground to test new ui components"""
    box_color = (23, 23, 55, 128)

    def setup(self):
        """ Setup the state """
        # nothing for now
        math = 100
        self.go_back = False
        self.window = pygame.display.set_mode(MAX_WINDOW_SIZE, pygame.RESIZABLE)
        self.surf = pygame.Surface((self.window.get_width()-math, self.window.get_height()-math), pygame.SRCALPHA)
        self.x, self.y = math//2,math//2

    def run(self) -> None:
        """Test mainloop"""
        # set game window size
        while True:
            deltatime = self.clock.tick(
                FPS
            )  # make use of delta time for blinkers and animations

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        self.go_back = True
                    if event.key == pygame.VIDEORESIZE:
                        # TODO: based on window size change, set self.sub_interface
                        pass
                global_event_handler(self, event)
            if self.go_back:
                self.jump_to_state("MainMenu")
            draw_background(self.window, Textures.background)
            # draw grid background box
            self.surf.fill(self.box_color)

            self.window.blit(self.surf, (self.x, self.y))
        
            # draw a grid
            """
            for x in range(0, self.window.get_width(), 50):
                pygame.draw.line(
                    self.window,
                    (255, 255, 255),
                    (x, 0),
                    (x, self.window.get_height()),
                    2,
                )
            for y in range(0, self.window.get_height(), 50):
                pygame.draw.line(
                    self.window,
                    (255, 255, 255),
                    (0, y),
                    (self.window.get_width(), y),
                    2,
                )
            """

            lcd_font_size = FontBank.lcd_font.get_height()
            text = FontBank.lcd_font.render(
                f"fps: {int(self.clock.get_fps())}", 1, (255, 255, 255)
            )
            self.window.blit(
                text,
                subtract_vectors(
                    self.window.get_rect().bottomleft, (0, lcd_font_size * 2)
                ),
            )
            pygame.display.flip()
