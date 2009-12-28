#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

import Engine
from Engine import GameEngine

from View import *

import random

from Config import Configuration

import Input

class Maplist(Layer):
  def __init__(self):
    self.engine = GameEngine()
    self.background = self.engine.loadImage(os.path.join("Data", "Interface", "mapbackground.png"))

    self.button = self.engine.data.mapbutton
    self.menubutton = self.engine.data.secondarybutton

    self.maps = []
    self.towns = self.engine.listpath(os.path.join("Data", "Places", "Towns"), "searchfile", "town.ini")
    self.dungeons = self.engine.listpath(os.path.join("Data", "Places", "Dungeons"), "searchfile", "dungeon.ini")
    self.maps.extend(self.towns), self.maps.extend(self.dungeons)

    self.formations = self.engine.listpath(os.path.join("Data", "Actors", "Enemies", "Formations"), "splitfiletype", ".ini")
    self.mapinfo = self.engine.makeWindow(scale = (310, 356))

    self.initmenu = self.engine.createMenu(self.engine.data.menuWindow, self.engine.data.menuwindowbutton, ["Show Maps", "Show Menu", "Random Battle"], (112, 126), 160)
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

      self.engine.drawWindow(self.mapinfo, coord = (480, 220))
  
      if self.selectedmap != None:
        self.engine.renderFont("default.ttf", self.selectedmap, (480, 70), size = 24, flags = "Shadow")
        self.engine.renderFont("default.ttf", "Location Type:", (480, 300), size = 20, flags = "Shadow")

        if self.selectedmap in self.dungeons:
          loctype = "Dungeon"
          mapback = self.engine.loadImage(os.path.join("Data", "Places", "Dungeons", self.selectedmap, "background.png"))
          self.engine.drawImage(mapback, coord = (480, 190), scale = (260,195))
        else:
          loctype = "Town"
          mapback = self.engine.loadImage(os.path.join("Data", "Places", "Towns", self.selectedmap, "background.png"))
          self.engine.drawImage(mapback, coord = (480, 190), scale = (260,195))
        self.engine.renderFont("default.ttf", loctype, (480, 320), size = 20, flags = "Shadow")

        
        active, flag = self.engine.drawButton(self.menubutton, coord= (480, 350), scale = (214,36))
        if flag == True:
          Engine.town = self.selectedmap
          if loctype == "Dungeon":
            from Dungeon import Dungeon
            self.engine.changescene(self, Dungeon())
          else:
            from Towns import Towns
            self.engine.changescene(self, Towns())

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
      buttons = self.engine.drawMenu(self.initmenu)
      if buttons[0][1] == True:
        self.showmaps = True
      elif buttons[1][1] == True:
        from MenuSystem import MenuSystem
        self.engine.changescene(self, MenuSystem())
      elif buttons[2][1] == True:
        if self.formations != []:
          from BattleScene import BattleScene 
          self.engine.changescene(self, BattleScene(str(self.formation)))
          from ExtraScenes import LoadingScene
          View().addscene(LoadingScene("Preparing Battle", 4.5))

