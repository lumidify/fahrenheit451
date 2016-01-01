import os
import sys
import pygame
from loader import *
from QuadTree import QuadTree
from Montag import *
from Obstacles import *
from Floor import Floor
from pygame.locals import *
"""
CHARACTER: PATH SMOOTHING; GETTING STUCK IN OBSTACLES
"""
TILEWIDTH = 128
TILEHEIGHT = 64
FLOORPATH = os.path.join("graphics", "floor_tiles")
ATLASPATH = "static.txt"
ANIMATIONSPATH = "animations.txt"
FONT = pygame.font.Font("Lumidify_Casual.ttf", 50)

class Engine():
    def __init__(self, screen):
        print("Initializing Lumidify Isometric Engine (LIE) Version 1.0 ...")
        self.screen = screen
        self.screen.blit(FONT.render("Loading...", True, (255, 255, 255)), (0, 0))
        pygame.display.update()
        self.tiles, self.obstacles, self.characters = load_tiles()
        self.floor = Floor(self.screen, self.tiles)
        self.obstacles = Obstacles(self.screen, self.obstacles, [50, 50], self.characters)
        #self.player = Montag(screen, "graphics/droids/red_guard/atlas.txt", "graphics/droids/red_guard/config.txt", self.obstacles.grid, [0, 0])
        self.obstacles.load_charactermap("TheMap/map.characters")
        self.game_variables = {}
        self.active_layer = 0
    def add_layer(self):
        self.floor.add_layer()
    def load_tilemap(self, tilemap, layer=0):
        self.floor.load_tilemap(tilemap, layer)
    def load_obstaclemap(self, path, layer=0):
        self.obstacles.load_obstaclemap(path, layer)
    def load_charactermap(self, path):
        pass
    def update(self, event=None):
        current_time = pygame.time.get_ticks()
        self.floor.update(current_time)
        self.obstacles.update(current_time=current_time, event=event)
        #self.player.update(None, event)
    def draw(self, screen_offset):
        self.floor.draw(screen_offset)
        self.obstacles.draw(screen_offset)
        #self.player.draw(screen_offset)
if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    clock = pygame.time.Clock()
    b = Engine(screen)
    b.load_tilemap("TheMap/map.floor", 0)
    b.load_obstaclemap("TheMap/map.obstacles", 0)
    while True:
        screen.fill((0, 0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                screen_size = event.dict["size"]
                screen = pygame.display.set_mode(screen_size, RESIZABLE)
            else:
                b.update(event)
        b.update()
        b.draw([0, 0])
        pygame.display.update()
