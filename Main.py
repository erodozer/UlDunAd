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

def main():
  #video_flags = DOUBLEBUF|OPENGL
  gc.enable()
  video_flags = 0
  pygame.init()
  window = pygame.display.set_mode((640,480), video_flags)

  GameEngine.screen = window

  View.startup()

  Done = False
  while not Done:
    pygame.event.pump()
    keyinput = pygame.key.get_pressed()
    if keyinput[K_ESCAPE] or pygame.event.peek(QUIT):
      break

    View.update()
    
    pygame.display.update()

  return

if __name__=="__main__":
    main()
