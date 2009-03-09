#
#  Entities.py
#  TurnShip
#
#  Created by Pete Lord on 22/12/2008.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#
import pygame, os, Options, Views, Maps, Graphics
   
class EntityHandler():
    def __init__(self, fullscreen, map, player, number_of_players):
        self.player = player
        self.selected = None # selected ship.
        self.ships = []
        self.effects = []
        
        self.view = Views.GameView(fullscreen, self)
        self.graphics = Graphics.GraphicsHandler()
        self.map = Maps.Map(self, map)
                
    def updateMap(self):
        self.map.updateSurface()
        
    def select(self):
        pass
    
    def deselect(self):
        pass
        
# testing stuff.
        
# end testing.

# main stuff.

    def addEffect(self, lifeTime, x, y):
        self.effects.append(Effects.Effect(self, lifeTime, 0, x, y, 0))

    def addCloud(self, x, y, colour):
        self.clouds.append(Clouds.Cloud(self, x, y, colour))
        
    def draw(self):
        self.view.draw()
        
    def poll(self):
        for effect in self.effects:
            effect.poll()
            if effect.lifeTime == 0:
                self.effects.remove(effect)
