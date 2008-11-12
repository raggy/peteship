import misc, pygame, random
pygame.init()

try:
    import psyco
    psyco.full()
except ImportError:
    pass

class Player():
    """ Player specific stats. """
    colour = misc.WHITE # hahaha why not.
    name = "Ronco"
    """ End of player specific stats """
    
    def __init__(self, map, startPoint, startingResources):
        self.map = map
        self.startX, self.startY = startPoint()
        self.resources = startingResources
        self.ships = []
        self.formations = []
        self.missiles = []

    def enemyShipClosestToXY(self, x, y):
        """
        Returns closest enemy ship to x, y
        """
        listOfShips = []
        for player in self.map.players:
            if player != self:
                listOfShips += player.ships
        return self.map.shipClosestToXY(listOfShips, x, y)

    """def shipOnScreenAtXY(self, x, y):
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
        return False"""
