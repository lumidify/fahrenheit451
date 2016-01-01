import os
import pygame
pygame.init()
screen = pygame.display.set_mode((0, 0))
from graphics.obstacles.obstacles import *
from graphics.floor_tiles.floor_tiles import *
DROIDPATH = os.path.join("graphics", "droids")
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
def add_to_list(lst, frame, content):
    length = len(lst)
    if frame >= length:
        lst += [None for x in range(frame - length)] + [content]
    else:
        lst[frame] = content
    return lst
def load_droid_atlas(path):
    directions = {0: "SE", 1: "E", 2: "NE", 3: "N", 4: "NW", 5: "W", 6: "SW", 7: "S"}
    images = {
        "N": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "S": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "E": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "W": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "NW": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "NE": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "SW": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []},
        "SE": {"stand": [], "walk": [], "gethit": [], "death": [], "attack": []}
        }
    folderpath = os.path.split(path)[0]
    with open(path) as f:
        image = None
        image_surf = None
        for line in f.readlines():
            if line.startswith("*"):
                image = line.split()[1]
                image_surf = pygame.image.load(os.path.join(folderpath, image)).convert_alpha()
            else:
                line = line.split()
                rot = directions[int(line[0][11])]
                state = line[0][13:-7]
                frame = int(line[0][-5])
                pos = [int(x) for x in line[1:3]]
                size = [int(x) for x in line[3:5]]
                offset = [int(x) for x in line[6:8]]
                images[rot][state] = add_to_list(images[rot][state], frame, {"offset": offset, "pos": pos, "size": size, "image": image_surf})
    return images
def load_character_graphics():
    graphics = {}
    for path in os.listdir(DROIDPATH):
        atlaspath = os.path.join(DROIDPATH, path, "atlas.txt")
        if os.path.exists(atlaspath):
            graphics[path] = load_droid_atlas(atlaspath)
    return graphics
def load_character_configs():
    configs = {}
    for path in os.listdir(DROIDPATH):
        configpath = os.path.join(DROIDPATH, path, "config.txt")
        if os.path.exists(configpath):
            fps = {}
            with open(configpath) as f:
                for line in f.readlines():
                    line_split = line.split("=")
                    if line_split[0].endswith("fps"):
                        fps[line_split[0][:-4]] = 1000 // int(line_split[1].strip())
            configs[path] = fps
    return configs
def load_droid_archetypes():
    characters = {}
    character = {}
    current = ""
    with open(os.path.join(DROIDPATH, "droids.txt")) as f:
        for line in f.readlines():
            if line.startswith("** Start of new Robot: **"):
                if current != "":
                    characters[current] = character
                    character = {}
                    current = ""
            elif line.startswith("#") or line.strip() == "":
                pass
            else:
                line_split = line.split("=")
                value = line_split[1].strip()
                if line_split[0] == "droidname":
                    current = value
                elif line_split[0] in ["class", "drop_item_class", "health", "heal_rate", "experience_reward", "hit_probability"]:
                    value = int(float(value))
                elif line_split[0] in ["speed", "aggression_distance", "time_spent_eyeing_player", "gethit_recover_time"]:
                    value = float(value)
                character[line_split[0]] = value
        characters[current] = character
    return characters
def load_characters():
    characters = load_droid_archetypes()
    configs = load_character_configs()
    graphics = load_character_graphics()
    final_characters = {}
    for character in characters.keys():
        temp = characters[character].copy()
        temp["fps"] = configs[temp["graphics_path"]]
        try:
            temp["images"] = graphics[temp["graphics_path"]]
        except:
            pass
        final_characters[character] = temp
    return final_characters
def load_tiles():
    images = load_images()
    characters = load_characters()
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
    return floor_tiles, obstacles, characters
