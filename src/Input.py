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
LtButton = K_LEFT
RtButton = K_RIGHT
UpButton = K_UP
DnButton = K_DOWN

def load(configini):
    global AButton, BButton, CButton, DButton
    global LtButton, RtButton, UpButton, DnButton
    
    inputSource = configini.input
    AButton = eval(inputSource.__getattr__("AButton"))
    BButton = eval(inputSource.__getattr__("BButton"))
    CButton = eval(inputSource.__getattr__("CButton"))
    DButton = eval(inputSource.__getattr__("DButton"))
    UpButton = eval(inputSource.__getattr__("UpButton"))
    DnButton = eval(inputSource.__getattr__("DnButton"))
    LtButton = eval(inputSource.__getattr__("LtButton"))
    RtButton = eval(inputSource.__getattr__("RtButton"))
    
def create(configini, keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_v, K_c, K_x, K_z]):
    inputSource = configini.input
    inputSource.__setattr__("UpButton", keys[0])
    inputSource.__setattr__("DnButton", keys[1])
    inputSource.__setattr__("LtButton", keys[2])
    inputSource.__setattr__("RtButton", keys[3])
    inputSource.__setattr__("AButton",  keys[4])
    inputSource.__setattr__("BButton",  keys[5])
    inputSource.__setattr__("CButton",  keys[6])
    inputSource.__setattr__("DButton",  keys[7])
    configini.save()
            
def processMouseMove(newpos):
    global mousepos
    displaySurface = pygame.display.get_surface()
    mousepos = (newpos[0]*(800.0/displaySurface.get_width()), 
                newpos[1]*(600.0/displaySurface.get_height()))

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
