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

class Playerlist(Layer):
  def __init__(self):
    self.engine = GameEngine
    #self.audio = self.engine.loadAudio("mapmenu.mp3")

    self.background = self.engine.loadImage(os.path.join("Data", "mapbackground.png"))
    self.background2 = self.engine.loadImage(os.path.join("Data", "mapmenu.png"))

    self.button = self.engine.data.secondarymenubutton
    self.menubutton = self.engine.data.defaultbutton

    self.players = self.engine.listpath(os.path.join("Data", "Players"), "splitfiletype", ".ini", "filename")

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
                GameEngine.party = self.partybuilt
                from Maplist import Maplist
                View.removescene(self)
                View.addscene(Maplist())
                  
        self.engine.renderFont("default.ttf", "Do you wish to build a party?", (320, 120), size = 20, flags = "Shadow")

      elif self.donebuilding == True:
        self.selecting = False
        self.engine.screenfade((0,0,0,130))
        for i, choice in enumerate(['Yes', 'No']):
          active, flag = self.engine.drawButton(self.button, "default.ttf", choice, size = 18, coord= (75+(490*i), 200), scale = (100,48))
          if active == True:
            if flag == True:
              if i == 0:
                GameEngine.party = self.partybuilt
                from Maplist import Maplist
                View.removescene(self)
                View.addscene(Maplist())
              else:
                self.donebuilding = False
                self.selecting = True
                self.partybuilt = []
                                  
        self.engine.renderFont("default.ttf", "Is this the party you want?", (320, 120), size = 20, flags = "Shadow")

        for i, partymember in enumerate(self.partybuilt):
          self.engine.renderFont("default.ttf", os.path.splitext(partymember)[0], (320, 180 + (i*24)), size = 20, flags = "Shadow")

  def clearscene(self):
    del  self.background, self.background2, self.engine, self.players

