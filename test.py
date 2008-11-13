#!/usr/bin/env python2.5

import peteship, players, ships, formations, random, orders, misc, effects, weapons, views, maps, pygame, psyco

try:
    import psyco
    psyco.full()
except ImportError:
    pass

GLOBAL_TESTSHIPS = 20 #Generic int for creating multiples of tsetingships.

map = maps.Map(1000, 1000, 500, 2) # 1000 x 1000 map with 500 resources and 2 players.
view = views.View(1024, 600, pygame.FULLSCREEN, map)

#player.ships.append(ships.S1s6(player, (player.width/2), (player.height/2)))
#player.ships[0].built = True

map.players[0].colour = misc.GREEN
map.players[1].colour = (150, 150, 255)

for player in map.players:
    for i in range(GLOBAL_TESTSHIPS): # GLOBAL_TESTSHIPS is located at the top, this is a pain to find sometimes.
        player.ships.append(ships.S1s1(view, player, (random.random()*map.width), (random.random()*map.height)))
        player.ships[len(player.ships) - 1].built = True
        player.ships[len(player.ships) - 1].launchers = [weapons.TestMissileLauncher(player.ships[len(player.ships) - 1], player.ships[len(player.ships) - 1].hardpoints[0])]
        #ships[i].order = MoveToXY(ships[i], 100.0, 100.0)

#for i in range(3):
#    map.players[1].ships.append(ships.S1s6(view, map.players[1], (random.random() * view.width), (random.random() * view.height)))
#    for j in range(100):
#        map.players[1].ships[i].addToBuildQueue()
for player in map.players:
    for ship in player.ships:
        ship.setOrder(orders.Attack(ship.player.enemyShipClosestToXY(ship.x, ship.y), 200))

#dave = map.players[0].ships[0]
#dave.colour = misc.GREEN
#dave.launchers = [weapons.TestMissileLauncher(dave, dave.hardpoints[0])]

"""
player.ships[0].setOrder(orders.MoveToXY(100.0, 100.0))
player.formations.append(formations.Formation(player.ships)) # updated in r109 to actually make it work ish.
"""
""""
#for i in range (10):
#    map.players[0].missiles.append(weapons.Missile(view, map.players[0], (random.random()*map.width, random.random()*map.height, random.random()*3), map.players[1].ships[3]))
"""
""" build test code """
#!Warning! ships[0] must be of class S1s6 or greater. !Warning!
#player.ships[0].addToBuildQueue()
#player.ships[0].addToBuildQueue()
#player.ships[0].addToBuildQueue()
#print ships[0].buildQueue
""" end build test code """

peteship.main(view, map) # run the game
