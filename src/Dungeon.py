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

from GameEngine import *
import GameEngine
import View
from View import *

import Config

import random

from Player import Player

class Dungeon(Layer):
  def __init__(self):

    self.engine = GameEngine
    self.dungeonname = self.engine.town

    self.party = []
    for i, partymember in enumerate(self.engine.party):
      self.party.append(Player(partymember))

    self.dungeonini = Config.Configuration(os.path.join("..", "Data", "Towns", self.dungeonname, "dungeon.ini")).dungeon

    try:
      self.background = self.engine.loadImage(os.path.join("Data", "Towns", self.dungeonname, "background.png"))
    except:
      self.background = None

    self.audio = None
#    if self.dungeonini.__getattr__("audio") != ("None" or ""):
#      self.audio = Sound().loadAudio(self.dungeonini.audio)

    self.menubutton = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))

    self.secondarybutton = self.engine.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.secondarybuttonactive = self.engine.loadImage(os.path.join("Data", "secondarymenubuttonactive.png"))


    Sound().volume(float(self.engine.volume)/10)

    self.cells = self.dungeonini.__getattr__("cells", "int")
    self.celldisplay = self.engine.loadImage(os.path.join("Data", "celldisplay.png"))
    self.cellactivated = False

    self.encounters = self.dungeonini.encounters.split(", ")

    if self.engine.cells == None:
      self.engine.cells = []
      for i in range(0, self.cells):
        if i == self.cells:
          self.engine.cells.append(self.dungeonini.bossformation)
        else:
          self.engine.cells.append(random.choice(self.encounters))
    
    self.notokay = False
    self.finished = False
  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))

    self.engine.renderFont("menu.ttf", self.dungeonname, (320, 44), size = 40, flags = "Shadow")
    if self.engine.currentcell > (self.cells):
      self.engine.renderFont("default.ttf", "Dungeon Cleared", (320, 90), size = 18)
    else:
      self.engine.renderFont("default.ttf", "Cell " + str(self.engine.currentcell) + " of " + str(self.cells), (320, 90), size = 18)

    for i in range(self.engine.currentcell - 1, self.cells):
      if i > 0 and i <= self.engine.currentcell + 1:
        self.engine.drawImage(self.celldisplay, (320+240*(i-self.engine.currentcell), 240), scale = (235,200))
        
    if self.cellactivated == True:
      if self.engine.cells[self.engine.currentcell].split(":")[0] == "gold":
        self.engine.screenfade((0,0,0,130))

        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 280), scale = (100,48))
        if flag == True:
          self.party[0].playerini.player.__setattr__("gold", self.party[0].gold + int(self.engine.cells[self.engine.currentcell].split(":")[1]))
          self.party[0].playerini.save()
          self.cellactivated = False
          self.engine.currentcell += 1
        else:
          buttonfont = self.engine.renderFont("default.ttf", "Okay", (320, 280), size = 16)
          self.engine.renderFont("default.ttf", "You found " + self.engine.cells[self.engine.currentcell].split(":")[1] + " gold", (320, 230), size = 20, flags = "Shadow")
      elif self.engine.cells[self.engine.currentcell].split(":")[0] == "item":
        if self.notokay == True:
          self.engine.screenfade((0,0,0,120))

          active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 280), scale = (100,48))
          if active == True:
            if flag == True:
              self.notokay = False
              self.finished = True
          buttonfont = self.engine.renderFont("default.ttf", "OK", (320, 280), size = 16)
          self.engine.renderMultipleFont("default.ttf", ("Your inventory is full!", "Some items were not picked up"), (320, 212), size = 20, flags = "Shadow")
        else:
          self.engine.screenfade((0,0,0,130))
 
          active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 280), scale = (100,48))
          if flag == True:
            self.party[0].playerini.save()
            self.cellactivated = False
            self.engine.currentcell += 1
            for i, player in enumerate(self.party):
              if i == 0:
                if len(player.inventory) < 20:
                  player.inventory.append(str(self.engine.cells[self.engine.currentcell].split(":")[1]))
                elif len(player.inventory) >= 20 and i+1 < len(self.party):
                  self.party[i+1].inventory.append(item)
              if i+1 >= len(self.party) and len(player.inventory) >= 20:
                self.notokay = True
            if self.notokay == False:
              self.finished = True
          buttonfont = self.engine.renderFont("default.ttf", "Okay", (320, 280), size = 16)
          self.engine.renderFont("default.ttf", "You found " + "", (320, 230), size = 20, flags = "Shadow")
          self.cellactivated = False
          self.engine.currentcell += 1

        if self.finished == True:
          self.engine.screenfade((0,0,0,130))

          for player in self.party:
            player.playerini.player.__setattr__("inventory", ", ".join(player.inventory))
            player.playerini.player.__setattr__("exp", player.exp)
            player.playerini.save()
            player.knockedout = False

      else:
        pygame.mixer.music.fadeout(400)
        from BattleScene import BattleScene
        View.removescene(self)
        View.addscene(BattleScene(self.engine.cells[self.engine.currentcell]+".ini"))
        from ExtraScenes import LoadingScene
        View.addscene(LoadingScene("Preparing Battle", 4.5))

    else:
      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (320, 420), scale = (200,45))
      if flag == True:
        self.cellactivated = True
      self.engine.renderFont("default.ttf", "Go to Next Cell", (320, 420))


      #return button
      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (100, 420), scale = (150,45))
      if active == True:
        if flag == True:
          from Maplist import Maplist
          View.removescene(self)
          View.addscene(Maplist())
          self.engine.town = None
          self.engine.currentcell += 1
          self.engine.cells = None
      self.engine.renderFont("default.ttf", "Return", (100, 420))

  def clearscene(self):
    del self.audio, self.background, self.dungeonini, self.dungeonname, self.engine

