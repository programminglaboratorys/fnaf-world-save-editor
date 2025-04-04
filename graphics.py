"""
This module provides functions for rendering graphics, including text with
outlines and drawing background images
"""

import pygame

from geometry import circlepoints
from textures import get_surface_hotspot

def render_text_with_outline(text: str, font: pygame.Font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=2):
    """
    Render text with an outline
    """
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in circlepoints(int(round(opx))):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def draw_background(window, image):
    """
    Draws a background image with a hotspot.
    The image is placed such that the position is at (0, 0) in the window.
    """
    hotspot = get_surface_hotspot(image)
    window.blit(image, (-hotspot.x, -hotspot.y))
