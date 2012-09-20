import random
import pygame

from ..panels import draw_rounded_rect


class Fadebox(object):
    FONT = pygame.font.Font(None, 20)
    def __init__(self):
        self.surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        self.temp_surf = pygame.Surface((self.surface.get_width(), self.surface.get_height())).convert()
        self.fade = 255
        self.redraw()

    def redraw(self):
        draw_rounded_rect(self.surface, (0, 0, 0, 0xDD), ((0, 0), (300, 200)), 15)
        for i, x in enumerate("hey you crazy kid!\nStop fading so much!\nStop it!\nOh goddddd".split("\n")):
            self.surface.blit(Fadebox.FONT.render(x, True, (0xFF, ) * 3), (15, 15 + i * 20))

    def blit_alpha(self, surf, (x, y), opacity):
        self.temp_surf.blit(surf, (-x, -y))
        self.temp_surf.blit(self.surface, (0, 0))
        self.temp_surf.set_alpha(opacity)
        surf.blit(self.temp_surf, (x, y))

    def reblit(self, surf):
        self.blit_alpha(surf, (25, 25), self.fade)
        dr = (self.fade % 2) * -4 + 2
        self.fade = min(0xFF, max(self.fade + dr, 0))


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
