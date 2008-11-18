import pygame, pygame.draw, misc, random

try:
    import psyco
    psyco.full()
except ImportError:
    pass

class View:
    """ Defines functions to interact with the pygame surface """

    width, height = size = 0, 0
    x = y                = 0.0
    zoom                 = 1.0
    tBound = bBound = lBound = rBound = 0

    selecting =      False
    selectedShips = []
    shipsOnScreen = []

    stars = [] # list of all the stars. format (x, y, colour, depth)

    effects = []
    lowEffects = [] # Effects to be drawn underneath the ships
    
    drawStars = True # Are we drawing stars?
    drawContrails = True # drawing contrails or not? detail option.
    drawMiniMap = True # Are we displaying the minimap?

    def __init__(self, width, height, flags, map):
        self.width, self.height = width, height
        self.calcBounds()
        self.screen = pygame.display.set_mode((self.width, self.height), flags) # Initialise the pygame surface
        self.map = map
        self.minimap = MiniMap(self, self.map)
        self.panBy(0, 0)
        for i in xrange(self.map.area / 10000): # Generate a list of stars consisting of a tuple of (x, y, colour, depth)
            depth = random.random() * 0.5 + 0.5
            self.stars.append((random.random() * self.map.width / depth, random.random() * self.map.height / depth, (120 * depth, 120 * depth, 120 * depth), depth))

    def calcBounds(self):
        self.tBound = self.y - 10 # 10 is the biggest radius so far, will replace when we have more ships.
        self.bBound = self.y + 10 + self.height / self.zoom # same kinda thing
        self.lBound = self.x - 10
        self.rBound = self.x + 10 + self.width / self.zoom

    """def focusOn(self, x, y):
        self.x = (x - (self.width / 2)) / self.zoom
        self.y = (y - (self.height / 2)) / self.zoom
    """

    def xy(self):
        """
        Return x, y as a tuple
        """
        return (x, y)

    def zoomInBy(self, zoom):
        """
        Zoom in on the map by 'zoom'
        """
        self.zoom = self.zoom * zoom # Zoom in
        self.panBy(((self.width / (self.zoom / zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom / zoom) - self.height / self.zoom) / 2)) # Recentre the view

    def zoomOutBy(self, zoom):
        """
        Zoom out from the map by 'zoom'
        """
        self.zoom = self.zoom / zoom # Zoom out
        self.panBy(((self.width / (self.zoom * zoom) - self.width / self.zoom) / 2), ((self.height / (self.zoom * zoom) - self.height / self.zoom) / 2)) # Recentre the view
    
    def panBy(self, x, y):
        """
        Pan the view by x, y
        """
        if self.width / self.zoom > self.map.width:
            self.x = (self.map.width - (self.width / self.zoom)) / 2
        elif self.x + x < 0.0:
            self.x = 0.0
        elif self.x + x > self.map.width - self.width / self.zoom:
            self.x = self.map.width - self.width / self.zoom
        else:
            self.x += x
        if self.height / self.zoom > self.map.height:
            self.y = (self.map.height - (self.height / self.zoom)) / 2
        elif self.y + y < 0.0:
            self.y = 0.0
        elif self.y + y > self.map.height - self.height / self.zoom:
            self.y = self.map.height - self.height / self.zoom
        else:
            self.y += y
        self.calcBounds() # Call calcBounds() because the view changed
        
class Button:
    """
    class to create the inteface with
    """
    def __init__(self, view, rect):
        self.view = view
        self.shape = rect
        self.clicked = False
        
    def draw(self):
        #pygame.draw.rect
        pass

class MiniMap:

    def __init__(self, view, map):
        self.view = view
        self.map = map
        self.border = pygame.Rect(self.view.x, self.view.y, 10, 10) # Rectangle representing the screen
        self.boundary = pygame.Rect(self.view.width - 60, self.view.height - 50 * self.map.height / self.map.width - 10, 50, 50 * self.map.height / self.map.width) # Rectangle representing the map

    def update(self):
        """
        Updates the rectangle showing the view's screen borders
        """
        self.border.left = self.boundary.left + self.view.x / self.map.width * self.boundary.size[0]
        self.border.top = self.boundary.top + self.view.y / self.map.height * self.boundary.size[1]
        self.border.width = (self.view.width / self.view.zoom) / self.map.width * self.boundary.size[0]
        self.border.height = (self.view.height / self.view.zoom) / self.map.height * self.boundary.size[1]

    def resize(self, x, y):
        """
        Resizes the minimap by x, y
        """
        if self.boundary.width + x >= 5 and self.boundary.width + x <= self.view.width - 20 and self.boundary.height + y >= 5 and self.boundary.height + y <= self.view.height - 20:
            self.boundary.left -= x
            self.boundary.width += x        
            self.boundary.top -= y * self.map.height / self.map.width
            self.boundary.height += y * self.map.height / self.map.width
    
    def draw(self):
        """
        Draws the minimap to self.view.screen
        """
        pygame.draw.rect(self.view.screen, misc.BLACK, self.boundary, 0) # Black out the background of the minimap
        self.update()
        for player in self.map.players:
            for ship in player.ships:
                tempX = self.boundary.left + ship.x / self.map.width * self.boundary.size[0] # arbitrary amount. Represents map size.
                tempY = self.boundary.top + ship.y / self.map.height * self.boundary.size[1] # as above.
                pygame.draw.line(self.view.screen, player.colour, (tempX, tempY), (tempX, tempY))
        pygame.draw.rect(self.view.screen, misc.DARKGREY, self.border, 1)
        pygame.draw.rect(self.view.screen, misc.WHITE, self.boundary, 1) # Border the minimap. Drawn after that lot so that the border overwrites the view indicator.
