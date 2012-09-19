import pygame

from sprites import Sprite, Animations, forever
from hitbox import AxisRectHB


# TODO: EVENTUALLY THIS IS GOING TO BE MORE GENERAL AND A SUPERCLASS

class DoorAI(Sprite):
    SPEED = 0
    def __init__(self, (x, y), facing):
        def iter_move(closing):
            def anon():
                frames = range(1, 4)
                if closing:
                    frames.reverse()
                for y in frames:
                    yield (facing, y, 50)
                yield (None, ("closed" if closing else "opened"), None)
            return anon

        def iter_hold(closed):
            def anon():
                while 1:
                    yield (facing, (not closed) * 4, forever)
            return anon

        animations = Animations("door_blu_key", (100, 100),
            {"open": iter_move(0), "close":iter_move(1),
             "opened": iter_hold(0), "closed":iter_hold(1)}, "closed")
        super(DoorAI, self).__init__(animations, (x, y))
        self.layer = 10
        hb_coords = {0: ((0, 50), (100, 50)), 1: ((0, 0), (100, 50)),
                     2: ((50, 0), (50, 100)), 3: ((0, 0), (50, 100))}
        self.hitbox = AxisRectHB(self, *hb_coords[facing])
        self.hold_hitbox = None
        self.open()

    def close(self):
        self.animations.set_animation("close")
        self.hitbox, self.hold_hitbox = self.hold_hitbox, self.hitbox

    def open(self):
        self.animations.set_animation("open")
        self.hitbox, self.hold_hitbox = self.hold_hitbox, self.hitbox
