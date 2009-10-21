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
import random

class Enemy:
  def __init__(self, enemy):

    self.enemyini = Configuration(os.path.join("..", "Data", "Enemies", "Info", enemy + ".ini")).enemy

    self.name = enemy
    self.hp = self.enemyini.__getattr__("hp", "int")
    self.sp = self.enemyini.__getattr__("sp", "int")
    self.atk = self.enemyini.__getattr__("atk", "int")
    self.defn = self.enemyini.__getattr__("defn", "int")
    self.spd = self.enemyini.__getattr__("spd", "int")
    self.mag = self.enemyini.__getattr__("mag", "int")
    self.evd = self.enemyini.__getattr__("evd", "int")
    self.exp = self.enemyini.__getattr__("exp", "int")
    self.lvl = self.enemyini.__getattr__("lvl", "int")
    self.image = self.enemyini.__getattr__("image")

    #item drops and rate of drop per item
    self.loot = self.enemyini.__getattr__("loot").replace(" ", "").split(",")
    self.lootchances = self.enemyini.__getattr__("lootchances").replace(" ", "").split(",")
    if self.loot == [''] or self.lootchances == ['']:
      self.lootchances = None
      self.loot = None

    #these are very important for battle
    self.currentatb = random.randint(0,100)
    self.defending = False
    self.currenthp = self.hp
    self.currentsp = self.sp

    #these numbers are for testing reasons, uncomment them if you require it
    #self.name = "AAAAAAAAAAAA"
    #self.hp = int(9999)
    #self.sp = int(999)


