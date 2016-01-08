import os
import sys
import pygame
import importlib
from pygame.locals import *

TILEWIDTH = 128
TILEHEIGHT = 64

FLOORPATH = os.path.join("graphics", "floor_tiles")
OBSTACLEPATH = os.path.join("graphics", "obstacles")
ITEMPATH = os.path.join("graphics", "items")

def load_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Tile():
    def __init__(self, screen, tile_dict, grid_pos, tiletype=None):
        self.screen = screen
        self.tiletype = tiletype
        self.image = tile_dict["image"]
        self.region = tile_dict["region"]
        self.offset = tile_dict["offset"]
        self.grid_pos = grid_pos
        self.isox = (self.grid_pos[0] - self.grid_pos[1]) * (TILEWIDTH // 2) + (self.offset[0] + TILEWIDTH // 2)
        self.isoy = (self.grid_pos[0] + self.grid_pos[1]) * (TILEHEIGHT // 2) + self.offset[1]
    def update(self, current_time=None):
        pass
    def draw(self, screen_offset):
        self.screen.blit(self.image, (self.isox + screen_offset[0], self.isoy + screen_offset[1]), self.region)
class AnimatedTile():
    def __init__(self, screen, tile_dict, grid_pos, tiletype=None):
        self.screen = screen
        self.tiletype = tiletype
        self.images = [info["image"] for info in tile_dict["images"]]
        self.regions = [info["region"] for info in tile_dict["images"]]
        self.offsets = [info["offset"] for info in tile_dict["images"]]
        self.grid_pos = grid_pos
        self.update_interval = 1000 // tile_dict.get("fps", 30)
        self.iso_positions = []
        for offset in self.offsets:
            isox = (self.grid_pos[0] - self.grid_pos[1]) * (TILEWIDTH // 2) + (offset[0] + TILEWIDTH // 2)
            isoy = (self.grid_pos[0] + self.grid_pos[1]) * (TILEHEIGHT // 2) + offset[1]
            self.iso_positions.append([isox, isoy])
        self.frame = 0
        self.current_time = pygame.time.get_ticks()
        self.time_passed = 0
    def switch_frame(self, reverse=False):
        if reverse:
            self.frame -= 1
        else:
            self.frame += 1
        if self.frame >= len(self.images):
            self.frame = 0
        elif self.frame < 0:
            self.frame = len(self.images) - 1
    def update(self, current_time=None, reverse=False):
        if not current_time:
            current_time = pygame.time.get_ticks()
        change_in_time = current_time - self.current_time
        self.time_passed += change_in_time
        self.current_time += change_in_time
        if self.time_passed >= self.update_interval:
            self.switch_frame(reverse)
            self.time_passed = 0
    def draw(self, screen_offset):
        self.screen.blit(self.images[self.frame], (self.iso_positions[self.frame][0] + screen_offset[0], self.iso_positions[self.frame][1] + screen_offset[1]), self.regions[self.frame])
class Floor():
    def __init__(self, screen, tiles):
        self.screen = screen
        self.tiles = tiles
        self.layers = [[]]
    def save(self, path, layers):
        temp_layers = []
        for layer in layers:
            temp_layers.append("")
            for line in layer:
                temp_line = []
                for x in line:
                    if x is None:
                        temp_line.append("-1")
                    else:
                        temp_line.append(str(x.tiletype))
                temp_layers[-1] = temp_layers[-1] + " ".join(temp_line) + "\n"
        with open(path, "w") as f:
            f.write("layers = " + repr(temp_layers))
    def add_layer(self):
        self.layers.append([])
    def load_tilemap(self, tilemap_path):
        
        self.layers = []
        temp = load_module(tilemap_path)
        for layer in temp.layers:
            self.layers.append([])
            for y, line in enumerate(layer.strip().splitlines()):
                self.layers[-1].append([])
                for x, tile in enumerate([int(char) for char in line.split()]):
                    self.layers[-1][-1].append(self.create_tile(tile, (x, y)))
    def replace_tile(self, tile_id, tile_pos, layer):
        self.layers[layer][tile_pos[1]][tile_pos[0]] = self.create_tile(tile_id, tile_pos)
    def create_tile(self, tile_id, grid_pos):
        if tile_id == -1:
            return None
        else:
            tile_dict = self.tiles[tile_id]
            if tile_dict.get("image", None):
                return Tile(self.screen, tile_dict, grid_pos, tile_id)
            else:
                return AnimatedTile(self.screen, tile_dict, grid_pos, tile_id)
    def update(self, current_time=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        for layer in self.layers:
            for line in layer:
                for tile in line:
                    if tile:
                        tile.update(current_time)
    def draw(self, screen_offset):
        for layer in self.layers:
            for line in layer:
                for tile in line:
                    if tile:
                        tile.draw(screen_offset)
