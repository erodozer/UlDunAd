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

class Playerlist(Layer):
  def __init__(self):
    self.engine = GameEngine
    #self.audio = self.engine.loadAudio("mapmenu.mp3")

    self.background = self.engine.loadImage(os.path.join("Data", "mapbackground.png"))
    self.background2 = self.engine.loadImage(os.path.join("Data", "mapmenu.png"))

    self.button, self.buttonactive = Menu.initMenu(os.path.join("Data", "mapmenubutton.png"), os.path.join("Data", "mapmenubuttonactive.png"))
  def update(self):
    self.engine.drawImage(self.background)
    self.engine.drawImage(self.background2)

    playerpath = os.path.join("Data", "Players")
    self.players = []
    defaultPlayer = None
    allplayers = os.listdir(playerpath)
    for name in allplayers:
      if os.path.splitext(name)[1].lower() == ".ini":
        self.players.append(os.path.splitext(name)[0])

    button = self.players
    buttonfont = self.players

    index = 0
    if index < 0:
      index = 0
    if index > len(self.players):
      index = len(self.players) - 7

    for i,choice in enumerate(self.players):
      button[i] = self.engine.drawImage(self.button, coord= (320, 64+(48*(i+1))), scale = (200,32))
      active, flag = self.engine.mousecol(button[i])
      if active == True:
        button[i] = self.engine.drawImage(self.buttonactive, coord= (320, 64+(48*(i+1))), scale = (200,32))
        if flag == True:
          from Maplist import Maplist
          View.removescene(self)
          View.addscene(Maplist())
          GameEngine.player = str(choice+".ini")  
      buttonfont[i] = self.engine.renderFont("menu.ttf", choice, (320, 64+(48*(i+1))), size = 24)

    button = self.engine.drawImage(self.button, coord= (320, 64), scale = (200,32))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.buttonactive, coord= (320, 64), scale = (200,32))
      if flag == True:
        index = index - 7
    buttonfont[i] = self.engine.renderFont("menu.ttf", "-UP-", (320, 64), size = 24)

    button = self.engine.drawImage(self.button, coord= (320, 432), scale = (200,32))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.buttonactive, coord= (320, 432), scale = (200,32))
      if flag == True:
        index = index - 7
    buttonfont[i] = self.engine.renderFont("menu.ttf", "-DOWN-", (320, 432), size = 24)

  def clearscene(self):
    del  self.background, self.background2, self.engine, self.players

