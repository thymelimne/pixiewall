# import the opencv library
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from random import random as rand

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


def capframe():

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


class Butterfly:

    def __init__(self, loc):
        self.locx = loc[0]
        self.locy = loc[1]
        self.angle = rand() * 360
        self.updatespeeds()
        self.color = (255, rand()*255, rand()*255)

        sizecoef = .5 + rand()
        self.size *= sizecoef
        self.regularspeed *= sizecoef
        self.speed *= sizecoef
        self.boostspeed *= sizecoef
        #self.color = (0, 255, 0)

    #color = BLUE
    speed = 2
    surface = screen

    locx = 200
    locy = 150

    size = .3
    spread = 1
    mostthin = .1
    mostthick = 1
    thinning = False
    thicking = False

    angle = 45
    speedx = np.cos(np.radians(angle)) * speed
    speedy = np.sin(np.radians(angle)) * speed

    regularspeed = 2
    boostspeed = 1

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


    def butterfly(self):
        wing1full = np.asarray(
            ((0, 0), (30, -70), (100, -100), (150, -110), (160, -90), (150, -40), (140, -10), (70, 50),
             (100, 70), (120, 100), (130, 120), (120, 160), (100, 190), (80, 200), (50, 190), (10, 140), (0, 110)),
            dtype=np.float64)
        wing2full = wing1full.copy()
        wing2full[:, 0] *= -1
        wing1 = np.copy(wing1full)
        wing2 = np.copy(wing2full)
        wing1 *= self.size
        wing2 *= self.size

        # Thinning the wings
        wing1[:, 0] *= self.spread
        wing2[:, 0] *= self.spread

        # Rotating the wings
        wing1 = self.rotatepoints(np.array([0, 0]), wing1, np.radians(self.angle))
        wing2 = self.rotatepoints(np.array([0, 0]), wing2, np.radians(self.angle))

        # Placing the wings
        wing1[:, 0] = wing1[:, 0] + self.locx
        wing1[:, 1] = wing1[:, 1] + self.locy
        wing2[:, 0] = wing2[:, 0] + self.locx
        wing2[:, 1] = wing2[:, 1] + self.locy

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
        self.locx += self.speedx
        self.locy -= self.speedy

        self.butterfly()  # This will call the animation

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


class Swarm:
    butterflies = []
    surface = screen
    timespawn = 0
    bz = 60
    def __init__(self):
        self.num_empties = rand() * 10
    should_transition = False
    def add(self, b):
        self.butterflies.append(b)
    def timestep(self):
        screen.fill(0)
        for b in self.butterflies:
            b.timestep()
            size = self.surface.get_size()
            if b.locx < -60 or b.locx > size[0] + 60 or b.locy < -60 or b.locy > size[1] + 60:
                print("deleted")
                self.butterflies.remove(b)
                del b
                if not self.butterflies:
                    print("_____EMPTY SCREEN______")
                    self.num_empties -= 1
                if not self.num_empties > 0:
                    self.should_transition = True
        if self.timespawn > 0:
           self.timespawn -= 1
        else:
            self.spawn()
            self.timespawn = rand() * 300
        clock.tick(60)
        global mode
        if self.should_transition:
            mode = 1
    def spawn(self):
        loc = [100, 100]
        if rand() < .5:
            loc[0] = self.surface.get_size()[0] + self.bz if rand() < .5 else 0-self.bz
            loc[1] = rand() * self.surface.get_size()[1]
        else:
            loc[0] = rand() * self.surface.get_size()[0]
            loc[1] = self.surface.get_size()[1] + self.bz if rand() < .5 else 0-self.bz
        angle = 0
        if loc[0] < 0:
            angle = rand() * 180
        elif loc[0] > self.surface.get_size()[0]:
            angle = 180 + rand() * 180
        elif loc[1] < 0:
            angle = 90 + rand() * 180
        elif loc[1] > self.surface.get_size()[1]:
            angle = rand() * 90 if rand() < .5 else 270 * rand() * 90
        print(loc)
        b = Butterfly(loc)
        print(b.angle)
        self.add(b)


b1 = Butterfly([100, 200])
b2 = Butterfly([300, 400])
s = Swarm()
s.add(b1)
s.add(b2)
s.spawn()

def reset_butterflies():
    s.butterflies.clear()

def reset_silhouettes():
    pass

mode = 2
while running:

    if mode == 1:
        toswitch = capframe()
        if (toswitch==2):
            reset_butterflies()
    if mode == 2:
        toswitch = s.timestep()
        if (toswitch==1):
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
                mode = 1
            if event.key == pygame.K_2:
                mode = 2

# After the loop release the cap object
vid.release()
cv2.destroyAllWindows()
pygame.quit()