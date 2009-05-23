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

import Config

player = GameEngine.player
playerini = Config.Configuration(os.path.join("Data", "Players", player)).player

race = playerini.race
raceini = Config.Configuration(os.path.join("Data", "Races", race)).race
levelcurve = raceini.levelcurve.split(",")
lvl = playerini.lvl
hp = raceini.hp + (levelcurve[0]*lvl)
sp = raceini.sp + (levelcurve[1]*lvl)
atk = raceini.atk + (levelcurve[2]*lvl)
defn = raceini.defn + (levelcurve[3]*lvl)
spd = raceini.spd + (levelcurve[4]*lvl)
mag = raceini.mag + (levelcurve[5]*lvl)
evd = raceini.evd + (levelcurve[6]*lvl)
weapon = playerini.weapon
armor = playerini.armor

def showstatus():
  engine = GameEngine

