import pygame

from sprites import Sprite, Animations

SPEED = 5
DIAG = SPEED / (2 ** .5)
class SlimeAI(Sprite):
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

    def move(self, xoff=0, yoff=0):
        dirc = (["upleft", "up", "upright", "left", "", "right",
                "downleft", "down", "downright"][xoff + yoff * 3 + 4], "")
        if dirc != self.animations.name:
            self.animations.set_animation(dirc)
        mult = DIAG if xoff and yoff else SPEED
        self.x += xoff * mult
        self.y += yoff * mult