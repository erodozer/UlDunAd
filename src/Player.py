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

class Player:
  def __init__(self, player = GameEngine.party[0]):

    self.playerini = Configuration(os.path.join("..", "Data", "Players", player))

    self.name = player.split(".ini")[0]
    self.race = self.playerini.player.race.split(".ini")[0] 
    self.raceini = Configuration(os.path.join("..", "Data", "Races", self.race + ".ini")).race

    self.levelcurve = self.raceini.__getattr__("levelcurve").replace(" ", "").split(",")
    for i, num in enumerate(self.levelcurve):
      self.levelcurve[i] = float(num)

    self.playerclass = self.playerini.player.playerclass.split(".ini")[0] 
    self.classini = Configuration(os.path.join("..", "Data", "Classes", str(self.playerini.player.playerclass))).defclass
    self.classcurve = self.classini.__getattr__("levelcurve").replace(" ", "").split(",")
    for i, num in enumerate(self.levelcurve):
      self.classcurve[i] = float(num)

    self.classpic = None
    if os.path.exists(os.path.join("..", "Data", "Classes", self.playerclass + ".png")) == True:
      self.classpic = GameEngine.loadImage(os.path.join("Data", "Classes", self.playerclass + ".png"))

    self.lvl = self.playerini.player.__getattr__("lvl", "int")

    self.hp = self.playerini.player.__getattr__("hp", "int") + int(self.levelcurve[0]*(self.lvl-1)) + int(self.classcurve[0]*(self.lvl-1))
    self.currenthp = self.playerini.player.__getattr__("currenthp", "int")
    if self.currenthp > self.hp:
      self.currenthp = self.hp
      self.playerini.save()

    self.sp = self.playerini.player.__getattr__("sp", "int") + int(self.levelcurve[1]*(self.lvl-1)) + int(self.classcurve[1]*(self.lvl-1))
    self.currentsp = self.playerini.player.__getattr__("currentsp", "int")
    if self.currentsp > self.sp:
      self.currentsp = self.sp
      self.playerini.save()

    self.atk = self.playerini.player.__getattr__("atk", "int") + int(self.levelcurve[2]*(self.lvl-1)) + int(self.classcurve[2]*(self.lvl-1))
    self.defn = self.playerini.player.__getattr__("defn", "int") + int(self.levelcurve[3]*(self.lvl-1)) + int(self.classcurve[3]*(self.lvl-1))
    self.spd = self.playerini.player.__getattr__("spd", "int") + int(self.levelcurve[4]*(self.lvl-1)) + int(self.classcurve[4]*(self.lvl-1))
    self.mag = self.playerini.player.__getattr__("mag", "int") + int(self.levelcurve[5]*(self.lvl-1)) + int(self.classcurve[5]*(self.lvl-1))
    self.evd = self.playerini.player.__getattr__("evd", "int") + int(self.levelcurve[6]*(self.lvl-1)) + int(self.classcurve[6]*(self.lvl-1))

    self.weapon = self.playerini.player.weapon
    self.armor = self.playerini.player.armor
    self.exp = self.playerini.player.__getattr__("exp", "int")
    self.explvl = 15*int(self.lvl**2)
    self.inventory = self.playerini.player.__getattr__("inventory").replace(" ", "").split(",")
    if self.playerini.player.__getattr__("inventory").isspace() == True:
      self.inventory = "None"
    self.monsterskilled = self.playerini.player.__getattr__("monsterskilled", "int")
    self.spells = self.playerini.player.__getattr__("spells").replace(" ", "").split(",")
    if self.playerini.player.__getattr__("spells") == "":
      self.spells = "None"

    self.gold = self.playerini.player.__getattr__("gold", "int")
    if self.gold == '':
      self.gold = 0

    #these are very important for battle
    self.currentatb = random.int(0,100)
    self.defending = False
    self.knockedout = False

    #these numbers are for testing reasons, uncomment them if you require it
    #self.name = "AAAAAAAAAAAA"
    #self.exp = self.explvl-1
    #self.hp = int(9999)
    #self.currenthp = int(9999)
    #self.sp = int(999)
    #self.currentsp = int(999)


