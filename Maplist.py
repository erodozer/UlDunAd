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

class Maplist(Layer):
  def __init__(self):
    self.engine = GameEngine
    self.background = self.engine.loadImage(os.path.join("Data", "mapbackground.png"))
    self.background2 = self.engine.loadImage(os.path.join("Data", "mapmenu.png"))
    #self.audio = self.engine.loadAudio("mapmenu.mp3")

    self.button, self.buttonactive = Menu.initMenu(os.path.join("Data", "mapmenubutton.png"), os.path.join("Data", "mapmenubuttonactive.png"))

  def update(self):
    self.engine.drawImage(self.background)
    self.engine.drawImage(self.background2)

    mappath = os.path.join("Data", "Towns")
    self.maps = []
    defaultTheme = None
    allmaps = os.listdir(mappath)
    for name in allmaps:
      if os.path.exists(os.path.join(mappath,name,"town.ini")):
        self.maps.append(name)

    self.menu = Menu.drawMapMenu(self, self.maps, self.button, self.buttonactive)

  def clearscene(self):
    
    del  self.menu, self.background, self.background2, self.maps, self.engine

