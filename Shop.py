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

class Shop(Layer):
  def __init__(self, shopini):

    self.engine = GameEngine
    self.shopini = shopini

    self.engine.loadImage(os.path.join("Data", "menubackground.png"))

    self.engine.renderFont("arial.ttf", "Welcome", (480,48), size = 32)
    self.choices = ["Buy", "Sell", "Exit"]

    self.selectedchoice = 0

    self.items = self.shopini.townchoice.__getattr__("items").split(", ")

  def update(self):
    if self.selectedchoice == 0:
      for i, choice in enumerate(self.choices):
        button = self.engine.drawImage(os.path.join("Data", "menubutton.png"), coord= (95 +(200*i), 400), scale = (150,45))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(os.path.join("Data", "menubuttonactive.png"), coord= (95 +(200*i), 400), scale = (150,45))
          if flag == True:
            if i == 0:
              pass
            elif i == 1:
              pass
            elif i == 2:
              import Towns
              View.removescene(self)
              View.addscene(Towns.Towns())
        buttonfont = self.engine.renderFont("default.ttf", choice, (95 +(200*i), 400))
