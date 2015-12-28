import os
import pygame
pygame.init()
screen = pygame.display.set_mode((0, 0))
from graphics.obstacles.obstacles import *
from graphics.floor_tiles.floor_tiles import *
def load_images():
    images = {}
    with open(os.path.join("graphics", "floor_tiles", "atlas.txt")) as atlas:
        floor_atlas = atlas.readlines()
    with open(os.path.join("graphics", "obstacles", "atlas.txt")) as atlas:
        obstacle_atlas = atlas.readlines()
    for line in floor_atlas:
        line = line.split()
        if line[0].startswith("*"):
            image = line[1]
            image_surf = pygame.image.load(os.path.join("graphics", "floor_tiles", image)).convert_alpha()
        else:
            pos = [int(x) for x in line[1:3]]
            size = [int(x) for x in line[3:5]]
            offset = [int(x) for x in line[6:8]]
            images[line[0]] = {"offset": offset, "image": image_surf, "region": [pos, size]}
    for line in obstacle_atlas:
        line = line.split()
        if line[0].startswith("*"):
            image = line[1]
            image_surf = pygame.image.load(os.path.join("graphics", "obstacles", image)).convert_alpha()
        else:
            pos = [int(x) for x in line[1:3]]
            size = [int(x) for x in line[3:5]]
            offset = [int(x) for x in line[6:8]]
            images[line[0]] = {"offset": offset, "image": image_surf, "region": [pos, size]}
    return images
def load_tiles():
    images = load_images()
    for obstacle in obstacles:
        if type(obstacle["images"]) == str:
            obstacle["images"] = images[obstacle["images"]]
        else:
            obstacle["images"] = [images[image] for image in obstacle["images"]]
    for index, tile in enumerate(floor_tiles):
        if type(tile) == str:
            floor_tiles[index] = images[tile]
        else:
            floor_tiles[index]["images"] = [images[image] for image in floor_tiles[index]["images"]]
    return floor_tiles, obstacles
