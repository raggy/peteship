#
#  Maps.py
#  TurnShip
#
#  Created by Pete Lord on 30/12/2008.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#
import pygame, os, Options
        
class Map():
    def __init__(self, entities, mapfile):
        self.entities = entities # link to entities above it & therefore view.
        self.height = mapfile.HEIGHT 
        self.width = mapfile.WIDTH
        self.data = mapfile.DATA
        
        self.surface = pygame.Surface((self.width, self.height))
        self.update_surface()
    
    def update_surface(self):
        # stuff goes here.
        self.surface.convert()
                 
    def draw(self):
        self.parent.view.screen.blit(self.surface, (0, 0), self.entities.view.rect)