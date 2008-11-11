import pygame, resources, random, misc, players, math

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
    
    def shipsAlongLine(self, startPoint, endPoint):
        """
        Function to check if a line passes through the radius of any ship.
        Returns a list of ships
        """
        tempShips = []
        
        offsetX = misc.positive(endPoint[0] - startPoint[0])
        offsetY = endPoint[1] - startPoint[1]
        distance = math.sqrt(offsetX ** 2 + offsetY ** 2)
        
        if offsetY > 0:
            theta = math.atan(offsetX / offsetY)
        elif offsetY == 0:
            theta = math.atan(offsetX)
        else:
            theta = misc.normalisedAngle(math.atan(offsetX / offsetY))
            
        for player in self.players:
            for ship in player.ships:
                if ship.distanceFrom(startPoint[0], startPoint[1]) - ship.radius <= distance: # If ship is within the radius
                    shipX = misc.positive(ship.x - startPoint[0])
                    shipY = ship.y - startPoint[1]
                    r = math.sqrt(shipX ** 2 + shipY ** 2)
                    if shipX > 0:
                        shipTheta = math.atan(shipX / shipY)
                    elif shipY == 0:
                        shipTheta = math.atan(shipX)
                    else:
                        shipTheta = misc.normalisedAngle(math.atan(shipX / shipY))
                    offsetTheta = misc.normalisedAngle(theta - shipTheta)
                    rotateX = r * math.cos(offsetTheta)
                    rotateY = r * math.sin(offsetTheta)
                    if rotateY + ship.radius >= 0 and rotateY - ship.radius <= 0 and ship.distanceFrom(endPoint[0], endPoint[1]) - ship.radius < distance: # If line passes through the ship
                        tempShips.append(ship) # Add ship to list
        return tempShips
        
    def closestShipsAlongLine(self, startPoint, endPoint):
        """
        Returns ships along line sorted by distance from startPoint
        """
        tempShips = self.shipsAlongLine(startPoint, endPoint)
        tempShips.sort(key=lambda ship: ship.distanceFrom(startPoint[0], startPoint[1]))
#        tempShips.reverse()
        return tempShips
