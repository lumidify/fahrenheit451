import os
import sys
import pygame
from Engine import *
from pygame.locals import *
from Character import *

TILEWIDTH = 128
TILEHEIGHT = 64

class Montag(Character):
    def __init__(self, screen, **kwargs):
        kwargs["side"] = "montag"
        super().__init__(screen, **kwargs)
        self.pressed = False
        self.pathfinding_grid = kwargs.get("pathfinding_grid", None)
        self.target_image = pygame.image.load("graphics/cursors/mouse_move_cursor_0.png").convert_alpha()
        self.last_mouse_pos = ()
        self.quests = {"open": [], "done": []}
    def has_quest(self, quest):
        if quest in self.quests["open"] or quest in self.quests["done"]:
            return True
        else:
            return False
    def finished_quest(self, quest):
        if quest in self.quests["done"]:
            return True
        else:
            return False
    def add_quest(self, quest):
        self.quests["open"].append(quest)
    def finish_quest(self, quest):
        try:
            self.quests["open"].remove(quest)
            self.quests["done"].append(quest)
        except:
            print("WARNING: Tried to remove unknown quest.")
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
                    self.walk_to(new_path)
        super().update(current_time)
    def draw(self, screen_offset):
        if self.walk_to_points:
            isox = (self.walk_to_points[-1][0] - self.walk_to_points[-1][1]) * (TILEWIDTH // 2) + 49
            isoy = (self.walk_to_points[-1][0] + self.walk_to_points[-1][1]) * (TILEHEIGHT // 2) - 7
            self.screen.blit(self.target_image, (isox + screen_offset[0], isoy + screen_offset[1]))
        super().draw()
