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

import os
import math

class Data:
  def __init__(self, Drawing):

    self.battlebutton = Drawing.loadImage(os.path.join("Data", "battlebutton.png"))
    self.mapbutton = Drawing.loadImage(os.path.join("Data", "mapmenubutton.png"))
    self.secondarybutton = Drawing.loadImage(os.path.join("Data", "secondarybutton.png"))
    self.defaultbutton = Drawing.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.menubutton = Drawing.loadImage(os.path.join("Data", "menubutton.png"))
    self.secondarymenubutton = Drawing.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.textbutton = Drawing.loadImage(os.path.join("Data", "textbutton.png"))
    self.bigtextbutton = Drawing.loadImage(os.path.join("Data", "bigtextbutton.png"))

    self.window = Drawing.loadImage(os.path.join("Data", "window.png"))

