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
import random

class Maplist(Layer):
  def __init__(self):
    self.engine = GameEngine
    self.background = self.engine.loadImage(os.path.join("Data", "mapbackground.png"))
    self.background2 = self.engine.loadImage(os.path.join("Data", "mapmenu.png"))
    #self.audio = self.engine.loadAudio("mapmenu.mp3")

    self.button, self.buttonactive = Menu.initMenu(os.path.join("Data", "mapmenubutton.png"), os.path.join("Data", "mapmenubuttonactive.png"))
    self.menubutton = self.engine.loadImage(os.path.join("Data", "menubutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "menubuttonactive.png"))

  def update(self):
    self.engine.drawImage(self.background)
    self.engine.drawImage(self.background2)

    mappath = os.path.join("Data", "Towns")
    self.maps = []
    allmaps = os.listdir(mappath)
    for name in allmaps:
      if os.path.exists(os.path.join(mappath,name,"town.ini")):
        self.maps.append(name)

    self.menu = Menu.drawMapMenu(self, self.maps, self.button, self.buttonactive)

    enemypath = os.path.join("Data", "Enemies")
    self.enemies = []
    allenemies = os.listdir(enemypath)
    for name in allenemies:
      if os.path.splitext(name)[1].lower() == ".ini":
        self.enemies.append(name)

    #activate beta battlescene
    button = self.engine.drawImage(self.menubutton, coord= (530, 425), scale = (150,45))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.menubuttonactive, coord= (530, 425), scale = (150,45))
      if flag == True:
        GameEngine.enemy = str(random.choice(self.enemies))
        View.removescene(self)
        import BattleScene
        View.addscene(BattleScene.BattleScene())
    buttonfont = self.engine.renderFont("default.ttf", "Random Battle", (530, 425))


  def clearscene(self):
    
    del  self.menu, self.background, self.background2, self.maps, self.engine

