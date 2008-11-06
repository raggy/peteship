# -*- coding: utf-8 -*-

import orders, math

class Formation:
    pattern = 0
    rotation = 0
    width = 20
    def __init__(self, shipList, pattern = 0, width = 20):
        self.ships = shipList
        self.pattern = pattern
        self.rotation = self.ships[0].rotation
        self.orders = self.ships[0].orders       
    
    def calcAssignPattern(self):
        for ship in self.ships[1:]:
            ship.setOrder(orders.Idle())
        tempXY = (0,0)
        if self.pattern == 0: # line formation, left to right.
            for order in self.orders:
                if isinstance(order, orders.MoveToXY):
                    self.xys = [(self.ships[0].orders[0].x, self.ships[0].orders[0].y)]
                    i = 0
                    for ship in self.ships[1:]:
                        i += 1
                        ship.queueOrder(orders.MoveToXY(self.ships[0].orders[0].x + (self.width * i) * math.sin(self.rotation + 3 * math.pi / 3), (self.ships[0].orders[0].y - self.ships[0].radius * math.cos(self.rotation + 3 * math.pi / 3)))) # set our ships move order.                                      
                else: # other orders go here. attacking etc.
                    print "Unrecognised order !!!Not move order. wtf!? we don't have any others!"
        else: # other formations
            print "No other patterns than 0, stop messing with the code without more formation!!!!"
            
    def poll(self): # if the orders change, this can be called to recalc nicely.
        self.calcAssignPattern()
