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
keypresses = [] 
finished = False

def processKeyPress(press):
  global finished
  if press.key == K_ESCAPE:
    finished = True
    return
  keypresses.append((press.key, press.unicode))

def getKeyPresses():
  while len(keypresses):
    yield keypresses.pop(0)

def resetKeyPresses():
  keypresses[:] = []

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
      processKeyPress(event)

