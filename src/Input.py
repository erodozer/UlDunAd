#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

from Resources import *
import pygame

import Log

#input handling
mousepos = (0, 0)
clicks = []
keypresses = [] 
finished = False

def mousecol(rect):
  active = rect.collidepoint(*mousepos)
  flag = any(rect.collidepoint(clickx, clicky) for clickx, clicky in clicks)

  return active, flag

def processMouseMove(newpos):
  global mousepos
  mousepos = newpos

def processClick():
  clicks.append(mousepos)

def resetClick():
    clicks[:] = []

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
      Sound().stop()
      break
    elif event.type == KEYDOWN:
      processKeyPress(event)
      #Log.debug("Key Pressed: " + str(event.key) + " " + str(event.unicode))
    elif event.type == MOUSEMOTION:
      processMouseMove(event.pos)
    elif event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        processClick()
        #Log.debug("Mouse Pressed at " + str(mousepos))

