'''
General class for a pygame element that can show stuff (not specific to a game.)
'''

import pygame
from random import random as rand

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