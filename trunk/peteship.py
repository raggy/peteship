#!/usr/local/bin/python
import sys, os, pygame, math, orders, players, misc, formations, maps, effects
#pygame.init()

try:
    import psyco
    psyco.full()
except ImportError:
    pass

def main(view, map):
    clock = pygame.time.Clock()
    keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,pygame.K_a:False,pygame.K_SPACE:False,pygame.K_w:False,pygame.K_s:False,pygame.K_d:False,pygame.K_1:False,pygame.K_2:False,pygame.K_o:False,pygame.K_l:False}
    running = True
    currentPlayer = map.players[0]

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
                flag = False
                for item in view.interface:
                    # check for clicks.
                    if  event.dict['pos'][0] >= (item.shape.left) and\
                        event.dict['pos'][0] <= (item.shape.right) and\
                        event.dict['pos'][1] >= (item.shape.top) and\
                        event.dict['pos'][1] <= (item.shape.bottom): # If player clicked on this ship
                            item.click()
                            flag = True
                            print view.selectedShips
                if flag == False:    
                    view.selStartPos = view.selEndPos = event.dict['pos']
                    view.selecting = True
            elif (event.dict['button'] == 2) or (event.dict['button'] == 3): # If right mouse button clicked
                if (event.dict['pos'][0] / view.zoom) + view.x >= 0.0 and\
                (event.dict['pos'][1] / view.zoom) + view.y >= 0.0 and\
                (event.dict['pos'][0] / view.zoom) + view.x <= map.width and\
                (event.dict['pos'][1] / view.zoom) + view.y <= map.height: # If player clicked somewhere on the map
                    #shipAtCursor = player.shipOnScreenAtXY(event.dict['pos'][0], event.dict['pos'][1])
                    shipAtCursor = False
                    
                    for ship in view.shipsOnScreen:
                        if event.dict['pos'][0] >= (ship.x - ship.radius - view.x) * view.zoom and\
                        event.dict['pos'][0] <= (ship.x + ship.radius - view.x) * view.zoom and\
                        event.dict['pos'][1] >= (ship.y - ship.radius - view.y) * view.zoom and\
                        event.dict['pos'][1] <= (ship.y + ship.radius - view.y) * view.zoom:
                            shipAtCursor = ship
                            
                    if shipAtCursor == False: # move.
                        if pygame.KMOD_SHIFT & pygame.key.get_mods():
                            for ship in view.selectedShips:
                                ship.queueOrder(orders.MoveToXY((float(event.dict['pos'][0])/ view.zoom + view.x), (float(event.dict['pos'][1])) / view.zoom + view.y))
                        else:
                            for ship in view.selectedShips:
                                ship.setOrder(orders.MoveToXY((float(event.dict['pos'][0])/ view.zoom + view.x), (float(event.dict['pos'][1])) / view.zoom + view.y))
                                
                    elif shipAtCursor.player != currentPlayer: # attack order
                        if pygame.KMOD_SHIFT & pygame.key.get_mods():
                            for ship in view.selectedShips:
                                ship.queueOrder(orders.FrontalAttack(shipAtCursor, 200))
                        else:
                            for ship in view.selectedShips:
                                ship.setOrder(orders.FrontalAttack(shipAtCursor, 200))
                                
                    else: # follow order
                        if pygame.KMOD_SHIFT & pygame.key.get_mods():
                            for ship in view.selectedShips:
                                ship.queueOrder(orders.MoveToShip(shipAtCursor))
                        else:
                            for ship in view.selectedShips:
                                ship.setOrder(orders.MoveToShip(shipAtCursor))
                                
            elif (event.dict['button'] == 4):
                view.zoomInBy(1.05)
            elif (event.dict['button'] == 5):
                view.zoomOutBy(1.05)
            """elif (event.dict['button'] == 6):
                view.panBy(-10,0)
            elif (event.dict['button'] == 7):
                view.panBy(10,0)
            """
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            if event.dict['button'] == 1:
                # loop through and check that the interface hasn't been clicked
                view.selectedShips = []
                view.selecting = False
                view.selEndPos = event.dict['pos']
                if view.selStartPos[0] > view.selEndPos[0]: # If the player has dragged leftwards
                    view.selStartPos, view.selEndPos = (view.selEndPos[0], view.selStartPos[1]), (view.selStartPos[0], view.selEndPos[1]) # then swap the x positions of start and end
                if view.selStartPos[1] > view.selEndPos[1]:
                    view.selEndPos, view.selStartPos = (view.selEndPos[0], view.selStartPos[1]), (view.selStartPos[0], view.selEndPos[1])
                for ship in view.shipsOnScreen:
                    if ship.player == currentPlayer:
                        if  view.selEndPos[0] >= (ship.x - ship.radius - view.x) * view.zoom and\
                            view.selStartPos[0] <= (ship.x + ship.radius - view.x) * view.zoom and\
                            view.selEndPos[1] >= (ship.y - ship.radius - view.y) * view.zoom and\
                            view.selStartPos[1] <= (ship.y + ship.radius - view.y) * view.zoom: # If player clicked on this ship
                            ship.select() # Append to selected ships

        for event in pygame.event.get(pygame.MOUSEMOTION):
            if view.selecting:
                view.selEndPos = event.dict['pos']

        # Check keys
        if keysHeld[pygame.K_UP]:
            view.panBy(0, -15 / view.zoom)

        if keysHeld[pygame.K_DOWN]:
            view.panBy(0, 15 / view.zoom)   

        if keysHeld[pygame.K_LEFT]:
            view.panBy(-15 / view.zoom, 0)

        if keysHeld[pygame.K_RIGHT]:
            view.panBy(15 / view.zoom, 0)

        if keysHeld[pygame.K_q]:
            view.zoomInBy(1.05)

        if keysHeld[pygame.K_a]:
            view.zoomOutBy(1.05)
            
        if keysHeld[pygame.K_l]:
            view.minimap.resize(-4, -4)
            
        if keysHeld[pygame.K_o]:
            view.minimap.resize(4, 4)
            
        if keysHeld[pygame.K_w]:
            print "Key W currently unbound."

        if keysHeld[pygame.K_s]:
            if len(view.selectedShips) > 0:
                for ship in view.selectedShips:
                    ship.setOrder(orders.Idle(ship))
        
        if keysHeld[pygame.K_d]:
            for ship in view.selectedShips:
                ship.die()

        if keysHeld[pygame.K_1]:
            view.selectedShips = []
            currentPlayer = map.players[0]

        if keysHeld[pygame.K_2]:
            view.selectedShips = []
            currentPlayer = map.players[1]

        view.screen.fill(misc.BLACK) #ARRR.
        
        # Draw stars. Sticking it all in one place to reduce calls.
        if view.drawStars: # If player wants to draw stars
            if view.width / view.zoom <= map.width and view.height / view.zoom <= map.height: # And they're not zoomed out too much
                for star in view.stars:
                    if star[0] > view.x and\
                    star[0] * star[3] < view.x * star[3] + view.width / view.zoom and\
                    star[1] > view.y and\
                    star[1] * star[3] < view.y * star[3] + view.height / view.zoom:
                        colour = (star[2][0] * view.zoom, star[2][1] * view.zoom, star[2][2] * view.zoom)
                        if colour[0] > 255:
                            colour = (255, 255, 255)
                        pygame.draw.line(view.screen, colour, ((star[0] - view.x) * view.zoom * star[3], (star[1] - view.y) * view.zoom * star[3]), ((star[0] - view.x) * view.zoom * star[3], (star[1] - view.y) * view.zoom * star[3]))
            
        # Draw lower effects layer.
        for effect in view.lowEffects:
            if effect.lifetime <= 0:
                effect.remove()
            else:
               effect.poll()
               # check to see if onscreen to go here.
               effect.draw()


        for ship in currentPlayer.ships:
            ship.drawOrders()
       
        # SHIP CALCULATIONS START HERE.
        view.shipsOnScreen = []
        for player in map.players:
            for formation in player.formations:
                formation.poll() # always needs to be done.

            for ship in (player.ships + player.missiles):
                ship.poll();
                if ship.x > view.lBound and ship.x < view.rBound and ship.y > view.tBound and ship.y < view.bBound:
                    ship.draw()
                    view.shipsOnScreen.append(ship) # Make a list of all ships on screen

            #Loop through the selected ships and draw their bounding box to highlight their selection
            for ship in view.selectedShips:
                ship.drawBounding()

        if view.selecting: # If the player is currently holding down the left mouse button
            # Draw a nice box for selection
            pygame.draw.line(view.screen, misc.DARKGREY, view.selStartPos, (view.selStartPos[0], view.selEndPos[1]))
            pygame.draw.line(view.screen, misc.DARKGREY, (view.selStartPos[0], view.selEndPos[1]), view.selEndPos)
            pygame.draw.line(view.screen, misc.DARKGREY, view.selEndPos, (view.selEndPos[0], view.selStartPos[1]))
            pygame.draw.line(view.screen, misc.DARKGREY, (view.selEndPos[0], view.selStartPos[1]), view.selStartPos)

        # Draw explosions. Pyrotechnic Glee.
        for effect in view.effects:
            if effect.lifetime <= 0:
                effect.remove()
            else:
               effect.poll()
               # check to see if onscreen to go here.
               effect.draw()
		
		# draw map boundary.s
        #if view.height / view.zoom > map.height: # If the player view is taller than the map height # eff off map boundary checks!
            # Draw horizontal edges
        pygame.draw.line(view.screen, misc.WHITE, ((-view.x) * view.zoom, (-view.y) * view.zoom), ((map.width - view.x) * view.zoom, (-view.y) * view.zoom))
        pygame.draw.line(view.screen, misc.WHITE, ((map.width - view.x) * view.zoom,(map.height - view.y) * view.zoom), ((-view.x) * view.zoom,(map.height - view.y) * view.zoom))
        #if view.width / view.zoom > map.width: # If the player view is wider than the map width
            # Draw vertical edges
        pygame.draw.line(view.screen, misc.WHITE, ((map.width - view.x) * view.zoom, (-view.y) * view.zoom), ((map.width - view.x) * view.zoom,(map.height - view.y) * view.zoom))
        pygame.draw.line(view.screen, misc.WHITE, ((-view.x) * view.zoom,(map.height - view.y) * view.zoom), ((-view.x) * view.zoom, (-view.y) * view.zoom))        


        # Draw minimap
        view.minimap.draw()
        
#        # Test shipsAlongLine
#        startPoint = (50.0, 50.0)
#        endPoint   = (1000.0, 100.0)
#        
#        #startPoint, endPoint = endPoint, startPoint # reverse the line
#        
#        # Draw the line on screen
#        shipsAlongLine = map.closestShipsAlongLine(startPoint, endPoint)
#        if shipsAlongLine == []: # If no ships crossing the line
#            pygame.draw.aaline(view.screen, misc.WHITE, ((startPoint[0] - view.x) * view.zoom, (startPoint[1] - view.y) * view.zoom), ((endPoint[0] - view.x) * view.zoom, (endPoint[1] - view.y) * view.zoom)) # Draw the full beam
#            
#        else: # Else draw the beam up until the intersection
#            ship = shipsAlongLine[0]
##            ship.damaged(1)
#            
#            offsetX = misc.positive(endPoint[0] - startPoint[0])
#            offsetY = endPoint[1] - startPoint[1]
#            
#            # Get the angle of the line
#            if offsetY > 0:
#                theta = misc.normalisedAngle(math.atan(offsetX / offsetY))
#            elif offsetY == 0:
#                theta = misc.normalisedAngle(math.atan(offsetX))
#            else:
#                theta = misc.normalisedAngle(math.atan(misc.positive(offsetX) / offsetY) + math.pi)
##            theta = math.atan(offsetX / offsetY)
#            # Calculate new co-ordinates for end of line
#            cutX = math.sin(theta) * (math.sqrt((ship.x - startPoint[0]) ** 2 + (ship.y - startPoint[1]) ** 2) - ship.radius)
#            cutY = math.cos(theta) * (math.sqrt((ship.x - startPoint[0]) ** 2 + (ship.y - startPoint[1]) ** 2) - ship.radius)
#            if startPoint[0] > endPoint[0]:
#                cutX = - cutX
#            cutY += startPoint[1]
#            cutX += startPoint[0]
#            
#            
#            pygame.draw.aaline(view.screen, misc.WHITE, ((startPoint[0] - view.x) * view.zoom, (startPoint[1] - view.y) * view.zoom), ((cutX - view.x) * view.zoom, (cutY - view.y) * view.zoom)) # Draw beam until ship
#            view.effects.append(effects.ExplosionShip(view, ship, 1)) # Spark from ship
#            
#        pygame.draw.circle(view.screen, misc.WHITE, ((startPoint[0] - view.x) * view.zoom, (startPoint[1] - view.y) * view.zoom), 2, 1)
        
#        # Draw ships along the line in white
#        for ship in map.closestShipsAlongLine(startPoint, endPoint):
#            ship.colour = misc.WHITE
#            ship.draw()
#            ship.colour = ship.player.colour
#        if len(map.closestShipsAlongLine(startPoint, endPoint)) > 0:
#            ship.colour = misc.GREEN
#            ship.draw()
#            ship.colour = ship.player.colour

        # draw the interface.
        for item in view.interface:
            item.draw()
        
        misc.drawText(view.screen, 10, 70, misc.WHITE, "TEST")

        pygame.display.flip()

        if keysHeld[pygame.K_ESCAPE]:
            running = False

        for event in pygame.event.get(pygame.QUIT):
            running = False
            
    pygame.quit()
