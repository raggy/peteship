import misc, math

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
                    self.ship.order = self.ship.nextOrder() # get next orders and
                self.ship.moveForward()          # cover the rest of the distance.
            else:
                self.ship.order = self.ship.nextOrder() # Get next orders

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
