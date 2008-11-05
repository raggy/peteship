import players, pygame, ships, orders, math, effects

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
        self.setOrder(orders.MoveToShip(targetShip))
        # contrail stuff
        self.contrailLength = self.contrailTimer = 20 # frames before a new contrail is added.
        self.contrailLifetime = 100 # how long the trails last.
        # Number of contrails in use when moving = contrailLifetime / contrailLength (3000 / 300 = 10 for example.)
        self.contrailThickness = 1 # thickness passed to contrail. 
        #add an initial contrail.
        self.contrail = self.player.effects.append(effects.Contrail(self)) # this'll make yer eyes bleed.
       
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
            self.contrail = self.player.effects.append(effects.Contrail(self)) # weyyy
        else:
            self.contrailTimer -= 1
            
    def select(self):
	pass
