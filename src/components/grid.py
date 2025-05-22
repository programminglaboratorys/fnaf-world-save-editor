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
        self.color = kwargs.get("color", (200, 200, 200))
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


class Grid:
    """
    A grid component, holds other components and lays them out in a grid.

    :param width: The width of the grid.
    :param height: The height of the grid.
    :param border_width: The width of the border.
    :param border_height: The height of the border.
    :param cell_width_padding: The width of the padding between cells.
    :param cell_height_padding: The height of the padding between cells.
    :param components: The components to be placed in the grid.
    """

    def __init__(
        self,
        width,
        height,
        border_width,
        border_height,
        cell_width_padding,
        cell_height_padding,
        components,
    ):
        self.grid_width = width
        self.grid_height = height
        self.border_width = border_width
        self.border_height = border_height
        self.cell_width_padding = cell_width_padding
        self.cell_height_padding = cell_height_padding
        self.components: list[Button] = components

    def draw(self, surface, deltatime):
        """
        Draw the grid onto the surface.

        :param surface: The surface to draw onto.
        :param deltatime: The time since the last frame.
        """
        # first draw the border
        pygame.draw.rect(
            surface, (0, 0, 0), (0, 0, self.width, self.height), self.border_width
        )
        pygame.draw.rect(
            surface, (0, 0, 0), (0, 0, self.width, self.height), self.border_height
        )

        # then draw the cells
        for i, c in enumerate(self.components):
            # calculate the position of the component
            x = (
                (i % (self.width // (c.width + self.cell_width_padding)))
                * (c.width + self.cell_width_padding)
                + self.border_width
                + self.cell_width_padding
            )
            y = (
                (i // (self.width // (c.width + self.cell_width_padding)))
                * (c.height + self.cell_height_padding)
                + self.border_height
                + self.cell_height_padding
            )

            # set the component's position
            c.rect.topleft = (x, y)

            # draw the component
            c.draw(surface, deltatime)

    @property
    def width(self):
        """The total width of the grid including borders."""
        return self.border_width * 2 + (
            self.grid_width * len(self.components)
            + self.cell_width_padding * (len(self.components) - 1)
        )

    @property
    def height(self):
        """The total height of the grid including borders."""
        rows = (
            len(self.components)
            + (self.grid_width // (self.components[0].width + self.cell_width_padding))
            - 1
        ) // (self.grid_width // (self.components[0].width + self.cell_width_padding))
        return self.border_height * 2 + (
            self.components[0].height * rows + self.cell_height_padding * (rows - 1)
        )

    @property
    def x(self):
        """The x-coordinate of the grid's top-left corner."""
        return 0  # Assuming grid starts at the origin

    @property
    def y(self):
        """The y-coordinate of the grid's top-left corner."""
        return 0  # Assuming grid starts at the origin

    @property
    def rect(self):
        """The rect of the grid."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def add(self, component):
        """Add a component to the grid."""
        self.components.append(component)

    def remove(self, component):
        """Remove a component from the grid."""
        self.components.remove(component)


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600, 600))

    grid = Grid(
        width=600,
        height=900,
        border_width=10,
        border_height=10,
        cell_width_padding=10,
        cell_height_padding=10,
        components=[
            Button(position=(0, 0), size=(100, 100), text="Button 1"),
            Button(position=(100, 100), size=(100, 100), text="Button 2"),
            Button(position=(200, 200), size=(100, 100), text="Button 3"),
            Button(position=(300, 300), size=(100, 100), text="Button 4"),
        ],
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        window.fill((255, 255, 255))
        grid.draw(window, 0)
        pygame.display.flip()
