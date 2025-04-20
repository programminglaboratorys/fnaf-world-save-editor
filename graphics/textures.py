"""Textures and helper functions for textures"""

from typing import Optional, Union

import pygame

from .geometry import TVector2

_textures_hotspot_table: dict[pygame.Surface, TVector2] = {}


def get_hotspot_from_string(surface: pygame.Surface, hotspot: str) -> tuple[int, int]:
    """
    Get the hotspot of a surface with given a string
    + + + + + + + + + + + + + + + + + + +
    + top-left | top-center | top-right +
    +     left | center     |     right +
    + bot-left | bot-center | bot-right +
    + + + + + + + + + + + + + + + + + + +
    """
    rect = surface.get_rect()
    try:
        return getattr(rect, hotspot)
    except AttributeError:
        raise ValueError(f"Invalid hotspot: {hotspot}") from None


def load_image(
    path: str, hotspot: Optional[Union[tuple[int, int], str]] = None, *, convert=False
) -> pygame.Surface:
    """
    Load an image with a hotspot
    """
    image = pygame.image.load(path)
    if convert:
        image = image.convert()
    if hotspot is None:
        hotspot = (0, 0)
    if isinstance(hotspot, str):
        hotspot = get_hotspot_from_string(image, hotspot)
    # else it is a tuple
    _textures_hotspot_table[image] = TVector2(hotspot)
    return image


def get_surface_hotspot(surface: pygame.Surface) -> Optional[TVector2]:
    """get the hotspot of a surface"""
    return _textures_hotspot_table.get(surface)
