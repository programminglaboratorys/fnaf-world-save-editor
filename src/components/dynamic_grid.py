import pygame
from abc import ABC, abstractmethod
from typing import Optional

class AbstractGridItem(ABC):
    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.get_surface(), self.get_rect())

class DynamicGrid:
    def __init__(self, items: list[AbstractGridItem],
                 min_cols_rows: tuple,
                 max_cols_rows: tuple,
                 padding: tuple[int, int]= (10, 10),
                 margin: tuple[int, int]= (10, 10),
                 *,
                 position: tuple[int, int]= (0, 0),
                 pre_setup: bool = False,
                 window_width: Optional[int] = None,
                 static: bool = False
                 ):
        self.items = items or []
        self.min_cols, self.min_rows = min_cols_rows
        self.max_cols, self.max_rows = max_cols_rows
        self.padding_x, self.padding_y = padding
        self.margin_x, self.margin_y = margin
        self.grid_x, self.grid_y = position
        self.static = static
        #
        self.last_col = 0
        self.last_row = 0
        self.update_item_size()
        if pre_setup:
            self.recalculate_grid(window_width)

    @staticmethod
    def roundit(value: float):
        if value - int(value) >= 0.7:
            return int(value) + 1
        return round(value)

    def set_position(self, x: int, y: int):
        """Sets the top-left position of the grid."""
        self.grid_x = x
        self.grid_y = y

    def refresh(self, window_width: int):
        self.update_item_size()
        self.recalculate_grid(window_width)

    def update_item_size(self):
        if not self.items:
            self.item_width, self.item_height = 0, 0
        else:
            self.item_width, self.item_height = self.items[0].get_rect().size

    def recalculate_grid(self, window_width: int):
        if not isinstance(window_width, int):
            raise TypeError(f"window_width is supposed to be int but got {type(window_width)} instead")
        available_width = window_width - (2 * self.margin_x)
        total_item_width = self.item_width + self.padding_x
        self.cols = min(self.max_cols, max(self.min_cols, self.roundit(max(1, available_width) / total_item_width)))

        for i, item in enumerate(self.items):
            if i >= self.max_cols * self.max_rows:
                break  # stop if we exceed the maximum number of items allowed in the grid

            item_rect = item.get_rect()
            col = self.last_col = i % self.cols
            row = self.last_row = i // self.cols

            item_rect.x = self.grid_x + self.margin_x + col * (self.item_width + self.padding_x)
            item_rect.y = self.grid_y + self.margin_y + row * (self.item_height + self.padding_y)

    def handle_event(self, event: pygame.Event):
        if event.type == pygame.VIDEORESIZE and not self.static:
            self.recalculate_grid(event.size[0])
        for item in self.items:
            if hasattr(item, "handle_event") and callable(item.handle_event):
                item.handle_event(event)

    def draw(self, screen: pygame.Surface):
        for item in self.items:
            item.draw(screen)

    def __getitem__(self, key: int):
        return self.items[key]
    
    def __setitem__(self, key: int, value: AbstractGridItem):
        self.items[key] = value
