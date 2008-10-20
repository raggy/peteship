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
        pygame.draw.circle(screen, midgreen, ((int(self.x) - player.x), (int(self.y)) - player.y), ship.radius, 2) # circle designators for the move. Currently living above ships so needs to be changed.
        """ Depreciated, using new function rotateTowardAngle 
        if ship.intRotation != self.angleToXY: # If not on target to move to the new point.           
            # Is this needed any more? The ships seem to rotate to their target within the first frame.
            if positive(self.angleToXY - ship.intRotation) < ship.intRotateSpeed: # If the amount the ship needs to turn is less than the amount it will turn in this frame (i.e. rotation speed)
                ship.rotateRight(positive(self.angleToXY - ship.intRotation)) # then rotate just enough to be on course.
            else:
                ship.rotateLeft(positive(self.angleToXY - ship.intRotation))
        """
        # New behaviour, rotate whilst moving
        if ship.distanceFrom(self.x, self.y) > math.sqrt(((ship.x + math.sin(ship.intRotation) * ship.intSpeed)-self.x)**2 + ((ship.y - math.cos(ship.intRotation) * ship.intSpeed)-self.y)**2): # If next move will bring you closer to the destination
            if normalisedAngle(self.angleToXY - ship.intRotation) < (math.pi / 4) or normalisedAngle(self.angleToXY - ship.intRotation) > (math.pi * 1.75):
                if (ship.x, ship.y) != (self.x, self.y): # stop the ship on target
                    if ship.distanceFrom(self.x, self.y) < ship.intSpeed: # If the destintion is a shorter distance than the move distance...
                        ship.order = Idle(ship) # dump orders and...
                    ship.moveForward()          # cover the rest of the distance.
                else:
                    ship.order = Idle(ship)     # if all else fails, dump orders.
        if ship.intRotation != self.angleToXY: # If the ship isn't already facing the right way
            self.angleToXY = ship.angleToXY(self.x, self.y)
            ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way
        ship.calcPoints()               # always recalculate points after moving. Rev 23: This is the source of the speedups slowdownsin ships. Calcpoints is part of the render loop.

        """ Old behaviour, rotate fully before moving
        if ship.intRotation != self.angleToXY: # If the ship isn't already facing the right way
            ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way
        else:
            if (ship.x, ship.y) != (self.x, self.y): # stop the ship on target
                if ship.distanceFrom(self.x, self.y) < ship.intSpeed: # If the destintion is a shorter distance than the move distance...
                    ship.order = Idle(ship) # dump orders and...
                ship.moveForward()          # cover the rest of the distance.
            else:
                ship.order = Idle(ship)     # if all else fails, dump orders.
        """
        ship.calcPoints()               # always recalculate points after moving. Rev 23: This is the source of the speedups slowdowns in ships. Calcpoints is part of the render loop.
      
class Ship():
    #basic stats for drawing & position.
    radius = 8                     # Size of the ship from the centre - size of largest part (if multiple parts are added)
    intRotation = math.radians(270.0) # Initial rotation of the ship. Changes every now and then for testing, doesn't matter usually.
    
    #speed stats.
    intSpeed = 0.5       # Movement
    intRotateSpeed = 0.01 # Rotation


    intSI = 1 # integer for the health of the ship

    intSide = 0 #game side. e.g 4th player in 4 player match = side 3

    points = [] # List of veticies that make up the ship.

    def __init__(self, player, x, y):
        self.player = player
        self.x, self.y = x, y
        self.order = Idle(self)
        self.calcPoints()
   
    def draw(self):
        #pygame.draw.line(screen, white, (50, 50), (25, 25))
        for i in range(0, len(self.points)):
            colour = player.colour
            for j in range(0, len(self.intEnginePoint)):
                if i == self.intEnginePoint[j]:
                    colour = red
            pygame.draw.line(screen, colour, ((self.points[i][0] - player.x), (self.points[i][1] - player.y)), ((self.points[i - 1][0] - player.x), (self.points[i - 1][1] - player.y)))
            
    """def rotateRight(self, rotateBy=0):
        # Depreciated
        if rotateBy == 0:
            rotateBy = self.intRotateSpeed
        self.intRotation = normalisedAngle(self.intRotation + rotateBy)

    def rotateLeft(self, rotateBy=0):
        # Depreciated
        if rotateBy == 0:
            rotateBy = self.intRotateSpeed
        self.intRotation = normalisedAngle(self.intRotation - rotateBy)
"""
    def rotateTowardAngle(self, angle):
        if positive(angle - ship.intRotation) < ship.intRotateSpeed: # If rotation speed is bigger than the amount which you need to turn
            self.intRotation = angle # then only turn to face the desired angle
        else:
            if normalisedAngle(angle - self.intRotation) > math.pi: # If the angle which you're rotating towards is more 180 degrees to the right, it makes more sense to turn left
                self.intRotation = normalisedAngle(self.intRotation - self.intRotateSpeed) # Turn left by self.intRotateSpeed
            else:
                self.intRotation = normalisedAngle(self.intRotation + self.intRotateSpeed) # Turn right by self.intRotateSpeed

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
        self.points = [(self.x + self.radius * math.sin(self.intRotation), (self.y - self.radius * math.cos(self.intRotation))),\
        (self.x + self.radius * math.sin(self.intRotation + 2.3 * math.pi / 3), (self.y - self.radius * math.cos(self.intRotation + 2.3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.intRotation + 3.7 * math.pi / 3), (self.y - self.radius * math.cos(self.intRotation + 3.7 * math.pi / 3)))]

class S1s2(Ship):
    """ as of rev 12, now a list """
    intEnginePoint = [2, 3]
      
    def calcPoints(self):
        self.points = [((self.x + self.radius * math.sin(self.intRotation)), (self.y - self.radius * math.cos(self.intRotation))),\
        (self.x + self.radius * math.sin(self.intRotation + 1.7 * math.pi / 3), (self.y - self.radius * math.cos(self.intRotation + 1.7 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.intRotation + 3 * math.pi / 3), (self.y - self.radius * math.cos(self.intRotation + 3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.intRotation + 4.3 * math.pi / 3), (self.y - self.radius * math.cos(self.intRotation + 4.3 * math.pi / 3)))]

""" New in r27 """
class Player(): 
    """ Set of stats to store what the player can see. """
    x = 0              # upper left position of the view, x axis.
    y = 0              # same, y axis.
    width = size [0]   # width of the screen, from left, in pixels.
    height = size [1]  # same, height
    tBound = 0
    bBound = 0
    lBound = 0
    rBound = 0
    """ End of player view stuff. """
    """ Player specific stats. """
    colour = midgreen # hahaha why not. Tank tastic.
    name = "Ronco"
    """ End of player specific stats """
    def __init__(self):
        self.calcBounds()

    def calcBounds(self):
        self.tBound = self.y - 10 # 10 is the biggest radius so far, will replace when we have more ships.
        self.bBound = self.y + self.height + 10 # same kinda thing
        self.lBound = self.x - 10
        self.rBound = self.x + self.width + 10

    def xy(self): # Return x, y as a tuple
        return (x, y)

player = Player()

ships = [S1s1(player, 100.0, 50.0), S1s2(player, 100.0, 100.0), S1s1(player, 150, 75)]
ships[0].intRotation = math.radians(270)
ships[1].intRotation = math.radians(269)
ships[0].order = MoveToXY(ships[0], 300.0, 50.0)
ships[1].order = MoveToXY(ships[1], 500.0, 100.0)
ships[2].order = MoveToXY(ships[2], 152.0, 75.0)
                
running = True

GC.start() # Start game clock

while running:
    for frame_count, game_time in GC.update():
        pygame.msg.message
        pygame.event.clear(pygame.MOUSEMOTION)
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN): # Loop through all MOUSEBUTTONDOWN events on the buffer
            if event.dict['button'] == 1: # If left mouse button clicked
                # then ask any ships if they're going to be selected
                for ship in ships:
                    if (event.dict['pos'][0] >= (ship.x - ship.radius - player.x) and event.dict['pos'][0] <= (ship.x + ship.radius - player.x)) and (event.dict['pos'][1] >= (ship.y - ship.radius - player.y) and event.dict['pos'][1] <= (ship.y + ship.radius - player.y)): # If player clicked on this ship
                        player.selectedShip = ship # Set player's selected ship
            elif event.dict['button'] == 3: # If right mouse button clicked
                player.selectedShip.order = MoveToXY(player.selectedShip, float(event.dict['pos'][0] - player.x), float(event.dict['pos'][1]) - player.y) # Give a move order to where player clicked
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_UP:
                player.y -= 10
            elif event.key == pygame.K_DOWN:
                player.y += 10
            elif event.key == pygame.K_LEFT:
                player.x -= 10
            elif event.key == pygame.K_RIGHT:
                player.x += 10
        screen.fill(black)
    
        for ship in ships: # Need to do code to check whether ships are on screen before drawing them
            ship.poll()
            ship.draw()
        
        pygame.display.flip()
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            running = False
