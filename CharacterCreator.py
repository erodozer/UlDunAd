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

import Config

import string
from pygame.locals import *

class CharacterCreator(Layer):

  def __init__(self):
    self.engine = GameEngine
    self.race = "Hume.ini"
    self.playerclass = "Warrior.ini"

    raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race
    classini = Config.Configuration(os.path.join("Data", "Classes", self.playerclass)).defclass

    self.stat = []
    self.stattitle = ["HP", "SP", "ATK", "DEF", "SPD", "MAG", "EVD"]
    self.hp = self.stat.append(int(raceini.hp) + int(classini.hp))
    self.sp =  self.stat.append(int(raceini.sp) + int(classini.sp))
    self.atk =  self.stat.append(int(raceini.atk) + int(classini.atk))
    self.defn =  self.stat.append(int(raceini.defn) + int(classini.defn))
    self.spd =  self.stat.append(int(raceini.spd) + int(classini.spd))
    self.mag =  self.stat.append(int(raceini.mag) + int(classini.mag))
    self.evd =  self.stat.append(int(raceini.evd) + int(classini.evd))

    self.capson = True

    self.name = []

    self.othercommands = ["Clear", "Delete", "Confirm"]
    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))
    
    self.textbutton = self.engine.loadImage(os.path.join("Data", "textbutton.png"))
    self.textbuttonactive = self.engine.loadImage(os.path.join("Data", "textbuttonactive.png"))

    self.menubutton = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))

    self.typingname = False
    self.racechooser = False
    self.classchooser = False

    self.racebutton = self.engine.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.racebuttonactive = self.engine.loadImage(os.path.join("Data", "secondarymenubuttonactive.png"))

    GameEngine.resetKeyPresses()

  def TypeName(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))
    name = string.join(self.name, '')
    for i, char in enumerate(self.name):
      self.engine.renderFont("default.ttf", char, (112 + i*34, 72), size = 32)
    for i in range(0, 13): 
      self.engine.renderFont("default.ttf", "_", (112 + i*34, 77), size = 32)

    for i in range(0,26):
      active, flag = self.engine.drawButton(self.textbutton, self.textbuttonactive, coord= (218 + (36*(i%9)) , 164+(36*(i/9))), scale = (32,32))
      if active == True:
        if flag == True and len(self.name) < 13:
          self.name.append(chr(97+i).upper())

      buttonfont = self.engine.renderFont("default.ttf", chr(97+i).upper(), (218 + (36*(i%9)) , 164+(36*(i/9))), size = 24)

      active, flag = self.engine.drawButton(self.textbutton, self.textbuttonactive, coord= (218 + (36*(i%9)) , 272+(36*(i/9))), scale = (32,32))
      if active == True:
        if flag == True and len(self.name) < 13:
          self.name.append(chr(97+i))

      buttonfont = self.engine.renderFont("default.ttf", chr(97+i), (218 + (36*(i%9)) , 272+(36*(i/9))), size = 24)

    for i, choice in enumerate(self.othercommands):
      active, flag = self.engine.drawButton(self.textbutton, self.textbuttonactive, coord= (90, 186 + (76*i)), scale = (150,44))
      if active == True:
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

    for i in range(0,2):
      active, flag = self.engine.drawButton(self.textbutton, self.textbuttonactive, coord= (218+(36*8), 236 + (108*i)), scale = (32,32))
      if active == True:
        if flag == True:
          self.name.append(" ")
      buttonfont = self.engine.renderFont("default.ttf", "_", (218+(36*8), 236 + (108*i)), size = 24)

    for key, char in GameEngine.getKeyPresses():
      if len(self.name) < 13:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
          self.name.append(char)
        elif key == K_SPACE:
          self.name.append(" ")

      if key == K_RETURN:
        self.typingname = False
      elif key == K_BACKSPACE:
        if len(self.name) > 0:
          del self.name[-1]

  def drawRaceMenu(self):

    racepath = os.path.join("Data", "Races")
    self.races = []
    allraces = os.listdir(racepath)
    for name in allraces:
      if os.path.splitext(name)[1].lower() == ".ini":
        self.races.append(name)

    for i, choice in enumerate(self.races):
      active, flag = self.engine.drawButton(self.racebutton, self.racebuttonactive, coord= (320, 64+(48*i)), scale = (200,32))
      if active == True:
        if flag == True:
          self.race = choice
          self.racechooser = False
          raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race
          classini = Config.Configuration(os.path.join("Data", "Classes", self.playerclass)).defclass
          self.stat = []
          self.hp = self.stat.append(int(raceini.hp) + int(classini.hp))
          self.sp =  self.stat.append(int(raceini.sp) + int(classini.sp))
          self.atk =  self.stat.append(int(raceini.atk) + int(classini.atk))
          self.defn =  self.stat.append(int(raceini.defn) + int(classini.defn))
          self.spd =  self.stat.append(int(raceini.spd) + int(classini.spd))
          self.mag =  self.stat.append(int(raceini.mag) + int(classini.mag))
          self.evd =  self.stat.append(int(raceini.evd) + int(classini.evd))

      buttonfont = self.engine.renderFont("menu.ttf", str(choice.split(".ini")[0]), (320, 64+(48*i)), size = 24)  

  def drawClassMenu(self):

    classpath = os.path.join("Data", "Classes")
    self.classes = []
    allclasses = os.listdir(classpath)
    for name in allclasses:
      if os.path.splitext(name)[1].lower() == ".ini":
        self.classes.append(name)

    for i, choice in enumerate(self.classes):
      active, flag = self.engine.drawButton(self.racebutton, self.racebuttonactive, coord= (320, 64+(48*i)), scale = (200,32))
      if active == True:
        if flag == True:
          self.playerclass = choice
          self.classchooser = False
          raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race
          classini = Config.Configuration(os.path.join("Data", "Classes", self.playerclass)).defclass
          self.stat = []
          self.hp = self.stat.append(int(raceini.hp) + int(classini.hp))
          self.sp =  self.stat.append(int(raceini.sp) + int(classini.sp))
          self.atk =  self.stat.append(int(raceini.atk) + int(classini.atk))
          self.defn =  self.stat.append(int(raceini.defn) + int(classini.defn))
          self.spd =  self.stat.append(int(raceini.spd) + int(classini.spd))
          self.mag =  self.stat.append(int(raceini.mag) + int(classini.mag))
          self.evd =  self.stat.append(int(raceini.evd) + int(classini.evd))

      buttonfont = self.engine.renderFont("menu.ttf", str(choice.split(".ini")[0]), (320, 64+(48*i)), size = 24)  
   
  def update(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))

    if self.typingname == True:
      self.TypeName()
    elif self.racechooser == True:
      self.drawRaceMenu()
    elif self.classchooser == True:
      self.drawClassMenu()
    else:
      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (90, 100), scale = (150,45))
      if active == True:
        if flag == True:
          self.typingname = True
      buttonfont = self.engine.renderFont("default.ttf", "Change Name", (90, 100))

      otherfont = self.engine.renderFont("default.ttf", "Name", (200, 100), size = 24)

      name = string.join(self.name, '')
      namefont = self.engine.renderFont("default.ttf", name, (380, 100), size = 32)

      self.engine.renderFont("default.ttf", "Create A Character", (170, 70), size = 24)

      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (90, 150), scale = (150,45))
      if active == True:
        if flag == True:
          self.racechooser = True

      buttonfont = self.engine.renderFont("default.ttf", "Change Race", (90, 150))
      otherfont = self.engine.renderFont("default.ttf", "Race", (200, 150), size = 24)

      name = self.race.split(".")
      namefont = self.engine.renderFont("default.ttf", name[0], (380, 150), size = 32)

      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (90, 200), scale = (150,45))
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (90, 200), scale = (150,45))
        if flag == True:
          self.classchooser = True

      buttonfont = self.engine.renderFont("default.ttf", "Change Class", (90, 200))
      otherfont = self.engine.renderFont("default.ttf", "Class", (200, 200), size = 24)

      name = self.playerclass.split(".")
      namefont = self.engine.renderFont("default.ttf", name[0], (380, 200), size = 32)

      for i, stat in enumerate(self.stat):
        self.engine.renderFont("default.ttf", self.stattitle[i], (100, 240 + (i*32)), size = 24)

        self.engine.renderFont("default.ttf", str(stat), (280, 240 + (i*32)), size = 24)

      name = string.join(self.name, '')
      active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (470, 420), scale = (150,45))
      if active == True:
        if flag == True:
          if name != "":
            Config.Configuration(os.path.join("Data", "Players", name + ".ini")).save()
            newconf = Config.Configuration(os.path.join("Data", "Players", name + ".ini"))
            raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race
            newconf.player.lvl = str(1)
            newconf.player.race = str(self.race)
            newconf.player.playerclass = str(self.playerclass)
            newconf.player.weapon = "None"
            newconf.player.armor = "None"
            newconf.player.exp = str(0)
            newconf.player.currenthp = str(int(self.stat[0]))
            newconf.player.currentsp = str(int(self.stat[1]))
            newconf.player.monsterskilled = str(0)
            newconf.player.inventory = str('item001, item001, item001, item002, item002')
            newconf.player.spells = str('')
            newconf.save()
            View.removescene(self)
            GameEngine.party.append(str(name+".ini"))
            from Maplist import Maplist
            View.addscene(Maplist())
            
      buttonfont = self.engine.renderFont("default.ttf", "Create", (470, 420))


