import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 700))
"""a = pygame.image.load("test2.png").convert_alpha()
b = pygame.image.load("title.jpg").convert_alpha()
c = pygame.surface.Surface((1000, 700)).convert_alpha()
while True:
    screen.blit(b, (0, 0))
    c.fill((0, 0, 0, 200))
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            raise Exception("YourMomError")
    c.blit(a, (pos[0] - 512, pos[1] - 256), None, BLEND_RGBA_SUB)
    screen.blit(c, (0, 0))
    pygame.display.update()"""
a = pygame.image.load("graphics/droids/blue_guard/blue_guard_1.png").convert_alpha()
c = pygame.surface.Surface(a.get_size()).convert_alpha()
c.fill((100, 100, 100, 0))
c.blit(a, (0, 0), None, BLEND_RGBA_ADD)
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            raise Exception("YourMomError")
    if Rect((0, 0), a.get_size()).collidepoint(pygame.mouse.get_pos()):
        screen.blit(c, (0, 0))
    else:
        screen.blit(a, (0, 0))
    pygame.display.update()
