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


import GameEngine

import View
from View import *
      
import pygame

class MainMenu:
  def __init__(self):
    self.engine = GameEngine
    self.background = self.engine.loadImage(os.path.join("Data", "mainbackground.png"))
    #self.engine.drawImage(os.path.join("Data", "mapmenu.png"))
    #self.audio = self.engine.loadAudio("Town001.mp3")
    self.choices = ["New Game", "Continue", "Quit"]

    self.button = self.engine.data.secondarymenubutton

    self.bar = self.engine.loadImage(os.path.join("Data", "dividerbar.png"))

    from ExtraScenes import TitleScreen
    View.addscene(TitleScreen())

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))
    w, h = self.engine.w, self.engine.h

    self.engine.drawImage(self.bar, coord = (320, 100+195), scale = (550, 3))
    self.engine.drawImage(self.bar, coord = (320, 100+285), scale = (550, 3))

    for i, choice in enumerate(self.choices):
      active, flag = self.engine.drawButton(self.button, coord= (320, 250 + 90*i), scale = (550, 80))
      if active == True:
        if flag == True:
          if i == 0:
            from CharacterCreator import CharacterCreator
            View.removescene(self)
            View.addscene(CharacterCreator())
          if i == 1:
            players = self.engine.listpath(os.path.join("Data", "Players"), "splitfiletype", ".ini")
            if players != []:
              from Playerlist import Playerlist
              View.removescene(self)
              View.addscene(Playerlist())

          elif i == 2:
             GameEngine.finished = True
      buttonfont = GameEngine.renderFont("default.ttf", str(choice), (320, 250 + 90*i), size = 32)

  def clearscene(self):
    del self.button, self.engine, self.choices
