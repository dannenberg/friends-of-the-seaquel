import pygame

class AxisRectHB(object):
    def __init__(self, linked, (x, y), (w, h)):
        self.linked = linked
        self.pos = (x, y)
        self.width, self.height = w, h

    x = property(lambda self: self.pos[0] + self.linked.x)
    y = property(lambda self: self.pos[1] + self.linked.y)

    def intersects(self, other, try_other=True):
        if other is None:
            return False

        try:
            return other.intersects(self, False)
        except TypeError:
            pass

        raise TypeError("unsupported operand type(s) for intersect: '" + type(self)
            + "' and '" + type(other) + "'")

    def reblit(self, surf, (vx, vy)):
        pygame.draw.rect(surf, (0xFF, 0, 0, 100),
                (map(int, (self.x - vx, self.y - vy)), (self.width, self.height)))


class CircleHB(object):
    def __init__(self, linked, (x, y), r):
        self.linked = linked
        self.pos = (x, y)
        self.r = r

    x = property(lambda self: self.pos[0] + self.linked.x)
    y = property(lambda self: self.pos[1] + self.linked.y)

    def line_intersect(self, ((x1, y1), (x2, y2))):
        """ < 0 : no intersect
            = 0 : tangent
            > 1 : 2 intersect """
        D2 = ((x1 * y2) - (x2 * y1)) ** 2
        dr2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return (self.r ** 2) * dr2 - D2

    def reblit(self, surf, (vx, vy)):
        pygame.draw.circle(surf, (0xFF, 0, 0, 100),
            (map(int, (self.x - vx, self.y - vy))), self.r)

    def intersects(self, other, try_other=True):
        if isinstance(other, AxisRectHB):
            circleDistancex = abs(self.x - (other.x + other.width / 2))
            circleDistancey = abs(self.y - (other.y + other.height / 2))

            if circleDistancex > (other.width / 2 + self.r):
                return False
            if circleDistancey > (other.height / 2 + self.r):
                return False

            if circleDistancex <= (other.width / 2):
                return True
            if circleDistancey <= (other.height / 2):
                return True

            cornerDistance_sq = ((circleDistancex - other.width / 2) ** 2 +
                                 (circleDistancey - other.height / 2) ** 2)

            return cornerDistance_sq <= (self.r ** 2)

        elif isinstance(other, CircleHB):
            return (self.r + other.r) ** 2 >= (self.x - other.x) ** 2 + (self.y - other.y) ** 2

        elif other is None:
            return False

        elif try_other:
            try:
                return other.intersects(self, False)
            except TypeError:
                pass

        raise TypeError("unsupported operand type(s) for intersect: '" + type(self)
            + "' and '" + type(other) +"'")
