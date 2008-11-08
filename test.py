#!/usr/bin/env python2.5

import peteship, players, ships, formations, random, orders, misc, effects, weapons, views, maps

GLOBAL_TESTSHIPS = 10 #Generic int for creating multiples of tsetingships.

map = maps.Map(1000, 1000, 500, 2) # 1000 x 1000 map with 500 resources and 2 players.
view = views.View(800, 480, 0, map)

#player.ships.append(ships.S1s6(player, (player.width/2), (player.height/2)))
#player.ships[0].built = True

map.players[0].colour = misc.RED
map.players[1].colour = misc.BLUE

for player in map.players:
    for i in range(GLOBAL_TESTSHIPS): # GLOBAL_TESTSHIPS is located at the top, this is a pain to find sometimes.
        player.ships.append(ships.S1s1(view, player, (random.random()*view.width), (random.random()*view.height)))
        player.ships[len(player.ships) - 1].built = True
        #ships[i].order = MoveToXY(ships[i], 100.0, 100.0)
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
