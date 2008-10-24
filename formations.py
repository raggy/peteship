import peteship

class Formation:
    pattern = 0
    ships = []
    xys = []
    rotation = 0
    width = 20
    orders = [peteship.Idle()]
    def __init__(self, shipList, pattern=0, width = 20):
        self.ships = shipList
        self.pattern = pattern
        self.xys[0] = (self.ships[0].x, self.ships[0].y)
        self.rotation = self.ships[0].rotation
        self.orders = self.ships[0].orders
    
    def calcPattern(self):
        x = 0
        if pattern = 0 # line formation, left to right.
            for order in orders:
                
                if isinstance(order, peteship.MoveToXY):
            """        
            for i = range(1 to (len(self.ships) - 1):
                self.xys[i] = (self.x + (self.width * i) * math.sin(self.rotation + 3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3 * math.pi / 3)
            for i = range(0 to (len(self.ships) - 1):
                if isinstance(self.orders[0], peteship.MoveToXY)
                      self.ships[i].setOrder(
          """

            

    def poll(self): # if the orders change, this can be called to recalc nicely.
        calcPattern()
