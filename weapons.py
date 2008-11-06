import players, pygame, ships, orders, math, effects
from misc import *

class Missile(ships.Ship):
    # Super class for weapons that are launched and home in towards a target.
    # Quite specific but this covers the basics and is therefore useable.
    def __init__(self, player, hardPoint, targetShip):
        self.built = True # always built.
        self.moving = True # always moving, unless it's hit.
        self.player = player
        self.x = hardPoint[0]
        self.y = hardPoint[1]
        self.rotation = hardPoint[2]
        self.setOrder(orders.MoveToTarget(targetShip))
        # contrail stuff
        self.contrailLength = self.contrailTimer = 5 # frames before a new contrail is added.
        self.contrailLifetime = 100 # how long the trails last.
        # Number of contrails in use when moving = contrailLifetime / contrailLength (3000 / 300 = 10 for example.)
        self.contrailThickness = 2 # thickness passed to contrail. 
        #add an initial contrail.
        self.contrail = self.player.lowEffects.append(effects.Contrail(self)) # this'll make yer eyes bleed.
        
        # changing the look of missiles.
        
        self.radius = 2
	self.shieldRadius = self.radius
       
    def draw(self):
        #calculate a simple single line to show the missile. Default thing.
        if self.needsToCalcPoints:
            self.calcPoints()
        pygame.draw.aalines(self.player.screen, self.player.colour, False, self.offsetPoints())
        
    def drawOrders(self):
	pass

    def calcPoints(self):
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation))),(self.x, self.y)]
        self.needsToCalcPoints = False
        
    def poll(self):
	self.orders[0].poll()
        self.calcExtras()
        if self.contrailTimer == 0:
            self.contrailTimer = self.contrailLength
            self.contrail = self.player.lowEffects.append(effects.Contrail(self)) # weyyy
        else:
            self.contrailTimer -= 1
	colliding = self.colliding()
	if not (not colliding):
	    colliding.die()
	    self.die()
            
    def select(self):
	pass
    
    def remove(self):
	self.dead = True
        for i in range(len(self.player.missiles)):
            if self.player.missiles[i] == self:
                del self.player.missiles[i]
                break
	del self

    def colliding(self):
	""" Function to check if missile is colliding with anything """
	for ship in self.player.ships:
	    if self.distanceFrom(ship.x, ship.y) <= ship.shieldRadius + self.shieldRadius:
		return ship
	return False