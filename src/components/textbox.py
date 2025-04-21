"""TextBox component for Pygame.

This module provides a `TextBox` class which you can use to create
text boxes in your Pygame application. The text box handles keyboard
input and can be used to input text from the user. The text box can
be customized in various ways, such as setting the color, border
thickness, and font. The text box can also be set to be inactive
when the user presses enter.

originally created by Mekire, improved version by iamme

"""

import re
from typing import Callable

import pygame as pg

ACCEPTED = r"[a-zA-Z0-9.\"#$%&'()*+,-./:;<=>?@\[\\\]\^_`{\|}~]*"


# TODO: give better comments and change it to a dataclass, solve sensible pylint warnings
# pylint: disable=too-many-instance-attributes
class TextBox:
    """TextBox component."""

    # rect: pg.Rect
    buffer: list
    final: str
    rendered: pg.Surface
    render_rect: pg.Rect
    render_area: pg.Rect
    blink: bool
    blink_timer: float
    transparent: bool
    id: str
    command: Callable[[str, str], None]
    active: bool
    color: pg.Color
    font_color: pg.Color
    outline_color: pg.Color
    invalid_color: pg.Color
    outline_width: int
    active_color: pg.Color
    font: pg.font.Font
    clear_on_enter: bool
    inactive_on_enter: bool
    outline_thickness: int
    broder_redius: int
    regex: re.Pattern
    invalid: bool

    # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-locals,
    def __init__(
        self,
        rect,
        buffer=None,
        blink=True,
        transparent=False,
        id=None,
        command=None,
        active=False,
        color=pg.Color("white"),
        font_color=pg.Color("black"),
        outline_color=pg.Color("black"),
        invalid_color=pg.Color("red"),
        outline_width=2,
        active_color=pg.Color("blue"),
        font=None,
        clear_on_enter=False,
        inactive_on_enter=True,
        outline_thickness=2,
        broder_redius=3,
        regex=re.compile(ACCEPTED),
    ):
        self.rect = pg.Rect(rect)
        self.buffer = buffer if buffer is not None else []
        self.blink = blink
        self.blink_timer = 0
        self.transparent = transparent
        self.id = id
        self.command = command
        self.active = active
        self.color = color
        self.font_color = font_color
        self.outline_color = outline_color
        self.invalid_color = invalid_color
        self.outline_width = outline_width
        self.active_color = active_color
        self.font = font
        self.clear_on_enter = clear_on_enter
        self.inactive_on_enter = inactive_on_enter
        self.outline_thickness = outline_thickness
        self.broder_redius = broder_redius
        self.regex = regex
        #
        self.invalid = False
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None

    def vaildate(self, char: str):
        """check if char is valid according to regex"""
        return self.regex.match(char) is not None

    def get_event(self, event):
        """get event and process it"""
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode:
                if self.vaildate(event.unicode):
                    self.invalid = False
                    self.buffer.append(event.unicode)
                else:
                    self.invalid = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            # TODO: remove
            # print(repr(self.id),
            # "RECT CLLIDE", self.rect.collidepoint(event.pos),
            # "RECT", self.rect,
            # "RENDER RECT CLLIDE", self.render_rect.collidepoint(event.pos))

    def execute(self):
        """execute the command with the current self.final as argument"""
        if self.command:
            self.command(self.id, self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def render_font(self, text) -> pg.Surface:
        """render text in font and color"""
        return self.font.render(text, True, self.font_color)

    def force_update(self):
        """force an update of the text box without needing to be focused"""
        self.final = "".join(self.buffer)
        self.rendered = self.render_font(self.final)
        self.render_rect = self.rendered.get_rect(
            x=self.rect.x + 2, centery=self.rect.centery
        )
        if self.render_rect.width > self.rect.width - 6:
            offset = self.render_rect.width - (self.rect.width - 6)
            self.render_area = pg.Rect(
                offset, 0, self.rect.width - 6, self.render_rect.height
            )
        else:
            self.render_area = self.rendered.get_rect(topleft=(0, 0))
        # TODO: change to use dalte time (check animate.py)
        if pg.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def update(self):
        """update the blink timer"""
        if not self.active and self.final is not None:  # an update is not necessary
            return
        # TODO: change to use dalte time (check animate.py)
        if pg.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.render_font(self.final)
            self.render_rect = self.rendered.get_rect(
                x=self.rect.x + 2, centery=self.rect.centery
            )
            if self.render_rect.width > self.rect.width - 6:
                offset = self.render_rect.width - (self.rect.width - 6)
                self.render_area = pg.Rect(
                    offset, 0, self.rect.width - 6, self.render_rect.height
                )
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))

    def draw(self, surface):
        """draw the text box"""
        outline_color = self.active_color if self.active else self.outline_color
        if self.invalid:
            outline_color = self.invalid_color
        outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
        if not self.transparent:
            if outline_color:
                pg.draw.rect(
                    surface,
                    outline_color,
                    outline,
                    self.outline_thickness,
                    self.broder_redius,
                )
            if self.color:
                surface.fill(self.color, self.rect)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color, (curse.right + 1, curse.y, 2, curse.h))
