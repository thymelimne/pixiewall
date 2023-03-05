# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand



def capframe(vid, y1, y2, x1, x2, sub, screen):

    # Frame
    ret, frame = vid.read()

    # Crop
    frame = frame[y1:y2, x1:x2]

    # Blur
    kernel = np.ones((4, 8), np.float32) / 25
    frame = cv2.filter2D(frame, -1, kernel)

    # Threshold
    ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

    # Subtract background
    frame = sub.apply(frame)

    # Blur
    frame = cv2.filter2D(frame, -1, kernel)

    # Threshold
    ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

    # Erode
    ke1 = np.ones((6, 6), np.float32)
    frame = cv2.erode(frame, ke1, iterations=2)

    # Dilate
    kd1 = np.ones((6, 6), np.float32)
    frame = cv2.dilate(frame, kd1, iterations=2)

    #Put to the screen
    surface = pygame.surfarray.make_surface(np.rot90(frame))
    screen.blit(surface, (0, 0))

    global mode
    if cv2.countNonZero(frame) < 10:
        print(cv2.countNonZero(frame))
        mode = 2
        return mode
