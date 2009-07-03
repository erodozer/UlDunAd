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
      
class MainMenu:
  def __init__(self):
    self.engine = GameEngine
    #self.background = self.engine.loadImage(os.path.join("Data", "menubackground.png"))
    #self.engine.drawImage(os.path.join("Data", "mapmenu.png"))
    #self.audio = self.engine.loadAudio("Town001.mp3")
    self.choices = ["New Game", "Continue", "Quit"]
    self.button = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))

  def update(self):
    #self.engine.drawImage(self.background)
    w, h = self.engine.w, self.engine.h
    self.engine.renderMultipleFont("default.ttf", ("Welcome to", "Ultimate Dungeon Adventure"), coord = (320, 100), size = 24)

    for i, choice in enumerate(self.choices):
      button = GameEngine.drawImage(self.button, coord= (220, 200+(60*i)), scale = (150,45))
      active, flag = GameEngine.mousecol(button)
      if active == True:
        button = GameEngine.drawImage(self.buttonactive, coord= (220, 200+(60*i)), scale = (150,45))
        if flag == True:
          if i == 0:
            from CharacterCreator import CharacterCreator
            View.removescene(self)
            View.addscene(CharacterCreator())
          if i == 1:
            playerpath = os.path.join("Data", "Players")
            players = []
            allplayers = os.listdir(playerpath)
            for name in allplayers:
              if os.path.splitext(name)[1].lower() == ".ini":
                players.append(name)

            if players != []:
              from Playerlist import Playerlist
              View.removescene(self)
              View.addscene(Playerlist())

          elif i == 2:
             GameEngine.finished = True
      buttonfont = GameEngine.renderFont("default.ttf", str(choice), (220, 200+(60*i)))

  def clearscene(self):
    del self.button, self.buttonactive, self.engine, self.choices
