""" main editor interface for fnaf world. going to only support fnaf world for now """
import glob
import json

from os import path

import pygame

from states import State
from utils.constants import FPS, global_event_handler
from utils.resources import Textures, FontBank
from utils.helper import add_vectors, subtract_vectors, quick_load
from graphics.textures import load_image
from graphics import draw_background
from components.animate import AnimatatedObject, Animation
from components.characterbox import CharacterBox

def load_location_buttons():
    """ load the location buttons """
    locations_buttons = AnimatatedObject()
    for file in glob.iglob("textures/locations/*.png"):
        texture = load_image(file, hotspot="center")
        name = path.basename(file).split('.')[0]
        animation = Animation(frames=[texture], speed=0, repeat=-1)
        locations_buttons.add_animation(name, animation)
    locations_buttons.change_animation(0)
    return locations_buttons


class Editor(State):
    """ the main editor interface for fnaf world """
    go_back: bool = False
    current_selected_character = 0
    last_selected_character = 0
    sub_interface: bool = True # make this a property because it depends on the window size
    locations_buttons = load_location_buttons()
    tokens = 0
    lcd_font_size = 20
    arialnb_font_size = 30

    action_buttons = AnimatatedObject()
    characterbox: CharacterBox

    def load_action_buttons(self):
        """ TODO: Insert docstring here """
        if not self.action_buttons.empty:
            return
        done_data = quick_load("done button", "textures/done button/done button.json")
        if done_data is None:
            print("no json file found for done button")
            return
        done_frames = [load_image(path.join("textures/done button/", frame), hotspot="center") for frame in json.loads(done_data)["frames"]]
        animation = Animation(frames=done_frames, speed=50, repeat=-1)
        self.action_buttons.add_animation("done button", animation)
        self.action_buttons.change_animation(0)



    def setup(self):
        self.characterbox = CharacterBox()
        #self.characterbox.force_update = True
        # TODO: load in a separate thread
        self.load_action_buttons()

    def render_character(self, deltatime):
        """ render current selected character """
        if self.last_selected_character != self.current_selected_character:
            self.last_selected_character = self.current_selected_character
            self.characters.change_animation(self.current_selected_character)
        rect = self.window.get_rect()
        position = subtract_vectors(rect.center, (0, -20))
        self.characters.draw(self.window, deltatime, position)
        pygame.draw.circle(self.window, (255, 0, 0), position, 5)

    def render_locations_buttons(self, deltatime: int):
        """ render locations buttons """
        # TODO: simplified, this is hard to read
        self.locations_buttons.change_animation(0)
        for index in range(1, len(self.locations_buttons.animations)):
            self.locations_buttons.draw(self.window,
                                        deltatime,
                                        add_vectors(self.window.get_rect().topleft, (30, index*50))
                                        )
            self.locations_buttons.change_animation(index)

    def render_action_buttons(self, deltatime):
        """ render action buttons """
        win_react = self.window.get_rect()
        self.action_buttons.draw(self.window, deltatime, (win_react.width-315, win_react.height-100))

    def run(self) -> None:
        """ Editor mainloop """
        self.go_back = False
        font = pygame.font.Font(None, 30)
        while True:
            deltatime = self.clock.tick(FPS) # make use of delta time for blinkers and animations

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        self.go_back = True
                    if event.key == pygame.VIDEORESIZE:
                        # TODO: based on window size change, set self.sub_interface
                        pass
                self.characterbox.process_event(event)
                global_event_handler(self, event)
            if self.go_back:
                self.jump_to_state("MainMenu")
            self.characterbox.update()
            draw_background(self.window, Textures.background)

            # draw the current slot
            text = font.render(str(self.globals.slot), 1, (255, 255, 255))
            textpos = text.get_rect(centerx=10, centery=10)
            self.window.blit(text, textpos)

            self.characterbox.render(self.window, deltatime)
            #self.render_character(deltatime)
            self.render_locations_buttons(deltatime)
            self.render_action_buttons(deltatime)

            lcd_font_size = FontBank.lcd_font.get_height()
            text = FontBank.lcd_font.render(f"tokens: {self.tokens}", 1, (255, 255, 255))
            self.window.blit(text, subtract_vectors(self.window.get_rect().bottomleft, (0, lcd_font_size)))

            text = FontBank.lcd_font.render(f"fps: {int(self.clock.get_fps())}", 1, (255, 255, 255))
            self.window.blit(text, subtract_vectors(self.window.get_rect().bottomleft, (0, lcd_font_size*2)))
            # pygame.draw.circle(self.window, (255, 0, 0), (self.window.get_rect().centerx, self.window.get_rect().centery), 5)
            pygame.display.flip()
