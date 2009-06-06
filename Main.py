#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# UlDunAd - Ultimate Dungeon Adventure                              #
# Copyright (C) 2009 Blazingamer(n_hydock@comcast.net               #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       #
# as published by the Free Software Foundation; either version 3    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,        #
# MA  02110-1301, USA.                                              #
#####################################################################


import os
import sys
import pygame
from pygame.locals import *
import GameEngine
import View
import os
import gc

FPS = 60

def main():
  #video_flags = DOUBLEBUF|OPENGL
  gc.enable()
  video_flags = 0
  pygame.init()

  os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

  window = pygame.display.set_mode((640,480), video_flags)

  GameEngine.screen = window

  View.startup()

  fpsClock = pygame.time.Clock()

  while not GameEngine.finished:
    # main event loop
    while True:
      event = pygame.event.poll()
      if event.type == NOEVENT:
        break  # no more events this frame
      elif event.type == QUIT:
        GameEngine.finished = True
        break
      elif event.type == KEYDOWN:
        GameEngine.processKeyPress(event)
      elif event.type == MOUSEMOTION:
        GameEngine.processMouseMove(event.pos)
      elif event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          GameEngine.processClick()

    View.update()

    pygame.display.update()
    GameEngine.resetClick()

    fpsClock.tick(FPS)

  return

if __name__=="__main__":
    main()
