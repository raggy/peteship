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

##player.ships[0].built = True

map.players[0].colour = misc.GREEN
map.players[1].colour = (100, 100, 212)

for player in map.players:
     player.ships.append(ships.S1s6(view, player, (view.width/2), (view.height/2)))
     player.ships[-1].built = True

#for i in range(3):
#    map.players[1].ships.append(ships.S1s6(view, map.players[1], (random.random() * view.width), (random.random() * view.height)))
#    for j in range(100):
#        map.players[1].ships[i].addToBuildQueue()
for player in map.players:
    for ship in player.ships:
        ship.setOrder(orders.Attack(ship.player.enemyShipClosestToXY(ship.x, ship.y), 200))
        
peteship.main(view, map) # run the game