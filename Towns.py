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

import Config

import Shop

class Towns(Layer):
  def __init__(self, townname):

    self.engine = GameEngine
    self.townname = townname

    self.townini = Config.Configuration(os.path.join("Data", "Towns", self.townname, "town.ini")).town

    self.background = None
    if self.townini.background != "None":
      self.background = self.engine.loadImage(os.path.join("Data", "Towns", self.townname, self.townini.background))
    self.sidebar = self.engine.loadImage(os.path.join("Data", "sidemenu.png"))

    self.audio = None
    if self.townini.audio != "None":
      self.audio = self.engine.loadAudio(self.townini.audio)

    self.choices = self.townini.choices.split(",")

    if os.path.exists(os.path.join("Data", "Towns", self.townname, "townbutton.png")) == True:
      self.menubutton = os.path.join("Data", "Towns", self.townname, "townbutton.png")
    else:
      self.menubutton = os.path.join("Data", "defaultbutton.png")

    if os.path.exists(os.path.join("Data", "Towns", self.townname, "townbuttonactive.png")) == True:
      self.menubuttonactive = os.path.join("Data", "Towns", self.townname, "townbuttonactive.png")
    else:
      self.menubuttonactive = os.path.join("Data", "defaultbuttonactive.png")

    self.button, self.buttonactive = Menu.initMenu(self.menubutton, self.menubuttonactive)

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))
    self.engine.drawImage(self.sidebar, coord = (100, 240))

    self.menu = Menu.drawTownMenu(self, self.choices, self.townini, self.button, self.buttonactive)

    self.towntitle = self.engine.renderFont("menu.ttf", self.townname, (430, 64), size = 32)

  def openshop(self, whichshop):
    View.removescene(self)
    View.addscene(Shop.Shop(os.path.join("Data", "Towns", self.townname, whichshop)))
    

  def clearscene(self):
    del self.menu, self.towntitle, self.menubuttonactive, self.menubutton, self.button, self.buttonactive, self.audio, self.sidebar, self.background, self.townini, self.townname, self.engine

