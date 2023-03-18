# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand
import time

kernel = np.ones((4, 8), np.float32) / 25
threshold = 127
th = 255
ke1 = np.ones((6, 6), np.float32)
kd1 = np.ones((6, 6), np.float32)
starttime = 0
def capframe(vid, y1, y2, x1, x2, sub, g):
    global kernel, ke1, kd1, threshold, th

    # Frame                     ~ video (but it's blue)
    ret, frame = vid.read()

    # Adjust colors             ~ correctly colored video
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #'''
    # Crop                      ~ cropped video
    frame = frame[y1:y2, x1:x2]

    # Blur                      ~ blurred video
    frame = cv2.filter2D(frame, -1, kernel)

    # Threshold                 ~ fiery orange effect video
    ret, frame = cv2.threshold(frame, th, 255, cv2.THRESH_BINARY)

    # Subtract background, KNN  ~ powdery white over black
    frame = sub.apply(frame)

    # Blur                      ~ fuzzy, Rainbow Fish-esque silhouette
    frame = cv2.filter2D(frame, -1, kernel)

    # Threshold
    ret, frame = cv2.threshold(frame, th, 255, cv2.THRESH_BINARY)

    # Erode
    frame = cv2.erode(frame, ke1, iterations=2)

    # Dilate
    frame = cv2.dilate(frame, kd1, iterations=2)

    # Avoid playing that blip of white-screen at the beginning
    if g.t < 5:
        frame *= 0

    if th > threshold:
        th -= 1

    #Put to the screen
    #surface = pygame.surfarray.make_surface(np.rot90(frame))
    #screen.blit(surface, (0, 0))

    return frame

    '''
    #Switch the mode, if necessary.
    if cv2.countNonZero(frame) < 10 and g.t > 50:
        g.mode = 2
        return g.mode
    g.t += 1
    '''

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


    class Game:
        mode = 2
        t = 0


    g = Game()
    running = True

    while running:
        frame = capframe(vid, y1, y2, x1, x2, sub, g)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        currenttime = time.time() - starttime
        if currenttime > 100:
            running = False

        g.t += 1

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    # After the loop release the cap object
    vid.release()
    cv2.destroyAllWindows()
    pygame.quit()
