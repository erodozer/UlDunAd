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

from View import *
import Actor

class Playerlist(Layer):
  def __init__(self):
    self.engine = GameEngine()
    #self.audio = self.engine.loadAudio("mapmenu.mp3")

    self.background = self.engine.loadImage(os.path.join("Data", "Interface", "mapbackground.png"))
    self.background2 = self.engine.loadImage(os.path.join("Data", "Interface", "mapmenu.png"))

    self.button = self.engine.data.secondarymenubutton
    self.menubutton = self.engine.data.defaultbutton

    self.players = self.engine.listpath(os.path.join("Data", "Actors", "Players"), "splitfiletype", ".ini", "filename")

    self.index = 0

    self.partybuilt = []
    self.partybuilding = False
    self.donebuilding = False
    self.partyactive = False
    self.selecting = True
    self.flag = False

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))
    self.engine.drawImage(self.background2, scale = (640,480))

    if self.index < 0:
      self.index = 0
    if self.index > len(self.players):
      self.index = len(self.players) - 7

    maxindex = len(self.players)
    for i in range(self.index, 7+self.index):
      if i < maxindex:

        active, flag = self.engine.drawButton(self.button, "menu.ttf", self.players[i], size = 24, coord= (320, 70 + (44*(i-self.index+1))), scale = (200,32))
        if active == True and self.selecting == True:
          if flag == True:
            if len(self.partybuilt) < 3:
              if self.partybuilt.count(str(self.players[i]+".ini")) == 0:
                self.partybuilt.append(str(self.players[i]+".ini"))
                self.flag = False
              else:
                self.flag = True
              if len(self.partybuilt) == 1:
                self.partyactive = True
              if len(self.partybuilt) >= 3:
                while len(self.partybuilt) > 3:
                  self.partybuilt.remove(-1)
                self.donebuilding = True

    if self.flag == True:
      self.engine.renderFont("menu.ttf", "That character is already in your party!", (320, 32), size = 24)

    active, flag = self.engine.drawButton(self.button, "menu.ttf", "-UP-", size = 24, coord= (320, 64), scale = (200,32))
    if active == True and self.selecting == True:
      if flag == True:
        if self.index - 7 >= 0:
          self.index -= 7

    active, flag = self.engine.drawButton(self.button, "menu.ttf", "-DOWN-", size = 24, coord= (320, 432), scale = (200,32))
    if active == True and self.selecting == True:
      if flag == True:
        if self.index + 7 < maxindex:
          self.index += 7

    if self.partyactive == True and self.partybuilding == True and len(self.partybuilt) > 0:
      active, flag = self.engine.drawButton(self.menubutton, "default.ttf", "Done", coord= (530, 425), scale = (150,45))
      if active == True:
        if flag == True:
          self.donebuilding = True

    if self.partyactive == True:

      if self.partybuilding == False:
        self.selecting = False
        self.engine.screenfade((0,0,0,130))
        for i, choice in enumerate(['Yes', 'No']):
          active, flag = self.engine.drawButton(self.button, "default.ttf", choice, size = 18, coord= (75+(490*i), 200), scale = (100,48))
          if active == True:
            if flag == True:
              if i == 0:
                self.partybuilding = True
                self.selecting = True
              else:
                Actor.party = self.partybuilt
                from Maplist import Maplist
                self.engine.changescene(self, Maplist())
                  
        self.engine.renderFont("default.ttf", "Do you wish to build a party?", (320, 120), size = 20, flags = "Shadow")

      elif self.donebuilding == True:
        self.selecting = False
        self.engine.screenfade((0,0,0,130))
        for i, choice in enumerate(['Yes', 'No']):
          active, flag = self.engine.drawButton(self.button, "default.ttf", choice, size = 18, coord= (75+(490*i), 200), scale = (100,48))
          if active == True:
            if flag == True:
              if i == 0:
                Actor.party = self.partybuilt
                from Maplist import Maplist
                self.engine.changescene(self, Maplist())
              else:
                self.donebuilding = False
                self.selecting = True
                self.partybuilt = []
                                  
        self.engine.renderFont("default.ttf", "Is this the party you want?", (320, 120), size = 20, flags = "Shadow")

        for i, partymember in enumerate(self.partybuilt):
          self.engine.renderFont("default.ttf", os.path.splitext(partymember)[0], (320, 180 + (i*24)), size = 20, flags = "Shadow")

