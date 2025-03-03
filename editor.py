""" main editor interface for fnaf world. going to only support fnaf world for now """
import pygame
import glob
from states import State
from constants import FPS, global_event_handler
from textures import Textures, draw_background, load_image, get_surface_hotspot, render_text_with_outline
from helper import add_vectors, subtract_vectors
from os import path
from editor_components import AnimatatedObject, Animation


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
    lcd_font: pygame.font.Font
    arialnb_font: pygame.font.Font
    go_back: bool = False
    current_selected_character = 0
    freddy = Textures.freddy
    sub_interface: bool = True # make this a property because it depends on the window size
    locations_buttons = load_location_buttons()
    tokens = 0
    lcd_font_size = 20
    arialnb_font_size = 30



    def setup(self):
        self.lcd_font = pygame.font.Font("textures/fonts/LcdSolid.ttf", self.lcd_font_size)
        self.arialnb_font = pygame.font.Font("textures/fonts/ARIALNB.TTF", self.arialnb_font_size)

    def render_character(self):
        """ render current selected character """
        # TODO: complete this function, animate and render current selected character
        texture = self.freddy
        hotspot = get_surface_hotspot(texture)
        rect = self.window.get_rect()
        position = subtract_vectors(rect.center, (0, -80))
        character_position = subtract_vectors(position, hotspot)
        self.window.blit(texture, character_position)
        pygame.draw.circle(self.window, (255, 0, 0), position, 5)

    def render_character_box(self):
        """ render character transparent box """
        win_react = self.window.get_rect()
        surf = pygame.Surface((win_react.width-200, win_react.height-60), pygame.SRCALPHA)
        surf.fill((23, 23, 55, 128))
        level_text = render_text_with_outline("Level", self.arialnb_font, (255, 255, 255), (0, 0, 0))
        level_next_text = render_text_with_outline("Next", self.arialnb_font, (255, 255, 255), (0, 0, 0))
        level_counter_text = render_text_with_outline("0", self.arialnb_font, (255, 255, 255), (0, 0, 0))
        level_next_counter_text = render_text_with_outline("0", self.arialnb_font, (255, 255, 255), (0, 0, 0))
        surf.blit(level_text, (20, surf.get_height()-level_text.get_height()-20))
        surf.blit(level_next_text, (20, surf.get_height()-level_next_text.get_height()-60))
        surf.blit(level_counter_text, (115, surf.get_height()-level_counter_text.get_height()-20))
        surf.blit(level_next_counter_text, (115, surf.get_height()-level_next_counter_text.get_height()-60))
        self.window.blit(surf, (115, 20))


    def render_locations_buttons(self, clock: pygame.time.Clock):
        """ render locations buttons """
        # TODO: simplified, this is hard to read
        self.locations_buttons.change_animation(0)
        for index in range(1, len(self.locations_buttons.animations)):
            self.locations_buttons.draw(self.window,
                                        clock,
                                        add_vectors(self.window.get_rect().topleft, (30, index*50))
                                        )
            self.locations_buttons.change_animation(index)

    def run(self) -> None:
        """ Editor mainloop """
        self.go_back = False
        font = pygame.font.Font(None, 30)
        while True:
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
            # self.window.fill((100, 149, 237)) # Cornflower Blue
            draw_background(self.window, Textures.background)

            # draw the current slot
            text = font.render(str(self.globals.slot), 1, (255, 255, 255))
            textpos = text.get_rect(centerx=10, centery=10)
            self.window.blit(text, textpos)

            self.render_character_box()
            self.render_character()
            self.render_locations_buttons(self.clock)
            #
            text = self.lcd_font.render(f"tokens: {self.tokens}", 1, (255, 255, 255))
            self.window.blit(text, subtract_vectors(self.window.get_rect().bottomleft, (0, self.lcd_font_size)))
            # pygame.draw.circle(self.window, (255, 0, 0), (self.window.get_rect().centerx, self.window.get_rect().centery), 5)
            pygame.display.flip()
            self.clock.tick(FPS)
