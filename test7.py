import os
import sys
from Engine import *
import pygame as pg
import tkinter as tk

w, h = 500, 200

# Add a couple widgets. We're going to put pygame in `embed`.
root = tk.Tk()
embed = tk.Frame(root)
embed.pack(fill="both", expand=1)
text = tk.Button(root, text='Blah.')
text.pack()

# Tell pygame's SDL window which window ID to use    
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

# The wxPython wiki says you might need the following line on Windows
# (http://wiki.wxpython.org/IntegratingPyGame).
#os.environ['SDL_VIDEODRIVER'] = 'windib'

# Show the window so it's assigned an ID.
root.update()

# Usual pygame initialization
pg.display.init()
screen = pg.display.set_mode((w,h))
def refresh_screen(event):
    global screen
    screen = pg.display.set_mode((event.width, event.height))
embed.bind('<Configure>', refresh_screen)
if __name__ == "__main__":
    b = Engine(screen)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            b.update(event)
        b.update()
        b.draw()
        pygame.display.flip()
        root.update()
