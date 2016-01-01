import pygame
from pygame.locals import *
pygame.init()
class DialogManager():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("Lumidify_Casual.ttf", 20)
        self.player_color = (255, 50, 50)
        self.npc_color = (255, 255, 255)
    def start_dialog(self, dialog_path, player, character):
        pass
    def draw(self):
        self.screen.blit(self.font.render("PLAYER", True, self.player_color), (0, 0))
        self.screen.blit(self.font.render("NPC", True, self.npc_color), (0, 40))
screen = pygame.display.set_mode((500, 500))
a = DialogManager(screen)
while True:
    screen.fill((0, 0, 0))
    a.draw()
    pygame.display.update()
