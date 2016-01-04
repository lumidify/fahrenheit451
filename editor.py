import os
import sys
import pygame
from Engine import *
from ImageBrowser import *
from pygame.locals import *

TILEWIDTH = 128
TILEHEIGHT = 64

class Editor():
    def __init__(self, screen, leftpos=0):
        self.screen = screen
        self.default_tile = pygame.image.load("grid.png").convert_alpha()
        self.offset = [300, 0]
        self.vel = [0, 0]
        self.cycle = 0
        self.current_time = pygame.time.get_ticks()
        self.time_passed = 0
        self.pos = [0, 0]
        self.iso_pos = [0, 0]
        self.pressed = False
        self.mouse_pos = pygame.mouse.get_pos()
        self.leftpos = leftpos
        self.engine = Engine(self.screen)
    def open(self, level):
        self.engine.load_map(level)
    def change_cursor_image(self, number):
        self.current_cursor = self.engine.layers[0].create_tile(number, [0, 0])
    def change_size(self, width, height):
        for line in self.tilemap:
            if len(line) > width:
                line = line[:width + 1]
            elif len(line) < width:
                line += [-1 for x in range(width - len(line))]
        if len(self.tilemap) > height:
            self.tilemap = self.tilemap[:height + 1]
        elif len(self.tilemap) < height:
            self.tilemap += [[-1 for x in range(width)] for y in range(height - len(self.tilemap))]
    def save(self):
        temp_list = []
        max_width = 0
        for line in self.tilemap:
            line = [str(x) for x in line]
            temp_list.append(line)
            line_max = max([len(x) for x in line])
            if line_max > max_width:
                max_width = line_max
        f = open(self.tilemap_path, "w")
        for line in temp_list:
            line = [x.rjust(max_width) for x in line]
            f.write(" ".join(line) + "\n")
        f.close()
        
    def update(self, event=None):
        time_change = pygame.time.get_ticks() - self.current_time
        self.time_passed += time_change
        self.current_time += time_change
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > self.leftpos:
            mouse_pos1 = [mouse_pos[0] - self.offset[0] - self.current_cursor.region[1][0] // 2, mouse_pos[1] - self.offset[1] - self.current_cursor.region[1][0] // 2]
            x = round((mouse_pos1[0] / (TILEWIDTH // 2) + mouse_pos1[1] / (TILEHEIGHT // 2)) / 2)
            y = round((mouse_pos1[1] / (TILEHEIGHT // 2) -(mouse_pos1[0] / (TILEWIDTH // 2))) / 2)
            self.current_cursor.grid_pos = [x, y]
        else:
            self.iso_pos[0] = self.leftpos
        if event:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.vel[0] = -5
                elif event.key == K_LEFT:
                    self.vel[0] = 5
                elif event.key == K_UP:
                    self.vel[1] = 5
                elif event.key == K_DOWN:
                    self.vel[1] = -5
                elif event.key == K_a:
                    self.current_image += 1
                    if self.current_image >= len(self.tiles):
                        self.current_image = 0
                elif event.key == K_d:
                    self.current_image -= 1
                    if self.current_image < 0:
                        self.current_image = len(self.tiles) - 1
                elif event.key == K_s:
                    self.save()
            elif event.type == KEYUP:
                if event.key in [K_RIGHT, K_LEFT]:
                    self.vel[0] = 0
                elif event.key in [K_UP, K_DOWN]:
                    self.vel[1] = 0
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and mouse_pos[0] > self.leftpos:
                self.pressed = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self.pressed = False
            elif event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[1]:
                    self.offset[0] += mouse_pos[0] - self.mouse_pos[0]
                    self.offset[1] += mouse_pos[1] - self.mouse_pos[1]
                self.mouse_pos = mouse_pos
        if self.pressed:
            try:
                if self.pos[0] >= 0 and self.pos[1] >= 0 and mouse_pos[0] > self.leftpos:
                    self.tilemap[self.pos[1]][self.pos[0]] = self.current_image
            except:
                pass
        self.offset[0] += self.vel[0]
        self.offset[1] += self.vel[1]
        self.engine.update()
    def draw(self):
        self.engine.draw(self.offset)
        for y in range(50):
            for x in range(50):
                isox = (x - y) * (TILEWIDTH // 2) + self.offset[0]
                isoy = (x + y) * (TILEHEIGHT // 2) + self.offset[1]
                screen.blit(self.default_tile, (isox, isoy))
                
        self.current_cursor.draw([0, 0])

if __name__ == "__main__":                
    pygame.init()
    screen_info = pygame.display.Info()
    screen_size = [screen_info.current_w, screen_info.current_h]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    tilemap = Editor(screen, os.path.join("graphics", "floor_tiles", "static.txt"), "TheMap/map.floor", 300)
    args = sys.argv
    if len(args) > 1:
        tilemap.load_tilemap(sys.argv[1])
    if len(args) == 4:
        tilemap.change_size(int(sys.argv[2]), int(sys.argv[3]))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(400, 100)
    imagebrowser = ImageBrowser(screen, [["graphics/floor_tiles/static.txt", "Floor Tiles"], ["graphics/obstacles/static.txt", "Obstacles"]], tilemap)
    imagebrowser.change_screen_size(screen_size)

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
                imagebrowser.change_screen_size(screen_size)
            else:
                tilemap.update(event)
                imagebrowser.update(event)
        tilemap.update()
        tilemap.draw()
        imagebrowser.draw()
        pygame.display.update()
