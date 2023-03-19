# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand


class Shamrock:

    def __init__(self, loc, screen):
        self.loc = loc
        self.angle = rand() * 360
        self.updatespeeds()
        self.color = (0, 100 + rand()*155, 0)

        sizecoef = .5 + rand()
        self.size *= sizecoef
        self.regularspeed *= sizecoef
        self.speed *= sizecoef
        self.boostspeed *= sizecoef

        self.surface = screen

        self.anglespeed = -4 + rand() * 8

    speed = 2

    loc = [200, 150]

    size = .3
    spread = 1
    mostthin = .01
    mostthick = 1
    thinning = False
    thicking = False

    angle = 45
    speedx = np.cos(np.radians(angle)) * speed
    speedy = np.sin(np.radians(angle)) * speed

    regularspeed = 2
    boostspeed = 1

    spinnedangle = 0
    anglespeed = 0


    def updatespeeds(self):
        self.speedx = np.sin(np.radians(self.angle)) * self.speed
        self.speedy = np.cos(np.radians(self.angle)) * self.speed


    def rotatepoint(self, origin, point, theta):
        newpoint = np.copy(point)
        newpoint[0] = origin[0] + np.cos(theta) * (point[0] - origin[0]) - np.sin(theta) * (point[1] - origin[1])
        newpoint[1] = origin[1] + np.sin(theta) * (point[0] - origin[0]) + np.cos(theta) * (point[1] - origin[1])
        return newpoint


    def rotatepoints(self, origin, points, theta):
        return np.array([self.rotatepoint(origin, point, theta) for point in points])


    def draw(self):
        wing1full = np.asarray(
            ((0,0), (0,-30), (40,-80), (80,-90), (100, -80), (130,-50), (130,0), (100,30), (70,50), (100,70), (120,100), (130,120), (120,160), (100,190), (80,200), (50,190), (30,170), (10,140), (0,110)), dtype=np.float64
        )
        wing2full = wing1full.copy()
        wing2full[:, 0] *= -1
        wing1 = np.copy(wing1full)
        wing2 = np.copy(wing2full)
        wing1 *= self.size
        wing2 *= self.size

        '''
        # Thinning the wings
        wing1[:, 0] *= self.spread
        wing2[:, 0] *= self.spread

        # Rotating the wings
        wing1 = self.rotatepoints(np.array([0, 0]), wing1, np.radians(self.angle))
        wing2 = self.rotatepoints(np.array([0, 0]), wing2, np.radians(self.angle))
        '''
        # Spin the shamrocks freely
        wing1 = self.rotatepoints(np.array([0,0]), wing1, np.radians(self.spinnedangle))
        wing2 = self.rotatepoints(np.array([0,0]), wing2, np.radians(self.spinnedangle))
        #'''

        # Placing the wings
        wing1[:, 0] = wing1[:, 0] + self.loc[0]
        wing1[:, 1] = wing1[:, 1] + self.loc[1]
        wing2[:, 0] = wing2[:, 0] + self.loc[0]
        wing2[:, 1] = wing2[:, 1] + self.loc[1]

        pygame.draw.polygon(self.surface, self.color, points=wing1)
        pygame.draw.polygon(self.surface, self.color, points=wing2)

    direction = 0
    timedirection = 0
    shouldflap = False
    timeflap = 0

    def agent(self):
        if self.timedirection > 0:
            self.timedirection -= 1
        else:
            if rand() < .33:
                self.direction = -1
            elif rand() < .33:
                self.direction = +1
            else:
                self.direction = 0
            self.timedirection = rand() * 100

        if self.timeflap > 0:
            self.shouldflap = False
            self.timeflap -= 1
        else:
            self.shouldflap = True
            self.timeflap = rand() * 120
        return self.shouldflap

    def flap(self):
        self.thinning = True
        self.speed += self.boostspeed

    def turnright(self):
        self.angle += .5
        self.updatespeeds()

    def turnleft(self):
        self.angle -= .5
        self.updatespeeds()

    def timestep(self):
        self.loc[0] += self.speedx
        self.loc[1] -= self.speedy

        self.draw()  # This will call the animation

        self.shouldflap = self.agent()
        if self.shouldflap:
            self.flap()

        if self.thinning:
            if self.spread >= self.mostthin:
                self.spread *= .8
            else:
                self.thinning = False
                self.thicking = True
        elif self.thicking:
            if self.spread <= self.mostthick:
                self.spread *= 1.25
            else:
                self.thicking = False

        if self.direction == 1:
            self.turnright()
        elif self.direction == -1:
            self.turnleft()

        if self.speed > self.regularspeed:
            self.speed -= .01
            self.updatespeeds()

        self.spinnedangle += self.anglespeed


class Billow:
    shamrocks = []
    timespawn = 0
    bz = 60
    spawnrarity = .0000001
    startbuffertime = 50
    def __init__(self, screen, clock, g):
        self.num_empties = rand() * 10
        self.surface = screen
        self.clock = clock
        self.g = g
    should_transition = False
    def add(self, b):
        self.shamrocks.append(b)
    def timestep(self, g):
        self.surface.fill(0)
        for b in self.shamrocks:
            b.timestep()

            # Trying this:
            #self.surface.blit(b.image, (b.locx, b.locy))

            size = self.surface.get_size()
            if b.loc[0] < -60 or b.loc[0] > size[0] + 60 or b.loc[1] < -60 or b.loc[1] > size[1] + 60:
                self.shamrocks.remove(b)
                del b
                if not self.shamrocks and not self.startbuffertime > 0:
                    print(self.num_empties)
                    self.num_empties -= 1
                if not self.num_empties > 0:
                    self.should_transition = True

        if rand() < .1:
            self.spawn()
        self.clock.tick(60)
        if self.startbuffertime > 0:
            self.startbuffertime -= 1
        elif self.should_transition:
            g.mode = 1
    def spawn(self):
        loc = [100, 100]
        '''
        if rand() < .5:
            loc[0] = self.surface.get_size()[0] + self.bz if rand() < .5 else 0-self.bz
            loc[1] = rand() * self.surface.get_size()[1]
        else:
            loc[0] = rand() * self.surface.get_size()[0]
            loc[1] = self.surface.get_size()[1] + self.bz if rand() < .5 else 0-self.bz
        '''
        loc[0] = rand() * self.surface.get_size()[0]
        loc[1] = 0 - self.bz
        #angle = 90
        if loc[0] < 0:
            angle = rand() * 180
        elif loc[0] > self.surface.get_size()[0]:
            angle = 180 + rand() * 180
        elif loc[1] < 0:
            angle = 90 + rand() * 180
        elif loc[1] > self.surface.get_size()[1]:
            angle = rand() * 90 if rand() < .5 else 270 * rand() * 90
        angle = 90

        print(self.spawnrarity)
        if self.spawnrarity < 30:
            self.spawnrarity += rand() * 300
        else:
            self.spawnrarity -= rand() * 10
        print(self.spawnrarity)

        b = Shamrock(loc, self.surface)
        self.add(b)
