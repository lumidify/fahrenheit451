import os
import sys
import math
import pygame
from call_trigger import *
from CONSTANTS import *
from pygame.locals import *
from Engine import *
TILEWIDTH = 128
TILEHEIGHT = 64
FONT = pygame.font.Font("Lumidify_Casual.ttf", 20)
BULLET_SOUND = pygame.mixer.Sound("Single_Pulse.ogg")
SWORD_SOUND = pygame.mixer.Sound("Sword.ogg")
BULLET_SOUND.set_volume(0.2)
SWORD_SOUND.set_volume(0.5)

class Character():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.type = kwargs.get("name")
        self.orig_info = kwargs.get("orig_info", {})
        self.weapon_name = kwargs.get("weapon", None)
        self.direction = kwargs.get("direction", "N")
        self.health = kwargs.get("health", 10)
        self.side = kwargs.get("side", "enemy")
        self.grid_pos = [kwargs.get("x", 0), kwargs.get("y", 0)]
        self.state = "stand"
        self.last_state = "stand"
        self.aggression_distance = kwargs.get("aggression_distance", 2)
        self.identifier = kwargs.get("id", None)
        self.label = kwargs.get("label", "DEFAULT NAME")
        self.images = kwargs["images"]
        self.weapon = kwargs.get("weapon_final", None)
        self.ondeath = kwargs.get("ondeath", None)
        self.walk_to_points = []
        self.last_walk_to_pos = []
        self.fps = kwargs["fps"]
        self.intervals = {x[0]:1000//x[1] for x in self.fps.items()}
        self.current_time = kwargs.get("current_time", pygame.time.get_ticks())
        self.time_passed = 0
        self.walk_time_passed = 0
        self.gethit_recover_time = kwargs.get("gethit_recover_time", 0) * 1000
        self.gethit_time_passed = 0
        self.individual_frame_time = self.intervals["walk"] // self.fps["walk"]
        self.vel = [0, 0]
        self.speed = kwargs.get("speed", 0.1)
        self.adjusted_speed = self.speed / self.fps["walk"]
        self.frame = 0
        self.dead = kwargs.get("dead", False)
        self.perfect_angle = 90
        self.next_delta = [0, 0]
        self.selected = False
        self.direction_angles = {90: "N", 45: "NE", 0: "E", -45: "SE", -90: "S", -135: "SW", 180: "W", -180: "W", 135: "NW"}
        self.realrect = Rect(0, 0, 0, 0)
        self.selectable = True
        self.movement_temporarily_suppressed = False
        self.adjusted_vel = [0, 0]
        if self.weapon:
            self.attack_time = self.weapon["weapon"]["attack_time"] * 1000
        self.attack_time_passed = 0
    def calc_dir_vel(self, deltax=None, deltay=None):
        if not deltax: 
            deltax = self.walk_to_points[0][0] - self.grid_pos[0]
        if not deltay:
            deltay = self.grid_pos[1] - self.walk_to_points[0][1]
        if self.walk_to_points[0] != self.last_walk_to_pos:
            self.last_walk_to_pos = self.walk_to_points[0]
            self.perfect_angle = math.atan2(deltay, deltax)
            self.direction = self.direction_angles[round(math.degrees(self.perfect_angle) / 45) * 45]
            self.vel[0] = math.cos(self.perfect_angle)
            self.vel[1] = -math.sin(self.perfect_angle)
            self.adjusted_vel = [self.vel[0] * self.adjusted_speed, self.vel[1] * self.adjusted_speed]
    def get_dict(self):
        temp = {"x": self.grid_pos[0], "y": self.grid_pos[1], "name": self.type}
        if self.direction != "N":
            temp["direction"] = self.direction
        if self.health != 10:
            temp["health"] = self.health
        if self.aggression_distance != self.orig_info["aggression_distance"]:
            temp["aggression_distance"] = self.aggression_distance
        if self.identifier is not None:
            temp["id"] = self.identifier
        if self.label != self.orig_info["label"]:
            temp["label"] = self.label
        if self.weapon is not None and self.weapon_name != self.orig_info["weapon"]:
            temp["weapon"] = self.weapon_name
        if self.ondeath is not None:
            temp["ondeath"] = self.ondeath
        if self.dead:
            temp["dead"] = self.dead
        if self.waypoints:
            temp["waypoints"] = self.waypoints
        if self.area:
            temp["random_walk_area"] = self.area
        return temp
    def walk(self):
        magnitude = self.walk_time_passed / self.individual_frame_time
        self.walk_time_passed = 0
        self.state = "walk"
        deltax = self.walk_to_points[0][0] - self.grid_pos[0]
        deltay = self.grid_pos[1] - self.walk_to_points[0][1]
        self.calc_dir_vel(deltax, deltay)
        next_deltax = self.walk_to_points[0][0] - (self.grid_pos[0] + self.adjusted_vel[0])
        next_deltay = (self.grid_pos[1] + self.adjusted_vel[1]) - self.walk_to_points[0][1]
        if abs(deltax) <= abs(next_deltax) and abs(deltay) <= abs(next_deltay):
            self.walk_to_points.pop(0)
            if self.walk_to_points:
                self.calc_dir_vel()
        if self.walk_to_points:
            self.grid_pos[0] += self.adjusted_vel[0] * magnitude
            self.grid_pos[1] += self.adjusted_vel[1] * magnitude
        else:
            self.state = "stand"
            self.frame = 0
    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False
    def hit(self, damage):
        if self.state != "gethit":
            self.last_state = self.state
            self.frame = 0
        self.state = "gethit"
        self.gethit_time_passed = 0
        self.health -= damage
        if self.health <= 0:
            self.die()
    def get_rect(self, rect_type):
        if rect_type == "realrect":
            return self.realrect
    def die(self):
        self.state = "death"
        self.frame = 0
        self.selectable = False
        if self.ondeath:
            call_trigger(self.ondeath, self.obstaclemap, self.identifier, self)
    def turn_to(self, character):
        deltax = character.grid_pos[0] - self.grid_pos[0]
        deltay = self.grid_pos[1] - character.grid_pos[1]
        self.perfect_angle = math.atan2(deltay, deltax)
        self.direction = self.direction_angles[round(math.degrees(self.perfect_angle) / 45) * 45]
    def attack(self, character):
        try:
            if self.movement_state == "waypoints":
                self.remaining_waypoints.insert(0, self.walk_to_points[0])
                self.last_walk_to_pos = None
        except:
            pass
        self.walk_to_points = []
        self.movement_temporarily_suppressed = True
        if self.weapon:
            if self.attack_time_passed >= self.attack_time and self.gethit_time_passed > self.gethit_recover_time:
                self.state = "attack"
                self.attack_time_passed = 0
                self.frame = 0
                if self.weapon.get("weapon", {}).get("melee", True):
                    SWORD_SOUND.play()
                    character.hit(self.weapon["weapon"]["damage"])
                else:
                    BULLET_SOUND.play()
                    temp = self.weapon["weapon"]["bullet"].copy()
                    temp.update({"damage": self.weapon["weapon"]["damage"], "side": self.side, "angle":self.perfect_angle, "grid_pos": list(self.grid_pos), "name": temp["type"], "direction": self.direction})
                    self.obstaclemap.add_bullet(temp)
    def walk_to(self, points):
        if self.state != "walk":
            self.frame = 0
        self.state = "walk"
        self.walk_to_points = points
    def update(self, current_time=None, event=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        if not self.dead:
            time_change = current_time - self.current_time
            self.attack_time_passed += time_change
            self.time_passed += time_change
            self.gethit_time_passed += time_change
            self.current_time = current_time
            if self.time_passed >= self.intervals[self.state]:
                self.frame += 1
                self.time_passed = 0
                if self.frame >= len(self.images[self.direction][self.state]):
                    if self.state == "death":
                        self.dead = True
                    elif self.state == "attack":
                        self.state = "stand"
                    elif self.state == "gethit":
                        self.state = self.last_state
                    self.frame = 0
            if self.walk_to_points:
                self.walk_time_passed += time_change
                if self.walk_time_passed >= self.individual_frame_time and self.state != "death" and self.state != "attack":
                    self.walk()
    def draw_label(self, screen_offset):
        if self.label:
            self.screen.blit(FONT.render(self.label, True, (255, 255, 255), (0, 0, 0)), (self.realrect.x + screen_offset[0], self.realrect.y + screen_offset[1]))
    def draw(self, screen_offset):
        if self.dead:
            tile_dict = self.images[self.direction]["death"][-1]
        else:
            tile_dict = self.images[self.direction][self.state][self.frame]
        isox = (self.grid_pos[0] - self.grid_pos[1]) * (TILEWIDTH // 2) + tile_dict["offset"][0]
        isoy = (self.grid_pos[0] + self.grid_pos[1]) * (TILEHEIGHT // 2) + tile_dict["offset"][1]
        #Update self.realrect here since isox and isoy are already computed
        self.realrect = Rect((isox, isoy), tile_dict["size"])
        if self.selected and not self.dead:
            temp_surf = pygame.surface.Surface(tile_dict["size"]).convert_alpha()
            temp_surf.fill((100, 100, 100, 0))
            temp_surf.blit(tile_dict["image"], (0, 0), (tile_dict["pos"], tile_dict["size"]), BLEND_RGBA_ADD)
            self.screen.blit(temp_surf, (isox + screen_offset[0], isoy + screen_offset[1]))
        else:
            self.screen.blit(tile_dict["image"], (isox + screen_offset[0], isoy + screen_offset[1]), (tile_dict["pos"], tile_dict["size"]))
        """
        For pathfinding debug:
        if self.walk_to_points:
            line_points = [((x[0] - x[1]) * (TILEWIDTH // 2) + screen_offset[0], (x[0] + x[1]) * (TILEHEIGHT // 2) + screen_offset[1]) for x in self.walk_to_points]
            if len(line_points) > 1:
                pygame.draw.lines(self.screen, (255, 255, 255), False, line_points, 2)
        """
