#!/usr/bin/env python2.5

import peteship, players, ships, formations, random, orders, misc, effects, weapons, views, maps, pygame, psyco

try:
    import psyco
    psyco.full()
except ImportError:
    pass

GLOBAL_TESTSHIPS = 20 #Generic int for creating multiples of tsetingships.

map = maps.Map(1000, 1000, 500, 2) # 1000 x 1000 map with 500 resources and 2 players.
view = views.View(1280, 800, pygame.FULLSCREEN, map)

map.players[0].colour = misc.GREEN
map.players[1].colour = (100, 100, 212)

for player in map.players:
     player.ships.append(ships.S1s6(view, player, (view.width/2), (view.height/2)))
     player.ships[-1].built = True
     
buildButton = views.BuildButton(view, pygame.Rect(10, 10, 20, 20), ships.S1s1)
buildButton = views.BuildButton(view, pygame.Rect(10, 40, 20, 20), ships.S1s4)
        
peteship.main(view, map) # run the game