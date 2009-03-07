import math, pygame

try:
    import psyco
    psyco.full()
except ImportError:
    pass

# Colour definitions
BLACK    = 0, 0, 0
WHITE    = 255, 255, 255
RED      = 255, 0, 0
MIDRED   = 170, 0, 0
GREEN    = 0, 255, 0
MIDGREEN = 0, 170, 0
BLUE     = 0, 0, 255
MIDBLUE  = 0, 0, 170
GREY     = 150, 150, 150
DARKGREY = 50, 50, 50
GUINESS  = 20, 10, 10
RESOURCEBROWN = 128, 64, 0
EXPLOSIONRED = 120, 0, 0

pygame.font.init()
BASICFONT = pygame.font.Font(None, 12) # default font size 12

def drawText(screen, x, y, colour, text):
    screen.blit(BASICFONT.render(text, True, colour), (x, y))

def positive(number):
    #Convert negative numbers to their positive equivalent.
    #If the number is positive, return it.
    if number < 0:
        return number * -1
    else:
        return number

def normalisedAngle(angle):
    #Ensure that an angle is in radians properly (0 ~ 2*math.pi)
    if angle >= (math.pi * 2):
        return normalisedAngle(angle - 2 * math.pi)
    elif angle < 0:
        return normalisedAngle(angle + 2 * math.pi)
    else:
        return angle
