#!/usr/bin/env python2.5

import os, sys, pygame, math

pygame.init()

centre = 200

screen = pygame.display.set_mode((400, 400))

numberOfPoints = input("Please enter the number of points desired.")
shipRadius = input("Enter a radius for the ship")
shipRotation = 0 # for later spinnying.
points = []

running = True
clock = pygame.time.Clock()

keysHeld = {pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_ESCAPE:False,pygame.K_q:False,pygame.K_a:False,pygame.K_SPACE:False}

class Point():
    def __init__(self, rotation, radiusMod): # possibility to load.
        self.rotation = rotation
        self.radiusMod = radiusMod
        
    def increaseRadiusMod(self):
        self.radiusMod += 0.1

    def decreaseRadiusMod(self):
        self.radiusMod -= 0.1
        
    def increaseRotation(self):
        self.rotation+= 0.1
        
    def decreaseRotation(self):
        self.rotation -= 0.1

for i in range(numberOfPoints):
    points.append(Point(0, 0))
    
selectedPoint = points[0]
currentSelectedPoint = 0
    
while running:
    clock.tick(30)
    pygame.msg.message
    
    for event in pygame.event.get(pygame.KEYDOWN):
        keysHeld[event.key] = True
    for event in pygame.event.get(pygame.KEYUP):
        keysHeld[event.key] = False
    
    if keysHeld[pygame.K_UP]:
        points[currentSelectedPoint].decreaseRadiusMod()
    if keysHeld[pygame.K_DOWN]:
        points[currentSelectedPoint].increaseRadiusMod()
               
    if keysHeld[pygame.K_LEFT]:
        points[currentSelectedPoint].increaseRotation()
    if keysHeld[pygame.K_RIGHT]:
        points[currentSelectedPoint].decreaseRotation()
            
    if keysHeld[pygame.K_q]:
        currentSelectedPoint += 1
        if currentSelectedPoint >= numberOfPoints - 1:
            currentSelectedPoint = 0
    if keysHeld[pygame.K_a]:
        currentSelectedPoint -= 1
        if currentSelectedPoint < 0:
            currentSelectedPoint = numberOfPoints - 1
                
    if keysHeld[pygame.K_SPACE]:
        # output
        pass
        
    # calc points:
    drawPoints = []
    for point in points:
        drawPoints.append((centre + (shipRadius + point.radiusMod) * math.sin(shipRotation + point.rotation * math.pi / 3), (centre - (shipRadius + point.radiusMod) * math.cos(shipRotation + point.rotation * math.pi / 3))))
            
# Draw code.
    screen.fill( 0, 0, 0)
    
    pygame.draw.aalines(screen, (255, 255, 255), True, drawPoints)
    
    pygame.display.flip()
    if keysHeld[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get(pygame.QUIT):
        running = False
