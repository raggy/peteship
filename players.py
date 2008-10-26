import misc, pygame
pygame.init()

class Player():
    """ Player specific stats. """
    colour = misc.WHITE # hahaha why not.
    name = "Ronco"
    resources = 9001 # MONEY, GET BACK.
    """ End of player specific stats """
    # Minimap stats
    mmShow = True # Are we displaying the minimap?
    mmViewRect = pygame.Rect(0,0,0,0) # See below init.
    mmBoundaryRect = pygame.Rect(0,0,0,0) # " " "
    def __init__(self):
        self.width, self.height = 400, 400  # width of the screen, from left, and height of the screen, from top, in pixels.
        self.screen = pygame.display.set_mode((self.width, self.height)) # Initialise the pygame surface
        self.x = self.y = 0.0               # upper left position of the player's view
        self.zoom = 1.0                     # player's current zoom %
        self.selecting = False
        self.tBound = self.bBound = self.lBound = self.rBound = 0
        self.ships = self.selectedShips = []
        self.calcBounds()

        #minimap init.
        self.mmViewRect = pygame.Rect(self.x, self.y, 10, 10) # Defines an area of the players view to use as the minimap.
        self.mmBoundaryRect = pygame.Rect(self.width - 60, self.height - 60, 50, 50) # Defines the boundary of the map on the game screen.

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
            
    def panBy(self, x, y): # argghhhh
        if self.x + x < 0.0:
            self.x = 0.0
        elif self.x + x > misc.GLOBAL_MAPWIDTH - self.width:
            self.x = misc.GLOBAL_MAPWIDTH - self.width
        else:
            self.x += x
        if self.y + y < 0.0:
            self.y = 0.0
        elif self.y + y > misc.GLOBAL_MAPHEIGHT - self.height:
            self.y = misc.GLOBAL_MAPHEIGHT - self.height
        else:
            self.y += y
        self.calcBounds()

    # Minimap code !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def updateMM(self):
        #Remember kids, the draw code for the mm is in the peteship.py file, under selection code! Last thing drawn before the flip, so it's over ships & other UI!
        self.mmViewRect.left = self.mmBoundaryRect.left + self.x / misc.GLOBAL_MAPWIDTH * self.mmBoundaryRect.size[0]
        self.mmViewRect.top = self.mmBoundaryRect.top + self.y / misc.GLOBAL_MAPHEIGHT * self.mmBoundaryRect.size[1]
        # Needs some code here to resize the rect to represent the player view.
        self.mmViewRect.width = ((misc.GLOBAL_MAPWIDTH - self.width) / misc.GLOBAL_MAPWIDTH) * self.mmBoundaryRect.size[0] 
        self.mmViewRect.height = self.height / self.mmBoundaryRect.size[1]

    def resizeMM(self, xChange, yChange):
        self.mmBoundaryRect.left -= xChange
        self.mmBoundaryRect.width += xChange
        self.mmBoundaryRect.top -= yChange
        self.mmBoundaryRect.height += yChange
        self.updateMM()




