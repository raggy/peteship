#!/usr/local/bin/python
import sys, os, pygame, math, ships, orders, players, misc, formations
pygame.init()

def main(player, MAPWIDTH, MAPHEIGHT): # NEEDS MAP HEIGHT! MAKES GAME BIGGER, DEFINES BOUNDARRRIESSSSSSSSS.....
    clock = pygame.time.Clock()
    keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,pygame.K_a:False,pygame.K_SPACE:False,pygame.K_w:False,pygame.K_s:False,pygame.K_d:False}
    running = True

    # Note on possible efficiency improvement: make a list of all ships on screen at the start of the frame

    while running:
        clock.tick(30)
        pygame.msg.message

        for event in pygame.event.get(pygame.KEYDOWN):
            keysHeld[event.key] = True
            
        for event in pygame.event.get(pygame.KEYUP):
            keysHeld[event.key] = False
        
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN): # Loop through all MOUSEBUTTONDOWN events on the buffer
            if event.dict['button'] == 1: # If left mouse button clicked
                # then ask any ships if they're going to be selected
                #Testing new box select
                player.selStartPos = player.selEndPos = event.dict['pos']
                player.selecting = True
            elif (event.dict['button'] == 2) or (event.dict['button'] == 3): # If right mouse button clicked
                if (event.dict['pos'][0] / player.zoom) + player.x >= 0.0 and\
                (event.dict['pos'][1] / player.zoom) + player.y >= 0.0 and\
                (event.dict['pos'][0] / player.zoom) + player.x <= MAPWIDTH and\
                (event.dict['pos'][1] / player.zoom) + player.y <= MAPHEIGHT: # If player clicked somewhere on the map
                    #shipAtCursor = player.shipOnScreenAtXY(event.dict['pos'][0], event.dict['pos'][1])
                    shipAtCursor = False
                    for ship in player.shipsOnScreen:
                        if event.dict['pos'][0] >= (ship.x - ship.radius - player.x) * player.zoom and\
                        event.dict['pos'][0] <= (ship.x + ship.radius - player.x) * player.zoom and\
                        event.dict['pos'][1] >= (ship.y - ship.radius - player.y) * player.zoom and\
                        event.dict['pos'][1] <= (ship.y + ship.radius - player.y) * player.zoom:
                            shipAtCursor = ship
                    if shipAtCursor == False:
                        if pygame.KMOD_SHIFT & pygame.key.get_mods():
                            for ship in player.selectedShips:
                                ship.queueOrder(orders.MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
                        else:
                            for ship in player.selectedShips:
                                ship.setOrder(orders.MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
                    else:
                        if pygame.KMOD_SHIFT & pygame.key.get_mods():
                            for ship in player.selectedShips:
                                ship.queueOrder(orders.MoveToShip(shipAtCursor))
                        else:
                            for ship in player.selectedShips:
                                ship.queueOrder(orders.MoveToShip(shipAtCursor))
            elif (event.dict['button'] == 4):
                player.zoomInBy(1.05)
            elif (event.dict['button'] == 5):
                player.zoomOutBy(1.05)
            """elif (event.dict['button'] == 6):
                player.panBy(-10,0)
            elif (event.dict['button'] == 7):
                player.panBy(10,0)
            """
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            if event.dict['button'] == 1:
                player.selectedShips = []
                player.selecting = False
                player.selEndPos = event.dict['pos']
                if player.selStartPos[0] > player.selEndPos[0]: # If the player has dragged leftwards
                    player.selStartPos, player.selEndPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1]) # then swap the x positions of start and end
                if player.selStartPos[1] > player.selEndPos[1]:
                    player.selEndPos, player.selStartPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1])
                for ship in player.shipsOnScreen:
                    if  player.selEndPos[0] >= (ship.x - ship.radius - player.x) * player.zoom and\
                        player.selStartPos[0] <= (ship.x + ship.radius - player.x) * player.zoom and\
                        player.selEndPos[1] >= (ship.y - ship.radius - player.y) * player.zoom and\
                        player.selStartPos[1] <= (ship.y + ship.radius - player.y) * player.zoom: # If player clicked on this ship
                        ship.select() # Append to selected ships

        for event in pygame.event.get(pygame.MOUSEMOTION):
            if player.selecting:
                player.selEndPos = event.dict['pos']

        # Check keys
        if keysHeld[pygame.K_UP]:
            player.panBy(0, -15 / player.zoom)

        if keysHeld[pygame.K_DOWN]:
            player.panBy(0, 15 / player.zoom)   

        if keysHeld[pygame.K_LEFT]:
            player.panBy(-15 / player.zoom, 0)

        if keysHeld[pygame.K_RIGHT]:
            player.panBy(15 / player.zoom, 0)

        if keysHeld[pygame.K_q]:
            player.zoomInBy(1.05)

        if keysHeld[pygame.K_a]:
            player.zoomOutBy(1.05)
            
        if keysHeld[pygame.K_s]:
            player.resizeMM(-4, -4)
            
        if keysHeld[pygame.K_w]:
            player.resizeMM(4, 4)
        
        if keysHeld[pygame.K_d]:
            for ship in player.selectedShips:
                ship.die()

        player.screen.fill(misc.BLACK) #ARRR.
        
    # Draw stars. Sticking it all in one place to reduce calls.
        if player.drawStars: # If player wants to draw stars
	    if player.width / player.zoom <= misc.GLOBAL_MAPWIDTH and player.height / player.zoom <= misc.GLOBAL_MAPHEIGHT: # And they're not zoomed out too much
		for star in player.stars:
		    if star[0] > player.x and\
		    star[0] * star[3] < player.x * star[3] + player.width / player.zoom and\
		    star[1] > player.y and\
		    star[1] * star[3] < player.y * star[3] + player.height / player.zoom:
			colour = (star[2][0] * player.zoom, star[2][1] * player.zoom, star[2][2] * player.zoom)
			if colour[0] > 255:
			    colour = (255, 255, 255)
			pygame.draw.line(player.screen, colour, ((star[0] - player.x) * player.zoom * star[3], (star[1] - player.y) * player.zoom * star[3]), ((star[0] - player.x) * player.zoom * star[3], (star[1] - player.y) * player.zoom * star[3]))
            
	# Draw contrails.
        for effect in player.lowEffects:
            if effect.lifetime <= 0:
                effect.remove()
            else:
               effect.poll()
               # check to see if onscreen to go here.
               effect.draw()
               
        # SHIP CALCULATIONS START HERE.
        # formations, so the orders are all good.
        for formation in player.formations:
            formation.poll() # always needs to be done.

        for ship in player.ships:
            ship.drawOrders()

        player.shipsOnScreen = []
        
        for ship in (player.ships + player.missiles): # Rev 43: Will work better when ships Idle properly. At the moment they stay with a move order.
            ship.poll()
            if ship.x > player.lBound and ship.x < player.rBound and ship.y > player.tBound and ship.y < player.bBound:
                ship.draw()
                player.shipsOnScreen.append(ship) # Make a list of all ships on screen

        if player.selecting: # If the player is currently holding down the left mouse button
            # Draw a nice box for selection
            pygame.draw.line(player.screen, misc.DARKGREY, player.selStartPos, (player.selStartPos[0], player.selEndPos[1]))
            pygame.draw.line(player.screen, misc.DARKGREY, (player.selStartPos[0], player.selEndPos[1]), player.selEndPos)
            pygame.draw.line(player.screen, misc.DARKGREY, player.selEndPos, (player.selEndPos[0], player.selStartPos[1]))
            pygame.draw.line(player.screen, misc.DARKGREY, (player.selEndPos[0], player.selStartPos[1]), player.selStartPos)

        # Draw edges of map
        if player.height / player.zoom > MAPHEIGHT: # If the player view is taller than the map height
            # Draw horizontal edges
            pygame.draw.line(player.screen, misc.WHITE, ((-player.x) * player.zoom, (-player.y) * player.zoom), ((MAPWIDTH - player.x) * player.zoom, (-player.y) * player.zoom))
            pygame.draw.line(player.screen, misc.WHITE, ((MAPWIDTH - player.x) * player.zoom,(MAPHEIGHT - player.y) * player.zoom), ((-player.x) * player.zoom,(MAPHEIGHT - player.y) * player.zoom))
        if player.width / player.zoom > MAPWIDTH: # If the player view is wider than the map width
            # Draw vertical edges
            pygame.draw.line(player.screen, misc.WHITE, ((MAPWIDTH - player.x) * player.zoom, (-player.y) * player.zoom), ((MAPWIDTH - player.x) * player.zoom,(MAPHEIGHT - player.y) * player.zoom))
            pygame.draw.line(player.screen, misc.WHITE, ((-player.x) * player.zoom,(MAPHEIGHT - player.y) * player.zoom), ((-player.x) * player.zoom, (-player.y) * player.zoom))        

        # Draw explosions. Pyrotechnic Glee.
        for effect in player.effects:
            if effect.lifetime <= 0:
                effect.remove()
            else:
               effect.poll()
               # check to see if onscreen to go here.
               effect.draw()

        # minimap draw code!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if player.mmShow: #showing the MiniMap?
            pygame.draw.rect(player.screen, misc.BLACK, player.mmBoundaryRect, 0) #Black out the background of the MM
            player.updateMM()
            for ship in player.ships:
                tempX = player.mmBoundaryRect.left + ship.x / MAPWIDTH * player.mmBoundaryRect.size[0] # arbitrary amount. Represents map size.
                tempY = player.mmBoundaryRect.top + ship.y / MAPHEIGHT * player.mmBoundaryRect.size[1] # as above.
                pygame.draw.line(player.screen, misc.WHITE, (tempX, tempY), (tempX, tempY))

            pygame.draw.rect(player.screen, misc.DARKGREY, player.mmViewRect, 1)
            pygame.draw.rect(player.screen, misc.WHITE, player.mmBoundaryRect, 1) #Border the minimap. Drawn after that lot so that the border overwrites the view indicator.
       # end of minimap draw code!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        pygame.display.flip()

        if keysHeld[pygame.K_ESCAPE]:
            running = False

        for event in pygame.event.get(pygame.QUIT):
            running = False
    pygame.quit()
