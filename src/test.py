"""test frame mainaly to test new ui components or new features in the fly without to mess other states code"""

import glob
import json
import os

import pygame

from components.animate import AnimatatedObject, Animation
from components.characterbox import CharacterBox
from components.dynamic_grid import DynamicGrid, AbstractGridItem
from graphics import draw_background
from graphics.textures import load_image
from states import State
from utils.constants import FPS, global_event_handler, MAX_WINDOW_SIZE
from utils.helper import add_vectors, quick_load, subtract_vectors
from utils.resources import FontBank, Textures

class CharacterIconItem(AbstractGridItem):
    def __init__(self, texture_path, id: int = -1):
        super().__init__()
        self.texture = load_image(texture_path, hotspot="center")
        self.rect = self.texture.get_rect()
        self.id = id

    def get_rect(self):
        return self.rect
    
    def get_surface(self):
        return self.texture

    def handle_event(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(*event.pos):
            print("character clicked id:", self.id)

CHARACTERS_GRID_ROWS = 6
CHARACTERS_GRID_COLS = 8

class CharactersSelectGrid(DynamicGrid):
    def __init__(self, items=None, **keyargs):
        super().__init__(items, (CHARACTERS_GRID_COLS, CHARACTERS_GRID_ROWS), (CHARACTERS_GRID_COLS, CHARACTERS_GRID_ROWS), padding=(2, 2), **keyargs)

    @staticmethod
    def roundit(value: float):
        if value - int(value) >= 0.3:
            return int(value) + 1
        return round(value)

def create_characters_grid():
    chars = CharactersSelectGrid(position=(0, 20))
    """
    for char in glob.iglob("textures/characters/*"):
        if not os.path.isdir(char):
            continue
        img_path = os.path.join(char, "icon.png")
        if not os.path.exists(img_path):
            img_path = "textures/characters/char-icon.png"
        chars.items.append(CharacterIconItem(img_path))
        # TODO: add the characters to the grid!
    """
    img_path = "textures/characters/char-icon.png"
    for _ in range(CHARACTERS_GRID_ROWS*CHARACTERS_GRID_COLS):
        chars.items.append(CharacterIconItem(img_path))
    return chars


class Test(State):
    """a Test Frame, can be also considered a Playground to test new ui components"""
    box_color = (23, 23, 55, 128)
    characters = create_characters_grid()

    def calculate_characters_grid_background_size(self):
        grid_width, grid_height = self.characters.last_col+1, self.characters.last_row+1
        item_width, item_height = self.characters.item_width, self.characters.item_height
        padding_x, padding_y = self.characters.padding_x, self.characters.padding_y
        print("grid size:", grid_width, grid_height, "item size:", item_width, item_height)
        width = (padding_y+item_width)*grid_width
        height = (padding_x+item_height)*grid_height
        return width, height

    def setup(self):
        """ Setup the state """
        # fit the characters grid to the screen
        math = 100
        self.x, self.y = math//2,math//2
        self.characters.set_position(self.x, self.y)
        self.characters.refresh(self.window.get_width())
        #
        self.go_back = False
        self.window = pygame.display.set_mode(MAX_WINDOW_SIZE, pygame.RESIZABLE)
        self.create_grid_background()
        # how can I access fnafw in editor frame but not in test frame? 
        #print("tokens:", self.save[self.sectionid].get(f"tokens"))

    def create_grid_background(self):
        self.surf = pygame.Surface(self.calculate_characters_grid_background_size() + pygame.Vector2(20, 15), pygame.SRCALPHA)
        # fill with box color
        self.surf.fill(self.box_color)

    def run(self) -> None:
        """Test mainloop"""
        # set game window size
        while True:
            deltatime = self.clock.tick(
                FPS
            )  # make use of delta time for blinkers and animations

            for event in pygame.event.get():
                global_event_handler(self, event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        self.go_back = True
                self.characters.handle_event(event)
                if event.type == pygame.VIDEORESIZE:
                    # TODO: based on window size change, set self.sub_interface
                    #self.create_grid_background()
                    pass
            if self.go_back:
                self.jump_to_state("MainMenu")
            draw_background(self.window, Textures.background)
            # draw grid background box
            self.window.blit(self.surf, (self.x, self.y))
            # draw grid
            self.characters.draw(self.window)
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
