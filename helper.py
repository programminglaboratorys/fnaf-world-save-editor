from typing import Union
from functools import lru_cache
import pygame

class Counter:
    """Class to create a counter with a defined range. The counter can
    be incremented or decremented within the range and the value
    will be clamped to the range if it goes outside of it. If the
    strict flag is set, a ValueError will be raised if the value
    goes outside of the range."""
    def __init__(self, value: int, min_val: int, max_val: int, *, strict: bool = False):
        self._min = min_val
        self._max = max_val
        self.strict = strict

        # Validate initial value
        if not min_val <= value <= max_val:
            if strict:
                raise ValueError(f"Initial value {value} must be between {min_val} and {max_val}")
            else:
                # Fix the value by clamping it
                value = min(max(value, min_val), max_val)

        self.value = value
    
    def __int__(self):
        return self.value

    def __add__(self, other: int) -> 'Counter':
        result_value = int(self) + other

        if not self._min <= result_value <= self._max:
            if self.strict:
                raise ValueError(f"Result {result_value} must be between {self._min} and {self._max}")
            else:
                # Fix the value by clamping it
                result_value = min(max(result_value, self._min), self._max)
        
        return Counter(result_value, self._min, self._max, strict=self.strict)

    def __sub__(self, other: int) -> 'Counter':
        result_value = int(self) - other
        
        if not self._min <= result_value <= self._max:
            if self.strict:
                raise ValueError(f"Result {result_value} must be between {self._min} and {self._max}")
            else:
                # Fix the value by clamping it
                result_value = min(max(result_value, self._min), self._max)

        return Counter(result_value, self._min, self._max, strict=self.strict)

    def __repr__(self) -> str:
        mode = "strict" if self.strict else "non-strict"
        return f"Counter(value={int(self)}, bounds=[{self._min}, {self._max}], mode='{mode}')"

    def __eq__(self, other: Union[int,'Counter']):
        return int(other) == int(self)

class AttrDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"type object '{type(self).__name__}' has no attribute '{attr}'") from None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(f"type object '{type(self).__name__}' has no attribute '{attr}'") from None

    def __dir__(self):
        return list(self) + dir(type(self))
    
    def __repr__(self):
        return f"AttrDict({dict.__repr__(self)})"



# TODO: remove _circle_cache, also, try and understand how this code works
@lru_cache
def _circlepoints(r):
    x, y, e = r, 0, 1 - r
    points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

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

    for dx, dy in _circlepoints(int(round(opx))):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf
