import os
import sys
import math
import pygame
from Engine import *
from pygame.locals import *
from call_trigger import *
from Character import *

TILEWIDTH = 128
TILEHEIGHT = 64

class Montag(Character):
    def __init__(self, screen, **kwargs):
        kwargs["side"] = "montag"
        super().__init__(screen, **kwargs)
        self.pressed = False
        self.obstaclemap = kwargs.get("obstaclemap", None)
        self.pathfinding_grid = self.obstaclemap.grid
        self.target_image = pygame.image.load("graphics/cursors/mouse_move_cursor_0.png").convert_alpha()
        self.last_mouse_pos = ()
        self.quests = {"open": [], "done": []}
        self.last_screen_offset = [0, 0]
        self.inventory = {"weapon": None, "books": []}
        self.after_walk = None
        self.walking = True
        self.attack_time = 500
        self.health_time_passed = 0
    def reset(self):
        self.attack_time_passed = 0
        self.gethit_time_passed = 0
        self.time_passed = 0
        self.frame = 0
        self.state = "stand"
        self.walking = False
        self.walk_to_points = []
        self.vel = [0, 0]
        self.adjusted_vel = [0, 0]
    def has_quest(self, quest):
        if quest in self.quests["open"] or quest in self.quests["done"]:
            return True
        else:
            return False
    def finished_quest(self, quest):
        if quest in self.quests["done"]:
            return True
        else:
            return False
    def add_quest(self, quest):
        self.quests["open"].append(quest)
    def finish_quest(self, quest):
        try:
            self.quests["open"].remove(quest)
            self.quests["done"].append(quest)
        except:
            print("WARNING: Tried to remove unknown quest.")
    def click_item(self, item):
        new_path = self.pathfinding_grid.find_path(tuple(self.grid_pos), item.grid_pos)
        if new_path:
            self.walk_to(new_path)
        self.after_walk = lambda: self.pickup_item(item)
    def get_inventory(self):
        temp = {}
        temp["weapon"] = self.inventory["weapon"]
        if temp["weapon"]:
            temp["weapon"] = temp["weapon"]["type"]
        temp["books"] = []
        for book in self.inventory["books"]:
            temp["books"].append(book["type"])
        return temp
    def load_inventory(self, inventory):
        self.inventory = {"weapon": None, "books": []}
        if inventory["weapon"]:
            self.inventory["weapon"] = self.obstaclemap.items[inventory["weapon"]]
            self.attack_time = self.inventory["weapon"]["weapon"]["attack_time"] * 1000
        for book in inventory["books"]:
            self.inventory["books"].append(self.obstaclemap.items[book])
    def has_book(self, item_id):
        return item_id in [item["type"] for item in self.inventory["books"]]
    def pickup_item(self, item):
        if item.item_info.get("slot", None) == "weapon":
            if self.inventory["weapon"]:
                temp = self.inventory["weapon"].copy()
                temp.update({"x": self.grid_pos[0], "y": self.grid_pos[1]})
                self.obstaclemap.add_item(temp)
            self.inventory["weapon"] = item.item_info
            self.attack_time = item.item_info["weapon"]["attack_time"] * 1000
        elif item.item_info["type"] == "Health Pill":
            self.health += 15
            if self.health > 100:
                self.health = 100
        else:
            self.inventory["books"].append(item.item_info)
        self.obstaclemap.delete_item(item)
        if item.onpickup:
            call_trigger(item.onpickup, self.obstaclemap, self.identifier, self)
    def attack(self, character=None):
        self.walk_to_points = []
        weapon = self.inventory["weapon"]
        if self.attack_time_passed >= self.attack_time:
            self.state = "attack"
            self.attack_time_passed = 0
            self.frame = 0
            if weapon:
                if weapon["weapon"].get("melee", True):
                    SWORD_SOUND.play()
                    if character:
                        if math.sqrt((character.grid_pos[0] - self.grid_pos[0]) ** 2 + (character.grid_pos[1] - self.grid_pos[1]) ** 2) < 1:
                            character.hit(weapon["weapon"]["damage"])
                else:
                    BULLET_SOUND.play()
                    temp = weapon["weapon"]["bullet"].copy()
                    temp.update({"damage": weapon["weapon"]["damage"], "side": self.side, "angle":self.perfect_angle, "grid_pos": list(self.grid_pos), "name": temp["type"], "direction": self.direction})
                    self.obstaclemap.add_bullet(temp)
            else:
                SWORD_SOUND.play()
                if character:                   
                    if math.sqrt((character.grid_pos[0] - self.grid_pos[0]) ** 2 + (character.grid_pos[1] - self.grid_pos[1]) ** 2) < 1:
                        character.hit(1)
    def update(self, **kwargs):
        current_time = kwargs.get("current_time", pygame.time.get_ticks())
        event = kwargs.get("event", None)
        mouse_pos = kwargs.get("mouse_pos", pygame.mouse.get_pos())
        if not self.dead and self.state != "death":
            time_change = current_time - self.current_time
            self.health_time_passed += time_change
            if self.health_time_passed >= 5000 and self.health < 100:
                self.health += 1
                self.health_time_passed = 0
            if event:
                if event.type == MOUSEBUTTONDOWN:
                    self.pressed = True
                elif event.type == MOUSEBUTTONUP:
                    self.pressed = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.attack()
            if self.pressed and mouse_pos != self.last_mouse_pos and self.state != "attack":
                self.after_walk = None
                self.last_mouse_pos = mouse_pos
                x = ((mouse_pos[0] / (TILEWIDTH // 2)) + (mouse_pos[1] / (TILEHEIGHT // 2))) / 2
                y = (((mouse_pos[0] / (TILEWIDTH // 2)) - mouse_pos[1] / (TILEHEIGHT // 2))) / -2
                self.marker_pos = (x, y)
                new_path = self.pathfinding_grid.find_path(tuple(self.grid_pos), (x, y))
                if new_path:
                    self.walking = True
                    self.walk_to(new_path)
            if not self.walk_to_points:
                if self.walking and self.after_walk:
                    self.after_walk()
                self.walking = False
                self.after_walk = None
        super().update(current_time)
    def draw(self, screen_offset):
        self.last_screen_offset = screen_offset
        if not self.dead and self.walk_to_points:
            isox = (self.marker_pos[0] - self.marker_pos[1]) * (TILEWIDTH // 2) - 16
            isoy = (self.marker_pos[0] + self.marker_pos[1]) * (TILEHEIGHT // 2) - 8
            self.screen.blit(self.target_image, (isox + screen_offset[0], isoy + screen_offset[1]))
        super().draw(screen_offset)
