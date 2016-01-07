import sys
import pygame
import random
from pygame.locals import *

#DISCLAIMER: I DON'T ACTUALLY UNDERSTAND ANY OF THE LINE INTERSECTION CODE!
#Explanation which I don't understand (as in: I haven't taken to time to really read it): http://stackoverflow.com/a/30160064
def rot_direction(p1x, p1y, p2x, p2y, p3x, p3y):
    if ((p3y - p1y) * (p2x - p1x)) > ((p2y - p1y) * (p3x - p1x)):
        return 1
    elif ((p3y - p1y) * (p2x - p1x)) == ((p2y - p1y) * (p3x - p1x)):
        return 0
    return -1

def linecollide(line1, line2):
    a = rot_direction(line1[0][0], line1[0][1], line1[1][0], line1[1][1], line2[1][0], line2[1][1])
    b = rot_direction(line1[0][0], line1[0][1], line1[1][0], line1[1][1], line2[0][0], line2[0][1])
    c = rot_direction(line1[0][0], line1[0][1], line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    d = rot_direction(line1[1][0], line1[1][1], line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    intersect = a != b and c != d
    if a == 0 and b == 0 and c == 0 and d == 0:
        intersect = True
    return intersect

def linerectcollide(line, rect):
    if rect.collidepoint(line[0]) or rect.collidepoint(line[1]):
        return True
    a = linecollide([(rect.topleft), (rect.topright)], line)
    b = linecollide([(rect.topleft), (rect.bottomleft)], line)
    c = linecollide([(rect.topright), (rect.bottomright)], line)
    d = linecollide([(rect.bottomleft), (rect.bottomright)], line)
    if a or b or c or d:
        return True
    else:
        return False

class QuadTree():
    def __init__(self, rect, level, maxlevels, maxitems, particles=[], rect_type="rect", screen=None, color=(255, 100, 100)):
        self.screen = screen
        self.maxlevel = maxlevels
        self.level = level
        self.maxparticles = maxitems
        self.rect = rect
        self.particles = particles
        self.rect_type = rect_type
        self.color = color
        self.branches = []
    def subdivide(self):
        for rect in self.split():
            self.branches.append(QuadTree(rect, self.level+1, self.maxlevel, self.maxparticles, [], self.rect_type, self.screen, self.color))
    def split(self):
        w = self.rect.width / 2
        h = self.rect.height / 2
        quadlist = []
        quadlist.append(Rect(self.rect.left, self.rect.top, w, h))
        quadlist.append(Rect(self.rect.left + w, self.rect.top, w, h))
        quadlist.append(Rect(self.rect.left, self.rect.top + h, w, h))
        quadlist.append(Rect(self.rect.left + w, self.rect.top + h, w, h))
        return quadlist

    def add_particle(self, particle):
        self.particles.append(particle)

    def subdivide_particles(self):
        for particle in self.particles:
            for branch in self.branches:
                if branch.rect.colliderect(particle.get_rect(self.rect_type)):
                    branch.add_particle(particle)
        self.particles = []

    def draw(self):
        if self.screen:
            pygame.draw.rect(self.screen, self.color, self.rect, 1)
            for branch in self.branches:
                branch.draw()
    def collidepoint(self, point):
        hit_list = []
        if self.branches:
            for branch in self.branches:
                if branch.rect.collidepoint(point):
                    hit_list += branch.collidepoint(point)
        else:
            for particle in self.particles:
                if particle.get_rect(self.rect_type).collidepoint(point):
                    hit_list.append(particle)
        return hit_list
    def collideline(self, line):
        hit_list = []
        if len(self.branches) > 0:
            for branch in self.branches:
                if linerectcollide(line, branch.rect):
                    hit_list += branch.collideline(line)
        else:
            for particle in self.particles:
                if linerectcollide(line, particle.get_rect(self.rect_type)):
                    hit_list.append(particle)
        return hit_list
    def colliderect(self, rect):
        hit_list = []
        if len(self.branches) > 0:
            for branch in self.branches:
                if branch.rect.colliderect(rect):
                    hit_list += branch.colliderect(rect)
        else:
            for particle in self.particles:
                if particle.get_rect(self.rect_type).colliderect(rect):
                    hit_list.append(particle)
        return hit_list
    def clear(self):
        self.particles = []
        self.branches = []
    def update(self):
        if len(self.particles) > self.maxparticles and self.level <= self.maxlevel:
            self.subdivide()
            self.subdivide_particles()
            for branch in self.branches:
                branch.update()

class Particle():
    def __init__(self, screen, rect, vel, color=(255, 255, 255)):
        self.screen = screen
        self.rect = rect
        self.vel = vel
        self.color = color
    def update(self):
        if self.rect.x + self.rect.width >= 1000 or self.rect.x <= 0:
            self.vel[0] = -self.vel[0]
        if self.rect.y + self.rect.height >= 700 or self.rect.y <= 0:
            self.vel[1] = -self.vel[1]
            
        self.rect.move_ip(self.vel)
    def collide(self, other_object):
        pass
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    quadtree = QuadTree(screen, pygame.rect.Rect(0, 0, 1000, 700), 0, 5, 5)
    particles = []
    for x in range(0, 1000):
        particles.append(Particle(screen, Rect(random.randint(0, 500), random.randint(0, 500), random.randint(10, 20), random.randint(10, 20)), [random.randint(1, 5), random.randint(1, 5)]))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)
        screen.fill((0, 0, 0))
        quadtree.clear()
        quadtree.particles = particles
        quadtree.update()
        quadtree.draw()
        for i, particle in enumerate(particles):
            particle.update()
            particle.draw()
            #for particle2 in particles[i + 1:]:
            #    if particle.rect.colliderect(particle2.rect):
            #        pass
        pygame.display.update()
