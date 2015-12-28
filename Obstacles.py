import os
import sys
import pygame
from Grid2D import *
from Floor import *
from CONSTANTS import *
from loader import *
from pygame.locals import *

#Sorting: bob.sort(key=lambda x: x.pos[1], x.pos[0])

def calculate_rect(grid_pos, borders):
    return Rect((
    grid_pos[0] + borders[0]) * WIDTH,
    (grid_pos[1] + borders[2]) * HEIGHT,
    (abs(borders[0]) + abs(borders[1])) * WIDTH,
    (abs(borders[2]) + abs(borders[3])) * HEIGHT)
class BasicObstacle():
    def __init__(self, grid_pos, width, height):
        self.grid_pos = grid_pos
        self.rect = Rect(grid_pos[0] * WIDTH, grid_pos[1] * HEIGHT, width * WIDTH, height * HEIGHT)
    def update(self, *args):
        pass
    def get_rect(rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return Rect(0, 0, 0, 0)
    def draw(self, *args):
        pass
class Obstacle(Tile):
    def __init__(self, screen, tile_dict, grid_pos, borders=[0, 0, 0, 0], onclick=None):
        super().__init__(screen, tile_dict, grid_pos)
        self.rect = calculate_rect(grid_pos, borders)
        self.realrect = Rect((self.isox, self.isoy), self.region[1])
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
class AnimatedObstacle(AnimatedTile):
    def __init__(self, screen, tile_dict, grid_pos, borders=[0, 0, 0, 0], onclick=None):
        super().__init__(screen, tile_dict, grid_pos)
        self.rect = calculate_rect(grid_pos, borders)
        self.realrect = Rect(self.iso_positions[0], self.regions[0][1])
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
class Item(Obstacle):
    def __init__(self, screen, tile_dict, grid_pos, tooltip, font):
        super().__init__(screen, tile_dict, grid_pos)
        if self.region:
            self.realrect = Rect((self.isox, self.isoy), self.region[1])
        else:
            self.realrect = Rect((self.isox, self.isoy), (abs(self.offset[0] * 2), abs(self.offset[1] * 2)))
        self.tooltip = tooltip
        self.tooltip_surf = font.render(self.tooltip, True, (255, 255, 255))
        text_size = font.size(tooltip)
        self.tooltip_pos = [self.realrect.centerx - text_size[0] // 2, self.isoy - text_size[1]]
        self.highlighted = False
    def rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def update(self, mouse_pos=None):
        if not mouse_pos:
            mouse_pos = pygame.mouse.get_pos()
        if self.realrect.collidepoint(mouse_pos):
            self.highlighted = True
        else:
            self.highlighted = False
    def draw(self, screen_offset):
        super().draw(screen_offset)
        if self.highlighted:
            self.screen.blit(self.tooltip_surf, self.tooltip_pos)

class Obstacles():
    def __init__(self, screen, obstacles, mapsize):
        self.screen = screen
        self.obstacles = obstacles
        self.mapsize = mapsize
        self.grid = Grid2D(mapsize)
        self.layers = [[]]
        self.reserves = {}
    def replace_index(self, index, new_id):
        pass
    def replace_id(self, old_id, new_id):
        pass
    def create_obstacle(self, info):
        if info["type"] == "RECT":
            return BasicObstacle((info["x"], info["y"]), info["width"], info["height"])
        else:
            tile_dict = self.obstacles[int(info["type"])]
            if type(tile_dict["images"]) == dict:
                return Obstacle(self.screen, tile_dict["images"], (info["x"], info["y"]), tile_dict.get("borders", [0, 0, 0, 0]))
            else:
                return AnimatedObstacle(self.screen, tile_dict, (info["x"], info["y"]), tile_dict.get("borders", [0, 0, 0, 0]))
    def add_layer(self):
        self.layers.append([])
    def load_obstaclemap(self, path, layer):
        self.layers[layer] = []
        with open(path) as f:
            maplines = f.readlines()
        state = ""
        obs = {}
        for line in maplines:
            if line != "\n" and not line.startswith("#"):
                if line.startswith("***reserve obs***"):
                    state = "reserve"
                elif line.startswith("***current obs***"):
                    state = "current"
                elif line.startswith("*obs"):
                    if len(obs) > 0:
                        if state == "reserve":
                            self.reserves[obs["id"]] = self.create_obstacle(obs)
                        elif state == "current":
                            self.layers[layer].append(self.create_obstacle(obs))
                    obs = {"type": line.split()[1]}
                else:
                    line_split = line.split("=")
                    value = line_split[1].strip()
                    if line_split[0] in ["x", "y", "height", "width"]:
                        value = float(value)
                    obs[line_split[0]] = value
        if len(obs) > 0:
            if state == "reserve":
                self.reserves[obs["id"]] = self.create_obstacle(obs)
            elif state == "current":
                self.layers[layer].append(self.create_obstacle(obs))
        self.layers[layer].sort(key=lambda x: (x.grid_pos[1], x.grid_pos[0]))
        temp = []
        for layer in self.layers:
            temp += layer
        self.grid.obstacles = temp
        self.grid.refresh()
    def update(self, current_time=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        for layer in self.layers:
            for obstacle in layer:
                obstacle.update(current_time)
    def draw(self, screen_offset=[0, 0]):
        for layer in self.layers:
            for obstacle in layer:
                obstacle.draw(screen_offset)
