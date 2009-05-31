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

enemy = "default"
enemyini = Configuration(os.path.join("Data", "Enemies", enemy+".ini")).enemy

name = enemy.split(".ini")[0]
hp = enemyini.__getattr__("hp", "int")
sp = enemyini.__getattr__("sp", "int")
atk = enemyini.__getattr__("atk", "int")
defn = enemyini.__getattr__("defn", "int")
spd = enemyini.__getattr__("spd", "int")
mag = enemyini.__getattr__("mag", "int")
evd = enemyini.__getattr__("evd", "int")
coord = enemyini.__getattr__("coord").split(",")

