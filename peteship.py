#!/usr/local/bin/python
import sys, pygame, math
from gameobjects.gametime import *
pygame.init()

GC = GameClock()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
grey = 150, 150, 150
darkgrey = 50, 50, 50
#Meh, fun.
pointsrgb = [red, green, blue]
      
class Ship():
    #basic stats for drawing & position.
    intRadius = 8
    intRotation = 120
   
    #speed stats.
    intSpeed = 0.01
    intRotateSpeed =  0.1

    #health.
    intSI = 1

    #game side. e.g 4th player in 4 player match = side 3
    intSide = 0

    #player owned?
    boolPlayer=True

    points = []

    hasOrder = False

    def __init__(self, side, player, x, y):
        self.side = side
        self.player = player
        self.x, self.y = x, y
        self.calcPoints()
   
    def draw(self):
        #pygame.draw.line(screen, white, (50, 50), (25, 25))
        for i in range(0, len(self.points)):
            if i == self.intEnginePoint:
                pygame.draw.aaline(screen, grey, self.points[i],self.points[i - 1])
            else:
                pygame.draw.aaline(screen, white, self.points[i],self.points[i - 1])

    def rotateRight(self):
        #Does exactly that.
        self.intRotation += self.intRotateSpeed
        if self.intRotation > 359:
            self.intRotation -= 360

    def moveForward(self):
        #LOLZ.
        self.y -= math.degrees((math.cos(math.radians(self.intRotation))) * self.intSpeed)   
        self.x += math.degrees((math.sin(math.radians(self.intRotation))) * self.intSpeed)

    def poll(self):
            if not self.hasOrder:
                  return False
            else:
                  return True

            
class S1s1(Ship):
    intEnginePoint = 2

    def calcPoints(self):
        self.points = [(self.x + self.intRadius * math.sin(math.radians(self.intRotation)), self.y - self.intRadius * math.cos(math.radians(self.intRotation))),\
        (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 2.3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 2.3 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 3.7 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 3.7 * math.pi / 3)))]

class S1s2(Ship):
    intEnginePoint = 2
      
    def calcPoints(self):
        self.points = [(self.x + self.intRadius * math.sin(math.radians(self.intRotation)), self.y - self.intRadius * math.cos(math.radians(self.intRotation))),\
        (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 1.7 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 1.7 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 3 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 4.3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 4.3 * math.pi / 3)))]


ships = [S1s1(0, True, 200.0, 50.0), S1s2(0, True, 100.0, 100.0)]

running = 1
GC.start()

while running:
    for frame_count, game_time in GC.update():
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
            pygame.quit()
    
        screen.fill(black)
            
        for ship in ships:
            ship.poll()
            ship.draw()
                  
        pygame.display.flip()
