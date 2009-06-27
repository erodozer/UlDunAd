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

class Towns(Layer):
  def __init__(self):

    self.engine = GameEngine
    self.townname = self.engine.town

    self.townini = Config.Configuration(os.path.join("Data", "Towns", self.townname, "town.ini")).town

    self.background = None
    if self.townini.background != "None":
      self.background = self.engine.loadImage(os.path.join("Data", "Towns", self.townname, self.townini.background))
    self.sidebar = self.engine.loadImage(os.path.join("Data", "sidemenu.png"))

    self.audio = None
    if self.townini.audio != "None":
      self.audio = self.engine.loadAudio(self.townini.audio)

    self.choices = self.townini.choices.split(", ")

    if os.path.exists(os.path.join("Data", "Towns", self.townname, "townbutton.png")) == True:
      self.menubutton = self.engine.loadImage(os.path.join("Data", "Towns", self.townname, "townbutton.png"))
    else:
      self.menubutton = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))

    if os.path.exists(os.path.join("Data", "Towns", self.townname, "townbuttonactive.png")) == True:
      self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "Towns", self.townname, "townbuttonactive.png"))
    else:
      self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))


  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))
    self.engine.drawImage(self.sidebar, coord = (100, 240))

    for i, choice in enumerate(self.choices):
      button = self.engine.drawImage(self.menubutton, coord= (100, 90+(60*i)), scale = (150,45))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.menubuttonactive, coord= (100, 90+(60*i)), scale = (150,45))
        if flag == True:
          if choice == "Library" or choice == "library":
            from Library import Library
            View.removescene(self)
            View.addscene(Library())
          else:
            choiceini = Config.Configuration(os.path.join("Data", "Towns", self.townname, choice+".ini"))
            if choiceini.townchoice.type == "Shop":
              from Shop import Shop
              View.removescene(self)
              View.addscene(Shop(choiceini))

      buttonfont = self.engine.renderFont("default.ttf", choice, (100, 90+(60*i)))

    #return button
    returnbutton = self.engine.drawImage(self.menubutton, coord= (100, 420), scale = (150,45))
    active, flag = self.engine.mousecol(returnbutton)
    if active == True:
      returnbutton = self.engine.drawImage(self.menubuttonactive, coord= (100, 420), scale = (150,45))
      if flag == True:
        from Maplist import Maplist
        View.removescene(self)
        View.addscene(Maplist())
    returnfont = self.engine.renderFont("default.ttf", "Return", (100, 420))

    self.towntitle = self.engine.renderFont("menu.ttf", self.townname, (430, 64), size = 32)

  def clearscene(self):
    del self.towntitle, self.menubuttonactive, self.menubutton
    if self.audio != None:
      self.engine.stopmusic()
    del self.audio, self.sidebar, self.background, self.townini, self.townname, self.engine

