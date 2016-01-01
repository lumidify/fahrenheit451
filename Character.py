import os
import sys
import math
import pygame
from pygame.locals import *
from Engine import *
TILEWIDTH = 128
TILEHEIGHT = 64
FONT = pygame.font.Font("Lumidify_Casual.ttf", 20)

class Character():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.direction = kwargs.get("direction", "N")
        self.side = kwargs.get("side", "enemy")
        self.grid_pos = [kwargs.get("x", 0), kwargs.get("y", 0)]
        self.state = "stand"
        self.identifier = kwargs.get("id", None)
        self.label = kwargs.get("label", "DEFAULT NAME")
        self.images = kwargs["images"]
        self.walk_to_points = []
        self.last_walk_to_pos = []
        self.fps = kwargs["fps"]
        self.current_time = kwargs.get("current_time", pygame.time.get_ticks())
        self.time_passed = 0
        self.vel = [0, 0]
        self.speed = kwargs.get("speed", 0.1)
        self.frame = 0
        self.dead = False
        self.perfect_angle = 90
        self.next_delta = [0, 0]
        self.selected = False
        self.direction_angles = {90: "N", 45: "NE", 0: "E", -45: "SE", -90: "S", -135: "SW", 180: "W", -180: "W", 135: "NW"}
        self.realrect = Rect(0, 0, 0, 0)
        self.selectable = True
    def calc_dir_vel(self, deltax=None, deltay=None):
        if not deltax: 
            deltax = self.walk_to_points[0][0] - self.grid_pos[0]
        if not deltay:
            deltay = self.grid_pos[1] - self.walk_to_points[0][1]
        if self.walk_to_points[0] != self.last_walk_to_pos:
            self.last_walk_to_pos = self.walk_to_points[0]
            self.perfect_angle = math.atan2(deltay, deltax)
            self.direction = self.direction_angles[round(math.degrees(self.perfect_angle) / 45) * 45]
            self.vel[0] = math.cos(self.perfect_angle) * self.speed
            self.vel[1] = -math.sin(self.perfect_angle) * self.speed
    def walk(self):
        self.state = "walk"
        deltax = self.walk_to_points[0][0] - self.grid_pos[0]
        deltay = self.grid_pos[1] - self.walk_to_points[0][1]
        self.calc_dir_vel(deltax, deltay)
        next_deltax = self.walk_to_points[0][0] - (self.grid_pos[0] + self.vel[0])
        next_deltay = (self.grid_pos[1] + self.vel[1]) - self.walk_to_points[0][1]
        if abs(deltax) <= abs(next_deltax) and abs(deltay) <= abs(next_deltay):
            self.walk_to_points.pop(0)
            if self.walk_to_points:
                self.calc_dir_vel()
        if self.walk_to_points:
            self.grid_pos[0] += self.vel[0]
            self.grid_pos[1] += self.vel[1]
        else:
            self.state = "stand"
            self.frame = 0
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    def get_rect(self, rect_type):
        if rect_type == "realrect":
            return self.realrect
    def die(self):
        self.state = "death"
        self.frame = 0
    def attack(self):
        self.walk_to_points = []
        self.state = "attack"
        self.frame = 0
    def walk_to(self, points):
        if self.state != "walk":
            self.frame = 0
        self.state = "walk"
        self.walk_to_points = points
    def update(self, current_time=None, event=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        if not self.dead:
            time_change = current_time - self.current_time
            self.time_passed += time_change
            self.current_time = current_time
            if self.time_passed >= self.fps[self.state]:
                self.frame += 1
                self.time_passed = 0
                if self.frame >= len(self.images[self.direction][self.state]):
                    if self.state == "death":
                        self.dead = True
                    elif self.state == "attack":
                        self.state = "stand"
                    self.frame = 0
                if self.walk_to_points:
                    self.walk()
    def draw_label(self):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), self.realrect)
    def draw(self, screen_offset):
        if self.dead:
            tile_dict = self.images[self.direction]["death"][-1]
        else:
            tile_dict = self.images[self.direction][self.state][self.frame]
        isox = (self.grid_pos[0] - self.grid_pos[1]) * (TILEWIDTH // 2) + (tile_dict["offset"][0] + TILEWIDTH // 2)
        isoy = (self.grid_pos[0] + self.grid_pos[1]) * (TILEHEIGHT // 2) + (tile_dict["offset"][1])
        #Update self.realrect here sinc isox and isoy are already computed
        self.realrect = Rect((isox, isoy), tile_dict["size"])
        if not self.selected or self.dead:
            self.screen.blit(tile_dict["image"], (isox, isoy), (tile_dict["pos"], tile_dict["size"]))
        else:
            temp_surf = pygame.surface.Surface(tile_dict["size"]).convert_alpha()
            temp_surf.fill((100, 100, 100, 0))
            temp_surf.blit(tile_dict["image"], (0, 0), (tile_dict["pos"], tile_dict["size"]), BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (isox, isoy))
        if self.walk_to_points:
            line_points = [((x[0] - x[1]) * (TILEWIDTH // 2), (x[0] + x[1]) * (TILEHEIGHT // 2)) for x in self.walk_to_points]
            if len(line_points) > 1:
                pygame.draw.lines(self.screen, (255, 255, 255), False, line_points, 2)
