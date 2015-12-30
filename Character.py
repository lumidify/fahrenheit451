import os
import sys
import math
import pygame
from pygame.locals import *
from Engine import *
TILEWIDTH = 128
TILEHEIGHT = 64

def add_to_list(lst, frame, content):
    length = len(lst)
    if frame >= length:
        lst += [None for x in range(frame - length)] + [content]
    else:
        lst[frame] = content
    return lst

class Character():
    def __init__(self, screen, atlas, config, **kwargs):
        self.screen = screen
        self.atlas = atlas
        self.config = config
        self.path = os.path.split(self.atlas)[0]
        self.direction = kwargs.get("direction", "N")
        self.side = kwargs.get("side", "enemy")
        self.pos = kwargs.get("pos", [0, 0])
        self.state = kwargs.get("state", "stand")
        self.walk_to_points = []
        self.last_walk_to_pos = []
        self.current_time = kwargs.get("current_time", pygame.time.get_ticks())
        self.time_passed = 0
        self.vel = [0, 0]
        self.frame = 0
        self.dead = False
        self.perfect_angle = 90
        self.next_delta = [0, 0]
        self.parse_config()
        self.selected = False
        self.directions = {0: "SE", 1: "E", 2: "NE", 3: "N", 4: "NW", 5: "W", 6: "SW", 7: "S"}
        self.direction_angles = {90: "N", 45: "NE", 0: "E", -45: "SE", -90: "S", -135: "SW", 180: "W", -180: "W", 135: "NW"}
        self.images = {
            "N": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "S": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "E": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "W": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "NW": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "NE": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "SW": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
            "SE": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []}
            }
        self.load()
    def parse_config(self):
        self.fps = {}
        with open(self.config) as f:
            for line in f.readlines():
                line_split = line.split("=")
                if line_split[0] == "health":
                    self.health = int(line_split[1][:-1])
                elif line_split[0] == "speed":
                    self.speed = float(line_split[1][:-1])
                elif line_split[0].endswith("fps"):
                    self.fps[line_split[0][:-4]] = 1000 // int(line_split[1][:-1])
    def load(self):
        f = open(self.atlas)
        image = None
        image_surf = None
        for line in f.readlines():
            if line.startswith("*"):
                image = line.split()[1]
                image_surf = pygame.image.load(os.path.join(self.path, image)).convert_alpha()
            else:
                line = line.split()
                rot = self.directions[int(line[0][11])]
                state = line[0][13:-7]
                frame = int(line[0][-5])
                pos = [int(x) for x in line[1:3]]
                size = [int(x) for x in line[3:5]]
                offset = [int(x) for x in line[6:8]]
                self.images[rot][state] = add_to_list(self.images[rot][state], frame, {"offset": offset, "pos": pos, "size": size, "image": image_surf})
        f.close()
    def calc_dir_vel(self, deltax=None, deltay=None):
        if not deltax: 
            deltax = self.walk_to_points[0][0] - self.pos[0]
        if not deltay:
            deltay = self.pos[1] - self.walk_to_points[0][1]
        if self.walk_to_points[0] != self.last_walk_to_pos:
            self.last_walk_to_pos = self.walk_to_points[0]
            self.perfect_angle = math.atan2(deltay, deltax)
            self.direction = self.direction_angles[round(math.degrees(self.perfect_angle) / 45) * 45]
            self.vel[0] = math.cos(self.perfect_angle) * self.speed
            self.vel[1] = -math.sin(self.perfect_angle) * self.speed
    def walk(self):
        self.state = "walk"
        deltax = self.walk_to_points[0][0] - self.pos[0]
        deltay = self.pos[1] - self.walk_to_points[0][1]
        self.calc_dir_vel(deltax, deltay)
        next_deltax = self.walk_to_points[0][0] - (self.pos[0] + self.vel[0])
        next_deltay = (self.pos[1] + self.vel[1]) - self.walk_to_points[0][1]
        if abs(deltax) <= abs(next_deltax) and abs(deltay) <= abs(next_deltay):
            self.walk_to_points.pop(0)
            if self.walk_to_points:
                self.calc_dir_vel()
        if self.walk_to_points:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
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
    def die(self):
        self.state = "death"
        self.frame = 0
    def attack(self):
        self.walk_to_points = []
        self.state = "attack"
        self.frame = 0
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
    def draw(self):
        if self.dead:
            tile_dict = self.images[self.direction]["death"][-1]
        else:
            tile_dict = self.images[self.direction][self.state][self.frame]
        isox = (self.pos[0] - self.pos[1]) * (TILEWIDTH // 2) + (tile_dict["offset"][0] + TILEWIDTH // 2)
        isoy = (self.pos[0] + self.pos[1]) * (TILEHEIGHT // 2) + (tile_dict["offset"][1])
        if not self.selected:
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
