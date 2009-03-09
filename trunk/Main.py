#!/usr/bin/env python
#
#  Main.py
#  Peteship
#
#  Created by Pete Lord on 20/02/2009.
#  Copyright (c) 2009 Turn Head Studios. All rights reserved.
#

import sys, os, pygame, math, Entities, TestMap, Options

#
## Not until we've got alot of calcs going on!
#try:
#    import psyco
#    psyco.profile()
#except ImportError:
#    print "(??) Warning: psyco not found."

pygame.init()

def main(map, players):
    clock = pygame.time.Clock()
    
    number_of_players = players
    
    keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,\
    pygame.K_a:False,pygame.K_SPACE:False,pygame.K_w:False,pygame.K_s:False,pygame.K_d:False,pygame.K_1:False,pygame.K_2:False,\
    pygame.K_o:False,pygame.K_l:False}
    
    running = True
    
    entities = Entities.EntityHandler(int(sys.argv[1]), map, 0, players) # Need to find which player is our player! Message from server i suppose
    pygame.display.set_icon(pygame.image.load(os.path.join('Data', 'icon.png')))
    pygame.key.set_repeat(100, 30)
    # Note on possible efficiency improvement: make a list of all ships on screen at the start of the frame

    while running:
        clock.tick(30)
        pygame.msg.message

        for event in pygame.event.get(pygame.KEYDOWN):
            keysHeld[event.key] = True
            
        for event in pygame.event.get(pygame.KEYUP):
            keysHeld[event.key] = False

        # Check keys
        if keysHeld[pygame.K_UP]:
            entities.view.mod_y(-Options.KEY_SCROLL)
            
        if keysHeld[pygame.K_DOWN]:
            entities.view.mod_y( Options.KEY_SCROLL)

        if keysHeld[pygame.K_LEFT]:
            entities.view.mod_x( Options.KEY_SCROLL)

        if keysHeld[pygame.K_RIGHT]:
            entities.view.mod_x(-Options.KEY_SCROLL)
            
        if keysHeld[pygame.K_l]:
            pass
            
        if keysHeld[pygame.K_o]:
            pass
            
        if keysHeld[pygame.K_w]:
            entities.view.mod_z( Options.KEY_ZOOM)

        if keysHeld[pygame.K_s]:
            entities.view.mod_z(-Options.KEY_ZOOM)
            
        if keysHeld[pygame.K_a]:
            entities.view.mod_r( Options.KEY_ROTATE)
                    
        if keysHeld[pygame.K_d]:
            entities.view.mod_r(-Options.KEY_ROTATE)

        #example of drawtext.
        # misc.drawText(view.screen, 10, 70, misc.WHITE, "Resources: " + str(currentPlayer.resources))
        
        entities.draw()
        pygame.display.flip()

        if keysHeld[pygame.K_ESCAPE]:
            running = False

        for event in pygame.event.get(pygame.QUIT):
            running = False
            
    pygame.quit()
    
main(TestMap, 1)
