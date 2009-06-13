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

from MainMenu import *

class Layer:
  def __init__(self):
    pass

  def update(self):
    pass

  def isMainLayer(self):
    pass

  def clearscene(self):
    pass

scenes = []
goingout = []
goingin = []

def startup():
  scenes.append(MainMenu())

def removescene(scene):
  if scene not in goingout:
    goingout.append(scene)

def addscene(scene):
  if scene not in scenes:
    goingin.append(scene)

def update():
  if goingout != []:
    for i, oldscene in enumerate(goingout):
      oldscene.clearscene()
      scenes.remove(goingout[i])
      goingout.remove(goingout[i])

  elif goingout == [] and goingin != []:
    for i, newscene in enumerate(goingin):
      scenes.append(newscene)
      goingin.remove(goingin[i])
  elif goingout == [] and goingin == []:
    scenes[-1].update()


