import pygame

from sprites import Sprite, Animations, forever
from hitbox import AxisRectHB


class TeleportAI(Sprite):
    SPEED = 0
    def __init__(self, (x, y), (dx, dy)):
        super(TeleportAI, self).__init__(None, (x, y))
        self.hitbox = AxisRectHB(self, (0, 0), (50, 50))
        self.dx, self.dy = dx, dy

    def on_hit(self, other):
        print "beam me up scottie"
        return True
