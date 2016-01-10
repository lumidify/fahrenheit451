import os
import sys
import math
import pygame
import loader
import importlib
import tkinter as tk
from QuadTree import *
from tkinter import ttk
from CONSTANTS import *
from pygame.locals import *

TILEWIDTH = 128
TILEHEIGHT = 64

def load_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def calculate_rect(grid_pos, borders):
    return Rect((
    grid_pos[0] + borders[0]) * WIDTH,
    (grid_pos[1] + borders[2]) * HEIGHT,
    (abs(borders[0]) + abs(borders[1])) * WIDTH,
    (abs(borders[2]) + abs(borders[3])) * HEIGHT)

class Floor():
    def __init__(self, screen, tiles):
        self.screen = screen
        self.tiles = tiles
        self.layers = []
        self.default_tile = pygame.image.load("grid.png").convert_alpha()
        self.size = [0, 0]
    def populate_listbox(self, listbox):
        listbox.delete(0, "end")
        for x in range(len(self.layers)):
            listbox.insert("end", "Layer " + str(x))
    def insert_layer(self, index, listbox):
        self.layers.insert(index, [[-1 for x in range(self.size[0])] for y in range(self.size[1])])
        self.populate_listbox(listbox)
    def remove_layer(self, index, listbox):
        self.layers.pop(index)
        self.populate_listbox(listbox)
    def load_tilemap(self, tilemap_path, size):
        self.layers = []
        self.size = size
        temp = load_module(tilemap_path)
        for layer in temp.layers:
            self.layers.append([])
            for line in layer.strip().splitlines():
                self.layers[-1].append([int(x) for x in line.strip().split()])
        self.change_size()
    def replace_tile(self, tile_id, tile_pos, layer):
        self.layers[layer][tile_pos[1]][tile_pos[0]] = tile_id
    def create_map(self, size):
        self.size = size
        self.layers = [[]]
        self.change_size()
    def change_size(self):
        if self.size[0] == 0 or self.size[1] == 0:
            self.layers = [[] for x in self.layers]
        for layer in self.layers:
            for line in layer:
                if len(line) > self.size[0]:
                    line[:] = line[:self.size[0]]
                elif len(line) < self.size[0]:
                    line += [-1 for x in range(self.size[0] - len(line))]
            if len(layer) > self.size[1]:
                layer[:] = layer[:self.size[1]]
            elif len(layer) < self.size[1]:
                layer += [[-1 for x in range(self.size[0])] for y in range(self.size[1]- len(layer))]
    def save(self, path):
        temp_layers = []
        for layer in self.layers:
            temp_layers.append("")
            max_width = 0
            for line in layer:
                line = [str(x) for x in line]
                line_max = max([len(x) for x in line])
                if line_max > max_width:
                    max_width = line_max
            for line in layer:
                temp_layers[-1] = temp_layers[-1] + " ".join([str(x).rjust(max_width) for x in line]) + "\n"
        with open(path, "w") as f:
            f.write("layers = " + repr(temp_layers))
    def draw_cursor(self, tile_id, pos, screen_offset):
        if tile_id != -1:
            tile_dict = self.tiles[tile_id]
            if not tile_dict.get("image", None):
                tile_dict = tile_dict["images"][0]
            isox = (pos[0] - pos[1]) * (TILEWIDTH // 2) + tile_dict["offset"][0]
            isoy = (pos[0] + pos[1]) * (TILEHEIGHT // 2) + tile_dict["offset"][1] + TILEHEIGHT // 2
            self.screen.blit(tile_dict["image"], (isox + screen_offset[0], isoy + screen_offset[1]), tile_dict["region"])
    def draw(self, screen_offset):
        if self.layers:
            for layer in self.layers:
                for line_index, line in enumerate(layer):
                    for tile_index, tile in enumerate(line):
                        if tile != -1:
                            tile_dict = self.tiles[tile]
                            if not tile_dict.get("image", None):
                                tile_dict = tile_dict["images"][0]
                            isox = (tile_index - line_index) * (TILEWIDTH // 2) + tile_dict["offset"][0]
                            isoy = (tile_index + line_index) * (TILEHEIGHT // 2) + tile_dict["offset"][1] + TILEHEIGHT // 2
                            self.screen.blit(tile_dict["image"], (isox + screen_offset[0], isoy + screen_offset[1]), tile_dict["region"])
            for y in range(len(self.layers[0])):
                for x in range(len(self.layers[0][0])):
                    isox = (x - y) * (TILEWIDTH // 2) - 64
                    isoy = (x + y) * (TILEHEIGHT // 2)
                    self.screen.blit(self.default_tile, (isox + screen_offset[0], isoy + screen_offset[1]))

class BasicObstacle():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.width = kwargs.get("width", 1)
        self.height = kwargs.get("height", 1)
        self.type = kwargs.get("type", "RECT")
        self.identifier = kwargs.get("identifier", None)
        self.selected = False
        self.generate_points()
    def set_values(self, **kwargs):
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.width = kwargs.get("width", self.width)
        self.height = kwargs.get("height", self.height)
        self.identifier = kwargs.get("identifier", self.identifier)
        self.generate_points()
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def generate_points(self):
        self.rect = Rect(self.x * WIDTH, self.y * HEIGHT, self.width * WIDTH, self.height * HEIGHT)
        self.topleft = ((self.x - self.y) * (TILEWIDTH // 2), (self.x + self.y) * (TILEHEIGHT // 2))
        self.bottomleft = ((self.x - (self.y + self.height)) * (TILEWIDTH // 2), (self.x + self.y + self.height) * (TILEHEIGHT // 2))
        self.topright = ((self.x + self.width - self.y) * (TILEWIDTH // 2), (self.x + self.width + self.y) * (TILEHEIGHT // 2))
        self.bottomright = ((self.x + self.width - (self.y + self.height)) * (TILEWIDTH // 2), (self.x + self.width + self.y + self.height) * (TILEHEIGHT // 2))
    def resize(self, height, width):
        self.height = height
        self.width = width
        self.generate_points()
    def move(self, x, y):
        self.x = x
        self.y = y
        self.generate_points()
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
    def get_dict(self):
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height, "type": self.type}
    def draw(self, screen_offset):
        if self.selected:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        points = []
        for point in [self.topleft, self.topright, self.bottomright, self.bottomleft]:
            points.append([point[0] + screen_offset[0], point[1] + screen_offset[1]])
        pygame.draw.lines(self.screen, color, True, points, 5)
class Trigger(BasicObstacle):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self.trigger = kwargs.get("trigger", None)
        self.deactivate_after_use = kwargs.get("deactivate_after_use", False)
        self.active = kwargs.get("active", True)
    def set_values(self, **kwargs):
        super().set_values(**kwargs)
        self.trigger = kwargs.get("trigger", self.trigger)
        self.deactivate_after_use = kwargs.get("deactivate_after_use", self.deactivate_after_use)
        self.active = kwargs.get("active", self.active)
    def get_dict(self):
        temp = {"x": self.x, "y": self.y, "width": self.width, "height": self.height, "trigger": self.trigger}
        if self.deactivate_after_use:
            temp.update({"deactivate_after_use": self.deactivate_after_use})
        if not self.active:
            temp.update({"active": self.active})
        return temp
class Obstacle():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.type = kwargs.get("type", None)
        self.image = kwargs["images"]["image"]
        self.region = kwargs["images"]["region"]
        self.offset = kwargs["images"]["offset"]
        self.borders = kwargs.get("borders", [0, 0, 0, 0])
        self.selected = False
        self.identifier = kwargs.get("id", None)
        self.onclick = kwargs.get("onclick", None)
        self.action = kwargs.get("action", None)
        self.animation = kwargs.get("animation", None)
        self.after_looting = kwargs.get("after_looting", None)
        self.label = kwargs.get("label", None)
        self.items = kwargs.get("items", None)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.set_values()
    def set_values(self, **kwargs):
        self.identifier = kwargs.get("identifier", self.identifier)
        self.onclick = kwargs.get("onclick", self.onclick)
        self.action = kwargs.get("action", self.action)
        self.animation = kwargs.get("animation", self.animation)
        self.after_looting = kwargs.get("after_looting", self.after_looting)
        self.label = kwargs.get("label", self.label)
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.items = kwargs.get("items", self.items)
        self.rect = calculate_rect((self.x, self.y), self.borders)
        self.isox = (self.x - self.y) * (TILEWIDTH // 2) + self.offset[0]
        self.isoy = (self.x + self.y) * (TILEHEIGHT // 2) + self.offset[1] + TILEHEIGHT // 2
        self.realrect = Rect((self.isox, self.isoy), self.region[1])
    def get_dict(self):
        temp = {"type": self.type, "x": self.x, "y": self.y, "id": self.identifier, "onclick": self.onclick, "action": self.action, "animation": self.animation, "after_looting": self.after_looting, "label": self.label, "items": self.items}
        final = {}
        for key, item in temp.items():
            if item is not None and item != [""] and item != "" and item != []:
                final[key] = item
        return final
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def draw(self, screen_offset):
        if self.selected:
            temp_surf = pygame.surface.Surface(self.realrect.size).convert_alpha()
            temp_surf.fill((255, 0, 0, 0))
            temp_surf.blit(self.image, (0, 0), self.region, BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
        else:
            self.screen.blit(self.image, (self.isox + screen_offset[0], self.isoy + screen_offset[1]), self.region)
class Item():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.image = kwargs.get("ingame", None)
        self.item_info = kwargs.get("item_info", None)
        self.offset = kwargs.get("offset", None)
        self.selected = False
        self.type = kwargs.get("type")
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.identifier = kwargs.get("id", None)
        self.label = kwargs.get("label", None)
        self.set_values()
    def set_values(self, **kwargs):
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.isox = (self.x - self.y) * (TILEWIDTH // 2) + self.offset[0]
        self.isoy = (self.x + self.y) * (TILEHEIGHT // 2) + self.offset[1] + TILEHEIGHT // 2
        self.realrect = Rect((self.isox, self.isoy), self.image.get_size())
        self.identifier = kwargs.get("identifier", self.identifier)
        self.label = kwargs.get("label", self.label)
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def get_rect(self, rect_type):
        if rect_type == "realrect":
            return self.realrect
    def get_dict(self):
        temp = {"type": self.type, "x": self.x, "y": self.y}
        if self.identifier is not None:
            temp["id"] = self.identifier
        if self.label != self.item_info.get("label", None):
            temp["label"] = self.label
        return temp
    def draw(self, screen_offset):
        if self.selected:
            temp_surf = pygame.surface.Surface(self.realrect.size).convert_alpha()
            temp_surf.fill((255, 0, 0, 0))
            temp_surf.blit(self.image, (0, 0), [(0, 0), self.realrect.size], BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
        else:
            self.screen.blit(self.image, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
class Character():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.type = kwargs.get("droidname", None)
        self.orig_info = kwargs.get("orig_info", {})
        self.images = kwargs["images"]
        self.frame = 0
        self.selected = False
        self.realrect = Rect(0, 0, 0, 0)
        self.state = "stand"
        self.dead = kwargs.get("dead", False)
        self.ondeath = kwargs.get("ondeath", None)
        self.weapon = kwargs.get("weapon", None)
        self.label = kwargs.get("label", "DEFAULT NAME")
        self.identifier = kwargs.get("id", None)
        self.aggression_distance = kwargs.get("aggression_distance", 2)
        self.y = kwargs.get("y", 0)
        self.x = kwargs.get("x", 0)
        self.direction = kwargs.get("direction", "N")
        self.health = kwargs.get("health", 10)
        self.random_walk_area = kwargs.get("random_walk_area", [])
        self.waypoints = kwargs.get("waypoints", [])
        self.set_values()
    def set_values(self, **kwargs):
        self.dead = kwargs.get("dead", self.dead)
        self.ondeath = kwargs.get("ondeath", self.ondeath)
        self.weapon = kwargs.get("weapon", self.weapon)
        self.label = kwargs.get("label", self.label)
        self.identifier = kwargs.get("identifier", self.identifier)
        self.aggression_distance = kwargs.get("aggression_distance", self.aggression_distance)
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.direction = kwargs.get("direction", self.direction)
        self.health = kwargs.get("health", self.health)
        self.random_walk_area = kwargs.get("random_walk_area", self.random_walk_area)
        self.waypoints = kwargs.get("waypoints", self.waypoints)
        
        if self.dead:
            self.tile_dict = self.images[self.direction]["death"][-1]
        else:
            self.tile_dict = self.images[self.direction][self.state][self.frame]
        self.isox = (self.x - self.y) * (TILEWIDTH // 2) + self.tile_dict["offset"][0]
        self.isoy = (self.x + self.y) * (TILEHEIGHT // 2) + self.tile_dict["offset"][1] + TILEHEIGHT // 2
        self.realrect = Rect((self.isox, self.isoy), self.tile_dict["size"])
        self.calculate_points()
    def calculate_points(self):
        self.final_waypoints = []
        self.final_walk_area = None
        if self.waypoints:
            for point in self.waypoints:
                self.final_waypoints.append([(point[0] - point[1]) * (TILEWIDTH // 2), (point[0] + point[1]) * (TILEHEIGHT // 2)])
        if self.random_walk_area:
            self.final_walk_area = BasicObstacle(self.screen, x=self.random_walk_area[0], y=self.random_walk_area[1], width=self.random_walk_area[2], height=self.random_walk_area[3])
            self.final_walk_area.select()
    def get_dict(self):
        temp = {"x": self.x, "y": self.y, "name": self.type}
        if self.direction != "N":
            temp["direction"] = self.direction
        if self.health != self.orig_info.get("health", 10):
            temp["health"] = self.health
        if self.aggression_distance != self.orig_info["aggression_distance"]:
            temp["aggression_distance"] = self.aggression_distance
        if self.identifier is not None:
            temp["id"] = self.identifier
        if self.label != self.orig_info["label"]:
            temp["label"] = self.label
        if self.weapon is not None and self.weapon != self.orig_info["weapon"]:
            temp["weapon"] = self.weapon
        if self.ondeath is not None:
            temp["ondeath"] = self.ondeath
        if self.dead:
            temp["dead"] = self.dead
        if self.waypoints:
            temp["waypoints"] = self.waypoints
        if self.random_walk_area:
            temp["random_walk_area"] = self.random_walk_area
        return temp
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def get_rect(self, rect_type):
        if rect_type == "realrect":
            return self.realrect
    def draw(self, screen_offset):
        if self.selected:
            if self.waypoints and len(self.final_waypoints) > 1:
                points = []
                for point in self.final_waypoints:
                    points.append([point[0] + screen_offset[0], point[1] + screen_offset[1]])
                pygame.draw.lines(self.screen, (255, 0, 0), True, points, 5)
            if self.random_walk_area:
                self.final_walk_area.draw(screen_offset)
        if self.selected and not self.dead:
            temp_surf = pygame.surface.Surface(self.tile_dict["size"]).convert_alpha()
            temp_surf.fill((255, 0, 0, 0))
            temp_surf.blit(self.tile_dict["image"], (0, 0), (self.tile_dict["pos"], self.tile_dict["size"]), BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
        else:
            self.screen.blit(self.tile_dict["image"], (self.isox + screen_offset[0], self.isoy + screen_offset[1]), (self.tile_dict["pos"], self.tile_dict["size"]))
class Obstacles():
    def __init__(self, screen, obstacles, characters, items):
        self.screen = screen
        self.obstacles = obstacles
        self.characters = characters
        self.items = items
        
        self.layers = [[], []]
        self.rect_obstacles = []
        self.charactermap = []
        self.triggers = []
        self.item_map = []
        
        self.selected = None
        self.screen_offset = [0, 0]
        self.properties_frame = None
    def save(self, path):
        final_characters = [character.get_dict() for character in self.charactermap]
        final_items = [item.get_dict() for item in self.item_map]
        final_triggers = [trigger.get_dict() for trigger in self.triggers]
        final_obstacles = [[obstacle.get_dict() for obstacle in self.layers[0] + self.rect_obstacles], [obstacle.get_dict() for obstacle in self.layers[1]]]
        with open(os.path.join(path, "characters.py"), "w") as f:
            f.write("characters = " + repr(final_characters))
        with open(os.path.join(path, "items.py"), "w") as f:
            f.write("items = " + repr(final_items))
        with open(os.path.join(path, "triggers.py"), "w") as f:
            f.write("triggers = " + repr(final_triggers))
        with open(os.path.join(path, "obstacles.py"), "w") as f:
            f.write("layers = " + repr(final_obstacles))
    def gen_real_rect(self, mapsize):
        self.mapsize = mapsize
        real_height = mapsize[1] * (ISOHEIGHT // 2) + mapsize[0] * (ISOHEIGHT // 2)
        real_width = mapsize[1] * (ISOWIDTH // 2) + mapsize[0] * (ISOWIDTH // 2)
        startx = -(mapsize[1] * (ISOWIDTH // 2))
        starty = 0
        return Rect(startx, starty, real_width, real_height)
    def create_map(self, mapsize):
        self.realrect_quadtree = QuadTree(self.gen_real_rect(mapsize), 0, 5, 10, [], "realrect")
        self.floor_quadtree = QuadTree(Rect(0, 0, mapsize[0] * WIDTH, mapsize[1] * TILEHEIGHT), 0, 5, 10, [], "rect")
        self.layers = [[], []]
        self.rect_obstacles = []
        self.charactermap = []
        self.triggers = []
        self.item_map = []
        self.refresh_realrect_quadtree()
        self.refresh_floor_quadtree()
        self.map_diam = math.ceil(math.sqrt(self.mapsize[0] ** 2 + self.mapsize[1] ** 2))
    def load_map(self, path, mapsize):
        self.realrect_quadtree = QuadTree(self.gen_real_rect(mapsize), 0, 5, 10, [], "realrect")
        self.floor_quadtree = QuadTree(Rect(0, 0, mapsize[0] * WIDTH, mapsize[1] * TILEHEIGHT), 0, 5, 10, [], "rect")
        self.load_obstaclemap(os.path.join(path, "obstacles.py"))
        self.load_charactermap(os.path.join(path, "characters.py"))
        self.load_triggermap(os.path.join(path, "triggers.py"))
        self.load_item_map(os.path.join(path, "items.py"))
        self.refresh_realrect_quadtree()
        self.refresh_floor_quadtree()
        self.map_diam = math.ceil(math.sqrt(self.mapsize[0] ** 2 + self.mapsize[1] ** 2))
    def change_size(self, size):
        self.mapsize = size
        self.realrect_quadtree = QuadTree(self.gen_real_rect(self.mapsize), 0, 5, 10, [], "realrect")
        self.floor_quadtree = QuadTree(Rect(0, 0, self.mapsize[0] * WIDTH, self.mapsize[1] * TILEHEIGHT), 0, 5, 10, [], "rect")
        self.refresh_realrect_quadtree()
        self.refresh_floor_quadtree()
        self.map_diam = math.ceil(math.sqrt(self.mapsize[0] ** 2 + self.mapsize[1] ** 2))
    def delete_item(self, item):
        self.item_map.remove(item)
    def add_item(self, item):
        self.item_map.append(self.create_item(item))
    def create_item(self, info):
        item_info = self.items[info["type"]].copy()
        temp = item_info.copy()
        temp.update(info)
        temp.update({"item_info": item_info.copy()})
        return Item(self.screen, **temp)
    def refresh_realrect_quadtree(self):
        self.realrect_quadtree.clear()
        self.realrect_quadtree.particles = [j for i in self.layers for j in i] + self.charactermap + self.item_map
        self.realrect_quadtree.update()
    def refresh_floor_quadtree(self):
        self.floor_quadtree.clear()
        self.floor_quadtree.particles = self.triggers + self.rect_obstacles
        self.floor_quadtree.update()
    def delete_obs(self, **kwargs):
        obs = kwargs.get("obstacle", None)
        for index, layer in enumerate(self.layers):
            try:
                layer.remove(obs)
                break
            except:
                continue
    def delete_trigger(self, trigger):
        try:
            self.triggers.remove(trigger)
        except:
            pass
    def delete_character(self, identifier):
        try:
            self.characters.remove(character)
        except:
            pass
    def create_obstacle(self, **info):
        if info["type"] == "RECT":
            return BasicObstacle(self.screen, x=info["x"], y=info["y"], width=info.get("width", 1), height=info.get("height", 1), type="RECT")
        else:
            tile_dict = self.obstacles[int(info["type"])]
            if type(tile_dict["images"]) == list:
                tile_dict["images"] = tile_dict["images"][0]
            complete_info = tile_dict.copy()
            complete_info.update(info)
            return Obstacle(self.screen, **complete_info)
    def spawn_character(self, **kwargs):
        if kwargs.get("info", None):
            self.charactermap.append(self.create_character(kwargs["info"]))
        else:
            self.charactermap.append(Character(self.screen, x=kwargs.get("x", 0), y=kwargs.get("y", 0), name=kwargs["name"]))
    def load_obstaclemap(self, path):
        self.layers = []
        self.rect_obstacles = []
        temp = load_module(path)
        for layer in temp.layers:
            self.layers.append([])
            for obs in layer:
                new = self.create_obstacle(**obs)
                if type(new) == BasicObstacle:
                    self.rect_obstacles.append(new)
                else:
                    self.layers[-1].append(new)
        self.refresh_floor_quadtree()
        self.refresh_realrect_quadtree()
    def load_charactermap(self, path):
        self.charactermap = []
        temp = load_module(path)
        for character in temp.characters:
            self.charactermap.append(self.create_character(character))
        self.refresh_realrect_quadtree()
    def load_triggermap(self, path):
        self.triggers = []
        temp = load_module(path)
        for trigger in temp.triggers:
            self.triggers.append(Trigger(self.screen, **trigger))
        self.refresh_floor_quadtree()
    def load_item_map(self, path):
        self.item_map = []
        temp = load_module(path)
        for item in temp.items:
            self.item_map.append(self.create_item(item))
        self.refresh_realrect_quadtree()
    def create_character(self, info):
        temp = self.characters[info["name"]].copy()
        temp.update(info)
        temp.update({"orig_info": self.characters[info["name"]].copy()})
        return Character(self.screen, obstaclemap=self, **temp)
    def set_entry_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, value)
    def click(self, mouse_pos, tile_pos, mode, current_obs, current_layer, current_item, current_character, current_tab, properties_frame):
        for thing in [j for i in self.layers for j in i] + self.charactermap + self.item_map + self.rect_obstacles + self.triggers:
            thing.deselect()
        self.selected = None
        if mode == 0:
            selected = self.realrect_quadtree.collidepoint(mouse_pos)
            selected1 = self.floor_quadtree.collidepoint((tile_pos[0] * WIDTH, tile_pos[1] * HEIGHT))
            if selected or selected1:
                self.selected = max(selected + selected1, key=lambda x: (x.x, x.y))
                self.selected.select()
        elif mode == 1:
            if current_tab == "Obstacles":
                new_obs = self.create_obstacle(type=current_obs, x=tile_pos[0], y=tile_pos[1], width=1, height=1)
                if type(new_obs) == BasicObstacle:
                    self.rect_obstacles.append(new_obs)
                else:
                    self.layers[current_layer].append(new_obs)
            elif current_tab == "Items":
                new_obs = self.create_item({"type": current_item, "x": tile_pos[0], "y": tile_pos[1]})
                self.item_map.append(new_obs)
            elif current_tab == "Characters":
                new_obs = self.create_character({"name": current_character, "x": tile_pos[0], "y": tile_pos[1]})
                self.charactermap.append(new_obs)
            elif current_tab == "Triggers":
                new_obs = Trigger(self.screen, x=tile_pos[0], y=tile_pos[1], width=1, height=1)
                self.triggers.append(new_obs)
            self.selected = new_obs
            new_obs.select()
            self.refresh_realrect_quadtree()
            self.refresh_floor_quadtree()
        self.create_properties_widget(properties_frame)
        if self.selected:
            return True
        else:
            return False
    def destroy_properties_widget(self):
        if self.properties_frame:
            self.properties_frame.destroy()
            self.properties_frame = None
            self.widgets = {}
    def create_properties_widget(self, parent):
        self.destroy_properties_widget()
        if self.selected:
            obs_type = type(self.selected)
            if obs_type == BasicObstacle:
                possible_options = ["x", "y", "width", "height", "identifier"]
            elif obs_type == Trigger:
                possible_options = ["x", "y", "width", "height", "deactivate_after_use", "active", "identifier", "trigger"]
            elif obs_type == Obstacle:
                possible_options = ["x", "y", "identifier", "action", "after_looting", "items", "animation", "label", "onclick"]
            elif obs_type == Character:
                possible_options = ["x", "y", "dead", "weapon", "label", "identifier", "aggression_distance", "direction", "health", "random_walk_area", "waypoints", "ondeath"]
            elif obs_type == Item:
                possible_options = ["x", "y", "label", "identifier"]
            self.properties_frame = ttk.Frame(parent)
            self.widgets = {}
            for index, option in enumerate(possible_options):
                if option in ["x", "y", "width", "height", "aggression_distance", "health"]:
                    if option in ["x", "width"]:
                        self.widgets[option] = tk.Spinbox(self.properties_frame, from_=0, to=self.mapsize[0], increment=0.1)
                    elif option in ["y", "height"]:
                        self.widgets[option] = tk.Spinbox(self.properties_frame, from_=0, to=self.mapsize[1], increment=0.1)
                    elif option == "aggression_distance":
                        self.widgets[option] = tk.Spinbox(self.properties_frame, from_=0, to=self.map_diam, increment=0.1)
                    elif option == "health":
                        self.widgets[option] = tk.Spinbox(self.properties_frame, from_=0, to=1000)
                    self.set_entry_value(self.widgets[option], getattr(self.selected, option))
                    self.widgets[option].grid(row=index, column=1, sticky="w")
                elif option in ["action", "weapon", "label", "identifier", "direction", "animation", "after_looting", "items"]:
                    self.widgets[option] = ttk.Entry(self.properties_frame)
                    attr = getattr(self.selected, option)
                    if option == "items" and attr is not None:
                        attr = ";".join(attr)
                    if attr is None:
                        attr = ""
                    self.set_entry_value(self.widgets[option], attr)
                    self.widgets[option].grid(row=index, column=1, sticky="w")
                elif option in ["active", "deactivate_after_use", "dead"]:
                    variable = tk.IntVar()
                    variable.set(int(getattr(self.selected, option)))
                    self.widgets[option] = {"widget": ttk.Checkbutton(self.properties_frame, text=option, variable=variable), "variable": variable}
                    self.widgets[option]["widget"].grid(row=index, column=1, sticky="w")
                elif option in ["onclick", "trigger", "ondeath"]:
                    self.widgets[option] = [ttk.Combobox(self.properties_frame, values=("REPLACE", "DELETE", "ADD", "KILL", "KILLALL", "SPAWN", "OPEN", "CLOSE", "DEACTIVATE", "ACTIVATE", "WINGAME", "TRYWINGAME", "CHANGEMAP")), ttk.Combobox(self.properties_frame, values=("obstacle", "character", "item", "trigger")), ttk.Entry(self.properties_frame), ttk.Entry(self.properties_frame), ttk.Entry(self.properties_frame)]
                    for widget_index, widget in enumerate(self.widgets[option]):
                        try:
                            if type(widget) == ttk.Combobox:
                                widget.set(getattr(self.selected, option)[widget_index])
                            else:
                                self.set_entry_value(widget, getattr(self.selected, option)[widget_index])
                        except:
                            pass
                        widget.grid(row=index + widget_index, column=1, sticky="w")
                elif option == "waypoints":
                    self.widgets[option] = ttk.Entry(self.properties_frame)
                    self.widgets[option].grid(row=index, column=1, sticky="w")
                    self.set_entry_value(self.widgets[option], ";".join(",".join([str(y) for y in x]) for x in getattr(self.selected, option)))
                elif option == "random_walk_area":
                    self.widgets[option] = ttk.Entry(self.properties_frame)
                    self.widgets[option].grid(row=index, column=1, sticky="w")
                    self.set_entry_value(self.widgets[option], ";".join(str(x) for x in getattr(self.selected, option)))
                if option not in ["deactivate_after_use", "dead", "active"]:
                    ttk.Label(self.properties_frame, text=option).grid(row=index, column=0, sticky="w")
            self.properties_frame.grid(row=1, column=0, sticky="nswe")
    def mousedrag(self, mouse_pos, pos_change):
        if self.selected:
            self.set_attributes(x=self.selected.x + pos_change[0], y=self.selected.y + pos_change[1])
        self.refresh_realrect_quadtree()
        self.refresh_floor_quadtree()
    def delete(self, *args):
        if self.selected:
            if type(self.selected) == Character:
                self.charactermap.remove(self.selected)
            elif type(self.selected) == Obstacle:
                try:
                    self.layers[0].remove(self.selected)
                except:
                    self.layers[1].remove(self.selected)
            elif type(self.selected) == Item:
                self.item_map.remove(self.selected)
            elif type(self.selected) == BasicObstacle:
                self.rect_obstacles.remove(self.selected)
            elif type(self.selected) == Trigger:
                self.triggers.remove(self.selected)
            self.selected = None
            self.refresh_floor_quadtree()
            self.refresh_realrect_quadtree()
    def set_attributes(self, **kwargs):
        if self.selected:
            if self.properties_frame:
                final_dict = {}
                for key, item in self.widgets.items():
                    if type(item) == dict:
                        value = bool(item["variable"].get())
                    elif type(item) == list:
                        value = []
                        for part in item:
                            temp_val = part.get()
                            if temp_val:
                                value.append(temp_val)
                    else:
                        value = item.get()
                        try:
                            if key in ["after_looting", "health"]:
                                value = int(value)
                            else:
                                value = float(value)
                        except:
                            pass
                    if key in ["x", "y", "width", "height"]:
                        try:
                            final_dict[key] = float(value)
                        except:
                            pass
                    elif key == "direction":
                        if value in ["NW", "N", "NE", "E", "W", "SW", "SE", "S"]:
                            final_dict[key] = value
                    elif key == "items":
                        if value:
                            value = [x.strip() for x in value.split(";")]
                            final_dict[key] = value
                    elif key == "waypoints":
                        try:
                            if value:
                                value = [[float(y) for y in x.split(",")] for x in value.split(";")]
                            for x in value:
                                if len(x) < 2:
                                    break
                            else:
                                final_dict[key] = value
                        except:
                            pass
                    elif key == "random_walk_area":
                        try:
                            if value:
                                value = [float(x) for x in value.split(";")]
                            if len(value) == 4 or not value:
                                final_dict[key] = value
                        except:
                            pass
                    else:
                        final_dict[key] = value
                final_dict.update(kwargs)
                self.selected.set_values(**final_dict)
                for key, item in kwargs.items():
                    if key in ["x", "y"]:
                        self.set_entry_value(self.widgets[key], item)
    def draw_cursor(self, tile_pos, current_obs, current_item, current_char,  current_tab, screen_offset):
        if current_tab == "Obstacles":
            temp = self.create_obstacle(type=current_obs, x=tile_pos[0], y=tile_pos[1])
        elif current_tab == "Items":
            temp = self.create_item({"type": current_item, "x": tile_pos[0], "y": tile_pos[1]})
        elif current_tab == "Characters":
            temp = self.create_character({"name": current_char, "x": tile_pos[0], "y": tile_pos[1]})
        elif current_tab == "Triggers":
            temp = Trigger(self.screen, x=tile_pos[0], y=tile_pos[1])
        temp.draw(screen_offset)
    def draw(self, screen_offset):
        self.set_attributes()
        final = sorted(self.layers[1] + self.charactermap, key=lambda x: (x.x, x.y))
        ground = sorted(self.layers[0] + self.triggers + self.rect_obstacles + self.item_map, key=lambda x: (x.x, x.y))
        for ground_obs in ground:
            ground_obs.draw(screen_offset)
        for thing in final:
            thing.draw(screen_offset)
