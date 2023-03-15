# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand
import time

kernel = np.ones((4, 8), np.float32) / 25
ke1 = np.ones((6, 6), np.float32)
kd1 = np.ones((6, 6), np.float32)
starttime = 50 
def capframe(vid, y1, y2, x1, x2, sub, screen, g):
    global kernel, ke1, kd1

    # Frame
    ret, frame = vid.read()

    # Crop
    frame = frame[y1:y2, x1:x2]

    # Blur
    #kernel = np.ones((4, 8), np.float32) / 25
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
    #ke1 = np.ones((6, 6), np.float32)
    frame = cv2.erode(frame, ke1, iterations=2)

    # Dilate
    #kd1 = np.ones((6, 6), np.float32)
    frame = cv2.dilate(frame, kd1, iterations=2)

    # Avoid playing that blip of white-screen at the beginning
    if g.t < 5:
        frame *= 0

    #Put to the screen
    surface = pygame.surfarray.make_surface(np.rot90(frame))
    screen.blit(surface, (0, 0))

    #Switch the mode, if necessary.
    if cv2.countNonZero(frame) < 10 and g.t > 50:
        g.mode = 2
        return g.mode
    g.t += 1

if __name__ == "__main__":
    time.sleep(2)
    starttime = time.time()

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


    class Game:
        mode = 2
        t = 0


    g = Game()
    while running:
        capframe(vid, y1, y2, x1, x2, sub, screen, g)
        pygame.display.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        currenttime = time.time() - starttime
        if currenttime > 100:
            running = False

    # After the loop release the cap object
    vid.release()
    cv2.destroyAllWindows()
    pygame.quit()
