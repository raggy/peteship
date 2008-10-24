import misc, pygame
pygame.init()

class Player():
    """ Player specific stats. """
    colour = misc.WHITE # hahaha why not.
    name = "Ronco"
    resources = 9001 # MONEY, GET BACK.
    """ End of player specific stats """
    def __init__(self):
        self.width, self.height = 800, 480  # width of the screen, from left, and height of the screen, from top, in pixels.
        self.screen = pygame.display.set_mode((self.width, self.height)) # Initialise the pygame surface
        self.x = self.y = 0.0               # upper left position of the player's view
        self.zoom = 1.0                     # player's current zoom %
        self.selecting = False
        self.tBound = self.bBound = self.lBound = self.rBound = 0
        self.ships = self.selectedShips = []
        self.calcBounds()

    def calcBounds(self):
        self.tBound = self.y - 10 / self.zoom # 10 is the biggest radius so far, will replace when we have more ships.
        self.bBound = self.y + (self.height + 10) / self.zoom # same kinda thing
        self.lBound = self.x - 10 / self.zoom
        self.rBound = self.x + (self.width + 10) / self.zoom

    def focusOn(self, x, y):
        self.x = (x - (self.width / 2)) / player.zoom
        self.y = (y - (self.height / 2)) / player.zoom

    def xy(self): # Return x, y as a tuple
        return (x, y)

    def zoomBy(self, zoom):
        if self.zoom + zoom > 0.4:
            self.zoom += zoom
            self.panBy(((self.width / (self.zoom - zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom - zoom) - self.height / self.zoom) / 2))
            
    def panBy(self, x, y):
        if self.x + x < 0.0:
            self.x = 0.0
        else:
            self.x += x
        if self.y + y < 0.0:
            self.y = 0.0
        else:
            self.y += y
        self.calcBounds()