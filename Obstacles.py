import os
import sys
import pygame
import importlib
from Grid2D import *
from Floor import *
from CONSTANTS import *
from pygame.locals import *
from call_trigger import *
from AICharacter import AICharacter
FONT = pygame.font.Font("Lumidify_Casual.ttf", 20)

#Sorting: bob.sort(key=lambda x: x.pos[1], x.pos[0])
#[j for i in self.layers for j in i] is just a piece of ugliness to join lists of lists into one list

def load_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Bullet():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.images = kwargs.get("images", [])
        self.side = kwargs.get("side", "enemy")
        self.phases_per_second = kwargs.get("phases_per_second", 6)
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.speed = kwargs.get("speed", 0)
        self.frame_interval = 1000 / self.phases_per_second / self.phases_per_second
        self.adjusted_speed = self.speed / self.phases_per_second
        self.lifetime = kwargs.get("lifetime", 0) * 1000
        self.current_time = kwargs.get("current_time", pygame.time.get_ticks())
        self.frame_time_passed = 0
        self.lifetime_passed = 0
        self.direction = kwargs.get("direction", "N")
        self.angle = kwargs.get("angle", 0)
        self.vel = [math.cos(self.angle) * self.adjusted_speed, -math.sin(self.angle) * self.adjusted_speed]
        self.grid_pos = kwargs.get("grid_pos", [0, 0])
        self.damage = kwargs.get("damage", 0)
        self.frame = 0
    def update(self, **kwargs):
        current_time = kwargs.get("current_time", pygame.time.get_ticks())
        time_change = current_time - self.current_time
        self.lifetime_passed += time_change
        if self.lifetime_passed > self.lifetime and self.lifetime >= 0:
            self.obstaclemap.delete_bullet(self)
        collide = self.obstaclemap.collidecharacter(self.grid_pos, self.side)
        collide2 = self.obstaclemap.grid.quadtree.collidepoint([self.grid_pos[0] * WIDTH, self.grid_pos[1] * HEIGHT])
        if collide2:
            self.obstaclemap.delete_bullet(self)
        if collide:
            for character in collide:
                character.hit(self.damage)
            self.obstaclemap.delete_bullet(self)
        self.frame_time_passed += time_change
        if self.frame_time_passed >= self.frame_interval:
            magnitude = self.frame_time_passed / self.frame_interval
            self.frame_time_passed = 0
            self.grid_pos[0] += self.vel[0] * magnitude
            self.grid_pos[1] += self.vel[1] * magnitude
            self.frame += 1
            if self.frame >= len(self.images[self.direction]):
                self.frame = 0
        self.current_time = current_time
    def draw(self, screen_offset):
        isox = ((self.grid_pos[0] - 0.2) - (self.grid_pos[1] - 0.2)) * (ISOWIDTH // 2) + (self.images[self.direction][self.frame]["offset"][0] + TILEWIDTH // 2 + screen_offset[0])
        isoy = ((self.grid_pos[0] - 0.2) + (self.grid_pos[1] - 0.2)) * (ISOHEIGHT // 2) + (self.images[self.direction][self.frame]["offset"][1] + screen_offset[1])
        self.screen.blit(self.images[self.direction][self.frame]["image"], (isox, isoy))
def calculate_rect(grid_pos, borders):
    return Rect((
    grid_pos[0] + borders[0]) * WIDTH,
    (grid_pos[1] + borders[2]) * HEIGHT,
    (abs(borders[0]) + abs(borders[1])) * WIDTH,
    (abs(borders[2]) + abs(borders[3])) * HEIGHT)
class Trigger():
    def __init__(self, **kwargs):
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.identifier = kwargs.get("id", None)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.onwalk = kwargs.get("trigger", None)
        self.deactivate_after_use = kwargs.get("deactivate_after_use", False)
        self.active = kwargs.get("active", True)
        self.rect = Rect(self.x * WIDTH, self.y * HEIGHT, self.width * WIDTH, self.height * HEIGHT)
    def get_dict(self):
        temp = {"x": self.x, "y": self.y, "width": self.width, "height": self.height, "trigger": self.onwalk}
        if self.deactivate_after_use:
            temp.update({"deactivate_after_use": self.deactivate_after_use})
        if not self.active:
            temp.update({"active": self.active})
        return temp
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
    def trigger(self):
        if self.active and self.onwalk:
            call_trigger(self.onwalk, self.obstaclemap, self.identifier, self)
            if self.deactivate_after_use:
                self.active = False
class BasicObstacle():
    def __init__(self, grid_pos, width, height, obstype, **kwargs):
        self.grid_pos = grid_pos
        self.type = obstype
        self.rect = Rect(grid_pos[0] * WIDTH, grid_pos[1] * HEIGHT, width * WIDTH, height * HEIGHT)
        self.realrect = Rect(0, 0, 0, 0)
        self.identifier = kwargs.get("id", None)
        self.selectable = False
    def get_dict(self):
        temp = {"x": self.x, "y": self.y, "width": self.width, "height": self.height, "type": self.type}
        if self.identifier:
            temp.update({"id": self.identifier})
        return temp
    def update(self, *args):
        pass
    def get_rect(self, rect_type):
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
        self.type = kwargs.get("type", None)
        self.realrect = Rect((self.isox, self.isoy), self.region[1])
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.dialogmanager = kwargs.get("dialogmanager", None)
        self.identifier = kwargs.get("id", None)
        self.onclick = kwargs.get("onclick", None)
        self.dialog = kwargs.get("dialog", None)
        self.action = kwargs.get("action", None)
        self.after_looting = kwargs.get("after_looting", None)
        self.label = kwargs.get("label", None)
        self.items = kwargs.get("items", [])
        self.selected = False
        self.selectable = False
        if self.action or self.dialog or self.onclick or self.label:
            self.selectable = True
    def get_dict(self):
        temp = {"type": self.type, "x": self.grid_pos[0], "y": self.grid_pos[1], "id": self.identifier, "onclick": self.onclick, "action": self.action, "after_looting": self.after_looting, "label": self.label, "items": self.items}
        final = {}
        for key, item in temp.items():
            if item is not None and item != []:
                final[key] = item
        return final
    def click(self):
        if self.onclick:
            call_trigger(self.onclick, self.obstaclemap, self.identifier, self)
        if self.dialog:
            self.dialogmanager.start_dialog(self.dialog)
        if self.action == "chest":
            for item in self.items:
                self.obstaclemap.add_item({"x": self.grid_pos[0] + 0.5, "y": self.grid_pos[1], "type": item})
            self.items = []
            if self.after_looting:
                self.obstaclemap.replace_obs(obstacle=self, new=self.after_looting)
        if self.action == "barrel":
            for item in self.items:
                self.obstaclemap.add_item({"x": self.grid_pos[0], "y": self.grid_pos[1], "type": item})
            self.obstaclemap.delete_obs(obstacle=self)
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def draw_label(self, screen_offset):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), (self.realrect.x + screen_offset[0], self.realrect.y + screen_offset[1]))
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
        self.type = kwargs.get("type", None)
        self.rect = calculate_rect(grid_pos, self.borders)
        self.realrect = Rect(self.iso_positions[0], self.regions[0][1])
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.dialogmanager = kwargs.get("dialogmanager", None)
        self.identifier = kwargs.get("id", None)
        self.onclick = kwargs.get("onclick", None)
        self.dialog = kwargs.get("dialog", None)
        self.action = kwargs.get("action", None)
        self.after_looting = kwargs.get("after_looting", None)
        self.label = kwargs.get("label", None)
        self.selected = False
        self.selectable = False
        self.items = kwargs.get("items", [])
        if self.action or self.dialog or self.onclick or self.label:
            self.selectable = True
    def get_dict(self):
        temp = {"type": self.type, "x": self.grid_pos[0], "y": self.grid_pos[1], "id": self.identifier, "onclick": self.onclick, "action": self.action, "after_looting": self.after_looting, "label": self.label, "items": self.items}
        final = {}
        for key, item in temp.items():
            if item is not None and item != []:
                final[key] = item
        return final
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def click(self):
        if self.onclick:
            call_trigger(self.onclick, self.obstaclemap, self.identifier, self)
        if self.dialog:
            self.dialogmap.start_dialog(self.dialog)
        if self.action == "chest":
            for item in self.items:
                self.obstaclemap.add_item({"x": self.grid_pos[0] + 0.5, "y": self.grid_pos[1], "type": item})
            self.obstaclemap.replace_obs(obstacle=self, new=self.after_looting)
        if self.action == "barrel":
            for item in self.items:
                self.obstaclemap.add_item({"x": self.grid_pos[0], "y": self.grid_pos[1], "type": item})
            self.obstaclemap.delete_obs(obstacle=self)
    def get_rect(self, rect_type):
        if rect_type == "rect":
            return self.rect
        else:
            return self.realrect
    def draw_label(self, screen_offset):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), (self.realrect.x + screen_offset[0], self.realrect.y + screen_offset[1]))
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
        self.animation = kwargs.get("animation", None)
    def get_dict(self):
        temp = {"type": self.type, "x": self.grid_pos[0], "y": self.grid_pos[1], "id": self.identifier, "onclick": self.onclick, "action": self.action, "animation": self.animation, "after_looting": self.after_looting, "label": self.label, "items": self.items}
        final = {}
        for key, item in temp.items():
            if item is not None and item != []:
                final[key] = item
        return final
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
class Item():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.image = kwargs.get("ingame", None)
        self.offset = kwargs.get("offset", None)
        self.grid_pos = [kwargs.get("x", 0), kwargs.get("y", 0)]
        self.item_info = kwargs["item_info"]
        self.label = kwargs.get("label", None)
        self.identifier = kwargs.get("id", None)
        self.isox = (self.grid_pos[0] - self.grid_pos[1]) * (TILEWIDTH // 2) + (self.offset[0] + TILEWIDTH // 2)
        self.isoy = (self.grid_pos[0] + self.grid_pos[1]) * (TILEHEIGHT // 2) + self.offset[1]
        self.realrect = Rect((self.isox, self.isoy), self.image.get_size())
        self.selected = False
        self.selectable = True
    def get_dict(self):
        temp = {"type": self.item_info["type"], "x": self.grid_pos[0], "y": self.grid_pos[1]}
        if self.identifier is not None:
            temp["id"] = self.identifier
        if self.label != self.item_info.get("label", None):
            temp["label"] = self.label
        return temp
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def get_rect(self, rect_type):
        if rect_type == "realrect":
            return self.realrect
    def draw_label(self, screen_offset):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), (self.realrect.x + screen_offset[0], self.realrect.y + screen_offset[1]))
    def draw(self, screen_offset):
        if self.selected:
            temp_surf = pygame.surface.Surface(self.realrect.size).convert_alpha()
            temp_surf.fill((100, 100, 100, 0))
            temp_surf.blit(self.image, (0, 0), [(0, 0), self.realrect.size], BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
        else:
            self.screen.blit(self.image, (self.isox + screen_offset[0], self.isoy + screen_offset[1]))
class Obstacles():
    def __init__(self, screen, obstacles, characters, items, bullets, engine):
        self.screen = screen
        self.engine = engine
        self.obstacles = obstacles
        self.characters = characters
        self.items = items
        self.bullet_archetypes = bullets
        self.layers = []
        self.charactermap = []
        self.triggers = []
        self.reserves = {}
        self.selected = None
        self.player = None
        self.screen_offset = [0, 0]
        self.bullets = []
        self.dead_characters = []
        self.item_map = []
        self.change_size([0, 0])
    def save(self, path, charactermap, item_map, triggers, layers):
        final_characters = [character.get_dict() for character in charactermap]
        final_items = [item.get_dict() for item in item_map]
        final_triggers = [trigger.get_dict() for trigger in triggers]
        final_obstacles = [[obstacle.get_dict() for obstacle in layers[0]], [obstacle.get_dict() for obstacle in layers[1]]]
        with open(os.path.join(path, "characters.py"), "w") as f:
            f.write("characters = " + repr(final_characters))
        with open(os.path.join(path, "items.py"), "w") as f:
            f.write("items = " + repr(final_items))
        with open(os.path.join(path, "triggers.py"), "w") as f:
            f.write("triggers = " + repr(final_triggers))
        with open(os.path.join(path, "obstacles.py"), "w") as f:
            f.write("layers = " + repr(final_obstacles))
    def wingame(self):
        self.engine.wingame()
    def trywingame(self):
        if self.player.has_book("Book 1"):
            self.engine.wingame()
    def gen_real_rect(self, mapsize):
        real_height = mapsize[1] * (ISOHEIGHT // 2) + mapsize[0] * (ISOHEIGHT // 2)
        real_width = mapsize[1] * (ISOWIDTH // 2) + mapsize[0] * (ISOWIDTH // 2)
        startx = -(mapsize[1] * (ISOWIDTH // 2))
        starty = 0
        return Rect(startx, starty, real_width, real_height)
    def change_size(self, mapsize):
        self.mapsize = mapsize
        self.realrect_quadtree = QuadTree(self.gen_real_rect(mapsize), 0, 5, 10, [], "realrect")
        self.trigger_quadtree = QuadTree(Rect(0, 0, mapsize[0] * WIDTH, mapsize[1] * TILEHEIGHT), 0, 5, 10, [], "rect")
        self.grid = Grid2D(mapsize)
        try:
            self.player.pathfinding_grid = self.grid
        except:
            pass
    def changemap(self, new_map, spawn_pos=None):
        self.engine.load_map(new_map, spawn_pos=spawn_pos)
    def add_bullet(self, info):
        temp = self.bullet_archetypes[info["name"]].copy()
        temp.update(info)
        self.bullets.append(Bullet(self.screen, obstaclemap=self, **temp))
    def delete_bullet(self, bullet):
        try:
            self.bullets.remove(bullet)
        except:
            pass
    def collidecharacter(self, point, side):
        hit_list = []
        for character in self.charactermap + [self.player]:
            if character.side != side and character.state != "death" and not character.dead:
                if math.sqrt((point[0] - character.grid_pos[0]) ** 2 + (point[1] - character.grid_pos[1]) ** 2) < 0.5:
                    hit_list.append(character)
        return hit_list
    def kill(self, identifier):
        for character in list(self.charactermap):
            if character.identifier == identifier:
                character.die()
                break
    def killall(self):
        for character in self.charactermap:
            character.die()
    def open_door(self, door):
        try:
            self.find_obs_id(door).open()
        except:
            print("Couldn't open door with id '%s'." %door)
    def close_door(self, door):
        try:
            self.find_obs_id(door).close()
        except:
            print("Couldn't close door with id '%s'" %door)
    def delete_item(self, item):
        try:
            self.item_map.remove(item)
        except:
            print("Couldn't remove item '%s'." %item)
    def add_item(self, item):
        self.item_map.append(self.create_item(item))
    def create_item(self, info):
        item_info = self.items[info["type"]].copy()
        temp = item_info.copy()
        temp.update(info)
        temp.update({"item_info": item_info.copy()})
        return Item(self.screen, **temp)
    def find_obs_id(self, identifier):
        for layer_index, layer in enumerate(self.layers):
            for obs_index, obstacle in enumerate(layer):
                if obstacle.identifier == identifier:
                    return obstacle, layer_index, obs_index
        return None
    def find_char_id(self, identifier):
        for index, character in enumerate(self.charactermap):
            if character.identifier == identifier:
                return character, index
    def find_trigger_id(self, identifier):
        for index, trigger in enumerate(self.triggers):
            if trigger.identifier == identifier:
                return trigger, index
    def refresh_realrect_quadtree(self):
        self.realrect_quadtree.clear()
        self.realrect_quadtree.particles = [j for i in self.layers for j in i] + self.charactermap + self.item_map
        self.realrect_quadtree.update()
    def refresh_trigger_quadtree(self):
        self.trigger_quadtree.clear()
        self.trigger_quadtree.particles = self.triggers
        self.trigger_quadtree.update()
    def refresh_grid(self):
        self.grid.obstacles = [j for i in self.layers for j in i]
        self.grid.refresh()
    def delete_obs(self, **kwargs):
        obs = kwargs.get("obstacle", None)
        identifier = kwargs.get("identifier", None)
        refresh_rect = Rect(0, 0, 0, 0)
        if obs:
            refresh_rect = obs.rect
            for index, layer in enumerate(self.layers):
                try:
                    layer.remove(obs)
                    break
                except:
                    continue
            else:
                print("WARNING: Couldn't delete obstacle '%s'." %obs)
        else:
            obs = self.find_obs_id(identifier)
            if obs:
                refresh_rect = obs[0].rect
                self.layers[obs[1]].pop(obs[2])
            else:
                print("WARNING: Couldn't delete obstacle '%s'." %obs)
        self.grid.obstacles = [j for i in self.layers for j in i]
        self.grid.refresh(refresh_rect)
    def replace_obs(self, **kwargs):
        orig_obs = kwargs.get("obstacle", None)
        new = kwargs.get("new", None)
        identifier = kwargs.get("identifier", None)
        if type(orig_obs) != str:
            for index, layer in enumerate(self.layers):
                try:
                    obs = orig_obs, index, layer.index(orig_obs)
                    break
                except:
                    continue
            else:
                print("WARNING: couldn't find obstacle '%s'." %orig_obs)
        else:
            obs = self.find_obs_id(orig_obs)
        try:
            if type(new) == int:
                new_obs = self.create_obstacle({"type": new, "x": obs[0].grid_pos[0], "y": obs[0].grid_pos[1]})
            else:
                new_obs = self.create_obstacle(new)
            self.layers[obs[1]][obs[2]] = new_obs
            self.grid.obstacles = [j for i in self.layers for j in i]
            self.grid.refresh(obs[0].rect)
            self.grid.calculate_clearance(new_obs.rect)
        except:
            print("WARNING: Couldn't replace obstacle '%s'." %orig_obs)
    def delete_trigger(self, identifier):
        for trigger in list(self.triggers):
            if trigger.identifier == identifier:
                self.triggers.remove(trigger)
                break
    def deactivate_trigger(self, identifier):
        for trigger in self.triggers:
            if trigger.identifier == identifier:
                trigger.active = False
                break
    def activate_trigger(self, identifier):
        for trigger in self.triggers:
            if trigger.identifier == identifier:
                trigger.active = True
                break
    def delete_character(self, identifier):
        for character in list(self.characters):
            if character.identifier == identifier:
                self.characters.remove(character)
                break
    def create_obstacle(self, info):
        if info["type"] == "RECT":
            return BasicObstacle((info["x"], info["y"]), info["width"], info["height"], "RECT")
        else:
            tile_dict = self.obstacles[int(info["type"])]
            complete_info = tile_dict.copy()
            complete_info.update(info)
            if type(tile_dict["images"]) == dict:
                return Obstacle(self.screen, tile_dict["images"], (info["x"], info["y"]), obstaclemap=self, **complete_info)
            else:
                if tile_dict.get("animation", None) == "door":
                    return Door(self.screen, tile_dict, (info["x"], info["y"]), obstaclemap=self, **complete_info)
                else:
                    return AnimatedObstacle(self.screen, tile_dict, (info["x"], info["y"]), obstaclemap=self, **complete_info)
    def spawn_character(self, **kwargs):
        if kwargs.get("info", None):
            self.charactermap.append(self.create_character(kwargs["info"]))
        else:
            self.charactermap.append(AICharacter(self.screen, x=kwargs.get("x", 0), y=kwargs.get("y", 0), **self.characters[kwargs["name"]]))
    def load_obstaclemap(self, path):
        self.layers = []
        temp = load_module(path)
        for layer in temp.layers:
            self.layers.append([])
            for obs in layer:
                self.layers[-1].append(self.create_obstacle(obs))
        self.layers[0].sort(key=lambda x: (x.grid_pos[1], x.grid_pos[0]))
        self.refresh_grid()
        self.refresh_realrect_quadtree
    def load_charactermap(self, path):
        self.charactermap = []
        temp = load_module(path)
        for character in temp.characters:
            self.charactermap.append(self.create_character(character))
    def load_triggermap(self, path):
        self.triggers = []
        temp = load_module(path)
        for trigger in temp.triggers:
            self.triggers.append(Trigger(obstaclemap=self, **trigger))
        self.refresh_trigger_quadtree()
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
        try:
            temp["weapon_final"] = self.items[temp["weapon"]]
        except:
            temp["weapon_final"] = None
        return AICharacter(self.screen, obstaclemap=self, **temp)
    def update(self, **kwargs):
        current_time = kwargs.get("current_time", pygame.time.get_ticks())
        event = kwargs.get("event", None)
        mouse_pos = kwargs.get("mouse_pos", pygame.mouse.get_pos())
        mouse_pos = [mouse_pos[0] - self.screen_offset[0], mouse_pos[1] - self.screen_offset[1]]
        for trigger in self.trigger_quadtree.collidepoint([self.player.grid_pos[0] * WIDTH, self.player.grid_pos[1] * HEIGHT]):
            trigger.trigger()
        for layer in self.layers:
            for obstacle in layer:
                obstacle.update(current_time)
        for character in list(self.charactermap):
            character.update(current_time)
            if character.dead:
                self.dead_characters.append(character)
                self.charactermap.remove(character)
            elif not self.player.dead and self.player.state != "death" and math.sqrt((self.player.grid_pos[0] - character.grid_pos[0]) ** 2 + (self.player.grid_pos[1] - character.grid_pos[1]) ** 2) <= character.aggression_distance:
                character.turn_to(self.player)
                character.attack(self.player)
            else:
                character.movement_temporarily_suppressed = False
        self.player.update(current_time=current_time, event=event, mouse_pos=mouse_pos)
        if not self.player.dead:
            selected = [x for x in self.realrect_quadtree.collidepoint(mouse_pos) if x.selectable]
            for thing in [j for i in self.layers for j in i] + self.charactermap + self.item_map:
                if thing.selectable:
                    thing.deselect()
            if selected:
                self.selected = max(selected, key=lambda x: (x.grid_pos[0], x.grid_pos[1]))
                self.selected.select()
                if type(self.selected) == Item and self.player.pressed:
                    self.player.click_item(self.selected)
                elif event and event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if type(self.selected) == AICharacter:
                        self.player.turn_to(self.selected)
                        self.player.attack(self.selected)
                    else:
                        self.selected.click()
            else:
                self.selected = None
        for obstacle in [j for i in self.layers for j in i]:
            if type(obstacle) == Door:
                for character in self.charactermap + [self.player]:
                    if math.sqrt((obstacle.grid_pos[0] - character.grid_pos[0]) ** 2 + (obstacle.grid_pos[1] - character.grid_pos[1]) ** 2) < 2:
                        obstacle.open()
                        break
                else:
                    obstacle.close()
        for bullet in list(self.bullets):
            bullet.update()
            if bullet.grid_pos[0] < 0 or bullet.grid_pos[0] > self.mapsize[0] or bullet.grid_pos[1] < 0 or bullet.grid_pos[1] > self.mapsize[1]:
                self.delete_bullet(bullet)
        self.refresh_realrect_quadtree()
        if self.player.dead and not self.engine.lostgame:
            if self.selected:
                self.selected.deselect()
            self.selected = None
            self.engine.losegame()
    def draw(self, screen_offset):
        self.screen_offset = screen_offset
        if not self.player.dead:
            final_unsorted = self.layers[1] + self.charactermap + [self.player] + self.bullets
            ground_unsorted = self.layers[0] + self.dead_characters + self.item_map
        else:
            final_unsorted = self.layers[1] + self.charactermap + self.bullets
            ground_unsorted = self.layers[0] + self.dead_characters + [self.player] + self.item_map
        final = sorted(final_unsorted, key=lambda x: (x.grid_pos[0], x.grid_pos[1]))
        ground = sorted(ground_unsorted, key=lambda x: (x.grid_pos[0], x.grid_pos[1]))
        for ground_obs in ground:
            ground_obs.draw(screen_offset)
        for thing in final:
            thing.draw(screen_offset)
        if self.selected:
            self.selected.draw_label(screen_offset)
