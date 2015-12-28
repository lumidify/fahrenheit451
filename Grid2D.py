import os
import sys
import math
import pygame
from CONSTANTS import *
from heapq import heappush, heappop
from pygame.locals import *
from QuadTree import QuadTree


def compute_g_score(a, b):
    delta = (abs(a[0] - b[0]), abs(a[1] - b[1]))
    if sum(delta) >= 2:
        return 14
    else:
        return 10

def get_neighbors(pos, maxwidth, maxheight):
    """
    Note: maxwidth and maxheight are geared towards zero-based indexing, so really the "actual" maxwidth would be maxwidth + 1
    """
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
    neighbors = []
    for direction in directions:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < maxwidth and neighbor[1] < maxheight:
            neighbors.append(neighbor)
    return neighbors
    
def heuristic(a, b, method="diagonal"):
    if method == "diagonal":
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return 10 * (dx + dy) - 6 * min(dx, dy)
    elif method == "manhattan":
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    else:
        return None



class Grid2D():
    def __init__(self, dimensions, obstacles=[], precision=4, tilesize=[64, 64]):
        self.precision = precision
        self.tilesize = tilesize
        self.split_tilesize = [tilesize[0] / precision, tilesize[1] / precision]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid = [[1 for x in range(self.width * precision)] for y in range(self.height * precision)]
        self.quadtree = QuadTree(Rect(0, 0, tilesize[0] * self.width, tilesize[1] * self.height), 0, int(tilesize[0] * self.width / 400), 5, obstacles)
        self.obstacles = obstacles
    def refresh(self):
        self.quadtree.clear()
        self.quadtree.particles = self.obstacles
        self.quadtree.update()
        self.calculate_clearance()
    def find_path(self, start, target, clearance=1, method="diagonal"):
        orig_target = target
        if not self.quadtree.collideline(((start[0] * WIDTH, start[1] * HEIGHT), (target[0] * WIDTH, target[1] * HEIGHT))):
            return [target]
        start = (round(start[0] * self.precision), round(start[1] * self.precision))
        target = (round(target[0] * self.precision), round(target[1] * self.precision))
        if (start[0] >= 0 and start[1] >= 0 and target[0] >= 0 and target[1] >= 0 and 
            start[0] <= self.width * self.precision - 1 and
            target[0] <= self.width * self.precision - 1 and 
            start[1] <= self.height * self.precision - 1 and
            target[1] <= self.height * self.precision - 1 and
            self.grid[target[1]][target[0]] >= clearance):
            parents = {}
            g_score = {start:0}
            h_score = {start:heuristic(start, target, method)}
            f_score = {start:h_score[start]}
            closed_list = []
            open_heap = []
            heappush(open_heap, (f_score[start], start))
            while open_heap:
                current = heappop(open_heap)[1]
                closed_list.append(current)
                if current == target:
                    path = []
                    while current in parents:
                        path.append(current)
                        current = parents[current]
                    path.reverse()
                    path = [[x[0] / self.precision, x[1] / self.precision] for x in path]
                    if path:
                        path[-1] = orig_target
                    return path
                for neighbor in get_neighbors(current, self.width * self.precision - 1, self.height * self.precision - 1):
                    if self.grid[neighbor[1]][neighbor[0]] < clearance or neighbor in closed_list:
                        continue
                    elif neighbor not in [x[1] for x in open_heap]:
                        g_score[neighbor] = g_score[current] + compute_g_score(current, neighbor)
                        h_score[neighbor] = heuristic(neighbor, target, method)
                        f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
                        heappush(open_heap, (f_score[neighbor], neighbor))
                        parents[neighbor] = current
                    else:
                        potential_g = g_score[current] + compute_g_score(current, neighbor)
                        potential_f = h_score[neighbor] + potential_g
                        if potential_f < f_score[neighbor]:
                            f_score[neighbor] = potential_f
                            g_score[neighbor] = potential_g
                            parents[neighbor] = current
                            heappush(open_heap, (f_score[neighbor], neighbor))
        return None
    def calculate_clearance(self):
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if self.quadtree.colliderect(Rect((j * self.split_tilesize[0], i * self.split_tilesize[1]), self.split_tilesize)):
                    self.grid[i][j] = 0
        """
        Calculating clearance makes it too slow
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x != 0:
                    clearance = 1
                    temp_pos = [j, i]
                    while True:
                        temp_pos[0] += 1
                        temp_pos[1] += 1
                        if temp_pos[0] >= len(self.grid[0]) or temp_pos[1] >= len(self.grid):
                            break
                        elif 0 in self.grid[temp_pos[1]][j:temp_pos[0] + 1] + [line[temp_pos[0]] for line in self.grid[i:temp_pos[1]]]:
                            break
                        else:
                            clearance += 1
                    if x == None or x > clearance:
                        self.grid[i][j] = clearance
        """
    def draw(self, screen_offset):
        for obstacle in self.obstacles:
            obstacle.draw()
