#!/usr/local/bin/python
import sys, pygame, math
from gameobjects.gametime import *
pygame.init()

""" rev12 : set framerate to 30, hopefully """
GC = GameClock(30)
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
midred = 170, 0, 0
green = 0, 255, 0
midgreen = 0, 170, 0
blue = 0, 0, 255
midblue = 0, 0, 170
grey = 150, 150, 150
darkgrey = 50, 50, 50
#Meh, fun.
pointsrgb = [red, green, blue]

def positive(number):
    #Convert negative numbers to their positive equivalent.
    #If the number is positive, return it.
    if number < 0:
        return number * -1
    else:
        return number

def normalisedAngle(angle):
    #Ensure that an angle is in radians properly (0 ~ 2*math.pi)
    if angle >= (math.pi * 2):
        return normalisedAngle(angle - 2 * math.pi)
    elif angle < 0:
        return normalisedAngle(angle + 2 * math.pi)
    else:
        return angle

class Order():
    def __init__(self, ship):
        return
    def poll(self):
        return

class Idle(Order):
    # do nothing. 
    def poll(self):
        return

class MoveToXY(Order):
    def __init__(self, ship, x, y):
        self.x, self.y = x, y
        self.angleToXY = ship.angleToXY(self.x, self.y)
    def poll(self):
        #pygame.draw.aaline(screen, red, (self.x - 10, self.y), (self.x + 10, self.y)) # movement testing markers
        #pygame.draw.aaline(screen, red, (self.x, self.y - 10), (self.x, self.y + 10)) # testing
        #pygame.draw.aaline(screen, green, (self.x, self.y), (ship.x, ship.y))         # testing
        """ rev12 : i like circles """
        pygame.draw.circle(screen, midgreen, (self.x, self.y), ship.intRadius, 2) # circle designators for the move. Currently living above ships so needs to be changed.
        if ship.intRotation != self.angleToXY: # If not on target to move to the new point.
            if positive(self.angleToXY - ship.intRotation) < ship.intRotateSpeed:
                 """ r23: Ben could you please markup this code? Not a clue how it works - BBP """
                ship.rotateRight(positive(self.angleToXY - ship.intRotation))
            else:
                """ new in rev 12, see appropriate function """
                ship.rotateLeft(positive(self.angleToXY - ship.intRotation))
        elif (ship.x, ship.y) != (self.x, self.y): # stop the ship on target
            if ship.distanceFrom(self.x, self.y) < ship.intSpeed: # If the destintion is a shorter distance than the move distance...
                ship.order = Idle(ship) # dump orders and...
            ship.moveForward()          # cover the rest of the distance.
        else:
            ship.order = Idle(ship)     # if all else fails, dump orders.
        ship.calcPoints()               # always recalculate points after moving. Rev 23: This is the source of the speedups slowdowns in ships. Calcpoints is part of the render loop.
      
class Ship()
    #basic stats for drawing & position.
    intRadius = 8                     # Size of the ship from the centre - size of largest part (if multiple parts are added)
    intRotation = math.radians(270.0) # Initial rotation of the ship. Changes every now and then for testing, doesn't matter usually.
   
    #speed stats.
    intSpeed = 2.0       # Movement
    intRotateSpeed = 1.0 # Rotation


    intSI = 1 # integer for the health of the ship

    intSide = 0 #game side. e.g 4th player in 4 player match = side 3

    points = [] # List of veticies that make up the ship.

    def __init__(self, side, x, y):
        self.side = side
        self.x, self.y = x, y
        self.order = Idle(self)
        self.calcPoints()
   
    def draw(self):
        """ Modded in rev 12 - effectively added multiple engine ports - seems dodgy though??? weird overwrite on the square. """
        #pygame.draw.line(screen, white, (50, 50), (25, 25))
        for i in range(0, len(self.points)):
            colour = white
            for j in range(0, len(self.intEnginePoint)):
                if i == self.intEnginePoint[j]:
                    colour = red
            pygame.draw.line(screen, colour, self.points[i], self.points[i - 1])
            
    def rotateRight(self, rotateBy=0):
        #Does exactly that
        if rotateBy == 0:
            rotateBy = self.intRotateSpeed
        self.intRotation = normalisedAngle(self.intRotation + rotateBy)

    def rotateLeft(self, rotateBy=0):
       #Does exactly that
       if rotateBy == 0:
           rotateBy = self.intRotateSpeed
       self.intRotation = normalisedAngle(self.intRotation - rotateBy)

    def moveForward(self, speed=0):
        #LOLZ.
        if speed == 0:
            speed = self.intSpeed             
        self.y -= math.cos(self.intRotation) * speed  
        self.x += math.sin(self.intRotation) * speed

    def poll(self):
        #update the ships data
        self.order.poll()

    def angleToXY(self, x, y):
        #calculate the angle from the referenced ships heading to the
        #given x,y point.
        if self.y - y > 0:
            return normalisedAngle(math.atan((self.x-x)/(y-self.y)))
        elif self.y - y == 0:
            return normalisedAngle(-math.atan(self.x-x))
        else:
            return normalisedAngle(math.atan((self.x-x)/(y-self.y))+math.pi)

    def distanceFrom(self, x, y):
        #Pythagoras up in this. yeah boy.
        return math.sqrt((self.x-x)**2 + (self.y-y)**2)

class S1s1(Ship):
    """ as of rev 12 now a list"""
    intEnginePoint = [2]

    def calcPoints(self):
    #calculate the three points of the triangle relative to the center xy of the ship
    #and the radius given to the ship.
        self.points = [(self.x + self.intRadius * math.sin(self.intRotation), (self.y - self.intRadius * math.cos(self.intRotation))),\
        (self.x + self.intRadius * math.sin(self.intRotation + 2.3 * math.pi / 3), (self.y - self.intRadius * math.cos(self.intRotation + 2.3 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin(self.intRotation + 3.7 * math.pi / 3), (self.y - self.intRadius * math.cos(self.intRotation + 3.7 * math.pi / 3)))]

class S1s2(Ship):
    """ as of rev 12, now a list """
    intEnginePoint = [2, 3]
      
    def calcPoints(self):
        self.points = [((self.x + self.intRadius * math.sin(self.intRotation)), (self.y - self.intRadius * math.cos(self.intRotation))),\
        (self.x + self.intRadius * math.sin(self.intRotation + 1.7 * math.pi / 3), (self.y - self.intRadius * math.cos(self.intRotation + 1.7 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin(self.intRotation + 3 * math.pi / 3), (self.y - self.intRadius * math.cos(self.intRotation + 3 * math.pi / 3))),\
        (self.x + self.intRadius * math.sin(self.intRotation + 4.3 * math.pi / 3), (self.y - self.intRadius * math.cos(self.intRotation + 4.3 * math.pi / 3)))]


ships = [S1s1(0, 100.0, 50.0), S1s2(0, 100.0, 100.0), S1s1(0, 150, 75)]
ships[0].order = MoveToXY(ships[0], 300.0, 50.0)
ships[1].order = MoveToXY(ships[1], 500.0, 100.0)
ships[2].order = MoveToXY(ships[2], 100.0, 100.0)
running = True

GC.start()

while running:
    for frame_count, game_time in GC.update():
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        else:
            #if event.type == click, etc.
            screen.fill(black)
    
            for ship in ships:
                ship.poll()
                ship.draw()
        
            pygame.display.flip()