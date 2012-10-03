import pygame
import math
samplesurf = pygame.Surface((600, 450), pygame.SRCALPHA)

IMMOBILE = float("inf")

class HB(object):
    def __init__(self, linked, (x, y), mass=IMMOBILE):
        self.linked = linked
        self.pos = (x, y)
        self.mass = mass

    x = property(lambda self: self.pos[0] + self.linked.x)
    y = property(lambda self: self.pos[1] + self.linked.y)


class AxisRectHB(HB):
    def __init__(self, linked, (x, y), (w, h), mass=IMMOBILE):
        super(AxisRectHB, self).__init__(linked, (x, y), mass)
        self.width, self.height = w, h

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
        samplesurf.fill((0, ) * 4)
        pygame.draw.rect(samplesurf, (0xFF, 0, 0, 100),
                (map(int, (self.x - vx, self.y - vy)), (self.width, self.height)))
        surf.blit(samplesurf, (0, 0))


class CircleHB(HB):
    def __init__(self, linked, (x, y), r, mass=IMMOBILE):
        super(CircleHB, self).__init__(linked, (x, y), mass)
        self.r = r

    def line_intersect(self, ((x1, y1), (x2, y2))):
        """ < 0 : no intersect
            = 0 : tangent
            > 1 : 2 intersect """
        D2 = ((x1 * y2) - (x2 * y1)) ** 2
        dr2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return (self.r ** 2) * dr2 - D2

    def reblit(self, surf, (vx, vy)):
        samplesurf.fill((0, ) * 4)
        pygame.draw.circle(samplesurf, (0xFF, 0, 0, 100),
            (map(int, (self.x - vx, self.y - vy))), self.r)
        surf.blit(samplesurf, (0, 0))

    def push(self, other, (xoff, yoff), try_other=True):
        if isinstance(other, AxisRectHB):
            """  | |
                -+-+-
                 | |
                -+-+-
                 | |  """
            xtri = .5
            ytri = .5
            if self.x + xoff < other.x:  # ( |) |
                xtri = 0
            elif self.x + xoff > other.x + other.width:  # | (| )
                xtri = 1
            if self.y + yoff < other.y:  # o
                ytri = 0                 # =
            elif self.y + yoff > other.y + other.height:  # =
                ytri = 1                                  # o
            assert(not (xtri == ytri == .5))
            totmass = float(self.mass + other.mass)
            if xtri == .5:  # hitting from the top or bottom
                yoff *= self.mass / totmass
                other.linked.y += yoff
            elif ytri == .5:  # hitting from the left or right
                xoff *= self.mass / totmass
                other.linked.x += xoff
            else:  # hitting a corner
                """ THIS IS CURRENTLY WRONG, AND POSSIBLY CATASTROPHICALLY SO """
                xcorn = other.x + xtri * other.width   # location of the corner
                ycorn = other.y + ytri * other.height  # of the box

                distx = -(xcorn - (self.x + xoff))
                disty = -(ycorn - (self.y + yoff))
                hypot = math.hypot(distx, disty)  # distance from circ center to corner
                mult = math.hypot(xoff, yoff)  # get how fast you're going (might have changed)

                pushx = (distx * mult) / hypot
                pushy = (disty * mult) / hypot
                pushx *= self.mass / totmass  # normalize the distance to the corner
                pushy *= self.mass / totmass  # and push back by your motion vector
                xoff += pushx
                yoff += pushy

                other.linked.x -= pushx
                other.linked.y -= pushy
            self.linked.x += xoff
            self.linked.y += yoff

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
