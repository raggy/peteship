import pygame, resources, random, misc, players

class StartPoint():
    def __init__(self, x, y):
        self.x, self.y = x, y #simple but makes code more readable. meh.
    def __call__(self):
        return (self.x, self.y)

class Map():
    resources = [] # list of each resource asteroid.
    players = []
    startPoints = []
    def __init__(self, width, height, resources, numberOfPlayers):
        self.width, self.height = width, height # defines the size of the map.
        self.area = width * height # for stars stuff an probably other stuff.
        self.resources = resources # for random generation this will be the total resources on the map.
        # also to be used for non random maps to determine the total resources and therefore resource levels. Yeah boy.
        # Petenote: Bear in mind that the size of an asteroid affects wether or not the asteroid will provide invisibility. Mkaing high resource maps a different style of play.
        for i in range(0, numberOfPlayers):
            startX = 50 # code to generate a starting point here.
            startY = 50 # likewise.
            self.startPoints.append(StartPoint(startX, startY)) # wey.
            self.players.append(players.Player(self, self.startPoints[i], 500)) # add some players. Needs modifications to Player() to take a start position.
    def addResource(self, x, y, amount, baseSize):
        self.resources.append(resources.Asteroid(x, y, amount, baseSize)) # just adds it to the map list so far.

    def addPlayerStart(self, x, y, player):
        pass # you know what this will do. Depends on how the start points are made.

    def shipClosestToXY(self, listOfShips, x, y):
        """
        Returns closest ship to x, y within listOfShips
        """
        closest = listOfShips[0]
        closestXY = listOfShips[0].distanceFrom(x, y)
        for ship in listOfShips[1:]:
            tempXY = ship.distanceFrom(x, y)
            if tempXY < closestXY:
                closest = ship
                closestXY = tempXY
        return closest

    def enemyShipClosestToXY(self, currentPlayer, x, y):
        """
        Returns closest enemy ship to x, y
        """
        listOfShips = []
        for player in self.players:
            if player != currentPlayer:
                listOfShips += player.ships
        return self.shipClosestToXY(listOfShips, x, y)