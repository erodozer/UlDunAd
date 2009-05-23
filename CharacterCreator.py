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
import Menu

import Config

import string

class CharacterCreator(Layer):

  def __init__(self):
    self.engine = GameEngine
    self.race = "Hume.ini"
    raceini = Config.Configuration(os.path.join("Data", "Races", self.race)).race

    self.hp = raceini.hp
    self.sp = raceini.sp
    self.atk = raceini.atk
    self.defn = raceini.defn
    self.spd = raceini.spd
    self.mag = raceini.mag
    self.evd = raceini.evd

    self.capson = True

    self.name = []
    self.capletters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', ' ']
    self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ' ']

    self.othercommands = ["Clear", "Delete", "Confirm"]
    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))
    
    self.textbutton = self.engine.loadImage(os.path.join("Data", "textbutton.png"))
    self.textbuttonactive = self.engine.loadImage(os.path.join("Data", "textbuttonactive.png"))

    self.menubutton = self.engine.loadImage(os.path.join("Data", "menubutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "menubuttonactive.png"))

    self.typingname = False

  def TypeName(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))
    name = string.join(self.name, '')
    namefont = GameEngine.renderFont("default.ttf", name, (320 , 96), size = 32)

    for i, choice in enumerate(self.capletters):
      if i <= 8:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*i) , 164), scale = (32,32))
      if 9 <= i <= 17:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i-9)) , 200), scale = (32,32))
      if 18 <= i <= 26:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i-18)) , 236), scale = (32,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        if i <= 8:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*i) , 164), scale = (32,32))
        if 9 <= i <= 17:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i-9)) , 200), scale = (32,32))
        if 18 <= i <= 26:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i-18)) , 236), scale = (32,32))
        if flag == True:
          self.name.append(self.capletters[i])

      if i <= 8:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*i) , 164), size = 24)
      if 9 <= i <= 17:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*(i-9)) , 200), size = 24)
      if 18 <= i <= 26:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*(i-18)) , 236), size = 24)

    for i, choice in enumerate(self.letters):
      if i <= 8:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*i) , 272), scale = (32,32))
      if 9 <= i <= 17:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i-9)) , 308), scale = (32,32))
      if 18 <= i <= 26:
        button = self.engine.drawImage(self.textbutton, coord= (218 + (36*(i-18)) , 344), scale = (32,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        if i <= 8:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*i) , 272), scale = (32,32))
        if 9 <= i <= 17:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i-9)) , 308), scale = (32,32))
        if 18 <= i <= 26:
          button = self.engine.drawImage(self.textbuttonactive, coord= (218 + (36*(i-18)) , 344), scale = (32,32))
        if flag == True:
          self.name.append(self.capletters[i])

      if i <= 8:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*i) , 272), size = 24)
      if 9 <= i <= 17:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*(i-9)) , 308), size = 24)
      if 18 <= i <= 26:
        buttonfont = GameEngine.renderFont("default.ttf", str(choice), (218 + (36*(i-18)) , 344), size = 24)
      
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
      buttonfont = GameEngine.renderFont("default.ttf", str(choice), (90, 186 + (76*i)), size = 24)

     
  def update(self):
    self.engine.drawImage(os.path.join(self.background), scale = (640,480))

    if self.typingname == True:
      self.TypeName()

    else:
      button = self.engine.drawImage(self.menubutton, coord= (90, 130), scale = (150,45))
      buttonfont = GameEngine.renderFont("default.ttf", "Change Name", (90, 130))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (90, 130), scale = (150,45))
        if flag == True:
          self.typingname = True

      otherfont = GameEngine.renderFont("default.ttf", "Name", (200, 130), size = 24)

      name = string.join(self.name, '')
      namefont = GameEngine.renderFont("default.ttf", name, (380, 130), size = 32)

