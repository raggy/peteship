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

def positive(number):
    if number < 0:
        return number * -1
    else:
        return number

def normalisedAngle(angle):
    if angle > 359:
        return normalisedAngle(angle - 360)
    elif angle < 0:
        return normalisedAngle(angle + 360)
    else:
        return angle

class Order():
    def poll(self, ship):
        return

class Idle(Order):
    def poll(self, ship):
        return

class MoveToXY(Order):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.angleToXY = ship.angleToXY(self.x, self.y)
        print self.angleToXY
    def poll(self, ship):
        if ship.intRotation != self.angleToXY:
            if (self.angleToXY - ship.intRotation) < ship.intRotateSpeed:
                ship.rotateRight(self.angleToXY - ship.intRotation)
            else:
                ship.rotateRight()
        elif (ship.x, ship.y) != (self.x, self.y):
            if ship.distanceFrom(self.x, self.y) < ship.intSpeed:
                ship.moveForward(ship.distanceFrom(self.x, self.y)
            ship.moveForward()
        else:
            ship.order = Idle()
        ship.calcPoints()
      
class Ship():
    #basic stats for drawing & position.
    intRadius = 8
    intRotation = 120
   
    #speed stats.
    intSpeed = 0.01
    intRotateSpeed =  10.0

    #health.
    intSI = 1

    #game side. e.g 4th player in 4 player match = side 3
    intSide = 0

    #player owned?
    boolPlayer=True

    points = []

    def __init__(self, side, player, x, y):
        self.side = side
        self.player = player
        self.x, self.y = x, y
        self.order = Idle()
        self.calcPoints()
   
    def draw(self):
        #pygame.draw.line(screen, white, (50, 50), (25, 25))
        for i in range(0, len(self.points)):
            if i == self.intEnginePoint:
                pygame.draw.aaline(screen, grey, self.points[i],self.points[i - 1])
            else:
                pygame.draw.aaline(screen, white, self.points[i],self.points[i - 1])

    def rotateRight(self, rotateBy=-1):
        #Does exactly that
        if rotateBy == -1:
            rotateBy = self.intRotateSpeed
        self.intRotation = normalisedAngle(self.intRotation + rotateBy)

    def moveForward(self):
        #LOLZ.
        self.y -= math.degrees((math.cos(math.radians(self.intRotation))) * self.intSpeed)   
        self.x += math.degrees((math.sin(math.radians(self.intRotation))) * self.intSpeed)

    def poll(self):
        self.order.poll(self)

    def angleToXY(self, x, y):
        return normalisedAngle(int(math.degrees(math.atan(y-self.y/x-self.x))))

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
ships[0].order = MoveToXY(10.0, 0.0)

GC.start()

while True:
    for frame_count, game_time in GC.update():
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
    
        screen.fill(black)

        for ship in ships:
            ship.poll()
            ship.draw()
        
        pygame.display.flip()
