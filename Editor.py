import os
import pygame
import loader
import importlib
import tkinter as tk
from subprocess import call
from tkinter import ttk, filedialog
from pygame.locals import *
from EditorClasses import *

"""
Notes:
1. This code is extremely bad, use at your own risk.
2. THIS WILL CRASH! Don't expect there to be any proper error handling.
"""


TILEWIDTH = 128
TILEHEIGHT = 64
LARGE_FONT = ("Arial", 15)

def load_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("Lumidify Isometric Level Editor")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.tabs = {}
        self.init_gui()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.floor = Floor(self.screen, self.tiles)
        self.obstaclemap = Obstacles(self.screen, self.obstacles, self.characters, self.items)
        self.bind('<Delete>', self.obstaclemap.delete)
        self.bind('<Control-o>', self.open_map)
        self.bind('<Control-n>', self.new)
        self.bind('<Control-S>', self.save_as)
        self.bind('<Control-s>', self.save)
        self.bind('<F5>', self.run)
        self.config = {}
        self.current_path = None
    def refresh_screen(self, event):
        self.screen = pygame.display.set_mode((event.width, event.height))
    def init_gui(self):
        self.create_menubar()
        self.create_main_area()
        self.tiles, self.obstacles, self.characters, self.items, self.bullets = loader.load_tiles()
        self.mode_variable = tk.IntVar()
        self.create_left_toolbar()
        self.create_right_toolbar()
        self.config_widgets = {}
        self.config_frame = None
    def open_map(self, *args):
        self.current_path = filedialog.askdirectory(title="Open...")
        self.load()
    def save_as(self, *args):
        self.current_path = filedialog.askdirectory(title="Save As...")
        if not os.path.isdir(self.current_path):
            os.mkdir(self.current_path)
        self.save()
    def load(self):
        self.config = load_module(os.path.join(self.current_path, "config.py")).config.copy()
        floor_size = self.config.get("level_dimensions", [50, 50])
        floor_size = [50, 50]
        self.floor.load_tilemap(os.path.join(self.current_path, "floor.py"), floor_size)
        self.floor.populate_listbox(self.layers)
        self.obstaclemap.load_map(self.current_path, floor_size)
        self.show_map_properties()
    def save(self, *args):
        if not self.current_path:
            self.save_as()
        self.floor.save(os.path.join(self.current_path, "floor.py"))
        self.obstaclemap.save(self.current_path)
        with open(os.path.join(self.current_path, "config.py"), "w") as f:
            f.write("config = " + repr(self.config))
    def run(self, *args):
        self.save()
        del os.environ['SDL_WINDOWID']
        call(["python", "Engine.py", self.current_path])
        os.environ['SDL_WINDOWID'] = str(self.main_area.winfo_id())
    def set_entry_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, value)
    def show_map_properties(self):
        self.obstaclemap.destroy_properties_widget()
        self.destroy_map_properties()
        self.config_widgets = {}
        self.config_frame = ttk.Frame(self.right_toolbar)
        self.config_widgets["level_dimensions"] = [tk.Spinbox(self.config_frame, from_=0, to=500, width=8), tk.Spinbox(self.config_frame, from_=0, to=500, width=8)]
        self.config_widgets["spawn_pos"] = [tk.Spinbox(self.config_frame, from_=0, to=500, width=8), tk.Spinbox(self.config_frame, from_=0, to=500, width=8)]
        self.config_widgets["music"] = ttk.Entry(self.config_frame)
        ttk.Label(self.config_frame, text="level_dimensions").grid(row=0, column=0, sticky="w")
        ttk.Label(self.config_frame, text="spawn_pos").grid(row=1, column=0, sticky="w")
        ttk.Label(self.config_frame, text="music").grid(row=2, column=0, sticky="w")
        self.config_widgets["level_dimensions"][0].grid(row=0, column=1, sticky="w")
        self.config_widgets["level_dimensions"][1].grid(row=0, column=2, sticky="w")
        self.config_widgets["spawn_pos"][0].grid(row=1, column=1, sticky="w")
        self.config_widgets["spawn_pos"][1].grid(row=1, column=2, sticky="w")
        self.config_widgets["music"].grid(row=2, column=1, columnspan=2, sticky="w")
        self.set_entry_value(self.config_widgets["level_dimensions"][0], self.config["level_dimensions"][0])
        self.set_entry_value(self.config_widgets["level_dimensions"][1], self.config["level_dimensions"][1])
        self.set_entry_value(self.config_widgets["spawn_pos"][0], self.config["spawn_pos"][0])
        self.set_entry_value(self.config_widgets["spawn_pos"][1], self.config["spawn_pos"][1])
        self.set_entry_value(self.config_widgets["music"], self.config["music"])
        self.config_frame.grid(row=1, column=0, columnspan=3)
    def destroy_map_properties(self):
        if self.config_frame:
            self.config_frame.destroy()
        self.config_frame = None
        self.config_widgets = {}
    def new(self, *args):
        self.floor.create_map([50, 50])
        self.obstaclemap.create_map([50, 50])
        self.floor.populate_listbox(self.layers)
        self.config = {"level_dimensions": [50, 50], "spawn_pos": [0, 0], "music": ""}
        self.show_map_properties()
    def create_menubar(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label="Run", command=self.run)
        file_menu.add_command(label="New", command=self.new)
        file_menu.add_command(label="Open...", command=self.open_map)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_command(label="Properties", command=self.show_map_properties)
        file_menu.add_command(label="Quit", command=self.destroy)
        self.menubar.add_cascade(label="Map", menu=file_menu)
    def create_left_toolbar(self):
        self.left_toolbar = ttk.Notebook(self)
        self.create_floor_tab()
        self.create_obstacle_tab()
        self.create_item_tab()
        self.create_character_tab()
        self.create_trigger_tab()
        self.left_toolbar.grid(row=0, column=0, sticky="ns")
    def create_main_area(self):
        self.main_area = ttk.Frame(self, width=500, height=500)
        self.main_area.grid(row=0, column=1, sticky="nswe")
        os.environ['SDL_WINDOWID'] = str(self.main_area.winfo_id())
        self.update()
        pygame.display.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.main_area.bind('<Configure>', self.refresh_screen)
        self.main_area.bind('<Motion>', self.calculate_mouse_pos)
        self.main_area.bind('<B2-Motion>', self.change_offset)
        self.main_area.bind('<B1-Motion>', self.mousedrag)
        self.main_area.bind('<Button-1>', self.click)
        self.mouse_pos = (0, 0)
        self.last_mouse_pos = (0, 0)
        self.exact_tilex = 0
        self.exact_tiley = 0
        self.last_exact_tilex = 0
        self.last_exact_tiley = 0
        self.screen_offset = [0, 0]
    def calculate_mouse_pos(self, event):
        self.last_mouse_pos = self.mouse_pos
        self.last_exact_tilex = self.exact_tilex
        self.last_exact_tiley = self.exact_tiley
        self.mouse_pos = (event.x, event.y)
        self.adjusted_mouse_pos = [self.mouse_pos[0] - self.screen_offset[0], self.mouse_pos[1] - self.screen_offset[1]]
        self.exact_tilex = (self.adjusted_mouse_pos[0] / (TILEWIDTH // 2) + self.adjusted_mouse_pos[1] / (TILEHEIGHT // 2)) / 2
        self.exact_tiley = (self.adjusted_mouse_pos[1] / (TILEHEIGHT // 2) - (self.adjusted_mouse_pos[0] / (TILEWIDTH // 2))) / 2
        self.tilex = round(self.exact_tilex)
        self.tiley = round(self.exact_tiley)
    def click(self, event):
        self.calculate_mouse_pos(event)
        tab = self.left_toolbar.tab(self.left_toolbar.select(), "text")
        if tab == "Floor Tiles":
            self.mousedrag(event)
        else:
            if self.obstaclemap.click(self.adjusted_mouse_pos, (self.exact_tilex, self.exact_tiley), self.mode_variable.get(), self.obstacle_lb.get("active"), self.obstacle_layers.index("active"), self.item_lb.get("active"), self.character_lb.get("active"), tab, self.right_toolbar):
                self.destroy_map_properties()
    def change_offset(self, event):
        self.screen_offset[0] += event.x - self.mouse_pos[0]
        self.screen_offset[1] += event.y - self.mouse_pos[1]
        self.mouse_pos = [event.x, event.y]
    def mousedrag(self, event):
        self.calculate_mouse_pos(event)
        tab = self.left_toolbar.tab(self.left_toolbar.select(), "text")
        if tab == "Floor Tiles":
            try:
                self.floor.replace_tile(self.floor_tile_lb.index("active") - 1, (self.tilex, self.tiley), self.layers.index("active"))
            except:
                pass
        else:
            self.obstaclemap.mousedrag(self.adjusted_mouse_pos, (self.exact_tilex - self.last_exact_tilex, self.exact_tiley - self.last_exact_tiley))
    def create_right_toolbar(self):
        self.right_toolbar = ttk.Frame(self)
        label = ttk.Label(self.right_toolbar, text="Properties", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky=("w", "e"))
        self.right_toolbar.grid(row=0, column=2, sticky="ns")
    def create_floor_tab(self):
        self.tabs["floor"] = ttk.Frame(self.left_toolbar)
        label =  ttk.Label(self.tabs["floor"], text="Layers", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="we")
        self.layers = tk.Listbox(self.tabs["floor"], exportselection=0)
        self.layers.grid(row=1, column=0, sticky="we", columnspan=4)
        button = ttk.Button(self.tabs["floor"], text="Append Layer", command=lambda: self.floor.insert_layer(self.layers.size(), self.layers))
        button.grid(row=0, column=1)
        button = ttk.Button(self.tabs["floor"], text="Insert Layer", command=lambda: self.floor.insert_layer(self.layers.index("active"), self.layers))
        button.grid(row=0, column=2)
        button = ttk.Button(self.tabs["floor"], text="Remove Layer", command=lambda: self.floor.remove_layer(self.layers.index("active"), self.layers))
        button.grid(row=0, column=3)
        self.tabs["floor"].grid_columnconfigure(0, weight=1)
        self.tabs["floor"].grid_rowconfigure(3, weight=1)
        
        label = ttk.Label(self.tabs["floor"], text="Tiles", font=LARGE_FONT)
        label.grid(row=2, sticky="w", column=0)
        
        self.floor_tile_lb = tk.Listbox(self.tabs["floor"], exportselection=0)
        self.floor_tile_lb.insert("end", "-1")
        for x in range(len(self.tiles)):
            self.floor_tile_lb.insert("end", str(x))
        self.floor_tile_lb.grid(row=3, column=0, sticky="nswe", columnspan=4)
        
        self.left_toolbar.add(self.tabs["floor"], text="Floor Tiles")
    def create_obstacle_tab(self):
        self.tabs["obstacles"] = ttk.Frame(self.left_toolbar)
        
        ttk.Radiobutton(self.tabs["obstacles"], text="Selection Mode", value=0, variable=self.mode_variable).grid(row=0, column=0)
        ttk.Radiobutton(self.tabs["obstacles"], text="Drawing Mode", value=1, variable=self.mode_variable).grid(row=0, column=1)
        
        ttk.Label(self.tabs["obstacles"], text="Layers", font=LARGE_FONT).grid(row=1, column=0, sticky="we")

        self.obstacle_layers = tk.Listbox(self.tabs["obstacles"], exportselection=0, height=2)
        self.obstacle_layers.insert("end", "Layer 0")
        self.obstacle_layers.insert("end", "Layer 1")
        self.obstacle_layers.grid(row=2, column=0, sticky="we", columnspan=3)

        ttk.Label(self.tabs["obstacles"], text="Obstacles", font=LARGE_FONT).grid(row=3, column=0, sticky="we")

        self.obstacle_lb = tk.Listbox(self.tabs["obstacles"], exportselection=0)
        for x in range(len(self.obstacles)):
            self.obstacle_lb.insert("end", str(x))
        self.obstacle_lb.insert("end", "RECT")
        self.obstacle_lb.grid(row=4, column=0, sticky="nswe", columnspan=3)
        
        self.tabs["obstacles"].grid_columnconfigure(2, weight=1)
        self.tabs["obstacles"].grid_rowconfigure(4, weight=1)
        self.left_toolbar.add(self.tabs["obstacles"], text="Obstacles")
    def create_item_tab(self):
        self.tabs["items"] = ttk.Frame(self.left_toolbar)
        
        ttk.Radiobutton(self.tabs["items"], text="Selection Mode", value=0, variable=self.mode_variable).grid(row=0, column=0)
        ttk.Radiobutton(self.tabs["items"], text="Drawing Mode", value=1, variable=self.mode_variable).grid(row=0, column=1)

        ttk.Label(self.tabs["items"], text="Items", font=LARGE_FONT).grid(row=1, column=0, sticky="we")

        self.item_lb = tk.Listbox(self.tabs["items"], exportselection=0)
        for key in sorted(self.items.keys()):
            self.item_lb.insert("end", key)
        self.item_lb.grid(row=2, column=0, sticky="nswe", columnspan=3)
        
        self.tabs["items"].grid_columnconfigure(2, weight=1)
        self.tabs["items"].grid_rowconfigure(2, weight=1)
        self.left_toolbar.add(self.tabs["items"], text="Items")
    def create_trigger_tab(self):
        self.tabs["triggers"] = ttk.Frame(self.left_toolbar)
        ttk.Radiobutton(self.tabs["triggers"], text="Selection Mode", value=0, variable=self.mode_variable).grid(row=0, column=0)
        ttk.Radiobutton(self.tabs["triggers"], text="Drawing Mode", value=1, variable=self.mode_variable).grid(row=0, column=1)
        self.left_toolbar.add(self.tabs["triggers"], text="Triggers")
    def create_character_tab(self):
        self.tabs["characters"] = ttk.Frame(self.left_toolbar)
        
        ttk.Radiobutton(self.tabs["characters"], text="Selection Mode", value=0, variable=self.mode_variable).grid(row=0, column=0)
        ttk.Radiobutton(self.tabs["characters"], text="Drawing Mode", value=1, variable=self.mode_variable).grid(row=0, column=1)

        ttk.Label(self.tabs["characters"], text="Characters", font=LARGE_FONT).grid(row=1, column=0, sticky="we")

        self.character_lb = tk.Listbox(self.tabs["characters"], exportselection=0)
        for key in sorted(self.characters.keys()):
            self.character_lb.insert("end", key)
        self.character_lb.grid(row=2, column=0, sticky="nswe", columnspan=3)
        
        self.tabs["characters"].grid_columnconfigure(2, weight=1)
        self.tabs["characters"].grid_rowconfigure(2, weight=1)
        self.left_toolbar.add(self.tabs["characters"], text="Characters")
    def change_config(self):
        if self.config_widgets:
            try:
                new_width = int(self.config_widgets["level_dimensions"][0].get())
                new_height = int(self.config_widgets["level_dimensions"][1].get())
                new_spawnx = float(self.config_widgets["spawn_pos"][0].get())
                new_spawny = float(self.config_widgets["spawn_pos"][1].get())
                new_music = self.config_widgets["music"].get()
                if new_width != self.config["level_dimensions"][0] or new_height != self.config["level_dimensions"][1]:
                    self.config["level_dimensions"] = [new_width, new_height]
                    self.floor.size = [new_width, new_height]
                    self.floor.change_size()
                    self.obstaclemap.change_size([new_width, new_height])
                self.config["spawn_pos"] = [new_spawnx, new_spawny]
                self.config["music"] = new_music
            except:
                pass
    def draw(self):
        self.change_config()
        self.screen.fill((0, 0, 0))
        self.floor.draw(self.screen_offset)
        self.obstaclemap.draw(self.screen_offset)
        current_tab = self.left_toolbar.tab(self.left_toolbar.select(), "text")
        mode = self.mode_variable.get()
        if current_tab == "Floor Tiles":
            try:
                self.floor.draw_cursor(self.floor_tile_lb.index("active") - 1, (self.tilex, self.tiley), self.screen_offset)
            except:
                pass
        elif mode == 1:
            try:
                self.obstaclemap.draw_cursor((self.exact_tilex, self.exact_tiley), self.obstacle_lb.get("active"), self.item_lb.get("active"), self.character_lb.get("active"), current_tab, self.screen_offset)
            except:
                pass
editor = Editor()
def main():
    while True:
        editor.draw()
        editor.update()
        pygame.display.update()
if __name__ == "__main__":
    main()
