import os
import sys
import random
import pygame
from Engine import *
from Montag import *
from Character import Character
from pygame.locals import *

class AICharacter(Character):
    def __init__(self, screen, atlas, config, **kwargs):
        super().__init__(screen, atlas, config, **kwargs)
        self.enemy = kwargs.get("enemy", None)
        self.movement_state = kwargs.get("movement_state", None)
        self.waypoints = kwargs.get("waypoints", None)
        self.pathfinding_grid = kwargs.get("pathfinding_grid", None)
        self.dialog = kwargs.get("dialog", None)
        self.dialogmanager = kwargs.get("dialogmanager", None)
        if self.waypoints:
            self.remaining_waypoints = self.waypoints.copy()
            self.walk_to_points = [self.remaining_waypoints.pop(0)]
            self.movement_state = "waypoints"
            self.state = "walk"
        self.area = kwargs.get("area", [0, 0, 0, 0])
        self.pause_time = kwargs.get("pause_time", 1000)
        self.pause_time_passed = 0
    def click(self):
        if self.dialog:
            self.dialogmanager.start_dialog(self.dialog)
    def hold_position(self):
        self.movement_state = None
    def update(self, current_time=None, event=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        if self.state == "stand":
            time_change = current_time - self.current_time
            self.pause_time_passed += time_change
        else:
            self.pause_time_passed = 0
        if not self.dead:
            if not self.walk_to_points and self.pause_time_passed >= self.pause_time:
                if self.movement_state == "random_walk":
                    self.walk_to_points = self.pathfinding_grid.find_path(self.pos, [
                    random.uniform(self.area[0], self.area[0] + self.area[2]),
                    random.uniform(self.area[1], self.area[1] + self.area[3])])
                    self.frame = 0
                elif self.movement_state == "waypoints":
                    self.walk_to_points = [self.remaining_waypoints.pop(0)]
                    if len(self.remaining_waypoints) == 0:
                        self.remaining_waypoints = self.waypoints.copy()
        super().update(current_time, event)
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    chars = []
    b = Engine(screen)
    b.load_tilemap("TheMap/map.floor", 0)
    b.load_obstaclemap("TheMap/map.obstacles", 0)
    montag = AICharacter(screen, "graphics/droids/blue_guard/atlas.txt", "graphics/droids/red_guard/config.txt", pathfinding_grid=b.obstacles.grid, pos=[3, 0], movement_state="random_walk", area=[5, 0, 10, 5])
    while True:
        current_time = pygame.time.get_ticks()
        clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                screen_size = event.dict["size"]
                screen = pygame.display.set_mode(screen_size, RESIZABLE)
            else:
                montag.update(current_time, event)
        
        b.update()
        b.draw([0, 0])
        #chars.sort(key=lambda x: (x.pos[1], x.pos[0]))
        montag.update(current_time)
        montag.draw()
        pygame.display.update()
