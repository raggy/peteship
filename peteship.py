#!/usr/local/bin/python
import sys, pygame, math, random
pygame.init()

""" rev12 : set framerate to 30, hopefully """
clock = pygame.time.Clock()
size = width, height = 800, 480 #Eee compatible resolution. ;)
screen = pygame.display.set_mode(size)

GLOBAL_TESTSHIPS = 1 #Generic int for creating multimples of tsetingships.

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
        """ rev12 : i like circles """
        #pygame.draw.circle(screen, midgreen, ((int(self.x * player.zoom) - player.x), (int(self.y) * player.zoom) - player.y), ship.radius - 3, 2) # circle designators for the move. Currently living above ships so needs to be changed.
        pygame.draw.line(screen, (20,20,20), ((int(self.x * player.zoom) - player.x), (int(self.y * player.zoom)) - player.y), ((ship.x * player.zoom) - player.x,(ship.y * player.zoom) - player.y))
        # New behaviour, rotate whilst moving
        if ship.distanceFrom(self.x, self.y) > math.sqrt(((ship.x + math.sin(ship.rotation) * ship.intSpeed)-self.x)**2 + ((ship.y - math.cos(ship.rotation) * ship.intSpeed)-self.y)**2): # If next move will bring you closer to the destination
            if normalisedAngle(self.angleToXY - ship.rotation) < (math.pi / 4) or normalisedAngle(self.angleToXY - ship.rotation) > (math.pi * 1.75):
                if (ship.x, ship.y) != (self.x, self.y): # stop the ship on target
                    if ship.distanceFrom(self.x, self.y) < ship.intSpeed: # If the destintion is a shorter distance than the move distance...
                        ship.order = Idle(ship) # dump orders and...
                    ship.moveForward()          # cover the rest of the distance.
                else:
                    ship.order = Idle(ship)     # if all else fails, dump orders.
        if ship.rotation != self.angleToXY: # If the ship isn't already facing the right way
            self.angleToXY = ship.angleToXY(self.x, self.y)
            ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way
        # always recalculate points after moving. Rev 23: This is the source of the speedups slowdownsin ships. Calcpoints is part of the render loop.
      
class Ship():
    #basic stats for drawing & position.
    radius = 8                      # Size of the ship from the centre - size of largest part (if multiple parts are added)
    rotation = math.radians(270.0)  # Initial rotation of the ship. Changes every now and then for testing, doesn't matter usually.
                                    # r43 : Changed to rotation instead of intRotation
    
    #speed stats.
    intSpeed = 2.5       # Movement
    intRotateSpeed = 0.05 # Rotation


    intSI = 1 # integer for the health of the ship

    intSide = 0 #game side. e.g 4th player in 4 player match = side 3

    points = [] # List of veticies that make up the ship.
    
    def __init__(self, player, x, y):
        self.player = player
        self.x, self.y = x, y
        self.order = Idle(self)
        self.calcPoints()
        self.calcExtras() # For buildships.

    def calcExtras(self):
        pass
   
    def draw(self):
        pygame.draw.polygon(screen, black, self.offsetPoints())
        pygame.draw.aalines(screen, player.colour, True, self.offsetPoints())
        
    def rotateTowardAngle(self, angle):
        if positive(angle - ship.rotation) < ship.intRotateSpeed: # If rotation speed is bigger than the amount which you need to turn
            self.rotation = angle # then only turn to face the desired angle
        else:
            if normalisedAngle(angle - self.rotation) > math.pi: # If the angle which you're rotating towards is more 180 degrees to the right, it makes more sense to turn left
                self.rotation = normalisedAngle(self.rotation - self.intRotateSpeed) # Turn left by self.intRotateSpeed
            else:
                self.rotation = normalisedAngle(self.rotation + self.intRotateSpeed) # Turn right by self.intRotateSpeed

    def moveForward(self, speed=0):
        #LOLZ.
        if speed == 0:
            speed = self.intSpeed             
        self.y -= math.cos(self.rotation) * speed  
        self.x += math.sin(self.rotation) * speed

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

    def offsetPoints(self):
        points = []
        for point in self.points:
            points.append(((point[0]* player.zoom - self.player.x), (point[1]* player.zoom-self.player.y)))
        return points

class S1s1(Ship):
    """ as of rev 12 now a list"""
    intEnginePoint = [2]

    #buildInfo
    buildCost = 10
    buildTime = 50

    def calcPoints(self):
    #calculate the three points of the triangle relative to the center xy of the ship
    #and the radius given to the ship.
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),\
        (self.x + self.radius * math.sin(self.rotation + 2.3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 2.3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 3.7 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3.7 * math.pi / 3)))]

class S1s2(Ship):
    """ as of rev 12, now a list """
    intEnginePoint = [2, 3]

    #buildInfo
    buildCost = 10
    buildTime = 10
      
    def calcPoints(self):
        self.points = [((self.x + self.radius * math.sin(self.rotation)), (self.y - self.radius * math.cos(self.rotation))),\
        (self.x + self.radius * math.sin(self.rotation + 1.7 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 1.7 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 4.3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 4.3 * math.pi / 3)))]

class S1s6(Ship):
    """ Carrier """
    intEnginePoint = [0, 0]
    buildPoints = [(0,0),(0,0)]
    buildQueue = []
    building = False
    buildTimeRemaining = 0
    buildShip = Ship


    #buildInfo
    buildCost = 10
    buildTime = 1000
        
    def calcPoints(self):
        self.points = [(self.x + self.radius * math.sin(self.rotation + 5.8 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 5.8 * math.pi /3))),\
        (self.x + self.radius * math.sin(self.rotation + 0.2 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 0.2 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 2 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 2 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 2.8 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 2.8 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 3.2 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3.2 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 4 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 4 * math.pi / 3)))]

    def calcExtras(self):
        self.buildPoints[0] = (self.x + (self.radius + 10) * math.sin(self.rotation)), (self.y - (self.radius + 10) * math.cos(self.rotation))

    def poll(self):
        #standard poll functions
        self.order.poll()
        # Update buildpoint. Needs to be done even when not on screen.
        self.buildPoints[0] = (self.x + (self.radius + 10) * math.sin(self.rotation)), (self.y - (self.radius + 10) * math.cos(self.rotation))
        if self.building == False and len(self.buildQueue) > 0:
            self.buildShip = self.buildQueue.pop(0)
            self.buildShip.order = Idle(self)
            self.player.resources -= self.buildShip.buildCost
            self.buildTimeRemaining = self.buildShip.buildTime
            ships.append(self.buildShip) # Add to list of ships.
#            print ships
            self.building = True
        elif self.building == True:
#            print self.buildTimeRemaining
            self.buildTimeRemaining -= 1
            self.buildShip.x = self.buildPoints[0][0]
#            print self.buildShip.x
            self.buildShip.y = self.buildPoints[0][1]
            self.buildShip.rotation = self.rotation
            self.buildShip.calcPoints()

            if self.buildTimeRemaining == 0:
                self.building = False
                
            

    def addToBuildQueue(self): #Currently only produces triangles.
        self.buildQueue.append(S1s1(self.player, self.buildPoints[0][0], self.buildPoints[0][1])) # Pete, you forgot the self. prefix
                          
""" New in r27 """
class Player(): 
    """ Set of stats to store what the player can see. """
    x = 0              # upper left position of the view, x axis.
    y = 0              # same, y axis.
    width = size [0]   # width of the screen, from left, in pixels.
    height = size [1]  # same, height
    zoom = 2.0
    tBound = 0
    bBound = 0
    lBound = 0
    rBound = 0
    selectedShip = False
    """ End of player view stuff. """
    """ Player specific stats. """
    colour = white # hahaha why not.
    name = "Ronco"
    resources = 9001 # MONEY, GET BACK.
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

"""
ships = [S1s1(player, 100.0, 50.0), S1s2(player, 100.0, 100.0), S1s1(player, 150, 75)]
ships[0].rotation = math.radians(270)
ships[1].rotation = math.radians(269)
ships[0].order = MoveToXY(ships[0], 300.0, 50.0)
ships[1].order = MoveToXY(ships[1], 500.0, 100.0)
ships[2].order = MoveToXY(ships[2], 152.0, 75.0)
"""

ships = []
for i in range(GLOBAL_TESTSHIPS): # GLOBAL_TESTSHIPS is located at the top, this is a pain to find sometimes.
    ships.append(S1s6(player, (random.random()*width), (random.random()*height)))
    ships[i].order = MoveToXY(ships[i], 100.0, 100.0)

""" build test code """
#!Warning! ships[0] must be of class S1s6 or greater. !Warning!
ships[0].addToBuildQueue()
ships[0].addToBuildQueue()
print ships[0].buildQueue

""" end build test code """

running = True

while running:
    clock.tick(30)
    pygame.msg.message
    pygame.event.clear(pygame.MOUSEMOTION)
    pygame.event.clear(pygame.MOUSEBUTTONUP)
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN): # Loop through all MOUSEBUTTONDOWN events on the buffer
        if event.dict['button'] == 1: # If left mouse button clicked
            # then ask any ships if they're going to be selected
            player.selectedShip = False
            for ship in ships:
                if (event.dict['pos'][0] >= ((ship.x - ship.radius)*player.zoom - player.x) and event.dict['pos'][0] <= ((ship.x + ship.radius)*player.zoom - player.x)) and (event.dict['pos'][1] >= ((ship.y - ship.radius)*player.zoom - player.y) and event.dict['pos'][1] <= ((ship.y + ship.radius)*player.zoom - player.y)): # If player clicked on this ship
                    player.selectedShip = ship # Set player's selected ship
        elif event.dict['button'] == 3: # If right mouse button clicked
            if not player.selectedShip is False:
                player.selectedShip.order = MoveToXY(player.selectedShip, ((float(event.dict['pos'][0]) + player.x)/ player.zoom), ((float(event.dict['pos'][1])) + player.y) / player.zoom) # Give a move order to where player clicked
    for event in pygame.event.get(pygame.KEYDOWN):
        if event.key == pygame.K_UP:
            player.y -= 10
        elif event.key == pygame.K_DOWN:
            player.y += 10
        elif event.key == pygame.K_LEFT:
            player.x -= 10
        elif event.key == pygame.K_RIGHT:
            player.x += 10
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            running = False
        elif event.key == pygame.K_q: # petenote: When i figure out how many pixels this changes by i'll move the display so the zoom is centered.
            player.zoom -= 0.1
        elif event.key == pygame.K_w:
            player.zoom += 0.1

    screen.fill(black) #ARRR.
    
    #Update ships x & y. If the ship is onscreen, draw it. If it's not moving, don't calculate the points again = saves proc time. Will lag more and more with more ships moving though.
    for ship in ships: # Rev 43: Will work better when ships Idle properly. At the moment they stay with a move order.
        ship.poll()
        if ship.x > player.lBound and ship.x < player.rBound and ship.y > player.tBound and ship.y < player.bBound:
            if not isinstance(ship.order,Idle):
                #print ship.order #debug to see if ships stop.
                ship.calcPoints()
            ship.draw()
    
    pygame.display.flip()
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        running = False
