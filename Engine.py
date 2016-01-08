import os
import sys
import pygame
pygame.init()
import importlib
from loader import *
from QuadTree import QuadTree
from Montag import *
from Obstacles import *
from Floor import Floor
from pygame.locals import *
from CONSTANTS import *
"""
This code is extremely bad, use at your own risk.
"""
TILEWIDTH = 128
TILEHEIGHT = 64
FLOORPATH = os.path.join("graphics", "floor_tiles")
FONT = pygame.font.Font("Lumidify_Casual.ttf", 50)

def load_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Engine():
    def __init__(self, screen):
        print("Initializing Lumidify Isometric Engine (LIE) Version 1.0 ...")
        self.screen = screen
        self.screen.blit(FONT.render("Loading...", True, (255, 255, 255)), (0, 0))
        self.screen.blit(FONT.render("Patience is a virtue.", True, (255, 255, 255)), (0, 40))
        pygame.display.update()
        self.tiles, self.obstacles, self.characters, self.items, self.bullets = load_tiles()
        self.floor = Floor(self.screen, self.tiles)
        self.obstacles = Obstacles(self.screen, self.obstacles, self.characters, self.items, self.bullets, self)
        temp = self.obstacles.characters["GUA"].copy()
        temp["weapon"] = None
        self.player = Montag(self.screen, x=0, y=0, obstaclemap=self.obstacles, **temp)
        self.obstacles.player = self.player
        self.game_variables = {}
        self.active_layer = 0
        self.screen_offset = [0, 0]
        self.loaded_maps = {}
        self.saved_maps = []
        self.current_map = ""
        self.wongame = False
        self.lostgame = False
    def savegame(self):
        if not os.path.isdir("save"):
            os.mkdir("save")
        for path, item in self.loaded_maps.items():
            final_path = os.path.join("save", path)
            if not os.path.exists(final_path):
                os.makedirs(final_path)
            self.obstacles.save(final_path, item["characters"] + item["dead_characters"], item["item_map"], item["triggers"], item["obstacles"])
            self.floor.save(os.path.join(final_path, "floor.py"), item["floor"])
            with open(os.path.join(final_path, "config.py"), "w") as f:
                f.write("config = " + repr(item["config"]))
        if not os.path.exists(os.path.join("save", self.current_map)):
            os.makedirs(os.path.join("save", self.current_map))
        self.obstacles.save(os.path.join("save", self.current_map), self.obstacles.charactermap + self.obstacles.dead_characters, self.obstacles.item_map, self.obstacles.triggers, self.obstacles.layers)
        self.floor.save(os.path.join("save", self.current_map, "floor.py"), self.floor.layers)
        with open(os.path.join("save", self.current_map, "config.py"), "w") as f:
            f.write("config = " + repr(self.config))
        player_config = {"dead": self.player.dead, "grid_pos": self.player.grid_pos.copy(), "current_map": self.current_map, "won": self.wongame, "lost": self.lostgame, "inventory": self.player.get_inventory(), "health": self.player.health}
        with open(os.path.join("save", "config.py"), "w") as f:
            f.write("player_config = " + repr(player_config))
    def load_game(self):
        if os.path.isdir("save"):
            player_config = load_module(os.path.join("save", "config.py")).player_config.copy()
            self.player.reset()
            self.player.dead = player_config["dead"]
            self.player.load_inventory(player_config["inventory"])
            self.saved_maps = os.listdir("save")
            self.current_map = player_config["current_map"]
            self.player.health = player_config["health"]
            self.saved_maps = os.listdir("save")
            self.load_map(self.current_map, spawn_pos=player_config["grid_pos"])
            if player_config["won"]:
                self.wingame()
            elif player_config["lost"]:
                self.losegame()
    def load_map(self, path, **kwargs):
        if path in self.saved_maps:
            self.saved_maps.remove(path)
            path = os.path.join("save", path)
        if self.current_map:
            self.loaded_maps[self.current_map] = {}
            self.loaded_maps[self.current_map]["floor"] = self.floor.layers.copy()
            self.loaded_maps[self.current_map]["obstacles"] = self.obstacles.layers.copy()
            self.loaded_maps[self.current_map]["characters"] = self.obstacles.charactermap.copy()
            self.loaded_maps[self.current_map]["dead_characters"] = self.obstacles.dead_characters.copy()
            self.loaded_maps[self.current_map]["item_map"] = self.obstacles.item_map.copy()
            self.loaded_maps[self.current_map]["bullets"] = self.obstacles.bullets.copy()
            self.loaded_maps[self.current_map]["triggers"] = self.obstacles.triggers.copy()
            self.loaded_maps[self.current_map]["config"] = self.config.copy()
        if path.startswith("save"):
            self.current_map = path[5:]
        else:
            self.current_map = path
        if path in self.loaded_maps:
            self.floor.layers = self.loaded_maps[path]["floor"].copy()
            self.obstacles.layers = self.loaded_maps[path]["obstacles"].copy()
            self.obstacles.charactermap = self.loaded_maps[path]["characters"].copy()
            self.obstacles.dead_characters = self.loaded_maps[path]["dead_characters"].copy()
            self.obstacles.item_map = self.loaded_maps[path]["item_map"].copy()
            self.obstacles.bullets = self.loaded_maps[path]["bullets"].copy()
            self.obstacles.triggers = self.loaded_maps[path]["triggers"].copy()
            self.config = self.loaded_maps[path]["config"].copy()
        else:
            self.floor.load_tilemap(os.path.join(path, "floor.py"))
            self.obstacles.load_obstaclemap(os.path.join(path, "obstacles.py"))
            self.obstacles.load_charactermap(os.path.join(path, "characters.py"))
            self.obstacles.load_item_map(os.path.join(path, "items.py"))
            self.obstacles.load_triggermap(os.path.join(path, "triggers.py"))
            self.obstacles.dead_characters = []
            self.obstacles.bullets = []
            self.config = load_module(os.path.join(path, "config.py")).config.copy()
        try:
            pygame.mixer.music.load(self.config.get("music", "Search_Art_S31_Undercover_Operative_0.ogg"))
            pygame.mixer.music.play(-1)
        except:
            pass
        if kwargs.get("spawn_pos", None):
            self.player.grid_pos = kwargs["spawn_pos"].copy()
        else:
            self.player.grid_pos = self.config.get("spawn_pos", [0, 0]).copy()
        self.player.reset()
        mapsize = self.config.get("level_dimensions", [50, 50])
        self.obstacles.change_size(mapsize)
        self.obstacles.refresh_trigger_quadtree()
        self.obstacles.refresh_grid()
    def update(self, event=None):
        if not self.wongame:
            screen_size = self.screen.get_size()
            isox = (self.player.grid_pos[0] - self.player.grid_pos[1]) * (ISOWIDTH // 2)
            isoy = (self.player.grid_pos[0] + self.player.grid_pos[1]) * (ISOHEIGHT // 2)
            self.screen_offset = [screen_size[0] // 2 - isox, screen_size[1] // 2 - isoy]
            current_time = pygame.time.get_ticks()
            self.floor.update(current_time)
            self.obstacles.update(current_time=current_time, event=event)
        if event and event.type == KEYDOWN:
            if event.key == K_F3:
                self.savegame()
            elif event.key == K_F4:
                self.load_game()
    def wingame(self):
        self.wongame = True
        pygame.mixer.music.load("wingame.ogg")
        pygame.mixer.music.play(-1)
    def losegame(self):
        self.lostgame = True
        pygame.mixer.music.load("Sad_Piano_3.ogg")
        pygame.mixer.music.play(-1)
    def draw(self):
        self.floor.draw(self.screen_offset)
        self.obstacles.draw(self.screen_offset)
        if self.wongame:
            screen.blit(FONT.render("Congratulations, you won!", True, (255, 255, 255)), (0, 0))
        elif self.lostgame:
            screen.blit(FONT.render("Shame be upon you! You lost!", True, (255, 255, 255)), (0, 0))
        self.screen.blit(FONT.render("Health: " + str(self.player.health), True, (255, 255, 255)), (self.screen.get_size()[0] - 200, 0))
if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Fahrenheit 451")
    engine = Engine(screen)
    if len(sys.argv) > 1:
        engine.load_map(sys.argv[1])
    else:
        engine.load_map("TheMap")
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
                engine.update(event)
        engine.update()
        engine.draw()
        pygame.display.update()
