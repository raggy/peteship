import pygame, random, math

# Module for effects within the game e.g. explosions

class Effect():
    
    def __init__(self):
        pass
        
    def poll(self):
        pass
        
    def draw(self):
        pass
    
    def remove(self):
        for i in range(len(self.view.effects)):
            if self.view.effects[i] == self:
                del self.view.effects[i]
                break

class Explosion(Effect):
    
    def __init__(self, view, xyAsTuple, size, length, colour):
        self.xy = xyAsTuple
        self.size = size # this is a multiplier, so should be done as such.
        self.lifetime = length
        self.view = view # to enable the explosion to draw itself
        self.colour = colour
        self.backColour = (colour[0] / 2, colour[1] / 2, colour[2] / 2)
        
    def poll(self):
        # Explosion() relies on peteship.py checking to see if each explosions lifetime == 0 and removing them before polling them.
        # for sake of some efficieny this code will probably live in peteship.py, but is included for usability in future.
        self.lifetime -= 1
        
    def draw(self):
        # draw a circle based on the lifetime of the explosion. So it shrinks. Cool.
        tempSize = self.lifetime * self.size # less cycles.
        if tempSize * self.view.zoom >= 1:
            pygame.draw.circle(self.view.screen, self.colour, ((self.xy[0] - self.view.x) * self.view.zoom, (self.xy[1] - self.view.y) * self.view.zoom), tempSize * self.view.zoom, 1) # alter the last value for thicker rings.
        
class Particle():
    
    def __init__(self, view, rotation, x, y, lifetime):
        self.view = view
        self.rotation = rotation
        self.x = x
        self.y = y
        self.maxlife = self.lifetime = lifetime #lollercaust
        
    def poll(self):
        self.y -= math.cos(self.rotation) * 0.4
        self.x += math.sin(self.rotation) * 0.4
        self.colour = ((255 * self.lifetime / self.maxlife),\
                       (255 * self.lifetime / self.maxlife),\
                       (255 * self.lifetime / self.maxlife))    # kept seperate so that different coloured particles can be made.
                       
        self.lifetime -= 1
        
    def draw(self):
        pygame.draw.line(self.view.screen, self.colour, ((self.x - self.view.x) * self.view.zoom, (self.y - self.view.y) * self.view.zoom), ((self.x - self.view.x) * self.view.zoom, (self.y - self.view.y) * self.view.zoom))
        
        
class ExplosionShip(Effect):
    
    particles = []
    lifetime = 500 # how long the particle lasts
    colour = (255, 255, 255) #white powe... particle!
        
    def __init__(self, view, ship):
        self.particles = []
        self.view      = view
        for i in range(10):
            self.particles.append(Particle(self.view, (random.random() * math.pi * 2), ((random.random() * 2) - 1) * ship.radius + ship.x, ((random.random() * 2) - 1) * ship.radius + ship.y, self.lifetime))
    def poll(self):
        for particle in self.particles:
            particle.poll()
        self.lifetime -= 1
            
    def draw(self):
        for particle in self.particles:
            particle.draw()
            
class Contrail(Effect):
    # putting this in each weapon made no sense as contrails would dissapear when the projectile hit (maybe desireable ?)
    def __init__(self, view, parent):
        self.parent = parent #woooooo
        
        self.x1 = parent.x # !!! x1 & y1 constitue the startPoint, while x2 & y2 constitue the endPoint.
        self.y1 = parent.y
        
        self.x2 = parent.x
        self.y2 = parent.y
        

        self.maxlife = self.lifetime = parent.contrailLifetime
        self.thickness = parent.contrailThickness
        #self.colour = colour    # do we need specific colours for view contrails? hmm...
        self.view = view
        self.updateStartPoint = True # do we need to move the startPoint? be obvious in calcExtras
        
    def poll(self):
        self.lifetime -= 1
        self.colour = ((75 * self.lifetime / self.maxlife),\
                       (75 * self.lifetime / self.maxlife),\
                       (75 * self.lifetime / self.maxlife))
        if self.updateStartPoint:
            self.x1 = self.parent.x
            self.y1 = self.parent.y
        
        if self.parent.contrailTimer == 0:
            self.updateStartPoint = False
                       
    def draw(self): 
        pygame.draw.line(self.view.screen, self.colour, ((self.x1 - self.view.x) * self.view.zoom, (self.y1 - self.view.y) * self.view.zoom), ((self.x2 - self.view.x) * self.view.zoom, (self.y2 -self.view.y) * self.view.zoom), self.thickness)

    def remove(self):
        for i in range(len(self.view.lowEffects)):
            if self.view.lowEffects[i] == self:
                del self.view.lowEffects[i]
                break