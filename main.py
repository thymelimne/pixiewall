# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand
import butterfliesmode
import silhouettesmode

# define a video capture object
vid = cv2.VideoCapture(0)
sub = cv2.createBackgroundSubtractorKNN(history=100, dist2Threshold=400, detectShadows=False)

# Dimensions for cropping
outputx = 64
outputy = 25
inputx = vid.read()[1].shape[1]
inputy = vid.read()[1].shape[0]
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
print(inputx)
print(inputy)

#b1 = butterfliesmode.Butterfly([100, 200], screen)
#b2 = butterfliesmode.Butterfly([300, 400], screen)
s = butterfliesmode.Swarm(screen, clock)
#s.add(b1)
#s.add(b2)
s.spawn()

def reset_butterflies():
    print("RESETTING BUTTERFLIES")
    s = butterfliesmode.Swarm(screen, clock)
    print(s.num_empties)

def reset_silhouettes():
    print("RESETTING SILHOUETTES")
    pass

class Game:
    mode = 2
g = Game()
while running:

    if g.mode == 1:
        silhouettesmode.capframe(vid, y1, y2, x1, x2, sub, screen, g)
        if g.mode == 2:
            reset_butterflies()
    if g.mode == 2:
        s.timestep(g)
        if g.mode == 1:
            reset_silhouettes()
    pygame.display.update()

    # 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_1:
                g.mode = 1
            if event.key == pygame.K_2:
                g.mode = 2

# After the loop release the cap object
vid.release()
cv2.destroyAllWindows()
pygame.quit()