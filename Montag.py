import os
import sys
import pygame
from Engine import *
from pygame.locals import *
from Character import *

TILEWIDTH = 128
TILEHEIGHT = 64

class Montag(Character):
    def __init__(self, screen, atlas, config, pathfinding_grid, pos=[0, 0], direction="N", state="stand"):
        super().__init__(screen, atlas, config, pos=pos, direction=direction, state=state, side="Montag")
        self.pathfinding_grid = pathfinding_grid
        self.pressed = False
        self.target_image = pygame.image.load("graphics/cursors/mouse_move_cursor_0.png").convert_alpha()
        self.last_mouse_pos = ()
    def update(self, current_time=None, event=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        if not self.dead:
            mouse_pos = pygame.mouse.get_pos()
            if event:
                if event.type == MOUSEBUTTONDOWN:
                    self.pressed = True
                elif event.type == MOUSEBUTTONUP:
                    self.pressed = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.attack()
            temp_time_passed = self.time_passed + (current_time - self.current_time)
            if temp_time_passed >= self.fps[self.state] and self.pressed and mouse_pos != self.last_mouse_pos:
                self.last_mouse_pos = mouse_pos
                mouse_pos = [mouse_pos[0] - TILEWIDTH // 2, mouse_pos[1]]
                x = ((mouse_pos[0] / (TILEWIDTH // 2)) + (mouse_pos[1] / (TILEHEIGHT // 2))) / 2
                y = (((mouse_pos[0] / (TILEWIDTH // 2)) - mouse_pos[1] / (TILEHEIGHT // 2))) / -2
                new_path = self.pathfinding_grid.find_path(tuple(self.pos), (x, y))
                if new_path:
                    self.state = "walk"
                    self.walk_to_points = new_path
        super().update(current_time)
    def draw(self):
        if self.walk_to_points:
            isox = (self.walk_to_points[-1][0] - self.walk_to_points[-1][1]) * (TILEWIDTH // 2) + 49
            isoy = (self.walk_to_points[-1][0] + self.walk_to_points[-1][1]) * (TILEHEIGHT // 2) - 7
            self.screen.blit(self.target_image, (isox, isoy))
        super().draw()
