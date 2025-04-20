"""A module for the character box class for the editor.

The character box class is a helper class for the editor that handles rendering
of the character box in the character selection menu. It also handles the
animation of the character.

"""

import glob
import json
from dataclasses import dataclass, field
from os import path

import pygame

from components.animate import AnimatatedObject, Animation
from components.textbox import TextBox
from graphics import render_text_with_outline
from graphics.textures import load_image
from utils.helper import add_vectors, quick_load
from utils.resources import CHARACTER_TEXTURES_PATH, FontBank


class StatusTextBox(TextBox):
    """an instance of the text box class with special font rendering"""

    def render_font(self, text):
        return render_text_with_outline(text, self.font, self.font_color)


@dataclass
class Character:
    """A character class holds data like it's id and name"""

    name: str
    frames: list[str] = field(repr=False)
    id: int
    speed: int
    icon: str = field(default="undefined.png")  # dummy data for now

    @staticmethod
    def from_json(data: str):
        """load Character from a json string"""
        # TODO: ignore invalid arguments
        return Character(**json.loads(data))


# pylint: disable=redefined-builtin
def _create_textbox(rect, id: str):
    return StatusTextBox(
        rect=rect,
        font=pygame.font.Font("textures/fonts/ARIALNB.TTF", 30),
        transparent=True,
        font_color=pygame.Color("white"),
        buffer=["0"],
        id=id,
    )


class CharacterBox:
    """the character box, here renders the character and the status of it"""

    box_color = (23, 23, 55, 128)
    textbox_width = 175
    size = (300, 380)
    current_selected_character: int
    last_selected_character: int
    level_textbox: TextBox
    next_textbox: TextBox
    characters: AnimatatedObject
    force_update: bool

    def load_characters_animations(self):
        """TODO: Insert docstring here"""
        print("process of loading animations")
        for folder in glob.iglob(f"{CHARACTER_TEXTURES_PATH}\\*\\"):
            print("folder found", folder)
            current_character_frames = []
            name = folder.split("\\")[1]

            data = quick_load(name, path.join(folder, f"{name}.json"))
            if data is None:
                print("no json file found for character:", name)
                continue
            character = Character.from_json(data)

            # pylint: disable=cell-var-from-loop
            for file in map(lambda f: path.join(folder, f), character.frames):
                texture = load_image(file, hotspot=(125, 220))
                current_character_frames.append(texture)
            animation = Animation(
                frames=current_character_frames, speed=character.speed, repeat=-1
            )
            self.characters.add_animation(name, animation)
            print(f"loaded {len(current_character_frames)} frames for {name!r}")
        self.characters.change_animation(0)

    def __init__(self):
        self.current_selected_character = 0
        self.last_selected_character = 0
        self.characters = AnimatatedObject()
        self.x = 115
        self.y = 20
        self.next_textbox = _create_textbox(
            self.calculate_rect_for_texbox(index=0), id="next"
        )
        self.level_textbox = _create_textbox(
            self.calculate_rect_for_texbox(index=1), id="level"
        )
        self.force_update = True
        self.load_characters_animations()

    def render_character(self, surface: pygame.Surface, deltatime):
        """render current selected character"""
        if self.last_selected_character != self.current_selected_character:
            self.last_selected_character = self.current_selected_character
            self.characters.change_animation(self.current_selected_character)
        # rect = surface.get_rect()
        height, width = self.size
        position = add_vectors(
            (self.x, self.y), self.size, (-(height // 1.85), -(width // 3))
        )  # subtract_vectors((380, 300), (0, -20))
        self.characters.draw(surface, deltatime, position)
        pygame.draw.circle(surface, (255, 0, 0), position, 5)

    def calculate_rect_for_texbox(self, index=0):
        """calculate the rect for the text box"""
        size = FontBank.arialnb_font.get_height() - 5
        textbox_height = size + 10
        _, width = self.size

        # 380 is the width of the characaterbox
        return (
            self.x + (width // 4.0),  # width//400%
            self.y + (self.size[1]) - textbox_height - 15 - (textbox_height * index),
            self.textbox_width,
            textbox_height,
        )
        # return (self.x+(self.width//1.25),
        # self.y+((box_size and box_size[1]) or 380)-textbox_height-15-(textbox_height*index),
        # self.textbox_width, textbox_height)
        # return ((self.x)+115, win_react.width-200-size+70, 200, size+10)

    def process_event(self, event):
        """process character box events"""
        self.level_textbox.get_event(event)
        self.next_textbox.get_event(event)

    def update(self):
        """update character box"""
        if self.force_update:
            self.level_textbox.force_update()
            self.next_textbox.force_update()
            self.force_update = False
            return
        self.level_textbox.update()
        self.next_textbox.update()

    def render(self, window: pygame.Surface, deltatime: int):
        """draw character box"""
        # size = subtract_vectors((win_react.width, win_react.height), (self.height, self.width)) # (300, 380)
        size = self.size
        surf = pygame.Surface(size, pygame.SRCALPHA)
        height, _ = surf.get_height(), surf.get_width()
        surf.fill(self.box_color)
        level_text = render_text_with_outline(
            "Level", FontBank.arialnb_font, (255, 255, 255), (0, 0, 0)
        )
        level_next_text = render_text_with_outline(
            "Next", FontBank.arialnb_font, (255, 255, 255), (0, 0, 0)
        )
        surf.blit(level_text, (20, height - level_text.get_height() - 20))
        surf.blit(level_next_text, (20, height - level_next_text.get_height() - 60))
        self.next_textbox.rect = pygame.Rect(self.calculate_rect_for_texbox(index=0))
        self.level_textbox.rect = pygame.Rect(self.calculate_rect_for_texbox(index=1))
        window.blit(surf, (self.x, self.y))
        pygame.draw.rect(window, (0, 0, 255), self.level_textbox.rect)
        pygame.draw.rect(window, (255, 0, 0), self.level_textbox.render_rect)

        pygame.draw.rect(window, (0, 0, 255), self.next_textbox.rect)
        pygame.draw.rect(window, (255, 0, 0), self.next_textbox.render_rect)
        self.level_textbox.draw(window)
        self.next_textbox.draw(window)
        self.render_character(window, deltatime)


# TODO: complete the class
class ButtonsGrid:
    """grid of buttons, holds the buttons and the current selected button"""

    def __init__(self):
        self.current_selected_button = 0
