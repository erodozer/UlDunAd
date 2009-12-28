#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

import os
import sys
import pygame

from pygame.locals import *

import Engine
from Engine import GameEngine

from Resources import *
import Resources

from ExtraScenes import TitleScreen

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
opacity = 0
screen = None

class View:
  def startup(self, caption, flags):
    engine = GameEngine()
    resolution = (engine.w, engine.h)
    screen = pygame.display.set_mode(resolution, flags)

    icon = pygame.image.load(os.path.join('..', 'uldunadicon.png')).convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption(caption)

    Resources.w, Resources.h, Resources.screen = engine.w, engine.h, screen
    Sound().inbattle, Sound().vol = Engine.inbattle, engine.volume

    GameEngine.data = Data()

    scenes.append(TitleScreen())

  def removescene(self, scene):
    if scene not in goingout:
      goingout.append(scene)

  def addscene(self, scene):
    if scene not in scenes:
      goingin.append(scene)
 
  def update(self):
    global opacity

    if goingout != []:
      if opacity < 255:
        opacity += 20
      elif opacity >=255:
        opacity = 255
        for i, oldscene in enumerate(goingout):
          scenes.remove(goingout[i])
          goingout.remove(goingout[i])

    elif goingout == [] and goingin != []:
      for i, newscene in enumerate(goingin):
        scenes.append(newscene)
        goingin.remove(goingin[i])

    elif goingout == [] and goingin == []:
      if opacity > 0:
        opacity -= 20
      elif opacity <= 0:
        opacity = 0
      scenes[-1].update()

    GameEngine().screenfade((0,0,0,opacity))

