"""A simple button class and a button grid class"""

# TODO: complete the class

import pygame


class Button:
    """A simple button class for Pygame."""

    __slots__ = ("rect", "text", "font", "color", "hover_color", "current_color")

    def __init__(
        self,
        position,
        size,
        **kwargs,
    ):
        self.rect = pygame.Rect(*position, *size)
        self.text = kwargs.get("text", "")
        self.font = kwargs.get("font") or pygame.font.Font(None, 36)
        self.color = kwargs.get("color", (255, 255, 255))
        self.hover_color = kwargs.get("hover_color", (200, 200, 200))
        self.current_color = self.color

    @property
    def width(self):
        """The width of the button."""
        return self.rect.width

    @property
    def height(self):
        """The height of the button."""
        return self.rect.height

    @property
    def x(self):
        """The x position of the button."""
        return self.rect.x

    @property
    def y(self):
        """The y position of the button."""
        return self.rect.y

    def draw(self, surface, daltetime: int):
        """Draw the button on the screen."""
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        """Change color on hover."""
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def is_clicked(self, event):
        """Check if the button is clicked."""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class ButtonsGrid(dict[str, Button]):
    """grid of buttons, holds the buttons and the current selected button"""

    def __init__(self):
        super().__init__()
        self.current_selected_button = 0

    def add(self, name, button: Button):
        """add a button to the grid"""
        if name in self:
            raise ValueError(f"Button with name {name} already exists")
        self[name] = button

    def process_event(self, event: pygame.event.Event):
        """process button grid events"""
        for name, button in self.items():
            if button.is_clicked(event):
                self.current_selected_button = list(self.keys()).index(name)
                self.on_button_clicked(name, button)

    def draw(self, surface: pygame.Surface, _: int):
        """draw the buttons"""
        if len(self) == 0:
            return
        for button in self.values():
            button.draw(surface)

    def on_button_clicked(self, name, button: Button):
        """a handler for when a button is clicked"""
        if not hasattr(self, f"on_{name}"):
            return
        return getattr(self, f"on_{name}")(button)
