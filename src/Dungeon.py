#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

from Engine import GameEngine
import Engine

import View
from View import *

import Config

import random

from Actor import Player
import Actor

import Input

class Dungeon(Layer):
  def __init__(self):

    self.engine = GameEngine()
    self.dungeonname = Engine.town

    self.party = [Player(partymember) for partymember in Actor.party]

    path = os.path.join("Data", "Places", "Dungeons", self.dungeonname)
    self.dungeonini = Config.Configuration(os.path.join(path, "dungeon.ini")).dungeon

    try:
      self.background = self.engine.loadImage(os.path.join(path, "background.png"))
    except:
      self.background = None

    self.menubutton = self.engine.data.secondarybutton
    self.secondarybutton = self.engine.data.secondarybutton

    self.cells = self.dungeonini.__getattr__("cells", "int")
    self.celldisplay = self.engine.loadImage(os.path.join("Data", "Interface", "celldisplay.png"))
    self.cellactivated = False

    self.encounters = self.dungeonini.encounters.split(", ")

    if Engine.cells == None:
      Engine.cells = []
      for i in range(0, self.cells):
        if i == self.cells:
          Engine.cells.append(self.dungeonini.bossformation)
        else:
          Engine.cells.append(random.choice(self.encounters))
    
    self.notokay = False
    self.finished = False
  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))

    self.engine.renderFont("menu.ttf", self.dungeonname, (320, 44), size = 40, flags = "Shadow")
    if self.engine.currentcell > (self.cells):
      self.engine.renderFont("default.ttf", "Dungeon Cleared", (320, 90), size = 18)
    else:
      self.engine.renderFont("default.ttf", "Cell " + str(Engine.currentcell) + " of " + str(self.cells), (320, 90), size = 18)

    for i in range(Engine.currentcell - 1, self.cells):
      if i > 0 and i <= Engine.currentcell + 1:
        self.engine.drawImage(self.celldisplay, (320+240*(i-Engine.currentcell), 240), scale = (235,200))
        
    if self.cellactivated == True:
      if Engine.cells[Engine.currentcell].split(":")[0] == "gold":
        self.engine.screenfade((0,0,0,130))

        active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", "Okay", size = 16, coord= (320, 280), scale = (100,48))
        if flag == True:
          self.party[0].gold += int(Engine.cells[Engine.currentcell].split(":")[1])
          self.party[0].updateINI()
          self.cellactivated = False
          Engine.currentcell += 1
        else:
          self.engine.renderFont("default.ttf", "You found " + Engine.cells[Engine.currentcell].split(":")[1] + " gold", (320, 230), size = 20, flags = "Shadow")
      elif Engine.cells[Engine.currentcell].split(":")[0] == "item":
        if self.notokay == True:
          self.engine.screenfade((0,0,0,120))

          active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", "Okay", size = 16, coord= (320, 280), scale = (100,48))
          if active == True:
            if flag == True:
              self.notokay = False
              self.finished = True
          self.engine.renderMultipleFont("default.ttf", ("Your inventory is full!", "Some items were not picked up"), (320, 212), size = 20, flags = "Shadow")
        else:
          self.engine.screenfade((0,0,0,130))
 
          active, flag = self.engine.drawButton(self.secondarybutton, coord= (320, 280), scale = (100,48))
          if flag == True:
            self.party[0].playerini.save()
            self.cellactivated = False
            Engine.currentcell += 1
            for i, player in enumerate(self.party):
              if i == 0:
                if len(player.inventory) < 20:
                  player.inventory.append(str(Engine.cells[Engine.currentcell].split(":")[1]))
                elif len(player.inventory) >= 20 and i+1 < len(self.party):
                  self.party[i+1].inventory.append(item)
              if i+1 >= len(self.party) and len(player.inventory) >= 20:
                self.notokay = True
            if self.notokay == False:
              self.finished = True
          buttonfont = self.engine.renderFont("default.ttf", "Okay", (320, 280), size = 16)
          self.engine.renderFont("default.ttf", "You found " + "", (320, 230), size = 20, flags = "Shadow")
          self.cellactivated = False
          Engine.currentcell += 1

        if self.finished == True:
          self.engine.screenfade((0,0,0,130))

          for player in self.party:
            player.updateINI()
            
      else:
        pygame.mixer.music.fadeout(400)
        from BattleScene import BattleScene
        self.engine.changescene(self, BattleScene(Engine.cells[Engine.currentcell]+".ini"))
        from ExtraScenes import LoadingScene
        View().addscene(LoadingScene("Preparing Battle", 4.5))

    else:
      active, flag = self.engine.drawButton(self.menubutton, font = "default.ttf", text = "Go to Next Cell", coord= (100, 380), scale = (178,36))
      if flag == True:
        self.cellactivated = True


      #return button
      active, flag = self.engine.drawButton(self.menubutton, font = "default.ttf", text = "Return", coord= (100, 420), scale = (178,36))
      if active == True:
        if flag == True:
          from Maplist import Maplist
          self.engine.changescene(self, Maplist())
          Engine.town = None
          Engine.currentcell = 1
          Engine.cells = None


