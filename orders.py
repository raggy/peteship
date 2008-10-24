import misc, math

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
        self.angleToXY = self.ship.angleToXY(self.x, self.y)
        
    def poll(self):
        """ rev12 : i like circles """
        #pygame.draw.circle(screen, midgreen, ((int(self.x * player.zoom) - player.x), (int(self.y) * player.zoom) - player.y), ship.radius - 3, 2) # circle designators for the move. Currently living above ships so needs to be changed.
        #pygame.draw.line(screen, (20,20,20), ((self.x - player.x) * player.zoom, (self.y - player.y) * player.zoom), ((ship.x  - player.x) * player.zoom, (ship.y - player.y) * player.zoom))
        # New behaviour, rotate whilst moving
        #if ship.distanceFrom(self.x, self.y) > math.sqrt(((ship.x + math.sin(ship.rotation) * ship.speed)-self.x)**2 + ((ship.y - math.cos(ship.rotation) * ship.speed)-self.y)**2): # If next move will bring you closer to the destination
        if (misc.normalisedAngle(self.angleToXY - self.ship.rotation) < (math.pi / 4) or misc.normalisedAngle(self.angleToXY - self.ship.rotation) > (math.pi * 1.75)) or (self.ship.moving):
            self.ship.moving = True
            if (self.ship.x, self.ship.y) != (self.x, self.y): # stop the ship on target
                if self.ship.distanceFrom(self.x, self.y) < self.ship.speed: # If the destintion is a shorter distance than the move distance...
                    self.ship.order = self.ship.nextOrder() # get next orders and
                self.ship.moveForward()          # cover the rest of the distance.
            else:
                self.ship.order = self.ship.nextOrder() # Get next orders
        
        if self.ship.rotation != self.angleToXY: # If the ship isn't already facing the right way
            self.angleToXY = self.ship.angleToXY(self.x, self.y)
            self.ship.rotateTowardAngle(self.angleToXY) # then rotate towards the right way
        # always recalculate points after moving. Rev 23: This is the source of the speedups slowdownsin ships. Calcpoints is part of the render loop.
