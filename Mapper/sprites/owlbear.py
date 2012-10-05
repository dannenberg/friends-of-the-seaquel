import pygame

from sprites import Sprite, Animations
from hitbox import CircleHB


class OwlbearAI(Sprite):
    SPEED = 5
    def __init__(self, (x, y)):
        def iter(xoff, delay):
            xoff = 0
            def anon():
                while 1:
                    yield (xoff, 0, 50 * delay)
                    yield (xoff, 1, 50 * delay)
                    yield (xoff, 2, 50 * delay)
                    yield (xoff, 1, 50 * delay)
                    yield (xoff, 0, 50 * delay)
                    yield (xoff, 3, 50 * delay)
                    yield (xoff, 4, 50 * delay)
                    yield (xoff, 3, 50 * delay)
            return anon
        def iter_idle(xoff, delay):
            xoff = 0
            delay = 3
            def anon():
                while 1:
                    yield (xoff, 0, 50 * delay)
                    yield (xoff, 5, 50 * delay)
                    yield (xoff, 6, 50 * delay)
                    yield (xoff, 5, 50 * delay)
            return anon
        andict = {(k, d): f(v, 1) for v, k in enumerate([
            "up", "upright", "right", "downright", "down",
            "downleft", "left", "upleft"])
            for f, d in [(iter, ""), (iter_idle, "idle")]}
        animations = Animations("owlbear", (50, 50), andict
            , ("downright", "idle"))
        super(OwlbearAI, self).__init__(animations, (x, y))
        self.layer = 5
        self.hitbox = CircleHB(self, (25, 25), 24, 50)
