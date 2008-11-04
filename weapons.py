import players, pygame, ships, orders, math

class Missile(ships.Ship):
    def __init__(self, player, hardPoint, targetShip):
        self.built = True # always built.
        self.moving = True # always moving, unless it's hit.
        self.player = player
        self.x = hardPoint[0]
        self.y = hardPoint[1]
        self.rotation = hardPoint[2]
        self.setOrder(orders.MoveToShip(targetShip))
        
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
        self.calcExtras

    def select(self):
	pass