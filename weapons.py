import players, pygame, ships, orders, math, effects
from misc import *

class Missile(ships.Ship):
    # Super class for weapons that are launched and home in towards a target.
    # Quite specific but this covers the basics and is therefore useable.
    def __init__(self, view, player, launcher, targetShip):
        self.built = True # always built.
        self.moving = True # always moving, unless it's hit.
        self.view = view
        self.player = player
        self.launcher = launcher
        self.x = self.launcher.hardPoint[0]
        self.y = self.launcher.hardPoint[1]
        self.rotation = self.launcher.hardPoint[2]
        self.setOrder(orders.MoveToTarget(targetShip))
        # contrail stuff
        self.contrailLength = self.contrailTimer = 5 # frames before a new contrail is added.
        self.contrailLifetime = 100 # how long the trails last.
        # Number of contrails in use when moving = contrailLifetime / contrailLength (3000 / 300 = 10 for example.)
        self.contrailThickness = 2 # thickness passed to contrail. 
        #add an initial contrail.
        self.contrail = self.view.lowEffects.append(effects.Contrail(self.view, self)) # this'll make yer eyes bleed.
        
        # changing the look of missiles
        self.radius = 2
        self.shieldRadius = self.radius # hit detection radius.
        
        #basic stats in case this class is called.
        self.range = self.launcher.range 
        self.lifetime = self.launcher.lifetime
        self.speed = 3 # ninja fast.
        # those two stats are very much related, as the range determines how many *LOGICAL TICKS* the missile will live for.
        self.damage = 5 # half of S1s1 as of r 116

    def draw(self):
        #calculate a simple single line to show the missile. Default thing.
        if self.needsToCalcPoints:
            self.calcPoints()
        pygame.draw.aalines(self.view.screen, self.player.colour, False, self.offsetPoints())
        
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
            self.contrail = self.view.lowEffects.append(effects.Contrail(self.view, self)) # weyyy
        else:
            self.contrailTimer -= 1
        colliding = self.colliding()
        if not (not colliding):
            colliding.die()
            self.die()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.die()
            
    def select(self):
        pass
    
    def remove(self):
        self.dead = True
        for i in range(len(self.player.missiles)):
            if self.player.missiles[i] == self:
                del self.player.missiles[i]
                break
        for i in range(len(self.launcher.weapons)):
            if self.launcher.weapons[i] == self:
                del self.launcher.weapons[i]
                break
        del self

    def colliding(self):
        """ Function to check if missile is colliding with anything """
        for player in self.view.map.players:
            for ship in player.ships:
                if self.distanceFrom(ship.x, ship.y) <= ship.shieldRadius + self.shieldRadius:
                    return ship
        return False
        
class State():
    # superclass similar to Orders for ship, though weapons are a lot more simple.
    # acts by controlling the launcher.
    def __init__(self, launcher):
        self.launcher = launcher # no setShip in this, seemed a bit clunky/unused? makes more sense to me in the constructor
                                 # though there's always time to edit later.
    def poll(self):
        pass
    
    def getEnemyTarget(self):
        pass
        
    def getFriendlyTarget(self):
        pass
        
class Idle(State):
    # sit in place and fire at passing ships.
    def poll(self):
        # first of all see if we have a target. 
        if len(self.launcher.targets) == 0:
            # add the closest enemy ship to the launcher to it's target list.
            if self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]).distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) < self.launcher.range:
                self.launcher.addTarget(self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]))
        else: # we have a target
            if self.launcher.targets[0].distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) > self.launcher.range:
                self.launcher.targets = [] # if it's too far away then remove it, we'll find a new one.
            # otherwise the launcher will handle firing itself. Wey.
        
class Launcher(): # Superclass that handles the launching of weapons, wether they be point to point, missile, turret or otherwise.
    def __init__(self, parent, hardpoint):
        # uses parent to pull most of it's data out, but uses the hardpoint reference so we don't need to keep doing
        # self.parent.hardpoints[1].x or whatever.
        self.parent = parent
        self.hardpoint = hardpoint # What's here? x, y & rotation.
        
        self.isTurret = False # One of these three need to be set for things to work. Not the best way to do it
        self.isMissile = True # but probably most readable. (first weapon evar was a missile so that's why the default is missile.)
        self.isShot = False # pew pew
        
        # this way a ship just needs to call S1turret1 or whatever, and the turret can be changed in this file.
        self.state = Idle(self) # idle up
        self.targets = [] # list of targets
        self.weapons = [] # list of fired weapons.
        
        self.refire = 50 # time between firing.
        self.refireWait = self.refire
        self.range = 500
        self.lifetime = 600 # game ticks before the missile dies.
        
    def addTarget(self, object):
        self.targets.append([object])
    
    def setState(self, state):
        self.targets = []
        self.state = state
        
    def fire(self, target):
        self.weapons.append([Missile(self.parent.view, self.parent.player, target)])
        # any fx code goes here.
        
    def poll(self):
        self.state.poll() # update state.
        if self.refireWait == 0 and len(self.targets) > 0:
            fire(self.targets[0])
            self.refireWait = self.refire
        elif self.refireWait > 0:
            self.refireWait -= 1
            
class TestMissile(Missile):
    damage = 5
    speed = 3
        
class TestMissileLauncher(Launcher):
    isMissile = True
        
    def fire(self, target):
        self.weapons.append([TestMissile(self.parent.view, self.parent.player, target)])
        # any fx code goes here.
        