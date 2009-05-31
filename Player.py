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

from Config import *
import os
import math

player = GameEngine.player
playerini = Configuration(os.path.join("Data", "Players", player)).player

name = player.split(".ini")[0]
raceini = Configuration(os.path.join("Data", "Races", str(playerini.race))).race
levelcurve = raceini.__getattr__("levelcurve").split(",")
for i, num in enumerate(levelcurve):
  levelcurve[i] = float(num)
lvl = playerini.__getattr__("lvl", "int")
hp = raceini.__getattr__("hp", "int") + int(levelcurve[0]*lvl)
sp = raceini.__getattr__("sp", "int") + int(levelcurve[1]*lvl)
atk = raceini.__getattr__("atk", "int") + int(levelcurve[2]*lvl)
defn = raceini.__getattr__("defn", "int") + int(levelcurve[3]*lvl)
spd = raceini.__getattr__("spd", "int") + int(levelcurve[4]*lvl)
mag = raceini.__getattr__("mag", "int") + int(levelcurve[5]*lvl)
evd = raceini.__getattr__("evd", "int") + int(levelcurve[6]*lvl)
weapon = playerini.weapon
armor = playerini.armor

