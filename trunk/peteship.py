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

def D2R(degrees):
      return degrees * (math.pi / 180)
      #nigh on unholy goodness.

def R2D(radians):
      return (radians * 180) / math.pi

"""
def renderLoop():
      screen.fill(black)
      dave.draw()
      john.draw()
      pygame.display.flip()
"""
      
class Ship():
      #basic stats for drawing & position.
      x = 50.0 #.0 for float plox.
      y = 50.0
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

class S1s1(Ship):
      intEnginePoint = 2
      def __init__(self, side, player=True):
            self.side = side
            self.player = player
            self.calcPoints()

      def calcPoints(self):
            self.points = [(self.x + self.intRadius * math.sin(math.radians(self.intRotation)), self.y - self.intRadius * math.cos(math.radians(self.intRotation))),\
                     (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 2.3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 2.3 * math.pi / 3))),\
                     (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 3.7 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 3.7 * math.pi / 3)))]

class S1s2(Ship):
      intEnginePoint = 2
      def __init__(self, side, player=True):
            self.side = side
            self.player = player
            self.calcPoints()

      def calcPoints(self):
            self.points = [(self.x + self.intRadius * math.sin(math.radians(self.intRotation)), self.y - self.intRadius * math.cos(math.radians(self.intRotation))),\
            (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 1.7 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 1.7 * math.pi / 3))),\
            (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 3 * math.pi / 3))),\
            (self.x + self.intRadius * math.sin((math.radians(self.intRotation) + 4.3 * math.pi / 3)), self.y - self.intRadius * math.cos((math.radians(self.intRotation) + 4.3 * math.pi / 3)))]
"""
dave = S1s1(0, True)
john = S1s2(0, True)
john.x = 100
john.y = 100
"""
ships = [S1s1(0, True), S1s2(0, True)]
ships[1].x = 100
ships[1].y = 100


running = 1
GC.start()

while running:
      for frame_count, game_time in GC.update():
            """
            #dave.rotateRight()
            dave.moveForward()
            john.moveForward()
            dave.calcPoints()
            john.calcPoints()
            """

            screen.fill(black)
            
            for ship in ships:
                  ship.moveForward()
                  ship.calcPoints()
                  ship.draw()

            pygame.display.flip()
            
            #renderLoop()
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                  running = 0
                  pygame.quit()

"""
while running:
   screen.fill(black)
   dave.draw()
   dave.rotateRight()
   #pygame.draw.line(screen, white, (50, 50), (75, 75))
   pygame.display.flip()
   event = pygame.event.poll()
   if event.type == pygame.QUIT:
      running = 0
      pygame.quit()
"""
