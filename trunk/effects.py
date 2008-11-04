import pygame, players

# Module for effects within the game e.g. explosions

class Explosion():
    
    def __init__(self, xyAsTuple, size, length, player, colour):
        self.xy = xyAsTuple
        self.size = size # this is a multiplier, so should be done as such.
        self.lifetime = length
        self.player = player # to enable the explosion to draw itself
        self.colour = colour
        
    def poll(self):
        # Explosion() relies on peteship.py checking to see if each explosions lifetime == 0 and removing them before polling them.
        # for sake of some efficieny this code will probably live in peteship.py, but is included for usability in future.
        self.lifetime -= 1
        
    def draw(self):
        # draw a circle based on the lifetime of the explosion. So it shrinks. Cool.
        pygame.draw.circle(self.player.screen, self.colour, self.xy, self.lifetime * self.size)
