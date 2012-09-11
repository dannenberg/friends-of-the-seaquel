import pygame
import random


pygame.font.init()

def draw_rounded_rect(surf, color, rect, radius):
    r1x = rect[0][0] + radius
    r2x = rect[0][0]
    r1y = rect[0][1]
    r2y = rect[0][1] + radius
    w, h = rect[1]
    pygame.draw.rect(surf, color, ((r1x, r1y), (w - radius * 2, h)))
    pygame.draw.rect(surf, color, ((r2x, r2y), (w, h - radius * 2)))
    for pos in ((r1x, r2y), (w + r2x - radius, r2y),
                (r1x, h + r1y - radius), (w + r2x - radius, h + r1y - radius)):
        pygame.draw.circle(surf, color, pos, radius)

class UsersInfoPanel(object):
    CELLSPACING = 10
    FONT = pygame.font.Font(None, 32)
    def __init__(self):
        self.surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        self.redraw()

    def redraw(self):
        w, h  = self.surface.get_size()
        CS = UsersInfoPanel.CELLSPACING
        draw_rounded_rect(self.surface, (0, 0, 0, 0xDD),
            ((0, 0), (w, h)), 15)
        #players = ("One", "Two", "Three")
        players = ("One", "Two", "Three", "Four", "Five", "Six")
        cell_height = (h - CS) // len(players)
        for i, p in enumerate(players):
            self.surface.blit(UserPanel(p, w - CS * 2, cell_height - CS),
                (CS, CS + i * cell_height))

    def reblit(self, surf):
        surf.blit(self.surface, (150, 25))

class UserPanel(pygame.Surface):
    def __init__(self, player, cell_width, cell_height):
        super(UserPanel, self).__init__((cell_width, cell_height), pygame.SRCALPHA)
        draw_rounded_rect(self, (0x33, 0x33, 0x33, 0xDD),
            ((0, 0), (cell_width, cell_height)), 10)
        self.blit(UsersInfoPanel.FONT.render(player, True, (0xFF, ) * 3), (5, 5))
        self.draw_bars(random.randint(0, 5))
        self.draw_dungeon_progress()

    def draw_dungeon_progress(self):
        for x in xrange(8):
            loc = (15 + 15 * x, 40)
            pygame.draw.circle(self, (0x66, ) * 3, loc, 5)
            pygame.draw.circle(self, (0, 0, 0), loc, 5, 2)

    def draw_bars(self, strength):
        width = 16
        NUM_BARS = 5
        offx, offy = self.get_width() - width - 5, 5
        interval = width // NUM_BARS
        frac = (float(strength) - 1) / (NUM_BARS - 1)

        divme = max((1 - frac), frac)

        color = map(int, (0xFF * (1 - frac) / divme, 0xFF * frac / divme, 0))
        for x in xrange(NUM_BARS):
            if strength == x:
                color = (0x66, ) * 3
            pygame.draw.rect(self, color,
                ((x * interval + offx, width - interval * (x + 1) + offy),
                (interval, interval * (x + 1) - 1)))
