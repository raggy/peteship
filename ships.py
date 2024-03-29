import misc, math, orders, pygame, effects

try:
    import psyco
    psyco.profile()
except ImportError:
    pass

class Ship():
    #basic stats for drawing & position.
    radius = 8                      # Size of the ship from the centre - size of largest part (if multiple parts are added)
    rotation = math.radians(270.0)  # Initial rotation of the ship. Changes every now and then for testing, doesn't matter usually.
                                    # r43 : Changed to rotation instead of intRotation
    dead = False # I'M ALIVEEEE
    #speed stats.
    speed = 2.5
    rotateSpeed = 0.05 # Rotation

    health = 1 # integer for the health of the ship

    points = [] # List of veticies that make up the ship.

    formation = False
    
    def __init__(self, view, player, x, y):
        self.player = player
        self.view = view
        self.colour = self.player.colour
        self.x, self.y = x, y
        self.shieldRadius = self.radius + 2
        self.orders = [orders.Idle(self)]
        self.moving = False
        self.built = False
        self.calcPoints()
        self.calcExtras() # Stuff that isn't points but needs to be calced.
        
    def drawShield(self, hitBy):
        self.view.effects.append(effects.BubbleShield(self, self.view, (self.x, self.y), self.shieldRadius, 0))
        #self.view.effects.append(effects.AngleShield(self, self.view, (self.x, self.y), self.radius + 2, 0, hitBy))
        
    def damaged(self, amount, hitBy):
        self.health -= amount
        self.drawShield(hitBy)
        if self.health <= 0:
            self.die()
        
    def remove(self):
        self.dead = True
        for i in range(len(self.player.ships)):
            if self.player.ships[i] == self:
                del self.player.ships[i]
                break
        for i in range(len(self.view.selectedShips)):
            if self.view.selectedShips[i] == self:
                del self.view.selectedShips[i]
                break
        del self
        
    def die(self):
        self.view.effects.append(effects.ExplosionShip(self.view, self, 10))
        self.view.effects.append(effects.Explosion(self.view, (self.x, self.y), 0.5, (self.radius * 4), misc.WHITE))
        #and remove the ship when done.
        self.remove()
        #any player related stats go here. like death count and such. Dunno if we want need these but hum.

    def calcExtras(self):
        pass
   
    def draw(self):
        if self.needsToCalcPoints:
            self.calcPoints()
        #self.drawOrders()
        pygame.draw.polygon(self.view.screen, misc.BLACK, self.offsetPoints())
        pygame.draw.aalines(self.view.screen, self.colour, True, self.offsetPoints())

    def drawOrders(self):
        lastx, lasty = self.x, self.y
        for order in self.orders:
            tempxy = order.xy()
            if not tempxy is False:
                pygame.draw.line(self.view.screen, order.colour, ((lastx - self.view.x) * self.view.zoom, (lasty - self.view.y) * self.view.zoom), ((tempxy[0]  - self.view.x) * self.view.zoom, (tempxy[1] - self.view.y) * self.view.zoom))
                #pygame.draw.circle(screen, (20,20,20), ((order.x - view.x) * view.zoom, (order.y - view.y) * view.zoom), 2)
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
        self.calcExtras()
#        self.view.lowEffects.append(effects.StaticParticle(self.view, self.x + self.radius * math.sin(self.rotation + math.pi), (self.y - self.radius * math.cos(self.rotation + math.pi)), 5))

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
            points.append(((point[0] - self.view.x) * self.view.zoom, (point[1] - self.view.y) * self.view.zoom))
        return points

    def nextOrder(self):
        self.orders.pop(0)
        if len(self.orders) == 0:
            self.moving = False
            self.orders.append(orders.Idle(self))

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
            self.orders = [orders.Idle(self), order]
            self.orders[1].setShip(self)

    def justBuilt(self):
        self.nextOrder()
        self.built = True

    def select(self):
        self.view.selectedShips.append(self)

    def drawBounding( self ):
        #Calculate the scaled center
        xCenter = ( self.x - self.view.x ) * self.view.zoom;
        yCenter = ( self.y - self.view.y ) * self.view.zoom;

        #Calculate the scaled size
        zSize = ( ( self.shieldRadius ) * self.view.zoom )

        #Calculate the minimum x for the bounding box
        xMin = xCenter - zSize
        xMax = xCenter + zSize
        
        #Calculate the minimum y for the bounding box
        yMin = yCenter - zSize
        yMax = yCenter + zSize
        
        #Draw bounding circle
        pygame.draw.circle(self.view.screen, misc.MIDGREEN, ((self.x - self.view.x) * self.view.zoom, (self.y - self.view.y) * self.view.zoom), (self.shieldRadius + 2) * self.view.zoom, 1)
		
        """
        #Draw bounding box of object
        
        pygame.draw.line(self.view.screen, misc.GREY, ( xMin, yMax ), ( xMax, yMax ),2 )
        pygame.draw.line(self.view.screen, misc.GREY, ( xMax, yMax ), ( xMax, yMin ),2 )
        pygame.draw.line(self.view.screen, misc.GREY, ( xMax, yMin ), ( xMin, yMin ),2 )
        pygame.draw.line(self.view.screen, misc.GREY, ( xMin, yMin ), ( xMin, yMax ),2 )
        """
        
        # SPECIFC SHIP CLASSES START HERE ! ! ! !  ! !  ! !  !   ! !  ! !  ! !  ! ! !  ! !  !

class S1s1(Ship):
    """ as of rev 12 now a list"""
    health = 10
    radius = 5
    shieldRadius = 5
    #buildInfo
    buildCost = 2
    buildTime = 400
    rotateSpeed = 0.05
    speed = 1
    canAttack = True # this ship has a weapon! useful for setting ui & making sure that ships that can't attack when selected
                            # with those that can don't get an erroneus attack order.
    launchers = []    # weapon related values
    hardpoints = []
    
    def __init__(self, view, player, x, y):
        self.enginePoint = (x, y) # engine points. one needs to be initialised so it is...
        """
        Please note that enginePoints function like hardpoints, due to the nature of the flickerCircle effect.
        Ho hum. If a ship has more than three engines i'll code it as a list. or something.
        
        On S1s1 it's calcpointed as a point nearer the rear of the ship.
        """
        # and we create a FlickerCircle for it...
        # FlickerCircle.__init__(self, view, xyAsTuple, size, speed, colour):
        self.engineFlicker = effects.FlickerCircle(view, self.enginePoint, 2.5, 0.25, misc.WHITE)
        view.lowEffects.append(self.engineFlicker)
        # this needs to have it's xy updated in calcpoints.
        Ship.__init__(self, view, player, x, y)
        
    def calcPoints(self):
    #calculate the three points of the triangle relative to the center xy of the ship
    #and the radius given to the ship.
    
        # starboard side
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),\
        (self.x + self.radius     * math.sin(self.rotation + 2.3 * math.pi / 3), (self.y - self.radius     * math.cos(self.rotation + 2.3 * math.pi / 3))),\
        (self.x + self.radius     * math.sin(self.rotation + 2.7 * math.pi / 3), (self.y - self.radius     * math.cos(self.rotation + 2.7 * math.pi / 3))),\
        # these two lines are the inner dips for the engine.
        (self.x + (self.radius-3) * math.sin(self.rotation + 2.6 * math.pi / 3), (self.y - (self.radius-3) * math.cos(self.rotation + 2.6 * math.pi / 3))),\
        (self.x + (self.radius-3) * math.sin(self.rotation + 3.4 * math.pi / 3), (self.y - (self.radius-3) * math.cos(self.rotation + 3.4 * math.pi / 3))),\
        # port side.
        (self.x + self.radius     * math.sin(self.rotation + 3.3 * math.pi / 3), (self.y - self.radius     * math.cos(self.rotation + 3.3 * math.pi / 3))),\
        (self.x + self.radius     * math.sin(self.rotation + 3.7 * math.pi / 3), (self.y - self.radius     * math.cos(self.rotation + 3.7 * math.pi / 3)))]
        self.needsToCalcPoints = False
    
    def calcExtras(self):
        self.hardpoints = [(self.x + (self.radius + 3) * math.sin(self.rotation), (self.y - (self.radius + 8) * math.cos(self.rotation)), self.rotation)]
        # engine point calcs. THESE NEED TO BE MOVED TO CALCPOINTS WHEN THEY'RE ONLY DRAWING WHEN ONSCREEN.
        # calculate the xy.
        self.enginePoint = ((self.x + (self.radius - 3.5)  * math.sin(self.rotation + 3 * math.pi / 3)), (self.y - (self.radius - 3.5) * math.cos(self.rotation + 3 * math.pi / 3)))
        # update the xy.
        if self.moving:
            self.engineFlicker.xy = self.enginePoint
            self.engineFlicker.visible = True # this could be handled in the poll of the FlickerCircle.
                                              # but it would be less offscreen efficient - this only gets polled when onscreen.
        else:
            self.engineFlicker.visible = False
        i = 0
        for launcher in self.launchers:
            launcher.hardpoint = self.hardpoints[i]
            launcher.poll()
            i += 1
            
    def die(self):
        self.view.effects.append(effects.ExplosionShip(self.view, self, 10))
        self.view.effects.append(effects.Explosion(self.view, (self.x, self.y), 0.5, (self.radius * 4), misc.WHITE))
        #and remove the ship when done.
        self.remove()
        #any player related stats go here. like death count and such. Dunno if we want need these but hum.
        self.engineFlicker.die()

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
        
class S1s4(Ship):
    """ Spear class cruiser """
    health = 50
    radius = 20
    shieldRadius = 22
    #buildInfo
    buildCost = 10
    buildTime = 1000
    rotateSpeed = 0.005
    speed = 0.2
    canAttack = True # this ship has a weapon! useful for setting ui & making sure that ships that can't attack when selected
                            # with those that can don't get an erroneus attack order.
    launchers = []    # weapon related values
    hardpoints = []
    
    def __init__(self, view, player, x, y):
        self.enginePoint2 = self.enginePoint1 = (x, y) # engine points. one needs to be initialised so it is...
        """
        Please note that enginePoints function like hardpoints, due to the nature of the flickerCircle effect.
        Ho hum. If a ship has more than three engines i'll code it as a list. or something.
        
        On S1s1 it's calcpointed as a point nearer the rear of the ship.
        """
        # and we create a FlickerCircle for it...
        # FlickerCircle.__init__(self, view, xyAsTuple, size, speed, colour):
        self.engineFlicker1 = effects.FlickerCircle(view, self.enginePoint1, 2.5, 0.25, misc.WHITE)
        self.engineFlicker2 = effects.FlickerCircle(view, self.enginePoint2, 2.5, 0.25, misc.WHITE)
        view.lowEffects.append(self.engineFlicker1)
        view.lowEffects.append(self.engineFlicker2)
        # this needs to have it's xy updated in calcpoints.
        Ship.__init__(self, view, player, x, y)
        
    def calcPoints(self):
    # HOLY COW!
        # starboard side
        # point 0: 0, 0 for this ship. Pointy.
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),\
        # point 1: 2.28 & 9.75   15 - 9.75 = 5.25
        (self.x + (self.radius-5.25) * math.sin(self.rotation + 2.3   * math.pi / 3), (self.y - (self.radius-5.25) * math.cos(self.rotation + 2.3   * math.pi / 3))),\
        # point 2: 2.67 @ 46 ...  = 3.5
        (self.x + (self.radius-3.5) * math.sin(self.rotation + 2.67 * math.pi / 3), (self.y - (self.radius-3.5) * math.cos(self.rotation + 2.67 * math.pi / 3))),\
            # Starboard side engine.
        # point 3: 2.6 & 17.5 ... 15 - 4.375  = 10.625 !!! minus four'd!
        (self.x + (self.radius-6.625) * math.sin(self.rotation + 2.6 * math.pi / 3), (self.y - (self.radius-6.625) * math.cos(self.rotation + 2.6 * math.pi / 3))),\
        # point 4: 2.79 ~ 2.8 & 14.0 ... 15 - 3.5 = 11.5  !!! minus four'd
        (self.x + (self.radius-7.5) * math.sin(self.rotation + 2.8 * math.pi / 3), (self.y - (self.radius-7.5) * math.cos(self.rotation + 2.8 * math.pi / 3))),\
            # begin tail assembly.
        # point 5: 2.87 & 49.5 ... 15 - 12.375 = 2.625
        (self.x + (self.radius-2.625) * math.sin(self.rotation + 2.87 * math.pi / 3), (self.y - (self.radius-2.625) * math.cos(self.rotation + 2.87 * math.pi / 3))),\
            # tail point.
        # point 6: 3 & radius.
        (self.x +  self.radius      * math.sin(self.rotation + 3   * math.pi / 3), (self.y -  self.radius      * math.cos(self.rotation + 3   * math.pi / 3))),\
            # final tail point.
        # point 7 equiv 5.
        (self.x + (self.radius-2.625) * math.sin(self.rotation + 3.13 * math.pi / 3), (self.y - (self.radius-2.625) * math.cos(self.rotation + 3.13 * math.pi / 3))),\
            # Portside engine.
        # point 8 equiv 4. !!! minus 4'd
        (self.x + (self.radius-7.5) * math.sin(self.rotation + 3.2 * math.pi / 3), (self.y - (self.radius-7.5) * math.cos(self.rotation + 3.2 * math.pi / 3))),\
        # point 9 equiv 3. !!! minus 4'd
        (self.x + (self.radius-6.625) * math.sin(self.rotation + 3.4 * math.pi / 3), (self.y - (self.radius-6.625) * math.cos(self.rotation + 3.4 * math.pi / 3))),\
            # Port side.
        # point 10 equiv 2.
        (self.x + (self.radius-3.5) * math.sin(self.rotation + 3.33 * math.pi / 3), (self.y - (self.radius-3.5) * math.cos(self.rotation + 3.33 * math.pi / 3))),\
        # point 11 equiv 1.
        (self.x + (self.radius-5.25) * math.sin(self.rotation + 3.7   * math.pi / 3), (self.y - (self.radius-5.25) * math.cos(self.rotation + 3.7   * math.pi / 3)))]
        self.needsToCalcPoints = False
    
    def calcExtras(self):
        self.hardpoints = [(self.x + (self.radius+2) * math.sin(self.rotation), (self.y - (self.radius+2) * math.cos(self.rotation)), self.rotation)]
        self.hardpoints.append((self.x + (self.radius+2) * math.sin(self.rotation + 2.3   * math.pi / 3), (self.y - (self.radius+2) * math.cos(self.rotation + 2.3   * math.pi / 3)), self.rotation + 2.3))
        self.hardpoints.append((self.x + (self.radius+2) * math.sin(self.rotation + 3.7   * math.pi / 3), (self.y - (self.radius+2) * math.cos(self.rotation + 3.7   * math.pi / 3)), self.rotation + 3.7))
        # engine point calcs. THESE NEED TO BE MOVED TO CALCPOINTS WHEN THEY'RE ONLY DRAWING WHEN ONSCREEN.
        # calculate the xy.
        self.enginePoint1 = ((self.x + (self.radius - 7)  * math.sin(self.rotation + 2.7 * math.pi / 3)), (self.y - (self.radius - 7) * math.cos(self.rotation + 2.7 * math.pi / 3)))
        self.enginePoint2 = ((self.x + (self.radius - 7)  * math.sin(self.rotation + 3.3 * math.pi / 3)), (self.y - (self.radius - 7) * math.cos(self.rotation + 3.3 * math.pi / 3)))
        # update the xy.
        if self.moving:
            self.engineFlicker1.xy = self.enginePoint1
            self.engineFlicker2.xy = self.enginePoint2
            self.engineFlicker1.visible = True
            self.engineFlicker2.visible = True
        else:
            self.engineFlicker1.visible = False
            self.engineFlicker2.visible = False
        i = 0
        for launcher in self.launchers:
            launcher.hardpoint = self.hardpoints[i]
            launcher.poll()
            i += 1
            
    def die(self):
        self.view.effects.append(effects.ExplosionShip(self.view, self, 10))
        self.view.effects.append(effects.Explosion(self.view, (self.x, self.y), 0.5, (self.radius * 4), misc.WHITE))
        #and remove the ship when done.
        self.remove()
        #any player related stats go here. like death count and such. Dunno if we want need these but hum.
        self.engineFlicker1.die()
        self.engineFlicker2.die()


class S1s6(Ship):
    """ Carrier """
    intEnginePoint = [0, 0]
    buildPoints = [(0,0),(0,0)]
    buildQueue = []
    building = False
    buildTimeRemaining = 0
    buildShip = Ship

    health = 40

    radius = 25

    rotateSpeed = 0.004
    speed = 0.1

    #buildInfo
    buildCost = 10
    buildTime = 1000
    
    availableToBuild = [S1s1]
        
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
            self.buildShip.orders = [orders.Idle(self)]
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

    def addToBuildQueue(self, ship): #Currently only produces triangles. only works on buildships.
        self.buildQueue.append(ship(self.view, self.player, self.buildPoints[0][0], self.buildPoints[0][1])) # Pete, you forgot the self. prefix
