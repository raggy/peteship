#
#  Angles.py
#  Peteship
#
#  Created by Pete Lord on 05/03/2009.
#  Copyright (c) 2009 Coventry University. All rights reserved.
#
import math, Misc

class Angle(float):

    def __init__(self, amount):
        float.__init__(self, amount % Misc.PIPI)
        
    def __add__(self, other):
        return Angle(float.__add__(self, other) % Misc.PIPI)

    def __sub__(self, other):
        return Angle(float.__sub__(self, other) % Misc.PIPI)
        
    def d(self):
        return math.degrees(self)

    def r(self):
        return self