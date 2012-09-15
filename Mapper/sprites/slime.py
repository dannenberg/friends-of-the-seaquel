import pygame

from sprites import Sprite, Animations


class SlimeAI(Sprite):
    SPEED = 5
    def __init__(self, (x, y)):
        def iter(xoff, delay):
            def anon():
                while 1:
                    yield (xoff, 0, 100 * delay)
                    yield (xoff, 1, 25 * delay)
                    yield (xoff, 2, 50 * delay)
                    yield (xoff, 1, 10 * delay)
            return anon
        animations = Animations("blob", (50, 50),
            {(k, d): iter(v, i) for v, k in enumerate([
            "up", "upright", "right", "downright", "down",
            "downleft", "left", "upleft"])
            for i, d in enumerate(["", "idle"], 1)}, ("downright", "idle"))
        super(SlimeAI, self).__init__(animations, (x, y))
        self.layer = 15
