import os
import sys
import pygame
from pygame.locals import *
def stuff():
    print("sdhklfsdjlhfsjfhdklfjjh")

class Button():
    def __init__(self, screen, pos, text, font=None, command=None, number=None):
        self.screen = screen
        self.text = text
        self.font = font
        if self.font == None:
            self.font = pygame.font.Font(None, 20)
        self.font_image = self.font.render(text, True, (255, 255, 255))
        temp_size = self.font.size(text)
        self.textrect = Rect((pos[0] + (100 - temp_size[0]) // 2, pos[1] + (50 - temp_size[1]) // 2), temp_size)
        self.command = command
        self.number = number
        self.image = pygame.image.load("button.png").convert_alpha()
        self.highlighted = False
        self.pressed = False
        self.rect = Rect(pos, (100, 50))
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(mouse_pos)
        if collide:
            self.highlighted = True
        else:
            self.highlighted = False
        if event.type == MOUSEBUTTONDOWN and collide:
            self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            self.pressed = False
            if collide and self.command != None:
                if self.number == None:
                    self.command()
                else:
                    self.command(self.number)
    def draw(self):
        region = [0, 0, 100, 50]
        if self.pressed:
            region = [0, 100, 100, 50]
        elif self.highlighted:
            region = [0, 50, 100, 50]
        self.screen.blit(self.image, self.rect, region)
        self.screen.blit(self.font_image, self.textrect)

class ImageButton():
    def __init__(self, screen, image, pos, command=None, number=None, region=None, size=[128, 64]):
        self.screen = screen
        self.orig_image = image
        self.pos = pos
        self.region = region
        self.command = command
        self.number = number
        self.size = size
        self.pressed = False
        self.calculate()
    def set_pos(self, pos):
        self.pos = pos
        self.calculate()
    def calculate(self):
        image_size = self.orig_image.get_size()
        if self.region == None:
            self.region = [[0, 0], image_size]
        self.image = pygame.Surface(self.region[1], SRCALPHA)
        self.image.blit(self.orig_image, [0, 0], self.region)
        self.image = pygame.transform.smoothscale(self.image, (self.size))
        self.rect = Rect(self.pos, self.size)
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN and collide and event.button == 1:
            self.pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.command != None:
                if self.number == None:
                    self.command()
                else:
                    self.command(self.number)
            self.pressed = False
    def draw(self):
        self.screen.blit(self.image, self.rect)

"""pygame.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font(None, 20)
button = ImageButton(screen, pygame.image.load("../graphics/floor_tiles/floor_tiles_atlas1.png").convert_alpha(), [0, 0], stuff, None, [0, 0, 128, 64])
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        button.update(event)
    button.draw()
    pygame.display.update(button.rect)"""
