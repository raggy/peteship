import pygame, random, math, misc

try:
    import psyco
    psyco.full()
except ImportError:
    pass


# Module for effects within the game e.g. explosions

class Effect():
    
    def __init__(self):
        pass
        
    def poll(self):
        pass
        
    def draw(self):
        pass
    
    def remove(self):
#    if self in self.view.effects:
        for i in range(len(self.view.effects)):
            if self.view.effects[i] == self:
                del self.view.effects[i]
                break
#    elif self in self.view.lowEffects:
        for i in range(len(self.view.lowEffects)):
            if self.view.lowEffects[i] == self:
                del self.view.lowEffects[i]
                break
                
class AngleShield(Effect):
    def __init__(self, parent, view, xyAsTuple, radius, lifetimeMod, hitBy):
        self.parent = parent #ship that got hit.
        self.view = view #for drawing.
        self.xy = xyAsTuple #xy of the shield. set the same as the parent.
        self.radius = radius # yeap. not used. will tweak out later.
        self.maxLifetime = self.lifetime = 25 + lifetimeMod # lifetime of the shield.
        self.maxColour = (150, 150, 150)
        self.hitBy = hitBy # what were we hit by? Where the heck is it? Pointer to the weapon that hit the parent

        self.baseAngle = self.angleToXY(self.hitBy.x, self.hitBy.y) # middle of the arc. This is the angle to the weapon that hit the parent.
        """ debug 
        print self.baseAngle 
        print self.parent.x, self.parent.y
        print self.hitBy.x, self.hitBy.y
        """
        self.startAngle = misc.normalisedAngle(self.baseAngle - 0.5) # make it an arc. Checkout pygame.draw.arc (google: pygame draw)
        self.endAngle = misc.normalisedAngle(self.baseAngle + 0.5)
 
        del self.hitBy # remove the hitBy reference so we on't clog up the memory.

    def angleToXY(self, v1, v2):
        #calculate the angle from the referenced ships x, y to the
        #given x,y point.
       
        #cheers ben! This one is specific to angle shield though.
        if self.xy[1] - y > 0:
            return misc.normalisedAngle(math.atan((self.xy[0]-x)/(y-self.xy[1])))
        elif self.xy[1] - y == 0:
            return misc.normalisedAngle(-math.atan(self.xy[0]-x))
        else:
            return misc.normalisedAngle(math.atan((self.xy[0]-x)/(y-self.xy[1]))+math.pi)
        
    def poll(self):
        self.lifetime -= 1
        self.xy = (self.parent.x, self.parent.y) # stick to the ship.
        
    def draw(self):
        if self.radius * self.view.zoom >= 2:
            self.colour = [(self.maxColour[0] / self.maxLifetime * self.lifetime),\
                           (self.maxColour[1] / self.maxLifetime * self.lifetime),\
                           (self.maxColour[2] / self.maxLifetime * self.lifetime)]
            # old bubbleshield draw. testing purposes.
#            pygame.draw.circle(self.view.screen, self.colour, ((self.xy[0] - self.view.x) * self.view.zoom, (self.xy[1] - self.view.y) * self.view.zoom), self.radius * self.view.zoom, 1)
            pygame.draw.arc(self.view.screen, self.colour,\
            # rectangle code. needs to be defined so it knows where to draw the arc. fassen rassen pygame. heh. we love you pygame!
            # to see why, google: pygame draw
            pygame.Rect(\
            ((self.parent.x - self.parent.shieldRadius) - self.view.x) * self.view.zoom,\
            ((self.parent.y - self.parent.shieldRadius) - self.view.y) * self.view.zoom,\
            (self.parent.shieldRadius * 2) * self.view.zoom,\

            (self.parent.shieldRadius * 2) * self.view.zoom),\
            self.startAngle, self.endAngle, 1) # last value width.
                
class BubbleShield(Effect):
    def __init__(self, parent, view, xyAsTuple, radius, lifetimeMod):
    # lifetime is set here, change it if you want.
        self.parent = parent
        self.view = view
        self.xy = xyAsTuple
        self.radius = radius
        self.maxLifetime = self.lifetime = 15 + lifetimeMod
        self.maxColour = (150, 150, 150)
        
    def poll(self):
        self.lifetime -= 1
        self.xy = (self.parent.x, self.parent.y)
        
    def draw(self):
        if self.radius * self.view.zoom >= 2:
            self.colour = [(self.maxColour[0] / self.maxLifetime * self.lifetime),\
                           (self.maxColour[1] / self.maxLifetime * self.lifetime),\
                           (self.maxColour[2] / self.maxLifetime * self.lifetime)]
            #self.colour = (200, 200, 200)
            pygame.draw.circle(self.view.screen, self.colour, ((self.xy[0] - self.view.x) * self.view.zoom, (self.xy[1] - self.view.y) * self.view.zoom), self.radius * self.view.zoom, 1)
            
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
            
class FlickerCircle(Effect):
    def __init__(self, view, xyAsTuple, size, speed, colour):
        """
        class that draws a flickery circle. designed to be inited and then activated / deactivated. e.g. engines, beams.
        minimum size == 1 i guess. 2 is best.
        best speed is probably 1.
        """
        self.visible = False # ships aren't moving by default. etc.
        self.view = view
        self.xy = xyAsTuple
        self.maxSize = size
        self.size = self.minSize = size / 2 # start small, else it'll just get smallized.
        self.speed = speed
        self.colour = colour
        self.lifetime = 1 # so that the effect can be removed on death easily.
        self.wakeTimer = 10
        self.wake = []
        
    def poll(self):
# every 5 frames. see waketimer.
        if self.visible:
            if self.wakeTimer == 0:
                self.wake.append(StaticBlockParticle(self.view, 1, self.xy[0], self.xy[1], 50, (150, 150, 150)))
                self.view.lowEffects.append(self.wake[len(self.wake) - 1])
                self.wakeTimer = 10
            else:
                self.wakeTimer -= 1
        # flicker size between the min & max. 
            if self.size >= self.maxSize:
                self.size = self.minSize
            else:
                self.size += self.speed # see what i did thar?
            # yes uber high speeds can go over the max size. but ho hum, don't do it. Doesn't need foolproofing
            
    def draw(self):
        if self.visible: # allows the flicker to be turned off.
            if self.size * self.view.zoom >= 1: 
                 pygame.draw.circle(self.view.screen, self.colour, ((self.xy[0] - self.view.x) * self.view.zoom, (self.xy[1] - self.view.y) * self.view.zoom), self.size * self.view.zoom, 1) # set to filled so it looks like that. can be changed. Meh.
                 
    def die(self):
        self.lifetime = 0 # effects loop will remove the effect itself. 
        # other code to tell it to ramp down can be added here and probably should be eventually.
            
        
class Particle(Effect):
    
    def __init__(self, view, rotation, x, y, lifetime, colour = (255, 255, 255)):
        self.view = view
        self.rotation = rotation
        self.x = x
        self.y = y
        self.maxlife = lifetime
        self.lifetime = lifetime #lollercaust
        self.maxColour = colour
        
    def poll(self):
        self.y -= math.cos(self.rotation) * 0.4
        self.x += math.sin(self.rotation) * 0.4
        self.colour = [(self.maxColour[0] * self.lifetime / self.maxlife),\
                       (self.maxColour[1] * self.lifetime / self.maxlife),\
                       (self.maxColour[2] * self.lifetime / self.maxlife)]    # kept seperate so that different coloured particles can be made.
        self.tempColour = [self.colour[0] * self.view.zoom, self.colour[1] * self.view.zoom, self.colour[2] * self.view.zoom]
        if self.tempColour[0] < self.colour[0]:
            self.colour = self.tempColour
                       
        self.lifetime -= 1
        
    def draw(self):
        if self.x >= self.view.x and\
        self.x <= self.view.x + self.view.width / self.view.zoom and\
        self.y >= self.view.y and\
        self.y <= self.view.y + self.view.height / self.view.zoom: # If particle is on screen
            pygame.draw.line(self.view.screen, self.colour, ((self.x - self.view.x) * self.view.zoom, (self.y - self.view.y) * self.view.zoom), ((self.x - self.view.x) * self.view.zoom, (self.y - self.view.y) * self.view.zoom)) # Draw it
            
class BlockParticle(Particle):
    
    def __init__(self, view, size, rotation, x, y, lifetime, colour = (255, 255, 255)):
        self.view = view
        self.rotation = rotation
        self.x = x
        self.y = y
        self.size = size
        self.size2 = self.size * 2
        self.maxlife = self.lifetime = lifetime #lollercaust 
        self.maxColour = colour
        
    def poll(self):
        self.y -= math.cos(self.rotation) * 0.4
        self.x += math.sin(self.rotation) * 0.4
        self.colour = [(self.maxColour[0] * self.lifetime / self.maxlife),\
                       (self.maxColour[1] * self.lifetime / self.maxlife),\
                       (self.maxColour[2] * self.lifetime / self.maxlife)]    # kept seperate so that different coloured particles can be made.
        self.tempColour = [self.colour[0] * self.view.zoom, self.colour[1] * self.view.zoom, self.colour[2] * self.view.zoom]
        if self.tempColour[0] < self.colour[0]:
            self.colour = self.tempColour
                       
        self.lifetime -= 1
        
    def draw(self):
        if self.x >= self.view.x and\
        self.x <= self.view.x + self.view.width / self.view.zoom and\
        self.y >= self.view.y and\
        self.y <= self.view.y + self.view.height / self.view.zoom: # If particle is on screen
            # dot draw code.
            if self.size2 * self.view.zoom < 2:
                self.view.screen.set_at(((self.x - self.view.x) * self.view.zoom, (self.y -self.view.y) * self.view.zoom), self.colour)
            else:
                self.square = pygame.Rect(((self.x - self.size) - self.view.x) * self.view.zoom, ((self.y - self.size) - self.view.y) * self.view.zoom, self.size2 * self.view.zoom, self.size2 * self.view.zoom)
                pygame.draw.rect(self.view.screen, self.colour, self.square, 0)
        
class StaticParticle(Particle):
    
    def __init__(self, view, x, y, lifetime, colour = (255, 255, 255)):
        self.view = view
        self.x, self.y = x, y
        self.maxlife = self.lifetime = lifetime
        self.maxColour = colour
        
    def poll(self):
        self.colour = [(self.maxColour[0] * self.lifetime / self.maxlife),\
                       (self.maxColour[1] * self.lifetime / self.maxlife),\
                       (self.maxColour[2] * self.lifetime / self.maxlife)]    # kept seperate so that different coloured can be made.
        self.tempColour = [self.colour[0] * self.view.zoom, self.colour[1] * self.view.zoom, self.colour[2] * self.view.zoom]
        if self.tempColour[0] < self.colour[0]:
            self.colour = self.tempColour
                       
        self.lifetime -= 1
        
class StaticBlockParticle(StaticParticle):
    # broken atm?
    def __init__(self, view, size, x, y, lifetime, colour = (255, 255, 255)):
        self.view = view
        self.x = x
        self.y = y
        self.size = size
        self.size2 = self.size * 2  
        self.maxlife = self.lifetime = lifetime #lollercaust 
        self.maxColour = colour
        
    def draw(self):
        if self.x >= self.view.x and\
        self.x <= self.view.x + self.view.width / self.view.zoom and\
        self.y >= self.view.y and\
        self.y <= self.view.y + self.view.height / self.view.zoom: # If particle is on screen
            # dot draw code.
            if self.size2 * self.view.zoom < 2:
                self.view.screen.set_at(((self.x - self.view.x) * self.view.zoom, (self.y -self.view.y) * self.view.zoom), self.colour)
            else:
                self.square = pygame.Rect(((self.x - self.size) - self.view.x) * self.view.zoom, ((self.y - self.size) - self.view.y) * self.view.zoom, self.size2 * self.view.zoom, self.size2 * self.view.zoom)
                pygame.draw.rect(self.view.screen, self.colour, self.square, 0)
        
class ExplosionShip(Effect):
    
    particles = []
    lifetime = 50 # how long the particle lasts
    colour = (255, 255, 255) #white powe... particle!
        
    def __init__(self, view, ship, particles):
        self.particles = []
        self.view      = view
        for i in range(particles):
            randomColour = random.random() * 255
            self.particles.append(BlockParticle(self.view, 0.5, (random.random() * math.pi * 2), ((random.random() * 2) - 1) * ship.radius + ship.x, ((random.random() * 2) - 1) * ship.radius + ship.y, self.lifetime, (randomColour, randomColour, randomColour))) #(random.random() * 255, random.random() * 255, random.random() * 255)))
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
        self.tempColour = [self.colour[0] * self.view.zoom, self.colour[1] * self.view.zoom, self.colour[2] * self.view.zoom]
        if self.tempColour[0] < self.colour[0]:
            self.colour = self.tempColour

        if self.updateStartPoint:
            self.x1 = self.parent.x
            self.y1 = self.parent.y
        
        if self.parent.contrailTimer == 0:
            self.updateStartPoint = False
                       
    def draw(self):
        if (self.x1 >= self.view.x\
        and self.x1 <= self.view.x + self.view.width / self.view.zoom\
        and self.y1 >= self.view.y\
        and self.y1 <= self.view.y + self.view.height / self.view.zoom)\
        or (self.x2 >= self.view.x\
        and self.x2 <= self.view.x + self.view.width / self.view.zoom\
        and self.y2 >= self.view.y\
        and self.y2 <= self.view.y + self.view.height / self.view.zoom): # If both points are on screen
            self.tempThickness = self.thickness * self.view.zoom
            if self.tempThickness > self.thickness:
                self.tempThickness = self.thickness
            elif self.tempThickness < 1:
                self.tempThickness = 1
            pygame.draw.line(self.view.screen, self.colour, ((self.x1 - self.view.x) * self.view.zoom, (self.y1 - self.view.y) * self.view.zoom), ((self.x2 - self.view.x) * self.view.zoom, (self.y2 -self.view.y) * self.view.zoom), self.tempThickness)

    def remove(self):
        for i in range(len(self.view.lowEffects)):
            if self.view.lowEffects[i] == self:
                del self.view.lowEffects[i]
                break
