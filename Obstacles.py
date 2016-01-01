import os
import sys
import pygame
from Grid2D import *
from Floor import *
from CONSTANTS import *
from pygame.locals import *
from AICharacter import AICharacter
FONT = pygame.font.Font("Lumidify_Casual.ttf", 20)
#Sorting: bob.sort(key=lambda x: x.pos[1], x.pos[0])
#Note: [j for i in x for j in i] is just a piece of ugliness which joins the lists in another list into one list.

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
        self.realrect = Rect(0, 0, 0, 0)
        self.selectable = False
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
    def __init__(self, screen, tile_dict, grid_pos, **kwargs):
        super().__init__(screen, tile_dict, grid_pos)
        self.borders = kwargs.get("borders", [0, 0, 0, 0])
        self.rect = calculate_rect(grid_pos, self.borders)
        self.realrect = Rect((self.isox, self.isoy), self.region[1])
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.dialogmanager = kwargs.get("dialogmanager", None)
        self.identifier = kwargs.get("id", None)
        self.onclick = kwargs.get("onclick", None)
        self.dialog = kwargs.get("dialog", None)
        self.animation = kwargs.get("animation", "default")
        self.action = kwargs.get("action", None)
        self.after_looting = kwargs.get("after_looting", None)
        self.label = kwargs.get("label", None)
        self.selected = False
        self.selectable = False
        if self.action or self.dialog or self.onclick or self.label:
            self.selectable = True
    def click(self):
        if self.onclick:
            if self.onclick[0] == "REPLACE":
                original = self.identifier if self.onclick[1] == "self" else self.onclick[1]
                try:
                    replacement = int(self.onclick[2])
                except:
                    replacement = self.onclick[2]
                self.obstaclemap.replace_id(original, replacement)
            elif self.onclick[0] == "DELETE":
                to_delete = self.identifier if self.onclick[1] == "self" else self.onclick[1]
                self.obstaclemap.delete_id(to_delete)
        if self.dialog:
            self.dialogmanager.start_dialog(self.dialog)
        if self.action == "chest":
            self.obstaclemap.replace_id(self.identifier, self.after_looting)
        if self.action == "barrel":
            self.obstaclemap.delete_id(self.identifier)
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def draw_label(self):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), self.realrect)
    def draw(self, screen_offset):
        if self.selected:
            temp_surf = pygame.surface.Surface(self.region[1]).convert_alpha()
            temp_surf.fill((100, 100, 100, 0))
            temp_surf.blit(self.image, (0, 0), self.region, BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
        else:
            super().draw(screen_offset)
class AnimatedObstacle(AnimatedTile):
    def __init__(self, screen, tile_dict, grid_pos, **kwargs):
        super().__init__(screen, tile_dict, grid_pos)
        self.borders = kwargs.get("borders", [0, 0, 0, 0])
        self.rect = calculate_rect(grid_pos, self.borders)
        self.realrect = Rect(self.iso_positions[0], self.regions[0][1])
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.dialogmanager = kwargs.get("dialogmanager", None)
        self.identifier = kwargs.get("id", None)
        self.onclick = kwargs.get("onclick", None)
        self.dialog = kwargs.get("dialog", None)
        self.animation = kwargs.get("animation", "default")
        self.action = kwargs.get("action", None)
        self.after_looting = kwargs.get("after_looting", None)
        self.label = kwargs.get("label", None)
        self.selected = False
        self.selectable = False
        if self.action or self.dialog or self.onclick or self.label:
            self.selectable = True
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def click(self):
        if self.onclick:
            if self.onclick[0] == "REPLACE":
                original = self.identifier if self.onclick[1] == "self" else self.onclick[1]
                try:
                    replacement = int(self.onclick[2])
                except:
                    replacement = self.onclick[2]
                self.obstaclemap.replace_id(original, replacement)
            elif self.onclick[0] == "DELETE":
                to_delete = self.identifier if self.onclick[1] == "self" else self.onclick[1]
                self.obstaclemap.delete_id(to_delete)
        if self.dialog:
            self.dialogmap.start_dialog(self.dialog)
        if self.action == "chest":
            self.obstaclemap.replace_id(self.identifier, self.after_looting)
        if self.action == "barrel":
            self.obstaclemap.delete_id(self.identifier)
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def draw_label(self):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), self.realrect)
    def draw(self, screen_offset):
        if self.selected:
            temp_surf = pygame.surface.Surface(self.regions[self.frame][1]).convert_alpha()
            temp_surf.fill((100, 100, 100, 0))
            temp_surf.blit(self.images[self.frame], (0, 0), self.regions[self.frame], BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.iso_positions[self.frame][0] + screen_offset[0], self.iso_positions[self.frame][1] + screen_offset[1]))
        else:
            super().draw(screen_offset)
class Door(AnimatedObstacle):
    def __init__(self, screen, tile_dict, grid_pos, **kwargs):
        super().__init__(screen, tile_dict, grid_pos, **kwargs)
        self.opening = False
        self.closing = False
    def open(self):
        self.opening = True
        self.closing = False
    def close(self):
        self.closing = True
        self.opening = False
    def update(self, current_time=None):
        if self.opening:
            if self.frame < len(self.images) - 1:
                super().update(current_time)
            else:
                self.opening = False
        elif self.closing:
            if self.frame > 0:
                super().update(current_time, True)
            else:
                self.closing = False
class Obstacles():
    def __init__(self, screen, obstacles, mapsize, characters):
        self.screen = screen
        self.obstacles = obstacles
        self.characters = characters
        self.mapsize = mapsize
        self.grid = Grid2D(mapsize)
        self.realrect_quadtree = QuadTree(Rect(0, 0, mapsize[0] * ISOWIDTH, mapsize[1] * ISOHEIGHT), 0, 5, 10, [], "realrect")
        self.layers = [[]]
        self.charactermap = []
        self.reserves = {}
        self.selected = None
    def find_obs_id(self, identifier):
        for layer_index, layer in enumerate(self.layers):
            for obs_index, obstacle in enumerate(layer):
                if obstacle.identifier == identifier:
                    return obstacle, layer_index, obs_index
        return None
    def refresh_realrect_quadtree(self):
        self.realrect_quadtree.clear()
        self.realrect_quadtree.particles = [j for i in self.layers for j in i] + self.charactermap
        self.realrect_quadtree.update()
    def delete_id(self, old_id):
        old_obs = self.find_obs_id(old_id)
        if old_obs:
            self.layers[old_obs[1]].pop(old_obs[2])
            self.grid.obstacles = [j for i in self.layers for j in i]
            self.grid.refresh(old_obs[0].rect)
    def replace_id(self, old_id, new):
        if old_id:
            old_obs = self.find_obs_id(old_id)
            if type(new) == int:
                new_obs = self.create_obstacle({"type": new, "x": old_obs[0].grid_pos[0], "y": old_obs[0].grid_pos[1]})
            else:
                new_obs = self.reserves[new]
            
            self.layers[old_obs[1]][old_obs[2]] = new_obs
            self.grid.obstacles = [j for i in self.layers for j in i]
            self.grid.refresh(old_obs[0].rect)
            self.grid.calculate_clearance(new_obs.rect)
    def create_obstacle(self, info):
        if info["type"] == "RECT":
            return BasicObstacle((info["x"], info["y"]), info["width"], info["height"])
        else:
            tile_dict = self.obstacles[int(info["type"])]
            complete_info = tile_dict.copy()
            complete_info.update(info)
            if type(tile_dict["images"]) == dict:
                return Obstacle(self.screen, tile_dict["images"], (info["x"], info["y"]), obstaclemap=self, **complete_info)
            else:
                if tile_dict.get("animation", None) == "door":
                    return Door(self.screen, tile_dict, (info["x"], info["y"]), obstaclemap=self)
                else:
                    return AnimatedObstacle(self.screen, tile_dict, (info["x"], info["y"]), obstaclemap=self, **complete_info)
    def add_layer(self):
        if len(self.layers) < 2:
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
        self.grid.obstacles = [j for i in self.layers for j in i]
        self.grid.refresh()
        self.refresh_realrect_quadtree()
    def load_charactermap(self, path):
        self.charactermap = []
        with open(path) as f:
            lines = f.readlines()
            current = {}
            for line in lines:
                line_split = line.split("=")
                if line.startswith("#"):
                    pass
                elif line.startswith("*character"):
                    if len(current) > 0:
                        self.charactermap.append(self.create_character(current))
                        current = {}
                    current["name"] = line.split()[1].strip()
                else:
                    value = line_split[1].strip()
                    if value == "None":
                        value = None
                    elif line_split[0] == "items_dropped":
                        value = [x.strip() for x in value.split(",")]
                    elif line_split[0] == "waypoints":
                        value = [[float(y) for y in x.split()] for x in value.split(",")]
                    elif line_split[0] == "random_walk_area":
                        value = [float(x) for x in value.split()]
                    elif line_split[0] == "health":
                        value = int(value)
                    elif line_split[0] in ["x", "y"]:
                        value = float(value)
                    current[line_split[0]] = value
            self.charactermap.append(self.create_character(current))
    def create_character(self, info):
        temp = self.characters[info["name"]].copy()
        temp.update(info)
        return AICharacter(self.screen, pathfinding_grid=self.grid, **temp)
    def update(self, **kwargs):
        current_time = kwargs.get("current_time", pygame.time.get_ticks())
        screen_offset = kwargs.get("screen_offset", [0, 0])
        event = kwargs.get("event", None)
        mouse_pos = kwargs.get("mouse_pos", pygame.mouse.get_pos())
        mouse_pos = [mouse_pos[0] + screen_offset[0], mouse_pos[1] + screen_offset[1]]
        for layer in self.layers:
            for obstacle in layer:
                obstacle.update(current_time)
        for character in self.charactermap:
            character.update(current_time)
        selected = [x for x in self.realrect_quadtree.collidepoint(mouse_pos) if x.selectable]
        for thing in [j for i in self.layers for j in i] + self.charactermap:
            thing.deselect()
        if selected:
            self.selected = max(selected, key=lambda x: (x.grid_pos[1], x.grid_pos[0]))
            self.selected.select()
            if event and event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.selected.click()
        else:
            self.selected = None
        if event and event.type == KEYDOWN and event.key == K_SPACE:
            for obstacle in self.layers[0]:
                if type(obstacle) == Door:
                    obstacle.open()
        if event and event.type == KEYDOWN and event.key == K_RETURN:
            for obstacle in self.layers[0]:
                if type(obstacle) == Door:
                    obstacle.close()
        self.refresh_realrect_quadtree()
    def draw(self, screen_offset=[0, 0]):
        final = sorted(self.layers[0] + self.charactermap, key=lambda x: (x.grid_pos[1], x.grid_pos[0]))
        for thing in final:
            thing.draw(screen_offset)
        if self.selected:
            self.selected.draw_label()
