import os
import sys
import pygame
from Engine import Engine
from pygame.locals import *
from Character import Character

TILEWIDTH = 128
TILEHEIGHT = 64

class Montag(Character):
    def __init__(self, screen, atlas, config, pathfinding_grid, pos=[0, 0], direction="N", state="stand"):
        super().__init__(screen, atlas, config, pos, direction, state, "Montag")
        self.pathfinding_grid = pathfinding_grid
        self.pressed = False
        self.target_image = pygame.image.load("../graphics2/cursors/mouse_move_cursor_0.png").convert_alpha()
        self.last_mouse_pos = ()
    def update(self, current_time=None, event=None):
        if not self.dead:
            mouse_pos = pygame.mouse.get_pos()
            if event:
                if event.type == MOUSEBUTTONDOWN:
                    self.pressed = True
                elif event.type == MOUSEBUTTONUP:
                    self.pressed = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.attack()
            if self.time_passed >= self.fps[self.state] and self.pressed and mouse_pos != self.last_mouse_pos:
                self.last_mouse_pos = mouse_pos
                mouse_pos = [mouse_pos[0] - TILEWIDTH // 2, mouse_pos[1]]
                x = ((mouse_pos[0] / (TILEWIDTH // 2)) + (mouse_pos[1] / (TILEHEIGHT // 2))) / 2
                y = (((mouse_pos[0] / (TILEWIDTH // 2)) - mouse_pos[1] / (TILEHEIGHT // 2))) / -2
                new_path = self.pathfinding_grid.find_path(tuple(self.pos), (x, y))
                if new_path:
                    self.state = "walk"
                    self.walk_to_points = new_path
        super().update(current_time)
    def draw(self):
        if self.walk_to_points:
            isox = (self.walk_to_points[-1][0] - self.walk_to_points[-1][1]) * (TILEWIDTH // 2) + 49
            isoy = (self.walk_to_points[-1][0] + self.walk_to_points[-1][1]) * (TILEHEIGHT // 2) - 7
            self.screen.blit(self.target_image, (isox, isoy))
        super().draw()
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    character = Montag(screen, "../graphics2/droids/red_guard/atlas.txt", "../graphics2/droids/red_guard/config.txt", [3, 0])
    b = Engine(screen)
    b.load_tilemap("TheMap/map.floor", 0)
    b.add_layer()
    b.load_tilemap("TheMap/map1.floor", 1)
    while True:
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
                character.update(event)
        b.update()
        b.draw([0, 0])
        character.update()
        character.draw()
        pygame.display.update()
