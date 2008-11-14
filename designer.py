#!/usr/bin/env python2.5

import os, sys, pygame, math

pygame.init()

centre = 200

screen = pygame.display.set_mode((400, 400))
shipRotation = 0 # for later spinnying.
points = []

# welcome message.
print ""
print "!!!"
print "Welcome to the peteship ship designer. This is a simple application designed in order to help pete and ben hack ships together. Yes it's pitifully simple."
print "Author: Pete Lord"
print "Date: 14/11/08 @ 03:19 a.k.a. coffee time."
print "!!!"
print ""
print "Key commands:"
print "Up: Move point towards centre (decrease radius mod). Down: Move point away from centre (increase radius mod)."
print "Left: Move point CLOCKWISE (increase rotation). Right: Move point ANTI - CLOCKWISE (decrease rotation)."
print "Q: Previous point. A: Next point. Escape: Quit. Space: print out data into terminal."
print "Power button when held for 20 seconds: Save. Just kidding."
print "Happy ship coding - Pete."
print ""
numberOfPoints = input("Please enter the number of points desired: ")
shipRadius = input("Enter a radius for the ship: ")
print ""

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
        self.rotation+= 0.05
        
    def decreaseRotation(self):
        self.rotation -= 0.05

for i in range(numberOfPoints):
    temp = 360 / numberOfPoints * i
    temp = math.pi * temp / 180
    points.append(Point(temp, shipRadius))
    
selectedPoint = points[0]
currentSelectedPoint = 0
print ""
print "Point: " + `currentSelectedPoint`

while running:
    clock.tick(15)
    
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
        print ""
        print "Point: " + `currentSelectedPoint`
        keysHeld[pygame.K_q] = False
        
    if keysHeld[pygame.K_a]:
        currentSelectedPoint -= 1
        if currentSelectedPoint < 0:
            currentSelectedPoint = numberOfPoints
        print ""
        print "Point: " + `currentSelectedPoint`
        keysHeld[pygame.K_a] = False
                        
    if keysHeld[pygame.K_SPACE]:
        for point in points:
            print ""
            print "Output for current point array:"
            print ""
            print "Rotation: " + `point.rotation` + " & Radius modification: " + `point.radiusMod`
            print " --- "
            
    # calc points:
    drawPoints = []
    for point in points:
        drawPoints.append((centre + (shipRadius + point.radiusMod) * math.sin(shipRotation + point.rotation * math.pi / 3), (centre - (shipRadius + point.radiusMod) * math.cos(shipRotation + point.rotation * math.pi / 3))))
            
# Draw code.
    screen.fill(( 0, 0, 0))
    
    pygame.draw.aalines(screen, (255, 255, 255), True, drawPoints)
    
    pygame.display.flip()
    if keysHeld[pygame.K_ESCAPE]:
        running = False
        print ""
        print "Exiting program..."
        print ""

    for event in pygame.event.get(pygame.QUIT):
        running = False
