import pygame, resources, random, misc, players

class StartPoint():
    def __init(self, x, y):
        self.x, self.y = x, y #simple but makes code more readable. meh.

class Map():
    resources = [] # list of each resource asteroid.
    playerList = []
    startPoints = []
    def __init__(self, width, height, resources, numberOfPlayers):
        self.width, self.height = width, height # defines the size of the map.
        self.resources = resources # for random generation this will be the total resources on the map.
                # also to be used for non random maps to determine the total resources and therefore resource levels. Yeah boy.
                # Petenote: Bear in mind that the size of an asteroid affects wether or not the asteroid will provide invisibility. Mkaing high resource maps a different style of play.
                for i in range(0, numberOfPlayers):
                    startX = 0 # code to generate a starting point here.
                    startY = 0 # likewise.
                    self.startPoints.append(StartPoint(startX, startY)) # wey.
                    self.playerList.append(players.Player()) # add some players. Needs modifications to Player() to take a start position.
    def addResource(self, x, y, amount, baseSize):
        self.resources.append(resources.Asteroid(x, y, amount, baseSize)) # just adds it to the map list so far.

    def addPlayerStart(self, x, y, player):
        pass # you know what this will do. Depends on how the start points are made.
