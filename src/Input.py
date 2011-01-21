'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import pygame
from pygame.locals import *

#input handling
mousepos = (0, 0)       #mouse position
clicks = []             #clicks this frame
keypresses = []         #key presses this frame

#tracks if the game engine is finished
finished = False

#input keys
# will be customizable for later
AButton = K_v
BButton = K_c
CButton = K_x
DButton = K_z
LButton = K_LEFT
RButton = K_RIGHT
UButton = K_UP
DButton = K_DOWN

def processMouseMove(newpos):
    global mousepos
    displaySurface = pygame.display.get_surface()
    mousepos = (newpos[0]*(800.0/displaySurface.get_width()), 
                newpos[1]*(640.0/displaySurface.get_height()))

def processClick():
    clicks.append(mousepos)

def resetClick():
    clicks[:] = []
  
def processKeyPress(press):
    keypresses.append((press.key, press.unicode))

def getKeyPresses():
    while len(keypresses):
        yield keypresses.pop(0)

def resetKeyPresses():
    keypresses[:] = []

def reset():
    resetClick()
    resetKeyPresses()
    
#refreshes input on every call
def update():
    global finished
    while True:
        event = pygame.event.poll()
        if event.type == NOEVENT:
            break  # no more events this frame
        elif event.type == QUIT:
            finished = True
            break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                finished = True
                break
            processKeyPress(event)
        elif event.type == MOUSEMOTION:
            processMouseMove(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                processClick()
