import players, pygame, ships, orders

class Missile(Ship):
    def __init__(self, hardPoint, targetShip):
        self.x = hardPoint[0]
        self.y = hardPoint[1]
        self.rotation = hardPoint[2]
        self.setOrder(orders.MoveToShip(targetShip))
        
        
    def draw(self):
        #calculate a simple single line to show the missile. Default thing.
        self.points = [(self.x + self.radius * math.sin(self.rotation), (self.y - self.radius * math.cos(self.rotation)),(self.x, self.y)]
        self.needsToCalcPoints = False
        
    def poll(self):
        self.orders[0].poll()
        self.calcExtras
        
    
