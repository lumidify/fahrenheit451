import os
import sys
import pygame
from pygame.locals import *

TILEWIDTH = 128
TILEHEIGHT = 64

class ObstacleMap():
    def __init__(self, atlas):
        self.atlas = atlas
        self.objects = []
        self.path = os.path.split(self.atlas)[0]
        self.load()
    def load(self):
        f = open(self.atlas)
        image = None
        image_surf = None
        for line in f.readlines():
            if line.startswith("*"):
                image = line.split()[1]
                image_surf = pygame.image.load(os.path.join(self.path, image))
            else:
                line = line.split()
                pos = [int(x) for x in line[1:3]]
                size = [int(x) for x in line[3:5]]
                offset = [int(x) for x in line[6:8]]
                self.objects.append({"offset": offset, "pos": pos, "size": size, "image": image_surf})
        f.close()
    def draw(self, screen, tiles):
        for y, line in enumerate(tiles):
            for x, tile in enumerate(line):
                if tile != -1:
                    tile_dict = self.objects[tile]
                    isox = (x - y) * (TILEWIDTH // 2) + (tile_dict["offset"][0] + TILEWIDTH // 2)
                    isoy = (x + y) * (TILEHEIGHT // 2) + (tile_dict["offset"][1] + TILEHEIGHT // 2)
                    screen.blit(tile_dict["image"], (isox, isoy), (tile_dict["pos"], tile_dict["size"]))

class TileMap():
    def __init__(self, atlas):
        self.atlas = atlas
        self.tiles = []
        self.path = os.path.split(self.atlas)[0]
        self.load()
    def load(self):
        f = open(self.atlas)
        image = None
        image_surf = None
        for line in f.readlines():
            if line.startswith("*"):
                image = line.split()[1]
                image_surf = pygame.image.load(os.path.join(self.path, image))
            else:
                line = line.split()
                pos = [int(x) for x in line[1:3]]
                size = [int(x) for x in line[3:5]]
                offset = [int(x) for x in line[6:8]]
                self.tiles.append({"offset": offset, "pos": pos, "size": size, "image": image_surf})
        f.close()
    def draw(self, screen, tiles):
        for y, line in enumerate(tiles):
            for x, tile in enumerate(line):
                tile_dict = self.tiles[tile]
                isox = (x - y) * (TILEWIDTH // 2) + (tile_dict["offset"][0] + TILEWIDTH // 2)
                isoy = (x + y) * (TILEHEIGHT // 2) + (tile_dict["offset"][1] + TILEHEIGHT // 2)
                screen.blit(tile_dict["image"], (isox, isoy), (tile_dict["pos"], tile_dict["size"]))
pygame.init()
tilemap = TileMap(os.path.join("graphics", "floor_tiles", "atlas.txt"))
obstaclemap = ObstacleMap(os.path.join("graphics", "obstacles", "atlas.txt"))
screen_info = pygame.display.Info()
screen_size = [screen_info.current_w, screen_info.current_h]
screen = pygame.display.set_mode(screen_size, RESIZABLE)

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            screen_size = event.dict["size"]
            screen = pygame.display.set_mode(screen_size, RESIZABLE)
    tilemap.draw(screen, [[35, 35, 35, 35, 35, 58, 11, 11, 11, 25, 29],
                          [35, 35, 35, 35, 35, 24, 11, 11, 11, 11, 12],
                          [35, 35, 35, 35, 35, 30, 11, 11, 11, 13, 18]])
    
    obstaclemap.draw(screen, [[-1, -1, -1, -1, -1, 35]])
    pygame.display.update()
