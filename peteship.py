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
    def __init__(self, ship):
        return
    def poll(self):
        return

class Idle(Order):
    def poll(self):
        return

class MoveToXY(Order):
    def __init__(self, ship, x, y):
        self.x, self.y = x, y
        self.angleToXY = ship.angleToXY(self.x, self.y)
    def poll(self):
        #pygame.draw.aaline(screen, red, (self.x - 10, self.y), (self.x + 10, self.y))
        #pygame.draw.aaline(screen, red, (self.x, self.y - 10), (self.x, self.y + 10))
        #pygame.draw.aaline(screen, green, (self.x, self.y), (ship.x, ship.y))        
        if ship.intRotation != self.angleToXY:
            if positive(self.angleToXY - ship.intRotation) < ship.intRotateSpeed:
                ship.rotateRight(positive(self.angleToXY - ship.intRotation))
            else:
                ship.rotateRight()
        elif (ship.x, ship.y) != (self.x, self.y):
            print ship.distanceFrom(self.x, self.y)
            if ship.distanceFrom(self.x, self.y) < (120 * ship.intSpeed):
                ship.x, ship.y = self.x, self.y
                ship.order = Idle(ship)
            ship.moveForward()
        else:
            ship.order = Idle(ship)
        ship.calcPoints()
      
class Ship():
    #basic stats for drawing & position.
    intRadius = 8
    intRotation = 120
   
    #speed stats.
    intSpeed = 0.01
    intRotateSpeed = 1.0

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
        self.order = Idle(self)
        self.calcPoints()
   
    def draw(self):
        #pygame.draw.line(screen, white, (50, 50), (25, 25))
        for i in range(0, len(self.points)):
            if i == self.intEnginePoint:
                pygame.draw.aaline(screen, grey, self.points[i],self.points[i - 1])
            else:
                pygame.draw.aaline(screen, white, self.points[i],self.points[i - 1])

    def rotateRight(self, rotateBy=0):
        #Does exactly that
        if rotateBy == 0:
            rotateBy = self.intRotateSpeed
        self.intRotation = normalisedAngle(self.intRotation + rotateBy)

    def moveForward(self, speed=0):
        #LOLZ.
        if speed == 0:
            speed = self.intSpeed             
        self.y -= math.degrees((math.cos(math.radians(self.intRotation))) * speed)   
        self.x += math.degrees((math.sin(math.radians(self.intRotation))) * speed)

    def poll(self):
        self.order.poll()

    def angleToXY(self, x, y):
        if self.y - y > 0:
            return normalisedAngle(int(math.degrees(math.atan((self.x-x)/(y-self.y)))))
        else:
            return normalisedAngle(int(math.degrees(math.atan((self.x-x)/(y-self.y)))+180))

    def distanceFrom(self, x, y):
        return math.sqrt((self.x-x)**2 + (self.y-y)**2)

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
ships[0].order = MoveToXY(ships[0], 300.0, 100.0)

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
