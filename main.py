# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand
import silhouettesmode
import shamrocksmode
import time

time.sleep(2)
starttime = time.time()

# Dimensions for cropping
outputx = 64
outputy = 25
inputx = 1280
inputy = 720
desiredaspectratio = outputx / outputy
ypixelstokeep = inputx * desiredaspectratio
y1 = int(inputy - ypixelstokeep)
y2 = inputy
x1 = 0
x2 = inputx

# Pygame
pygame.init()
screen = pygame.display.set_mode([inputx, inputy], pygame.FULLSCREEN)
pygame.display.set_caption('game')
clock = pygame.time.Clock()
pygame.display.update()
running = True
print(inputx)  # 1280
print(inputy)  # 720


def reset_butterflies(g):
    print("RESETTING BUTTERFLIES")
    s = shamrocksmode.Billow(screen, clock)
    g.t = 0
    print(s.num_empties)


def reset_silhouettes(g):
    print("RESETTING SILHOUETTES")
    g.t = 0
    pass


class Game:
    mode = 2
    t = 0


g = Game()
s = shamrocksmode.Billow(screen, clock, g)
s.spawn()


while running:

    s.timestep(g)
    pygame.display.update()

    # 'q' to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_1:
                g.mode = 1
                reset_silhouettes(g)
            if event.key == pygame.K_2:
                g.mode = 2
                reset_butterflies(g)
                
    currenttime = time.time() - starttime
    
pygame.quit()

