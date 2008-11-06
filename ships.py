import misc, math, orders, pygame, effects

class Ship():
    #basic stats for drawing & position.
    radius = 8                      # Size of the ship from the centre - size of largest part (if multiple parts are added)
    rotation = math.radians(270.0)  # Initial rotation of the ship. Changes every now and then for testing, doesn't matter usually.
                                    # r43 : Changed to rotation instead of intRotation
    dead = False
    #speed stats.
    speed = 2.5
    rotateSpeed = 0.05 # Rotation

    intSI = 1 # integer for the health of the ship

    intSide = 0 #game side. e.g 4th player in 4 player match = side 3

    points = [] # List of veticies that make up the ship.

    formation = False
    
    def __init__(self, player, x, y):
        self.player = player
        self.colour = self.player.colour
        self.x, self.y = x, y
	self.shieldRadius = self.radius + 2
        self.orders = [orders.Idle()]
        self.moving = False
        self.built = False
        self.calcPoints()
        self.calcExtras() # For buildships.
        
    def remove(self):
	self.dead = True
        for i in range(len(self.player.ships)):
            if self.player.ships[i] == self:
                del self.player.ships[i]
                break
        for i in range(len(self.player.selectedShips)):
            if self.player.selectedShips[i] == self:
                del self.player.selectedShips[i]
                break
	del self
        
    def die(self):
        #also needs adding in
        #death animation goes here.
        self.player.effects.append(effects.ExplosionShip(self))
        self.player.effects.append(effects.Explosion((self.x, self.y), 0.5, (self.radius * 4), self.player, misc.WHITE))
        #and remove the ship when done.
        self.remove()
        #any player related stats go here. like death count and such. Dunno if we want need these but hum.

    def calcExtras(self):
        pass
   
    def draw(self):
        if self.needsToCalcPoints:
            self.calcPoints()
        #self.drawOrders()
        pygame.draw.polygon(self.player.screen, misc.BLACK, self.offsetPoints())
        pygame.draw.aalines(self.player.screen, self.player.colour, True, self.offsetPoints())

    def drawOrders(self):
        lastx, lasty = self.x, self.y
        for order in self.orders:
            tempxy = order.xy()
            if not tempxy is False:
                pygame.draw.line(self.player.screen, misc.DARKGREY, ((lastx - self.player.x) * self.player.zoom, (lasty - self.player.y) * self.player.zoom), ((tempxy[0]  - self.player.x) * self.player.zoom, (tempxy[1] - self.player.y) * self.player.zoom))
                #pygame.draw.circle(screen, (20,20,20), ((order.x - player.x) * player.zoom, (order.y - player.y) * player.zoom), 2)
                lastx, lasty = tempxy[0], tempxy[1]
        
    def rotateTowardAngle(self, angle):
        if misc.positive(angle - self.rotation) < self.rotateSpeed: # If rotation speed is bigger than the amount which you need to turn
            self.rotation = angle # then only turn to face the desired angle
        else:
            if misc.normalisedAngle(angle - self.rotation) > math.pi: # If the angle which you're rotating towards is more 180 degrees to the right, it makes more sense to turn left
                self.rotation = misc.normalisedAngle(self.rotation - self.rotateSpeed) # Turn left by self.rotateSpeed
            else:
                self.rotation = misc.normalisedAngle(self.rotation + self.rotateSpeed) # Turn right by self.rotateSpeed
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
            return misc.normalisedAngle(math.atan((self.x-x)/(y-self.y)))
        elif self.y - y == 0:
            return misc.normalisedAngle(-math.atan(self.x-x))
        else:
            return misc.normalisedAngle(math.atan((self.x-x)/(y-self.y))+math.pi)

    def distanceFrom(self, x, y):
        #Pythagoras up in this. yeah boy.
        return math.sqrt((self.x-x)**2 + (self.y-y)**2)

    def offsetPoints(self):
        points = []
        for point in self.points:
            points.append(((point[0] - self.player.x) * self.player.zoom, (point[1] - self.player.y) * self.player.zoom))
        return points

    def nextOrder(self):
        self.orders.pop(0)
        if len(self.orders) == 0:
            self.moving = False
            self.orders.append(orders.Idle())

    def queueOrder(self, order):
        if len(self.orders) > 0:
            if not isinstance(self.orders[-1], orders.Idle):
                self.orders.append(order)
                self.orders[-1].setShip(self)
            else:
                self.setOrder(order)
        else:
            self.setOrder(order)

    def setOrder(self, order):
        if self.built:
            self.orders = [order]
            self.orders[0].setShip(self)
        else:
            self.orders = [orders.Idle(), order]
            self.orders[1].setShip(self)

    def justBuilt(self):
        self.nextOrder()
        self.built = True

    def select(self):
	self.player.selectedShips.append(self)

class S1s1(Ship):
    """ as of rev 12 now a list"""
    intEnginePoint = [2]
    radius = 3
    rotateSpeed = 0.1 
    #buildInfo
    buildCost = 10
    buildTime = 500
    rotateSpeed = 0.1
    canAttack = True # this ship has a weapon! useful for setting ui & making sure that ships that can't attack when selected
                            # with those that can don't get an erroneus attack order.
    
    def calcPoints(self):
    #calculate the three points of the triangle relative to the center xy of the ship
    #and the radius given to the ship.
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),\
        (self.x + self.radius * math.sin(self.rotation + 2.3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 2.3 * math.pi / 3))),\
        (self.x + self.radius * math.sin(self.rotation + 3.7 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3.7 * math.pi / 3)))]
        self.needsToCalcPoints = False
    
    def calcExtras(self):
        self.hardpoints = [(self.x + self.radius * math.sin(self.rotation), self.y - self.radius * math.cos(self.rotation), self.rotation)]

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
            self.buildShip.orders = [orders.Idle()]
            self.buildShip.rotation = self.rotation
            self.player.resources -= self.buildShip.buildCost
            self.buildTimeRemaining = self.buildShip.buildTime
            self.player.ships.append(self.buildShip) # Add to list of ships.
#            print ships
            self.building = True
        elif self.building == True:
#            print self.buildTimeRemaining
            self.buildTimeRemaining -= 1
            self.buildShip.x = self.buildPoints[0][0]
#            print self.buildShip.x
            self.buildShip.y = self.buildPoints[0][1]
            #self.buildShip.rotation = self.rotation
            self.buildShip.rotation = misc.normalisedAngle(0.02 + self.buildShip.rotation)
            self.buildShip.calcPoints()
            self.buildShip.colour = ((self.player.colour[0] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime),\
                                     (self.player.colour[1] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime),\
                                     (self.player.colour[2] * (self.buildShip.buildTime - self.buildTimeRemaining + 1) / self.buildShip.buildTime))
            #print self.buildShip.colour

            if self.buildTimeRemaining == 1:
                #self.buildShip.setOrder(orders.MoveToXY(10,10))
                self.buildShip.justBuilt()
                self.building = False            

    def addToBuildQueue(self): #Currently only produces triangles. only works on buildships.
        self.buildQueue.append(S1s1(self.player, self.buildPoints[0][0], self.buildPoints[0][1])) # Pete, you forgot the self. prefix
