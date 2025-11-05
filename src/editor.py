"""main editor interface for fnaf world. going to only support fnaf world for now"""

import glob
import json
import os

import pygame

from typing import Optional

from components.animate import AnimatatedObject, Animation
from components.characterbox import CharacterBox
from components.dynamic_grid import DynamicGrid, AbstractGridItem
from graphics import draw_background
from graphics.textures import load_image
from states import State
from utils.constants import FPS, global_event_handler
from utils.helper import add_vectors, quick_load, subtract_vectors
from utils.resources import FontBank, Textures

class AreaButton(AbstractGridItem):
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
            print("area clicked id:",self.id)

class AreaButtonsGrid(DynamicGrid):
    def __init__(self, items=None, **keyargs):
        super().__init__(items, (1, 99), (1, 99), padding=(0, 10), **keyargs)
    
    def draw(self, screen):
        for item in self.items[:-1]: # remove the last item
            item.draw(screen)

def load_location_buttons():
    """load the location buttons"""
    locations_buttons = AreaButtonsGrid(position=(5, 30), margin=(5, 0))
    for ind, file in enumerate(glob.iglob("textures/locations/*.png")):
        locations_buttons.items.append(AreaButton(file, ind+1))
    return locations_buttons

class Editor(State):
    """the main editor interface for fnaf world"""

    go_back: bool = False
    current_selected_character = 0
    last_selected_character = 0
    sub_interface: bool = (
        True  # make this a property because it depends on the window size
    )
    locations_buttons = load_location_buttons()
    tokens = 0
    lcd_font_size = 20
    arialnb_font_size = 30

    action_buttons = AnimatatedObject()
    characterbox: CharacterBox

    def load_action_buttons(self):
        """TODO: Insert docstring here"""
        if not self.action_buttons.empty:
            return
        done_data = quick_load("done button", "textures/done button/done button.json")
        raw_data = quick_load("raw button", "textures/raw button/raw button.json")
        if None in [raw_data, done_data]:
            print("no json file found for some action button! (Please Debug!)")
            return
        done_frames = [
            load_image(os.path.join("textures/done button/", frame), hotspot="topleft")
            for frame in json.loads(done_data)["frames"]
        ]
        raw_frames = [
            load_image(os.path.join("textures/raw button/", frame), hotspot="topleft")
            for frame in json.loads(raw_data)["frames"]
        ]

        animation = Animation(frames=done_frames, speed=50, repeat=-1)
        self.action_buttons.add_animation("done button", animation)
        #
        animation = Animation(frames=raw_frames, speed=50, repeat=-1)
        self.action_buttons.add_animation("raw button", animation)
        #
        self.action_buttons.change_animation(0)

    def setup(self):
        self.characterbox = CharacterBox()
        # TODO: load in a separate thread
        self.load_action_buttons()
        self.locations_buttons.refresh(pygame.display.get_window_size()[0])

    def render_locations_buttons(self, deltatime: int):
        """render locations buttons"""
        self.locations_buttons.draw(self.window)
        return
        self.locations_buttons.draw(self.window, deltatime, (30, 50))
        # TODO: simplified, this is hard to read
        # TODO: actually check if areas are opened or not
        self.locations_buttons.change_animation(0)
        self.locations_buttons.draw(
            self.window,
            deltatime,
            add_vectors(self.window.get_rect().topleft, (30, 50)),
        )  # draw location 1
        # print(self.locations_buttons.animations.keys())
        for index in range(1, len(self.locations_buttons.animations) - 1):
            # 2 location is id 1, 3 location is id 2, etc
            if self.save[self.sectionid].get(f"sw{index}") != "1":
                self.locations_buttons.change_animation(
                    len(self.locations_buttons.animations) - 1
                )
            else:
                self.locations_buttons.change_animation(index)
            self.locations_buttons.draw(
                self.window,
                deltatime,
                add_vectors(self.window.get_rect().topleft, (30, (index + 1) * 50)),
            )
            # self.locations_buttons.change_animation(index)

    def render_action_buttons(self, deltatime):
        """render action buttons"""
        # TODO: use a grid
        # win_react = self.window.get_rect()
        characterbox = self.characterbox
        self.action_buttons.draw(
            self.window,
            deltatime,
            pygame.Vector2(characterbox.x, characterbox.y)
            + pygame.Vector2(0, characterbox.height)
            + (-1, 10),
        )


    def run(self) -> None:
        """Editor mainloop"""
        self.go_back = False
        # font = pygame.font.Font(None, 30)
        while True:
            deltatime = self.clock.tick(
                FPS
            )  # make use of delta time for blinkers and animations

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        self.go_back = True
                if event.type == pygame.VIDEORESIZE:
                    # TODO: based on window size change, set self.sub_interface
                    pass
                self.locations_buttons.handle_event(event)
                self.characterbox.process_event(event)
                global_event_handler(self, event)
            if self.go_back:
                self.jump_to_state("MainMenu")
            self.characterbox.update()
            draw_background(self.window, Textures.background)

            # draw the current slot
            # text = font.render(str(self.globals.slot), 1, (255, 255, 255))
            # textpos = text.get_rect(centerx=10, centery=10)
            # self.window.blit(text, textpos)

            self.characterbox.render(self.window, deltatime)
            self.render_locations_buttons(deltatime)
            self.render_action_buttons(deltatime)

            lcd_font_size = FontBank.lcd_font.get_height()
            text = FontBank.lcd_font.render(
                f"tokens: {self.tokens}", 1, (255, 255, 255)
            )
            self.window.blit(
                text,
                subtract_vectors(self.window.get_rect().bottomleft, (0, lcd_font_size)),
            )

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
