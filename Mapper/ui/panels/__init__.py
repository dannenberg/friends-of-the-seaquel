import pygame

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