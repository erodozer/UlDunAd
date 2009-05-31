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

from View import *
import Menu

import Config

import string

class CharacterCreator(Layer):

  def __init__(self):
    self.engine = GameEngine
    self.race = "Hume.ini"
    raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race

    self.stat = []
    self.stattitle = ["HP", "SP", "ATK", "DEF", "SPD", "MAG", "EVD"]
    self.hp = self.stat.append(raceini.hp)
    self.sp =  self.stat.append(raceini.sp)
    self.atk =  self.stat.append(raceini.atk)
    self.defn =  self.stat.append(raceini.defn)
    self.spd =  self.stat.append(raceini.spd)
    self.mag =  self.stat.append(raceini.mag)
    self.evd =  self.stat.append(raceini.evd)

    self.capson = True

    self.name = []

    self.othercommands = ["Clear", "Delete", "Confirm"]
    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))
    
    self.textbutton = self.engine.loadImage(os.path.join("Data", "textbutton.png"))
    self.textbuttonactive = self.engine.loadImage(os.path.join("Data", "textbuttonactive.png"))

    self.menubutton = self.engine.loadImage(os.path.join("Data", "menubutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "menubuttonactive.png"))

    self.typingname = False
    self.racechooser = False

    self.racebutton = self.engine.loadImage(os.path.join("Data", "mapmenubutton.png"))
    self.racebuttonactive = self.engine.loadImage(os.path.join("Data", "mapmenubuttonactive.png"))

  def TypeName(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))
    name = string.join(self.name, '')
    namefont = self.engine.renderFont("default.ttf", name, (320 , 96), size = 32)

    for i in range(0,26):
      button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i%9)) , 164+(36*(i/9))), scale = (32,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i%9)) , 164+(36*(i/9))), scale = (32,32))
        if flag == True:
          self.name.append(chr(97+i).upper())

      buttonfont = self.engine.renderFont("default.ttf", chr(97+i).upper(), (218 + (36*(i%9)) , 164+(36*(i/9))), size = 24)

      button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i%9)) , 272+(36*(i/9))), scale = (32,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i%9)) , 272+(36*(i/9))), scale = (32,32))
        if flag == True:
          self.name.append(chr(97+i))

      buttonfont = self.engine.renderFont("default.ttf", chr(97+i), (218 + (36*(i%9)) , 272+(36*(i/9))), size = 24)

    for i, choice in enumerate(self.othercommands):
      button = self.engine.drawImage(self.textbutton, coord= (90, 186 + (76*i)), scale = (150,44))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.textbuttonactive, coord= (90, 186 + (76*i)), scale = (150,44))
        if flag == True:
          if i == 0:
            self.name = []
          if i == 1:
            if self.name != []:
              self.name.reverse()
              self.name.pop(0)
              self.name.reverse()
          if i == 2:
            self.name = self.name
            self.typingname = False     
      buttonfont = self.engine.renderFont("default.ttf", str(choice), (90, 186 + (76*i)), size = 24)


  def drawRaceMenu(self):

    racepath = os.path.join("Data", "Races")
    self.races = []
    allraces = os.listdir(racepath)
    for name in allraces:
      if os.path.splitext(name)[1].lower() == ".ini":
        self.races.append(os.path.splitext(name)[0])

    button = self.races
    buttonfont = self.races

    for i, choice in enumerate(self.races):
      button[i] = self.engine.drawImage(self.racebutton, coord= (320, 64+(48*i)), scale = (200,32))
      active, flag = self.engine.mousecol(button[i])
      if active == True:
        button[i] = self.engine.drawImage(self.racebuttonactive, coord= (320, 64+(48*i)), scale = (200,32))
      if flag == True:
        self.race = choice
        self.racechooser = False
      buttonfont[i] = self.engine.renderFont("menu.ttf", str(choice), (320, 64+(48*i)), size = 24)  
   
  def update(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))

    if self.typingname == True:
      self.TypeName()
    elif self.racechooser == True:
      self.drawRaceMenu()
    else:
      button = self.engine.drawImage(self.menubutton, coord= (90, 130), scale = (150,45))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (90, 130), scale = (150,45))
        if flag == True:
          self.typingname = True
      buttonfont = self.engine.renderFont("default.ttf", "Change Name", (90, 130))

      otherfont = self.engine.renderFont("default.ttf", "Name", (200, 130), size = 24)

      name = string.join(self.name, '')
      namefont = self.engine.renderFont("default.ttf", name, (380, 130), size = 32)

      self.engine.renderFont("default.ttf", "Create A Character", (170, 70), size = 24)

      button = self.engine.drawImage(self.menubutton, coord= (90, 190), scale = (150,45))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (90, 190), scale = (150,45))
        if flag == True:
          self.racechooser = True

      buttonfont = self.engine.renderFont("default.ttf", "Change Race", (90, 190))
      otherfont = self.engine.renderFont("default.ttf", "Race", (200, 190), size = 24)

      name = self.race.split(".")
      namefont = self.engine.renderFont("default.ttf", name[0], (380, 190), size = 32)

      for i, stat in enumerate(self.stat):
        self.engine.renderFont("default.ttf", self.stattitle[i], (100, 240 + (i*32)), size = 24)

        self.engine.renderFont("default.ttf", str(stat), (280, 240 + (i*32)), size = 24)

      name = string.join(self.name, '')
      button = self.engine.drawImage(self.menubutton, coord= (470, 420), scale = (150,45))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (470, 420), scale = (150,45))
        if flag == True:
          if name != "":
            Config.Configuration(os.path.join("Data", "Players", name + ".ini")).save()
            newconf = Config.Configuration(os.path.join("Data", "Players", name + ".ini"))
            newconf.player.lvl = str(1)
            newconf.player.race = str(self.race)
            newconf.player.weapon = "None"
            newconf.player.armor = "None"
            newconf.save()
            View.removescene(self)
            GameEngine.player = str(name+".ini")
            from Maplist import Maplist
            View.addscene(Maplist())
            
      buttonfont = self.engine.renderFont("default.ttf", "Create", (470, 420))

