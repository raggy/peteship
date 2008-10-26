#!/usr/local/bin/python
import sys, os, pygame, math, ships, orders, players, misc, formations
pygame.init()

GLOBAL_ZOOMAMOUNT = 0.05

def main(player, MAPWIDTH, MAPHEIGHT): # NEEDS MAP HEIGHT! MAKES GAME BIGGER, DEFINES BOUNDARRRIESSSSSSSSS.....
    clock = pygame.time.Clock()
    keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,pygame.K_w:False,pygame.K_SPACE:False}
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
                if pygame.KMOD_SHIFT & pygame.key.get_mods():
                    for ship in player.selectedShips:
                        ship.queueOrder(orders.MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
                else:
                    for ship in player.selectedShips:
                        ship.setOrder(orders.MoveToXY((float(event.dict['pos'][0])/ player.zoom + player.x), (float(event.dict['pos'][1])) / player.zoom + player.y))
            elif (event.dict['button'] == 4):
                player.panBy(0,-10)
            elif (event.dict['button'] == 5):
                player.panBy(0,10)
            elif (event.dict['button'] == 6):
                player.panBy(-10,0)
            elif (event.dict['button'] == 7):
                player.panBy(10,0)

        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            if event.dict['button'] == 1:
                player.selectedShips = []
                player.selecting = False
                player.selEndPos = event.dict['pos']
                if player.selStartPos[0] > player.selEndPos[0]: # If the player has dragged leftwards
                    player.selStartPos, player.selEndPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1]) # then swap the x positions of start and end
                if player.selStartPos[1] > player.selEndPos[1]:
                    player.selEndPos, player.selStartPos = (player.selEndPos[0], player.selStartPos[1]), (player.selStartPos[0], player.selEndPos[1])
                for ship in player.ships:
                    if  player.selEndPos[0] >= (ship.x - ship.radius - player.x) * player.zoom and\
                        player.selStartPos[0] <= (ship.x + ship.radius - player.x) * player.zoom and\
                        player.selEndPos[1] >= (ship.y - ship.radius - player.y) * player.zoom and\
                        player.selStartPos[1] <= (ship.y + ship.radius - player.y) * player.zoom: # If player clicked on this ship
                        player.selectedShips.append(ship) # Set player's selected ship

        for event in pygame.event.get(pygame.MOUSEMOTION):
            if player.selecting:
                player.selEndPos = event.dict['pos']

        # Check keys
        if keysHeld[pygame.K_UP]:
            player.panBy(0,-10)

        if keysHeld[pygame.K_DOWN]:
            player.panBy(0,10)

        if keysHeld[pygame.K_LEFT]:
            player.panBy(-10,0)

        if keysHeld[pygame.K_RIGHT]:
            player.panBy(10,0)

        if keysHeld[pygame.K_q]: # petenote: When i figure out how many pixels this changes by i'll move the display so the zoom is centered.
            player.zoomBy(-GLOBAL_ZOOMAMOUNT)

        if keysHeld[pygame.K_w]:
            player.zoomBy(GLOBAL_ZOOMAMOUNT)

        player.screen.fill(misc.BLACK) #ARRR.

        for ship in player.ships:
            ship.drawOrders()

        for ship in player.ships: # Rev 43: Will work better when ships Idle properly. At the moment they stay with a move order.
            ship.poll()
            if ship.x > player.lBound and ship.x < player.rBound and ship.y > player.tBound and ship.y < player.bBound:
                ship.draw()

        if player.selecting: # If the player is currently holding down the left mouse button
            # Draw a nice box for selection
            pygame.draw.line(player.screen, misc.DARKGREY, player.selStartPos, (player.selStartPos[0], player.selEndPos[1]))
            pygame.draw.line(player.screen, misc.DARKGREY, (player.selStartPos[0], player.selEndPos[1]), player.selEndPos)
            pygame.draw.line(player.screen, misc.DARKGREY, player.selEndPos, (player.selEndPos[0], player.selStartPos[1]))
            pygame.draw.line(player.screen, misc.DARKGREY, (player.selEndPos[0], player.selStartPos[1]), player.selStartPos)

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

            
        pygame.display.flip()

        if keysHeld[pygame.K_ESCAPE]:
            running = False

        for event in pygame.event.get(pygame.QUIT):
            running = False
    pygame.quit()
