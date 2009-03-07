import pygame, misc, players

class Asteroid():
    def __init__(self, view, x, y, amount, baseSize):
        self.radius = amount + baseSize # cool idea no?
        self.x, self.y = x, y
        self.view = view
        # this section defines if a resource asteroid blocks radar.
        if self.radius > 500:
            self.blocksRadar = True
        else:
            self.blocksRadar = False

        self.amount = amount # how many units remaining?

        self.colour = misc.RESOURCEBROWN #mmmm mocha.

        self.si = self.radius # arbitrary health amount.

    def draw(self):
        pygame.draw.circle(self.view.screen, self.colour, (self.x, self.y), self.radius, 0) 

    def poll(self):
        if self.dead == False: #skips alot of stuff if the asteroid isn't going to change.
            if self.amount == 0:
                self.colour = misc.GREY
            else:
                self.radius = amount + baseSize

#Petenote: Resource cluster to come in a later rev with automatic random placements n shite.
