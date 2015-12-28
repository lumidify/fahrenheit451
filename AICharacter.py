import os
import sys
import random
import pygame
from Engine import *
from Montag import *
from Character import Character
from pygame.locals import *

#WAYPOINTS

class AICharacter(Character):
    def __init__(self, screen, atlas, config, pos, enemy=None, follow_enemy=True, area=[5, 0, 5, 5], movement_state="random_move", pause_time=1000, direction="N", state="stand"):
        super().__init__(screen, atlas, config, pos, direction, state)
        self.movement_state = movement_state
        self.area = area
        self.pause_time = pause_time
        self.current_time1 = pygame.time.get_ticks()
        self.time_passed1 = 0
        self.following = None
        self.enemy = enemy
        self.follow_enemy = follow_enemy
        self.last_movement_state = self.movement_state
    def hold_position(self):
        self.movement_state = None
    def follow(self, character):
        self.following = character
        self.movement_state = "following"
    def update(self, current_time=None, event=None):
        if not current_time:
            current_time = pygame.time.get_ticks()
        if self.state == "stand":
            time_change = current_time - self.current_time
            self.time_passed1 += time_change
            self.current_time1 += time_change
        else:
            self.current_time1 = current_time
            self.time_passed1 = 0
        if not self.dead:
            if self.movement_state == "random_move" and not self.walk_to_points and self.time_passed1 >= self.pause_time:
                self.walk_to_points = [[
                random.uniform(self.area[0], self.area[0] + self.area[2]),
                random.uniform(self.area[1], self.area[1] + self.area[3])]]
                self.frame = 0
            elif self.movement_state == "following":
                self.walk_to_points = [self.following.pos.copy()]
            elif self.follow_enemy and self.enemy:
                if self.area[0] <= self.enemy.pos[0] <= self.area[0] + self.area[2] and self.area[1] <= self.enemy.pos[1] <= self.area[3]:
                    self.walk_to_points = [self.enemy.pos.copy()]
        super().update(current_time, event)
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    chars = []
    montag = Montag(screen, "../graphics2/droids/blue_guard/atlas.txt", "../graphics2/droids/red_guard/config.txt", [3, 0])
    for x in range(50):
        chars.append(AICharacter(screen, "../graphics2/droids/598/atlas.txt", "../graphics2/droids/blue_guard/config.txt", [3, 2], montag, True))
    chars.append(montag)
    b = Engine(screen)
    b.load_tilemap("TheMap/map.floor", 0)
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
                for char in chars:
                    char.update(current_time, event)
        
        b.update()
        b.draw([0, 0])
        chars.sort(key=lambda x: (x.pos[1], x.pos[0]))
        for char in chars:
            char.update(current_time)
            char.draw()
        pygame.display.update()
