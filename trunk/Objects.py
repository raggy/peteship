#
#  Objects.py
#  TurnShip
#
#  Created by Pete Lord on 11/02/2009.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#
import Options, Misc, Angles

class Object():
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = Angles.Angle(r)
        
    def getLocation(self):
        return (x, y, z, r)
        
    def mod_x(self, amount):
        self.x += amount
    
    def mod_y(self, amount):
        self.y += amount
        
    def mod_z(self, amount):
        self.z += amount
        
    def mod_r(self, amount):
        self.r += amount
        
    def mod_all(self, x, y, z, r):
        self.x += x
        self.y += y
        self.z += z
        self.r += r