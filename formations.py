# -*- coding: utf-8 -*-
import peteship

class Formation:
    pattern = 0
    ships = []
    xys = []
    rotation = 0
    width = 20
    orders = []
    def __init__(self, shipList, pattern=0, width = 20):
        self.ships = shipList
        self.pattern = pattern
        self.xys[0] = (self.ships[0].x, self.ships[0].y)
        self.rotation = self.ships[0].rotation
        self.orders.append(self.ships[0].orders)
    
    def calcAssignPattern(self):
        for i in range(1, (len(self.ships) - 1)):
            self.ships.setOrder(peteship.Idle())
        tempXY = (0,0)
        if pattern == 0: # line formation, left to right.
            for order in orders:
                if isinstance(order, peteship.MoveToXY):
                    for i in range(1, (len(self.ships) - 1)):
                        tempXY = (self.x + (self.width * i) * math.sin(self.rotation + 3 * math.pi / 3), (self.y - self.radius * math.cos(self.rotation + 3 * math.pi / 3)))
                        self.ships[i].queueOrder(peteship.MoveToXY(tempXY[0],tempXY[1])) # set our ships move order.                                      
                else: # other orders go here. attacking etc.
                    print "Unrecognised order !!!Not move order. wtf!? we don't have any others!"
        else: # other formations
            print "No other patterns than 0, stop messing with the code without more formation!!!!"
            
    def poll(self): # if the orders change, this can be called to recalc nicely.
        calcAssignPattern()
