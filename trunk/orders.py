import misc, math, ships

class Order():
    def __init__(self):
        pass
    def xy(self):
        return False
    def setShip(self, ship):
        pass
    def poll(self):
        pass

class Idle(Order):
    # do nothing. 
    def poll(self):
        pass

class MoveToXY(Order):
    colour = (0, 50, 0) # Dark green
    
    def __init__(self, x, y):
        self.x, self.y = x, y

    def setShip(self, ship):
        self.ship = ship
        self.angleToXY = self.ship.angleToXY(self.x, self.y)

    def xy(self):
        return (self.x, self.y)

    def moveTowards(self, x, y):
        if (misc.normalisedAngle(self.angleToXY - self.ship.rotation) < (math.pi / 4) or misc.normalisedAngle(self.angleToXY - self.ship.rotation) > (math.pi * 1.75)) or (self.ship.moving):
            self.ship.moving = True
            if (self.ship.x, self.ship.y) != (x, y): # stop the ship on target
                if self.ship.distanceFrom(x, y) < self.ship.speed: # If the destintion is a shorter distance than the move distance...
                    self.ship.nextOrder() # get next orders and
                self.ship.moveForward()          # cover the rest of the distance.
            else:
                self.ship.nextOrder() # Get next orders

    def rotateTowards(self, x, y):
        if self.ship.rotation != self.angleToXY: # If the ship isn't already facing the right way
            self.angleToXY = self.ship.angleToXY(x, y)
            self.ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way
        
    def poll(self):
        self.moveTowards(self.x, self.y)
        self.rotateTowards(self.x, self.y)

class MoveToShip(MoveToXY):
    def __init__(self, ship):
        self.target = ship
        self.x, self.y = self.target.x, self.target.y

    def xy(self):
        return (self.target.x, self.target.y)

    def rotateTowards(self, x, y):
        if self.ship.rotation != self.angleToXY: # If the ship isn't already facing the right way
            self.ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way

    def poll(self):
        self.x, self.y = self.target.x, self.target.y
        self.moveTowards(self.x, self.y)
        self.angleToXY = self.ship.angleToXY(self.x, self.y)
        self.rotateTowards(self.x, self.y)

class MoveToTarget(MoveToShip):
    """
    Essentially like MoveToShip except that if
    target ship dies then it will move to the
    next nearest ship
    """

    def poll(self):
        if self.target.dead:
            self.target = self.ship.player.enemyShipClosestToXY(self.ship.x, self.ship.y) # Retarget
        self.x, self.y = self.target.x, self.target.y
        self.moveTowards(self.x, self.y)
        self.angleToXY = self.ship.angleToXY(self.x, self.y)
        self.rotateTowards(self.x, self.y)

class RotateToAngle(Order):
    def __init__(self, angle):
        self.angle = angle

    def setShip(self, ship):
        self.ship = ship

    def poll(self):
        if self.ship.rotation == self.angle: 
            self.ship.nextOrder()
        self.ship.rotateTowardAngle(self.angle)
        
class Attack(MoveToShip):
    """
    Ship moves within range and then circles target
    """
    
    colour = (50, 0, 0) # Dark red
    
    def __init__(self, target, range):
        self.target = target
        self.x, self.y = self.target.x, self.target.y
        self.range = range
        
    def poll(self):
        self.x, self.y = self.target.x, self.target.y
        if not self.target.dead: # If target isn't dead
            if self.ship.distanceFrom(self.target.x, self.target.y) > self.range: # If not yet within range
                self.moveTowards(self.x, self.y)                             # Move closer
                self.angleToXY = self.ship.angleToXY(self.x, self.y)
                self.rotateTowards(self.x, self.y)
            else:   # Else circle target
                self.ship.moveForward() # Always keep moving
    #            if self.ship.angleToXY(self.target.x, self.target.y) # check whether to turn left or right 
                self.ship.rotateTowardAngle(misc.normalisedAngle(self.ship.angleToXY(self.target.x, self.target.y) + math.pi / 2))
        else:
            self.ship.setOrder(Attack(self.ship.player.enemyShipClosestToXY(self.ship.x, self.ship.y), 30)) # Acquire new target
#            self.ship.nextOrder()
