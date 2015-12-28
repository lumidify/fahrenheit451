import os
import sys
import pygame
from Button import Button, ImageButton
from pygame.locals import *

TILEWIDTH = 128
TILEHEIGHT = 64

class ScrollBar():
    def __init__(self, screen, pos, mode, size, scroll_box_size):
        self.screen = screen
        self.pos = pos
        self.mode = mode
        self.size = size
        self.scroll_box_size = scroll_box_size
        self.normal_color = (255, 100, 100)
        self.highlighted_color = (255, 150, 150)
        self.pressed_color = (200, 200, 200)
        self.background_color = (255, 255, 255)
        self.highlighted = False
        self.selected = False
        self.rect = Rect(self.pos, (0, 0))
        self.background_rect = Rect(self.pos, self.size)
        self.calculate_handle_size()
        self.selected_point = []
    def calculate_handle_size(self):
        if self.mode == "vertical":
            self.handle_size = (self.size[0], self.size[1] / self.scroll_box_size[1] * self.size[1])
        elif self.mode == "horizontal":
            self.handle_size = (self.size[0] / self.scroll_box_size[0] * self.size[0], self.size[1])
        self.rect.size = self.handle_size
    def update_box_size(self, new_size):
        self.scroll_box_size = new_size
        self.calculate_handle_size()
    def update_height(self, height):
        temp_offset = (self.rect.y - self.pos[1]) / self.size[1]
        self.size[1] = height
        self.background_rect.height = height
        self.calculate_handle_size()
        self.rect.y = temp_offset * self.size[1] + self.pos[1]
    def get_offset(self):
        if self.mode == "vertical":
            return -(self.get_decimal() * self.scroll_box_size[1])
        elif self.mode == "horizontal":
            return -(self.get_decimal() * self.scroll_box_size[0])
    def get_percent(self):
        return round(self.get_decimal() * 100)
    def get_decimal(self):
        if self.mode == "vertical":
            return (self.rect.y - self.pos[1]) / (self.size[1] - self.handle_size[1])
        elif self.mode == "horizontal":
            return (self.rect.x - self.pos[0]) / (self.size[0] - self.handle_size[0])
    def set_position(self, position):
        if self.mode == "vertical":
            self.rect.y = position
        elif self.mode == "horizontal":
            self.rect.x == position
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_rect = self.rect.collidepoint(mouse_pos)
        collide_background_rect = self.background_rect.collidepoint(mouse_pos)
        
        if collide_rect:
            self.highlighted = True
        else:
            self.highlighted = False
        if event.type == MOUSEMOTION:
            if self.selected:
                if self.mode == "vertical":
                    self.rect.y = mouse_pos[1] - self.selected_point[1]
                elif self.mode == "horizontal":
                    self.rect.x = mouse_pos[0] - self.selected_point[0]
                self.adjust()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if collide_rect:
                    self.set_selected(mouse_pos)
                elif collide_background_rect and not collide_rect:
                    if self.mode == "vertical":
                        self.rect.centery = mouse_pos[1]
                        self.set_selected(mouse_pos)
                    elif self.mode == "horizontal":
                        self.rect.centerx = mouse_pos[0]
                        self.set_selected(mouse_pos)
                else:
                    self.selected = False
            elif event.button == 4:
                self.rect.centery -= int(0.1 * self.rect.height)
                print(self.rect.height)
            elif event.button == 5:
                self.rect.centery += int(0.1 * self.rect.height)
            self.adjust()
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.selected = False
    def set_selected(self, mouse_pos):
        self.selected = True
        self.selected_point = [mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y]
    def adjust(self):
        if self.rect.top <= self.pos[1]:
            self.rect.top = self.pos[1]
        if self.rect.bottom >= self.pos[1] + self.size[1]:
            self.rect.bottom = self.pos[1] + self.size[1]
        if self.rect.left <= self.pos[0]:
            self.rect.left = self.pos[0]
        if self.rect.right >= self.pos[0] + self.size[0]:
            self.rect.right = self.pos[0] + self.size[0]
    def draw(self):
        color = self.normal_color
        if self.highlighted:
            color = self.highlighted_color
        if self.selected:
            color = self.pressed_color
        pygame.draw.rect(self.screen, self.background_color, self.background_rect)
        pygame.draw.rect(self.screen, color, self.rect)

class ImageTab():
    def __init__(self, screen, atlas, parent, pos=[0, 0], height=440):
        self.screen = screen
        self.atlas = atlas
        self.parent = parent
        self.path = os.path.split(self.atlas)[0]
        self.images = []
        self.offset = [0, 0]
        self.pos = pos
        self.height = height
        self.load()
    def get_height(self):
        return round(len(self.images) / 2) * 64
    def load(self):
        f = open(self.atlas)
        image = None
        image_surf = None
        counter = 0
        for line in f.readlines():
            if line.startswith("*"):
                image = line.split()[1]
                image_surf = pygame.image.load(os.path.join(self.path, image)).convert_alpha()
            else:
                line = line.split()
                pos = [int(x) for x in line[1:3]]
                size = [int(x) for x in line[3:5]]
                self.images.append(ImageButton(self.screen, image_surf, [0, 0], self.change_cursor_image, counter, [pos, size]))
                counter += 1
        f.close()
        self.adjust()
    def set_offset(self, offset):
        self.offset = offset
        self.adjust()
    def set_height(self, height):
        self.height = height
        self.adjust()
    def adjust(self):
        for index, image in enumerate(self.images):
            image.set_pos([index % 2 * (TILEWIDTH) + self.offset[0] + self.pos[0], index // 2 * (TILEHEIGHT) + self.offset[1] + self.pos[1]])
        start = int(-self.offset[1] / 32)
        if start > 2:
            start -= 2
        else:
            start = 0
        self.visible_images = self.images[start:start + round(self.height / 32) + 1]
    def change_cursor_image(self, number):
        self.parent.change_cursor_image(number)
    def update(self, event):
        for image in self.visible_images:
            image.update(event)
    def draw(self):
        for image in self.visible_images:
            image.draw()
    
class ImageBrowser():
    def __init__(self, screen, atlases, editor):
        self.screen = screen
        self.tabs = []
        self.tab_buttons = []
        self.scrollbars = []
        self.offset = [0, 0]
        self.editor = editor
        for index, atlas in enumerate(atlases):
            self.tabs.append(ImageTab(self.screen, atlas[0], self, [0, 60]))
            self.tab_buttons.append(Button(self.screen, [index * 100, 0], atlas[1], None, self.switch_tab, index))
            self.scrollbars.append(ScrollBar(self.screen, [TILEWIDTH * 2, 60], "vertical", [20, 440], [0, self.tabs[-1].get_height()]))
        self.active_tab = 0
        self.rect = Rect([0, 0], [256, screen.get_height()])
    def update(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.tabs[self.active_tab].update(event)
            for button in self.tab_buttons:
                button.update(event)
        self.scrollbars[self.active_tab].update(event)
        new_offset = self.scrollbars[self.active_tab].get_offset()
        if new_offset != self.offset:
            self.tabs[self.active_tab].set_offset([0, new_offset])
            self.offset = new_offset
    def change_screen_size(self, screen_size):
        self.rect.height = screen_size[1]
        for scrollbar in self.scrollbars:
            scrollbar.update_height(screen_size[1] - 60)
        for tab in self.tabs:
            tab.set_height(screen_size[1] - 60)
    def switch_tab(self, number):
        self.active_tab = number
    def change_cursor_image(self, number):
        self.editor.change_cursor_image(number)
    def draw(self):
        self.tabs[self.active_tab].draw()
        for button in self.tab_buttons:
            button.draw()
        self.scrollbars[self.active_tab].draw()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    bob = ImageBrowser(screen, [["../graphics/floor_tiles/atlas.txt", "Floor Tiles"], ["../graphics/obstacles/atlas.txt", "Obstacles"]])
    while True:
        screen.fill((0, 255, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            bob.update(event)
        bob.draw()
        pygame.display.update()
