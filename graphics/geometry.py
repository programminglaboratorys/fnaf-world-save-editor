from functools import lru_cache

class TVector2(tuple):
    """ 2D vector """
    @property
    def x(self):
        """ x component of the vector """
        return self[0]

    @property
    def y(self):
        """ y component of the vector """
        return self[1]

    def __repr__(self):
        return f"TVector2(x={self.x}, y={self.y})"

@lru_cache
def circlepoints(r):
    """
    Returns a list of points in a circle of radius r centered at the origin.
    
    This function uses Bresenham's circle algorithm to generate the points.
    """
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
