#!/usr/local/bin/python
import sys, os, pygame, math, random
sys.path.append(os.path.abspath(".."))
import formations
pygame.init()

""" rev12 : set framerate to 30, hopefully """
clock = pygame.time.Clock()
size = width, height = 800, 480 #Eee compatible resolution. ;)
screen = pygame.display.set_mode(size)

GLOBAL_TESTSHIPS = 10 #Generic int for creating multimples of tsetingships.
GLOBAL_ZOOMAMOUNT = 0.05

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
    def __init__(self):
        self.x = self.y = False
    def poll(self):
        return

class Idle(Order):
    # do nothing. 
    def poll(self):
        return

class MoveToXY(Order):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def setShip(self, ship):
        self.ship = ship
        self.angleToXY = ship.angleToXY(self.x, self.y)
        
    def poll(self):
        """ rev12 : i like circles """
        #pygame.draw.circle(screen, midgreen, ((int(self.x * player.zoom) - player.x), (int(self.y) * player.zoom) - player.y), ship.radius - 3, 2) # circle designators for the move. Currently living above ships so needs to be changed.
        #pygame.draw.line(screen, (20,20,20), ((self.x - player.x) * player.zoom, (self.y - player.y) * player.zoom), ((ship.x  - player.x) * player.zoom, (ship.y - player.y) * player.zoom))
        # New behaviour, rotate whilst moving
        #if ship.distanceFrom(self.x, self.y) > math.sqrt(((ship.x + math.sin(ship.rotation) * ship.speed)-self.x)**2 + ((ship.y - math.cos(ship.rotation) * ship.speed)-self.y)**2): # If next move will bring you closer to the destination
        if (normalisedAngle(self.angleToXY - ship.rotation) < (math.pi / 4) or normalisedAngle(self.angleToXY - ship.rotation) > (math.pi * 1.75)) or (ship.moving):
            ship.moving = True
            if (ship.x, ship.y) != (self.x, self.y): # stop the ship on target
                if ship.distanceFrom(self.x, self.y) < ship.speed: # If the destintion is a shorter distance than the move distance...
                    ship.order = ship.nextOrder() # get next orders and
                ship.moveForward()          # cover the rest of the distance.
            else:
                ship.order = ship.nextOrder() # Get next orders
        
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
    speed = 2.5       # Movementdisabled
    rotateSpeed = 0.05 # Rotation

    intSI = 1 # integer for the health of the ship

    intSide = 0 #game side. e.g 4th player in 4 player match = side 3

    points = [] # List of veticies that make up the ship.

    formation = False
    
    def __init__(self, player, x, y):
        self.player = player
        self.colour = self.player.colour
        self.x, self.y = x, y
        self.orders = [Idle()]
        self.moving = False
        self.built = False
        self.calcPoints()
        self.calcExtras() # For buildships.

    def calcExtras(self):
        pass
   
    def draw(self):
        if self.needsToCalcPoints:
            self.calcPoints()
        #self.drawOrders()
        pygame.draw.polygon(screen, black, self.offsetPoints())
        pygame.draw.aalines(screen, player.colour, True, self.offsetPoints())

    def drawOrders(self):
        lastx, lasty = self.x, self.y
        for order in self.orders:
            if not (order.x is False and order.y is False):
                pygame.draw.line(screen, (20,20,20), ((lastx - player.x) * player.zoom, (lasty - player.y) * player.zoom), ((order.x  - player.x) * player.zoom, (order.y - player.y) * player.zoom))
                #pygame.draw.circle(screen, (20,20,20), ((order.x - player.x) * player.zoom, (order.y - player.y) * player.zoom), 2)
                lastx, lasty = order.x, order.y
        
    def rotateTowardAngle(self, angle):
        if positive(angle - ship.rotation) < ship.rotateSpeed: # If rotation speed is bigger than the amount which you need to turn
            self.rotation = angle # then only turn to face the desired angle
        else:
            if normalisedAngle(angle - self.rotation) > math.pi: # If the angle which you're rotating towards is more 180 degrees to the right, it makes more sense to turn left
                self.rotation = normalisedAngle(self.rotation - self.rotateSpeed) # Turn left by self.rotateSpeed
            else:
                self.rotation = normalisedAngle(self.rotation + self.rotateSpeed) # Turn right by self.rotateSpeed
        self.needsToCalcPoints = True

    def moveForward(self):       
        self.y -= math.cos(self.rotation) * self.speed
        self.x += math.sin(self.rotation) * self.speed
        self.needsToCalcPoints = True

    def poll(self):
        #update the ships data
        self.orders[0].poll()
        self.calcExtras

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
            points.append(((point[0] - self.player.x) * player.zoom, (point[1] - self.player.y) * player.zoom))
        return points

    def nextOrder(self):
        self.orders.pop(0)
        if len(self.orders) == 0:
            self.moving = False
            self.orders.append(Idle())

    def queueOrder(self, order):
        if len(self.orders) > 0:
            if not isinstance(self.orders[-1], Idle):
                self.orders.append(order)
                self.orders[-1].setShip(self)
            else:
                self.setOrder(order)
        else:
            self.setOrder(order)

    def setOrder(self, order):
        if ship.built:
            self.orders = [order]
            self.orders[0].setShip(self)
        else:
            self.orders = [Idle(), order]
            self.orders[1].setShip(self)

    def justBuilt(self):
        self.nextOrder()
        self.built = True

class S1s1(Ship):
    """ as of rev 12 now a list"""
    intEnginePoint = [2]
    radius = 3
    rotateSpeed = 0.1 
    #buildInfo
    buildCost = 10
    buildTime = 50
    rotateSpeed = 0.1

    def calcPoints(self):
    #calculate the three points of the triangle relative to the center xy of the ship
    #and the radius given to the ship.
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),\
        (self.x + self.radius * math.sin(self.rotation + 2.3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 2.3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 3.7 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3.7 * math.pi / 3)))]
        self.needsToCalcPoints = False

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
        self.needsToCalcPoints = False

class S1s6(Ship):
    """ Carrier """
    intEnginePoint = [0, 0]
    buildPoints = [(0,0),(0,0)]
    buildQueue = []
    building = False
    buildTimeRemaining = 0
    buildShip = Ship

    radius = 12

    rotateSpeed = 0.004
    speed = 0.1

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
        self.needsToCalcPoints = False

    def calcExtras(self):
        self.buildPoints[0] = (self.x + (self.radius + 10) * math.sin(self.rotation)), (self.y - (self.radius + 10) * math.cos(self.rotation))

    def poll(self):
        #standard poll functions
        self.orders[0].poll()
        self.calcExtras()
        if self.building == False and len(self.buildQueue) > 0:
            self.buildShip = self.buildQueue.pop(0)
            self.buildShip.orders = [Idle()]
            self.buildShip.rotation = self.rotation
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
            #self.buildShip.rotation = self.rotation
            self.buildShip.rotation = normalisedAngle(0.02 + self.buildShip.rotation)
            self.buildShip.calcPoints()
            self.buildShip.colour = ((self.player.colour[0] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime),\
                                     (self.player.colour[1] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime),\
                                     (self.player.colour[2] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime))
            #print self.buildShip.colour

            if self.buildTimeRemaining == 1:
                #self.buildShip.setOrder(MoveToXY(10,10))
                self.buildShip.justBuilt()
                self.building = False            

    def addToBuildQueue(self): #Currently only produces triangles.
        self.buildQueue.append(S1s1(self.player, self.buildPoints[0][0], self.buildPoints[0][1])) # Pete, you forgot the self. prefix
                          
""" New in r27 """
class Player(): 
    """ Set of stats to store what the player can see. """
    x = 0.0              # upper left position of the view, x axis.
    y = 0.0              # same, y axis.
    width = size [0]   # width of the screen, from left, in pixels.
    height = size [1]  # same, height
    zoom = 1.0
    tBound = 0
    bBound = 0
    lBound = 0
    rBound = 0
    selectedShips = []
    """ End of player view stuff. """
    """ Player specific stats. """
    colour = white # hahaha why not.
    name = "Ronco"
    resources = 9001 # MONEY, GET BACK.
    """ End of player specific stats """
    def __init__(self):
        self.calcBounds()

    def calcBounds(self):
        self.tBound = self.y - 10 / self.zoom # 10 is the biggest radius so far, will replace when we have more ships.
        self.bBound = self.y + (self.height + 10) / self.zoom # same kinda thing
        self.lBound = self.x - 10 / self.zoom
        self.rBound = self.x + (self.width + 10) / self.zoom

    def focusOn(self, x, y):
        self.x = (x - (self.width / 2)) / player.zoom
        self.y = (y - (self.height / 2)) / player.zoom

    def xy(self): # Return x, y as a tuple
        return (x, y)

    def zoomBy(self, zoom):
        if self.zoom + zoom > 0.4:
            self.zoom += zoom
            self.panBy(((self.width / (self.zoom - zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom - zoom) - self.height / self.zoom) / 2))
            
    def panBy(self, x, y):
        if self.x + x < 0.0:
            self.x = 0.0
        else:
            self.x += x
        if self.y + y < 0.0:
            self.y = 0.0
        else:
            self.y += y
        self.calcBounds()
            
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
#shipsOnScreen = []
for i in range(GLOBAL_TESTSHIPS): # GLOBAL_TESTSHIPS is located at the top, this is a pain to find sometimes.
    ships.append(S1s1(player, (random.random()*width), (random.random()*height)))
    ships[i].built = True
#ships.append(S1s6(player, (player.width/2), (player.height/2)))
#ships[0].built = True
    #ships[i].order = MoveToXY(ships[i], 100.0, 100.0)

lollerLine = formations.Formation(ships)


""" build test code """
#!Warning! ships[0] must be of class S1s6 or greater. !Warning!
ships[0].addToBuildQueue()
#ships[0].addToBuildQueue()
#print ships[0].buildQueue

""" end build test code """

#player.focusOn(ships[0].x, ships[0].y)
player.selecting = False
keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,pygame.K_w:False,pygame.K_SPACE:False}
running = True

# Note on possible efficiency improvement: make a list of all ships on screen at the start of the frame

while running:
    clock.tick(30)
    pygame.msg.message

    for event in pygame.event.get(pygame.KEYDOWN):
        keysHeld[event.key] = True
        
    for event in pygame.event.get(pygame.KEYUP):
        keysHeld[event.key] = False
    
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN): # Loop through all MOUSEBUTTONDOWN events on the buffer
        if event.dict['button'] == 1: # If left mouse button clicked
            # then ask any ships if they're going to be selected
            #Testing new box select
            player.selStartPos = player.selEndPos = event.dict['pos']
            player.selecting = True
        elif (event.dict['button'] == 2) or (event.dict['button'] == 3): # If right mouse button clicked
            if pygame.KMOD_SHIFT & pygame.key.get_mods():
                for ship in player.selectedShips:
                    ship.queueOrder(MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
            else:
                for ship in player.selectedShips:
                    ship.setOrder(MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
        elif (event.dict['button'] == 4):
            player.panBy(0,-10)
        elif (event.dict['button'] == 5):
            player.panBy(0,10)
        elif (event.dict['button'] == 6):
            player.panBy(-10,0)
        elif (event.dict['button'] == 7):
            player.panBy(10,0)
    for event in pygame.event.get(pygame.MOUSEBUTTONUP):
        if event.dict['button'] == 1:
            player.selectedShips = []
            player.selecting = False
            player.selEndPos = event.dict['pos']
            if player.selStartPos[0] > player.selEndPos[0]: # If the player has dragged leftwards
                player.selStartPos, player.selEndPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1]) # then swap the x positions of start and end
            if player.selStartPos[1] > player.selEndPos[1]:
                player.selEndPos, player.selStartPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1])
            for ship in ships:
                if  player.selEndPos[0] >= (ship.x - ship.radius - player.x) * player.zoom and\
                    player.selStartPos[0] <= (ship.x + ship.radius - player.x) * player.zoom and\
                    player.selEndPos[1] >= (ship.y - ship.radius - player.y) * player.zoom and\
                    player.selStartPos[1] <= (ship.y + ship.radius - player.y) * player.zoom: # If player clicked on this ship
                    player.selectedShips.append(ship) # Set player's selected ship
    for event in pygame.event.get(pygame.MOUSEMOTION):
        if player.selecting:
            player.selEndPos = event.dict['pos']

    # Check keys
    if keysHeld[pygame.K_UP]:
        player.panBy(0,-10)
    if keysHeld[pygame.K_DOWN]:
        player.panBy(0,10)
    if keysHeld[pygame.K_LEFT]:
        player.panBy(-10,0)
    if keysHeld[pygame.K_RIGHT]:
        player.panBy(10,0)
    """if keysHeld[pygame.K_SPACE]:
        if player.selectedShip != False:
            player.focusOn(player.selectedShip.x, player.selectedShip.y)"""
    if keysHeld[pygame.K_q]: # petenote: When i figure out how many pixels this changes by i'll move the display so the zoom is centered.
        player.zoomBy(-GLOBAL_ZOOMAMOUNT)
    if keysHeld[pygame.K_w]:
        player.zoomBy(GLOBAL_ZOOMAMOUNT)
        #player.zoom += GLOBAL_ZOOMAMOUNT
        #player.x += (player.width/(player.zoom - GLOBAL_ZOOMAMOUNT) - player.width/player.zoom)
        #player.y += (player.height/(player.zoom - GLOBAL_ZOOMAMOUNT) - player.height/player.zoom)
        #print (player.width/(player.zoom - GLOBAL_ZOOMAMOUNT) - player.width/player.zoom)

    screen.fill(black) #ARRR.

    #for i in range(0,1000,100):
     #   pygame.draw.line(screen, darkgrey, (i*player.zoom, 0), (i*player.zoom, 1000))

    #shipsOnScreen = []
    #Update ships x & y. If the ship is onscreen, add to shipsOnScreen list. If it's not moving, don't calculate the points again = saves proc time. Will lag more and more with more ships moving though.
    for ship in ships:
        ship.drawOrders()

    for ship in ships: # Rev 43: Will work better when ships Idle properly. At the moment they stay with a move order.
        ship.poll()
        if ship.x > player.lBound and ship.x < player.rBound and ship.y > player.tBound and ship.y < player.bBound:
            #shipsOnScreen.append(ship)
            #if not isinstance(ship.order,Idle):
                #print ship.order #debug to see if ships stop.
                #ship.calcPoints()
            ship.draw()

    #for ship in shipsOnScreen:
    #    ship.draw()
    
    if player.selecting: # If the player is currently holding down the left mouse button
        # Draw a nice box for selection
        pygame.draw.line(screen, darkgrey, player.selStartPos, (player.selStartPos[0], player.selEndPos[1]))
        pygame.draw.line(screen, darkgrey, (player.selStartPos[0], player.selEndPos[1]), player.selEndPos)
        pygame.draw.line(screen, darkgrey, player.selEndPos, (player.selEndPos[0], player.selStartPos[1]))
        pygame.draw.line(screen, darkgrey, (player.selEndPos[0], player.selStartPos[1]), player.selStartPos)
        
    pygame.display.flip()
    if keysHeld[pygame.K_ESCAPE]:
        pygame.quit()
        running = False
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        running = False
