import pygame

from sprites import Sprite, Animations, forever
from hitbox import AxisRectHB


class BlockAI(Sprite):
    SPEED = 0
    def __init__(self, (x, y)):
        def iter_hold():
            while 1:
                yield (0, 0, forever)

        animations = Animations("block", (50, 50),
            {"idle":iter_hold}, "idle")
        super(BlockAI, self).__init__(animations, (x, y))
        self.layer = 9
        self.hitbox = AxisRectHB(self, (0, 0), (50, 50), 50)
