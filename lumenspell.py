# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand
import time
from game import Game, Spell

kernel = np.ones((4, 8), np.float32) / 25
threshold = 127
th = 255
ke1 = np.ones((6, 6), np.float32)
kd1 = np.ones((6, 6), np.float32)
starttime = 0

inputx = 1280
inputy = 720
pygame.init()
screen = pygame.display.set_mode([inputx, inputy], pygame.RESIZABLE)
pygame.display.set_caption('game')
clock = pygame.time.Clock()
pygame.display.update()
running = True

t = 0

def get_wand(vid, topleft, bottomright, sub, g):
	global kernel, ke1, kd1, threshold, th
	x1, y1 = topleft
	x2, y2 = bottomright

	# Frame                     ~ video (but it's blue)
	ret, frame = vid.read()

	# Adjust colors             ~ correctly colored video
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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

	if th > threshold:
		th -= 1

	# Wand placement:
	M = cv2.moments(frame)

	# calculate x,y coordinate of center of wand
	if M["m00"] != 0:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	else:
		cX, cY = 0, 0

	wandpixels = np.sum(frame >= 255)
	wandrelativesize = wandpixels / (frame.shape[0] * frame.shape[1])

	wandrelativeloc = [cX / frame.shape[0], cY / frame.shape[1]]

	return frame, wandrelativeloc, wandrelativesize


if __name__ == "__main__":
	time.sleep(2)
	starttime = time.time()

	# define a video capture object
	vid = cv2.VideoCapture(0)
	sub = cv2.createBackgroundSubtractorKNN(history=100, dist2Threshold=400, detectShadows=False)

	# Dimensions for cropping
	outputx = 64
	outputy = 25
	sizex = vid.read()[1].shape[1]
	sizey = vid.read()[1].shape[0]
	desiredaspectratio = outputx / outputy
	ypixelstokeep = sizey * desiredaspectratio
	y1 = int(sizey - ypixelstokeep)
	y2 = sizey
	x1 = 0
	x2 = sizex
	topleft = [x1, y1]
	bottomright = [x2, y2]

	g = Game()
	s = Spell()
	running = True

	while running:
		frame, wandloc, wandsize = get_wand(vid, topleft, bottomright, sub, g)
		#cv2.imshow("Frame", frame)
		print(wandloc)

		# Update the size.
		prev_size = s.size
		new_size = max(60, 100 * wandsize)
		s.size = new_size

		# Update the thing.
		g.window.fill((0, 0, 0))
		pygame.draw.circle(g.window, color=s.color, center=(inputx-wandloc[0]*inputx,wandloc[1]*inputy), radius=s.size)
		pygame.display.update()

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		currenttime = time.time() - starttime
		if currenttime > 100:
			running = False

		t += 1

	# After the loop release the cap object
	vid.release()
	# Destroy all the windows
	cv2.destroyAllWindows()

	# After the loop release the cap object
	vid.release()
	cv2.destroyAllWindows()
	pygame.quit()
