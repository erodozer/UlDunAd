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

import random

from Config import Configuration

class Maplist(Layer):
  def __init__(self):
    self.engine = GameEngine
    self.background = self.engine.loadImage(os.path.join("Data", "mapbackground.png"))

    self.button = self.engine.data.mapbutton
    self.menubutton = self.engine.data.secondarybutton

    self.maps = self.engine.listpath(os.path.join("Data", "Towns"), "searchfile", "town.ini")
    self.maps.extend(self.engine.listpath(os.path.join("Data", "Towns"), "searchfile", "dungeon.ini"))
    self.formations = self.engine.listpath(os.path.join("Data", "Enemies", "Formations"), "splitfiletype", ".ini")
    self.mapinfo = self.engine.loadImage(os.path.join("Data", "mapinfo.png"))

    self.index = 0
    self.showmaps = False
    self.selectedmap = None

    if self.formations != []:
      self.formation = random.choice(self.formations)

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))

    if self.showmaps == True:
      if self.index < 0:
        self.index = 0
      if self.index > len(self.maps):
        self.index = len(self.maps) - 10

      maxindex = len(self.maps)
      for i in range(self.index, 10+self.index):
        if i < maxindex:
          active, flag = self.engine.drawButton(self.button, coord= (127, 70 + (36*(i+1))), scale = (214,36))
          if flag == True:
            self.selectedmap = self.maps[i]
          
          buttonfont = self.engine.renderFont("default.ttf", self.maps[i], (70, 70+(36*(i+1))), size = 16, flags = "Shadow", alignment = 1)

      self.engine.drawImage(self.mapinfo, coord = (480, 220), scale = (310,356))
  
      if self.selectedmap != None:
        self.engine.renderFont("default.ttf", self.selectedmap, (480, 70), size = 24, flags = "Shadow")
        self.engine.renderFont("default.ttf", "Location Type:", (480, 300), size = 20, flags = "Shadow")

        if os.path.exists(os.path.join("..","Data", "Towns", self.selectedmap, "dungeon.ini")):
          loctype = "Dungeon"
        else:
          loctype = "Town"
        self.engine.renderFont("default.ttf", loctype, (480, 320), size = 20, flags = "Shadow")

        if os.path.exists(os.path.join("..", "Data", "Towns", self.selectedmap, "background.png")):
          self.mapback = self.engine.loadImage(os.path.join("Data", "Towns", self.selectedmap, "background.png"))
          self.engine.drawImage(self.mapback, coord = (480, 190), scale = (260,195))
        
        active, flag = self.engine.drawButton(self.menubutton, coord= (480, 350), scale = (214,36))
        if flag == True:
          GameEngine.town = self.selectedmap
          if loctype == "Dungeon":
            from Dungeon import Dungeon
            View.removescene(self)
            View.addscene(Dungeon())
          else:
            from Towns import Towns
            View.removescene(self)
            View.addscene(Towns())
        buttonfont = self.engine.renderFont("default.ttf", "Explore", (480, 350), size = 16, flags = "Shadow")

      active, flag = self.engine.drawButton(self.button, coord= (127, 70), scale = (214,36))
      if flag == True:
        if self.index + 10 < maxindex:
          self.index += 10
      buttonfont = self.engine.renderFont("default.ttf", "-UP-", (70, 70), size = 16, alignment = 1, flags = "Shadow")

      active, flag = self.engine.drawButton(self.button, coord= (127, 430), scale = (214,36))
      if flag == True:
        if self.index - 10 >= 0:
          self.index -= 10
      buttonfont = self.engine.renderFont("default.ttf", "-DOWN-", (70, 430), size = 16, alignment = 1, flags = "Shadow")

      active, flag = self.engine.drawButton(self.menubutton, coord= (520, 430), scale = (214,36))
      if flag == True:
        self.selectedmap = None
        self.showmaps = False
      buttonfont = self.engine.renderFont("default.ttf", "Hide Maps", (520, 430), size = 16, flags = "Shadow")

    else:
      choices = ["Show Maps", "Show Menu", "Random Battle"]
      for i, choice in enumerate(choices):
        active, flag = self.engine.drawButton(self.menubutton, coord= (112, 90 + (36*i)), scale = (178,36))
        if flag == True:
          if i == 0:
            self.showmaps = True
          elif i == 1:
            from MenuSystem import MenuSystem
            View.removescene(self)
            View.addscene(MenuSystem())
          elif i == 2:
            if self.formations != []:
              from BattleScene import BattleScene
              View.removescene(self)
              View.addscene(BattleScene(str(self.formation)))
              from ExtraScenes import LoadingScene
              View.addscene(LoadingScene("Preparing Battle", 4.5))
         
        buttonfont = self.engine.renderFont("default.ttf", choice, (40, 90 + (36*i)), size = 16, alignment = 1, flags = "Shadow")

  def clearscene(self):
    del  self.background, self.maps, self.menubutton, self.engine

