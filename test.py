#!/usr/bin/env python2.5

import peteship, players, ships, formations, random, orders, misc, effects, weapons

GLOBAL_TESTSHIPS = 10 #Generic int for creating multiples of tsetingships.
# misc contains GLOBAL_MAPWIDTH, GLOBAL_MAPHEIGHT. This should probably be moved to a map class at some point. But not today. Maybe monday morning. Pete. r70.

"""
ships = [S1s1(player, 100.0, 50.0), S1s2(player, 100.0, 100.0), S1s1(player, 150, 75)]
ships[0].rotation = math.radians(270)
ships[1].rotation = math.radians(269)
ships[0].order = MoveToXY(ships[0], 300.0, 50.0)
ships[1].order = MoveToXY(ships[1], 500.0, 100.0)
ships[2].order = MoveToXY(ships[2], 152.0, 75.0)
"""

player = players.Player()

for i in range(GLOBAL_TESTSHIPS): # GLOBAL_TESTSHIPS is located at the top, this is a pain to find sometimes.
    player.ships.append(ships.S1s1(player, (random.random()*player.width), (random.random()*player.height)))
    player.ships[i].built = True
#ships.append(S1s6(player, (player.width/2), (player.height/2)))
#ships[0].built = True
    #ships[i].order = MoveToXY(ships[i], 100.0, 100.0)

player.ships[0].setOrder(orders.MoveToXY(100.0, 100.0))
lollerLine = formations.Formation(player.ships)
lollerLine.calcAssignPattern()

player.ships.append(weapons.Missile(player, (300, 300, 1), player.ships[3]))

# Explosion test code. Woo!
#player.effects.append(effects.Explosion((200, 200), 0.5, 100, player, misc.EXPLOSIONRED))
#player.effects.append(effects.Explosion((20, 20), 0.5, 20, player, misc.EXPLOSIONRED))
#player.effects.append(effects.Explosion((204, 100), 0.5, 20, player, misc.EXPLOSIONRED))

""" build test code """
#!Warning! ships[0] must be of class S1s6 or greater. !Warning!
#player.ships[0].addToBuildQueue()
#ships[0].addToBuildQueue()
#print ships[0].buildQueue
""" end build test code """

#player.focusOn(ships[0].x, ships[0].y)

peteship.main(player, misc.GLOBAL_MAPWIDTH, misc.GLOBAL_MAPHEIGHT) # run the game