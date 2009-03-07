#
#  Graphics.py
#  Peteship
#
#  Created by Pete Lord on 06/03/2009.
#  Copyright (c) 2009 Coventry University. All rights reserved.
#
import os, pygame

from OpenGL.GL import *
from OpenGL.GLU import *

class GraphicsHandler():

    def __init__(self):
        self.ships = []
        # VVV to be replaced with recursive stuff to load all images. VVV
        self.ships.append([pygame.image.load(os.path.join('Data', 'icon.png'))])    
        
        for list in self.ships:
            for surface in list:
                print surface
                textureData = pygame.image.tostring(surface, "RGBA", 1)
                print "1"
                glBindTexture(GL_TEXTURE_2D, 0)
                print "2"
                glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0,\
                              GL_RGBA, GL_UNSIGNED_BYTE, textureData )
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    