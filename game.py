'''
General class for a pygame element that can show stuff (not specific to a game.)
'''

import pygame
from random import random as rand
import numpy as np

class Game():

	window = None
	elements = None
	clock = None

	def __init__(self, elements=None):
		pygame.init()
		self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
		clock = pygame.time.Clock()

class Spell():

	size = 50
	color = (255, rand() * 255, rand() * 255)

	num_rungs = 20
	prev_spots = []
	prev_sizes = []
	prev_colrs = []

	def add_rung(self, pos, siz):
		self.prev_spots.append(pos)
		self.prev_sizes.append(siz)
		#self.prev_colrs.append(clr)

		if len(self.prev_spots) > self.num_rungs:
			self.prev_spots.pop(0)
			self.prev_sizes.pop(0)
			#self.prev_colrs.pop(0)