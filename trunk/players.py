import misc, pygame, random
pygame.init()

class Player():
    """ Player specific stats. """
    colour = misc.WHITE # hahaha why not.
    name = "Ronco"
    resources = 9001 # MONEY, GET BACK.
    """ End of player specific stats """
    # effects are lurking here for now. I'm not sure why.
    effects = []
    lowEffects = [] # Effects to be drawn underneath the ships
    
    # Star effects lurking here
    drawStars = True # Are we drawing stars?
    upperStars = [] # list of all the stars. format (x, y, colour)
    lowerStars = []
    
    # contrail specific.
    drawContrails = True # rev 100: is the player drawing contrails or not? detail option.
    
    # Minimap specific
    mmShow = True # Are we displaying the minimap?
    mmViewRect = pygame.Rect(0,0,0,0) # See below init.
    mmBoundaryRect = pygame.Rect(0,0,0,0) # 
    
    def __init__(self):
        self.width, self.height = 800, 480  # width of the screen, from left, and height of the screen, from top, in pixels.
        self.screen = pygame.display.set_mode((self.width, self.height)) # Initialise the pygame surface
        self.x = self.y = 0.0               # upper left position of the player's view
        self.zoom = 1.0                     # player's current zoom %
        self.selecting = False
        self.tBound = self.bBound = self.lBound = self.rBound = 0
        self.ships = []
	self.selectedShips = []
	self.missiles = []
        self.panBy(0.0, 0.0)
        self.calcBounds()

        #minimap init.
        self.mmViewRect = pygame.Rect(self.x, self.y, 10, 10) # Defines an area of the players view to use as the minimap.
        self.mmBoundaryRect = pygame.Rect(self.width - 60, self.height - 50 * misc.GLOBAL_MAPHEIGHT / misc.GLOBAL_MAPWIDTH - 10, 50, 50 * misc.GLOBAL_MAPHEIGHT / misc.GLOBAL_MAPWIDTH) # Defines the boundary of the map on the game screen.
        
        #Stars init.
        
        # This is going to assume a MINIMUM MAP WIDTH OR HEIGHT of 10. Woo.
        # First of all check if we're drawing stars.
        if self.drawStars:
            # create a set of stars using a tuple of (x, y, colour). We're using misc.GLOBAL_MAPHEIGHT instead of map at the moment.
            # In future revs when an instance of the Map class is passed to Player class this will need to be changed.
            for i in range(misc.GLOBAL_MAPAREA / 10000):
                self.upperStars.append([random.random()*misc.GLOBAL_MAPWIDTH, random.random()*misc.GLOBAL_MAPHEIGHT, (90, 90 ,90)]) #brighter upperstar
                self.lowerStars.append([random.random()*misc.GLOBAL_MAPWIDTH, random.random()*misc.GLOBAL_MAPHEIGHT, (50, 50, 50)]) #darker lowerstar
        #Stars are drawn in peteship.py, as the first draw.
                   
    def calcBounds(self):
        self.tBound = self.y - 10 # 10 is the biggest radius so far, will replace when we have more ships.
        self.bBound = self.y + 10 + self.height / self.zoom # same kinda thing
        self.lBound = self.x - 10
        self.rBound = self.x + 10 + self.width / self.zoom

    def focusOn(self, x, y):
        self.x = (x - (self.width / 2)) / player.zoom
        self.y = (y - (self.height / 2)) / player.zoom

    def xy(self): # Return x, y as a tuple
        return (x, y)

    def zoomInBy(self, zoom):
        self.zoom = self.zoom * zoom
        self.panBy(((self.width / (self.zoom / zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom / zoom) - self.height / self.zoom) / 2))

    def zoomOutBy(self, zoom):
        self.zoom = self.zoom / zoom
        self.panBy(((self.width / (self.zoom * zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom * zoom) - self.height / self.zoom) / 2))

    """ Depreciated, now use zoomInBy and zoomOutBy
    def zoomBy(self, zoom):
        if self.zoom + zoom > 0.05:
            self.zoom += zoom
            self.panBy(((self.width / (self.zoom - zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom - zoom) - self.height / self.zoom) / 2))
    """
    
    def panBy(self, x, y): # argghhhh
        if self.width / self.zoom > misc.GLOBAL_MAPWIDTH:
            self.x = (misc.GLOBAL_MAPWIDTH - (self.width / self.zoom)) / 2
        elif self.x + x < 0.0:
            self.x = 0.0
        elif self.x + x > misc.GLOBAL_MAPWIDTH - self.width / self.zoom:
            self.x = misc.GLOBAL_MAPWIDTH - self.width / self.zoom
        else:
            self.x += x
        if self.height / self.zoom > misc.GLOBAL_MAPHEIGHT:
            self.y = (misc.GLOBAL_MAPHEIGHT - (self.height / self.zoom)) / 2
        elif self.y + y < 0.0:
            self.y = 0.0
        elif self.y + y > misc.GLOBAL_MAPHEIGHT - self.height / self.zoom:
            self.y = misc.GLOBAL_MAPHEIGHT - self.height / self.zoom
        else:
            self.y += y
        self.calcBounds()

    def shipOnScreenAtXY(self, x, y):
        for ship in self.ships:
            if x >= (ship.x - ship.radius - self.x) * self.zoom and\
                        x <= (ship.x + ship.radius - self.x) * self.zoom and\
                        y >= (ship.y - ship.radius - self.y) * self.zoom and\
                        y <= (ship.y + ship.radius - self.y) * self.zoom:
                return ship
        return False

    def shipAtXY(self, x, y):
        for ship in self.ships:
            if x >= ship.x - ship.radius and\
                        x <= ship.x + ship.radius and\
                        y >= ship.y - ship.radius and\
                        y <= ship.y + ship.radius:
                return ship
        return False
        
    # Minimap code !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def updateMM(self):
        #Remember kids, the draw code for the mm is in the peteship.py file, under selection code! Last thing drawn before the flip, so it's over ships & other UI!
        self.mmViewRect.left = self.mmBoundaryRect.left + self.x / misc.GLOBAL_MAPWIDTH * self.mmBoundaryRect.size[0]
        self.mmViewRect.top = self.mmBoundaryRect.top + self.y / misc.GLOBAL_MAPHEIGHT * self.mmBoundaryRect.size[1]
        # Needs some code here to resize the rect to represent the player view.
        self.mmViewRect.width = (self.width / self.zoom) / misc.GLOBAL_MAPWIDTH * self.mmBoundaryRect.size[0]
        self.mmViewRect.height = (self.height / self.zoom) / misc.GLOBAL_MAPHEIGHT * self.mmBoundaryRect.size[1]

    def resizeMM(self, xChange, yChange):
        if self.mmBoundaryRect.width + xChange >= 5 and self.mmBoundaryRect.width + xChange <= self.width - 20 and self.mmBoundaryRect.height + yChange >= 5 and self.mmBoundaryRect.height + yChange <= self.height - 20:
            self.mmBoundaryRect.left -= xChange
            self.mmBoundaryRect.width += xChange        
            self.mmBoundaryRect.top -= yChange * misc.GLOBAL_MAPHEIGHT / misc.GLOBAL_MAPWIDTH
            self.mmBoundaryRect.height += yChange * misc.GLOBAL_MAPHEIGHT / misc.GLOBAL_MAPWIDTH
