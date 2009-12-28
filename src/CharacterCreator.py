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
import Actor

from View import *

import Config

import string
from pygame.locals import *

import Input

class CharacterCreator(Layer):

  def __init__(self):
    self.engine = GameEngine()
    self.race = "Hume.ini"
    self.playerclass = "Warrior.ini"

    self.stattitle = ["HP", "SP", "ATK", "DEFN", "SPD", "MAG", "EVD"]

    self.loadplayerini()

    self.capson = False

    self.name = []

    self.specialcommands = ["CLEAR", "SPACE", "END"]
    self.othercommands = ["Reverse", "Delete"]
    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))
    self.namewindow = self.engine.makeWindow(scale = (600, 122))
    self.statwindow = self.engine.makeWindow(scale = (310, 420))
    
    self.textbutton = self.engine.data.textbutton
    self.bigtextbutton = self.engine.data.bigtextbutton

    self.racebutton = self.engine.data.secondarymenubutton
    self.menubutton = self.engine.data.defaultbutton

    self.typingname = False
    self.racechooser = False
    self.classchooser = False

    Input.resetKeyPresses()

  def TypeName(self):

    for key, char in Input.getKeyPresses():
      if len(self.name) < 13:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
          self.name.append(char)
        elif key == K_SPACE:
          self.name.append(" ")

      if key == K_CAPSLOCK:
        if self.capson == True:
          self.capson = False
        else:
          self.capson = True
        
      if key == K_RETURN:
        self.typingname = False
      elif key == K_BACKSPACE:
        if len(self.name) > 0:
          del self.name[-1]

    self.engine.drawWindow(self.namewindow, coord = (320, 74))

    name = string.join(self.name, '')
    for i, char in enumerate(self.name):
      self.engine.renderFont("default.ttf", char, (112 + i*34, 72), size = 32)
    for i in range(0, 13): 
      self.engine.renderFont("default.ttf", "_", (112 + i*34, 77), size = 32)

    for i in range(0,26):
      active, flag = self.engine.drawButton(self.textbutton, coord= (112 + (52*(i%9)) , 240+(52*(i/9))), scale = (48,48))
      if active == True:
        if flag == True and len(self.name) < 13:
          if self.capson == True:
            self.name.append(chr(97 + i).upper())
          else:
            self.name.append(chr(97 + i))

      if self.capson == True:
        buttonfont = self.engine.renderFont("default.ttf", chr(97 + i).upper(), (112 + (52*(i%9)) , 240+(52*(i/9))), size = 24)
      else:
        buttonfont = self.engine.renderFont("default.ttf", chr(97 + i), (112 + (52*(i%9)) , 240+(52*(i/9))), size = 24)

    active, flag = self.engine.drawButton(self.bigtextbutton, coord= (320, 180), scale = (180,48))
    if flag == True:
      if self.capson == True:
        self.capson = False
      else:
        self.capson = True

    if self.capson == True:
      self.engine.renderFont("default.ttf", "Caps Lock ON", (320, 180), size = 24, color = (0,255,0))
    else:
      self.engine.renderFont("default.ttf", "Caps Lock OFF", (320, 180), size = 24, color = (255,0,0))

    for i, choice in enumerate(self.othercommands):
      active, flag = self.engine.drawButton(self.bigtextbutton, coord= (155 + (325*i), 180), scale = (120,48))
      if flag == True:
        if i == 0:
          if self.name != []:
            self.name.reverse()
        if i == 1:
          if self.name != []:
            self.name.pop(-1)
      buttonfont = self.engine.renderFont("default.ttf", str(choice), (155 + (325*i), 180), size = 24)

    for i, choice in enumerate(self.specialcommands):
      active, flag = self.engine.drawButton(self.bigtextbutton, coord= (180 + (140*i), 420), scale = (120,48))
      if flag == True:
        if i == 0:
          self.name = []
        if i == 1:
          self.name.append(" ")
        if i == 2:
          self.name = self.name
          self.typingname = False     
      buttonfont = self.engine.renderFont("default.ttf", str(choice), (180 + (140*i), 420), size = 24)

  def drawRaceMenu(self):

    self.races = self.engine.listpath(os.path.join("Data", "Actors", "Races"), "splitfiletype", ".ini")

    for i, choice in enumerate(self.races):
      active, flag = self.engine.drawButton(self.racebutton, coord= (320, 64+(48*i)), scale = (200,32))
      if active == True:
        if flag == True:
          self.race = choice
          self.racechooser = False
          self.loadplayerini()

      buttonfont = self.engine.renderFont("menu.ttf", str(choice.split(".ini")[0]), (320, 64+(48*i)), size = 24)  

  def drawClassMenu(self):

    self.classes = self.engine.listpath(os.path.join("Data", "Actors", "Classes"), "splitfiletype", ".ini")

    for i, choice in enumerate(self.classes):
      active, flag = self.engine.drawButton(self.racebutton, coord= (320, 64+(48*i)), scale = (200,32))
      if active == True:
        if flag == True:
          self.playerclass = choice
          self.classchooser = False
          self.loadplayerini()
      buttonfont = self.engine.renderFont("menu.ttf", str(choice.split(".ini")[0]), (320, 64+(48*i)), size = 24)  
  
  def loadplayerini(self):
    raceini = Config.Configuration(os.path.join("Data", "Actors", "Races", self.race)).race
    classini = Config.Configuration(os.path.join("Data", "Actors", "Classes", self.playerclass)).defclass
    self.stat = []
    self.hp = self.stat.append(int(raceini.hp) + int(classini.hp))
    self.sp =  self.stat.append(int(raceini.sp) + int(classini.sp))
    self.atk =  self.stat.append(int(raceini.atk) + int(classini.atk))
    self.defn =  self.stat.append(int(raceini.defn) + int(classini.defn))
    self.spd =  self.stat.append(int(raceini.spd) + int(classini.spd))
    self.mag =  self.stat.append(int(raceini.mag) + int(classini.mag))
    self.evd =  self.stat.append(int(raceini.evd) + int(classini.evd))
 
  def endcreation(self, name):
    Config.Configuration(os.path.join("Data", "Actors", "Players", name + ".ini")).save()
    newconf = Config.Configuration(os.path.join("Data", "Actors", "Players", name + ".ini"))
    newconf.player.lvl = str(1)
    newconf.player.race = str(self.race)
    newconf.player.playerclass = str(self.playerclass)
    newconf.player.weapon = "None"
    newconf.player.armor = "None"
    newconf.player.exp = str(0)
    for i in range(0, 7):
      newconf.player.__setattr__(self.stattitle[i].lower(), self.stat[i])
    newconf.player.currenthp = str(int(self.stat[0]))
    newconf.player.currentsp = str(int(self.stat[1]))
    newconf.player.monsterskilled = str(0)
    newconf.player.inventory = str('item001, item001, item001, item002, item002')
    newconf.player.spells = str('')
    newconf.player.gold = str(250)
    newconf.save()
    Actor.party.append(str(name+".ini"))
    from Maplist import Maplist
    self.engine.changescene(self, Maplist())

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))

    if self.typingname == True:
      self.TypeName()
    elif self.racechooser == True:
      self.drawRaceMenu()
    elif self.classchooser == True:
      self.drawClassMenu()
    else:
      self.engine.renderFont("default.ttf", "Create A Character", (170, 50), size = 24)

      self.engine.drawWindow(self.statwindow, coord = (455, 250))
      commands = ["Change Name", "Change Race", "Change Class", "Create"]
      for i, command in enumerate(commands):
        x = 110
        if i == 3:
          y = 250
        else:
          y = 100
        active, flag = self.engine.drawButton(self.menubutton, coord= (x, y + (50*i)), scale = (150,45))
        if flag == True:
          if i == 0:
            self.typingname = True
          elif i == 1:
            self.racechooser = True
          elif i == 2:
            self.classchooser = True
          elif i == 3:
            name = string.join(self.name, '')
            if name != '':
              self.endcreation(name)
        buttonfont = self.engine.renderFont("default.ttf", command, (x, y + (50*i)))

      otherfont = self.engine.renderFont("menu.ttf", "Name", (400, 80), size = 24)
      name = string.join(self.name, '')
      namefont = self.engine.renderFont("default.ttf", name, (450, 100), size = 28)

      otherfont = self.engine.renderFont("menu.ttf", "Race", (400, 130), size = 24)
      name = self.race.split(".")
      namefont = self.engine.renderFont("default.ttf", name[0], (450, 150), size = 28)

      otherfont = self.engine.renderFont("menu.ttf", "Class", (400, 180), size = 24)
      name = self.playerclass.split(".")
      namefont = self.engine.renderFont("default.ttf", name[0], (450, 200), size = 28)

      for i, stat in enumerate(self.stat):
        self.engine.renderFont("default.ttf", self.stattitle[i], (350, 240 + (i*32)), size = 24)

        self.engine.renderFont("default.ttf", str(stat), (560, 240 + (i*32)), size = 24)


