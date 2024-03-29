import players, pygame, ships, orders, math, effects
from misc import *

try:
    import psyco
    psyco.profile()
except ImportError:
    pass

class Beam():
    def __init__(self, thickness, changeTime, launcher, target):
        self.maxThickness = thickness
        self.thickness = 0
        self.maxTimer = changeTime
        self.timer = 0
        self.launcher = launcher
        self.target = target
        self.nextState = True
        self.state = False
    def poll(self):
        #check that we're in the correct state
        if self.state != self.nextState:
            # oh crikey, we need to change state...
            if self.state:
                # we were in on, need to turn off so:
                self.timer += 1
                self.thickness = self.maxThickness / (self.maxTimer - self.timer)
                if self.timer == self.maxTimer:
                    self.state = self.nextState
                    self.timer = 0
            else:
                # was off, needs to go on.
                self.timer += 1
                self.thickness = self.maxThicckness / (self.maxTimer - self.timer)
                if self.timer == self.maxTimer:
                    #hurray! we're there!
                    self.state = self.nextState
                    self.timer = 0
        
    def draw(self):
        pass
        
class Missile(ships.Ship):
    # Super class for weapons that are launched and home in towards a target.
    # Quite specific but this covers the basics and is therefore useable.
    def __init__(self, view, player, launcher, targetShip):
        self.built = True # always built.
        self.moving = True # always moving, unless it's hit.
        self.view = view
        self.player = player
        self.launcher = launcher
        self.x = self.launcher.hardpoint[0]
        self.y = self.launcher.hardpoint[1]
        self.rotation = self.launcher.hardpoint[2]
        self.setOrder(orders.MoveToTarget(targetShip))
        # contrail stuff
        self.contrailLength = self.contrailTimer = 5 # frames before a new contrail is added.
        self.contrailLifetime = 15 # how long the trails last.
        # Number of contrails in use when moving = contrailLifetime / contrailLength (3000 / 300 = 10 for example.)
        self.contrailThickness = 2 # thickness passed to contrail. 
        # changing the look of missiles.
        
        # this is currently set to a nice GREY.
#        self.engineGlow = effects.FlickerCircle(self.view, (self.x, self.y), 2, 0.25, GREY)
#        self.view.lowEffects.append(self.engineGlow) # ehhhgghsfkh
#        self.engineGlow.visible = True
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
        pygame.draw.lines(self.view.screen, self.player.colour, False, self.offsetPoints())
#        self.engineGlow.xy = (self.x, self.y) # update engine glow location
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
            colliding.damaged(self.damage, self)
            self.die()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.die()
 # particle contrails      
#         self.view.lowEffects.append(effects.StaticParticle(self.view, self.x, self.y, 20, (70, 70, 50)))
            
    def select(self):
        pass
    
    def remove(self):
        # remove engine glow
        # self.engineGlow.die() # OO method.
#        self.engineGlow.lifetime = 0 # non OO method.
        
        # other remove self stuff.
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
        
class AttackTarget(State):
    """ 
    actively attack only the targets in the list.
    """
    def poll(self):
        if self.launcher.isTurret: # turret code.
            pass
        elif self.launcher.isShot: # shot code.
            pass
        else: # missile code
            pass
        
class HoldFire(State):
    def poll(self):
        pass # do NOTHING.
        
class Idle(State):
    # sit in place and fire at passing ships.
    def poll(self):
        if self.launcher.isTurret: # code for turrets.
            pass # nothing yet.
            
        elif self.launcher.isShot: # code for shot weapons e.g. railgun, beam.
            """ hacked in missile fire code """
            # first of all see if we have a target. 
            if len(self.launcher.targets) == 0:
                # add the closest enemy ship to the launcher to it's target list.
                if self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]).distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) < self.launcher.range:
                    self.launcher.addTarget(self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]))
            else: # we have a target
                if self.launcher.targets[0].distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) > self.launcher.range or self.launcher.targets[0].dead == True:
                    self.launcher.targets = [] # if it's too far away or dead then remove it, we'll find a new one.
                # otherwise the launcher will handle firing itself. Wey.
                
        else: # code for missiles.
            # first of all see if we have a target. 
            if len(self.launcher.targets) == 0:
                # add the closest enemy ship to the launcher to it's target list.
                if self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]).distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) < self.launcher.range:
                    self.launcher.addTarget(self.launcher.parent.player.enemyShipClosestToXY(self.launcher.hardpoint[0], self.launcher.hardpoint[1]))
            else: # we have a target
                if self.launcher.targets[0].distanceFrom(self.launcher.hardpoint[0], self.launcher.hardpoint[1]) > self.launcher.range or self.launcher.targets[0].dead == True:
                    self.launcher.targets = [] # if it's too far away or dead then remove it, we'll find a new one.
                # otherwise the launcher will handle firing itself. Wey.
        
class Launcher(): # Superclass that handles the launching of weapons, wether they be point to point, missile, turret or otherwise.
    def __init__(self, parent, hardpoint):
        # uses parent to pull most of it's data out, but uses the hardpoint reference so we don't need to keep doing
        # self.parent.hardpoints[1].x or whatever.
        self.parent = parent
        self.hardpoint = hardpoint # What's here? x, y & rotation.
        
        self.isTurret = False # if neither of these are set, assumed to be a missile.
        self.isShot = False # pew pew
        
        # this way a ship just needs to call S1turret1 or whatever, and the turret can be changed in this file.
        self.state = Idle(self) # idle up
        self.targets = [] # list of targets
        self.weapons = [] # list of fired weapons.
        
        self.refire = 50 # time between firing.
        self.refireWait = self.refire
        self.range = 40
        self.lifetime = 60 # game ticks before the missile dies.
        
    def addTarget(self, object):
        self.targets.append(object)
    
    def setState(self, state):
        self.targets = []
        self.state = state
        
    def fire(self, target):
        self.parent.player.missiles.append(Missile(self.parent.view, self.parent.player, self, target))
        # any fx code goes here.
        
    def poll(self):
        self.state.poll() # update state.
        if self.refireWait == 0 and len(self.targets) > 0:
            self.fire(self.targets[0])
            self.refireWait = self.refire
        elif self.refireWait > 0:
            self.refireWait -= 1
            
class TestMissile(Missile):
    def __init__(self, view, player, launcher, targetShip):
        Missile.__init__(self, view, player, launcher, targetShip)
        self.damage = 1
        self.speed = 4
        self.rotateSpeed = 0.15
        self.contrailLength = self.contrailTimer = 2
        self.contrailLifetime = 8
        
                    #add an initial contrail. NESSECARY IN ALL MISSILE WEAPON
        self.contrail = self.view.lowEffects.append(effects.Contrail(self.view, self)) # this'll make yer eyes bleed.
        
class TestMissileLauncher(Launcher):
    def __init__(self, parent, hardpoint):
        Launcher.__init__(self, parent, hardpoint)
        self.range = 250
        self.lifetime = 90
        self.refire = 50 # time between firing.
        self.refireWait = self.refire
        
    def fire(self, target):
        self.parent.player.missiles.append(TestMissile(self.parent.view, self.parent.player, self, target))
        # any fx code goes here.
        
#class TestBeam(Beam):
        
class TestBeamGun(Launcher):
    isShot = True
    def __init__(self, parent, hardpoint):
        Launcher.__init__(self, parent, hardpoint)
        self.range = 150
        self.lifetime = 90
        self.refire = 10 # time between firing.
        self.refireWait = self.refire
    
    def fire(self, thickness, changeTime, launcher, target):
        pass
        
class TestCannon(Launcher):
    """ Shot weapons fake a weapon. They just do the damage and do a contrail. Simple. """
    isShot = True
    def __init__(self, parent, hardpoint):
        Launcher.__init__(self, parent, hardpoint)
        self.range = 150
        self.lifetime = 90
        self.damage = 2
        self.refireWait = self.refire = 40
        
    def fire(self, target):
        target.damaged(self.damage, self)
        # damage code.
        # fx code
        # hacked contrail. It technically starts at the enemy ship and draws to the launcher.
            #def __init__(self, view, start, end, lifeTime, thickness):
        self.parent.view.lowEffects.append(effects.ShotContrail(self.parent.view, self.hardpoint, (target.x, target.y), 50, 2))