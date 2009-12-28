#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

from GameEngine import GameEngine

from Config import *
import os
import math
import random

actorPath = os.path.join("Data", "Actors")
party = []
class Actor:
  def __init__(self, actorini):

    self.hp = actorini.__getattr__("hp", "int")
    self.sp = actorini.__getattr__("sp", "int")
    self.atk = actorini.__getattr__("atk", "int")
    self.defn = actorini.__getattr__("defn", "int")
    self.spd = actorini.__getattr__("spd", "int")
    self.mag = actorini.__getattr__("mag", "int")
    self.evd = actorini.__getattr__("evd", "int")
    self.exp = actorini.__getattr__("exp", "int")
    self.lvl = actorini.__getattr__("lvl", "int")

    #these are very important for battle
    self.currentATB = random.randint(0,100)
    self.defending = False
    self.currenthp = self.hp
    self.currentsp = self.sp
    self.knockedout = False

    self.spells = actorini.__getattr__("spells").replace(" ", "").split(",")
    if actorini.__getattr__("spells") == "":
      self.spells = "None"

class Player(Actor):
  def __init__(self, player):
    self.player = player
    self.playerini = Configuration(os.path.join(actorPath, "Players", self.player)).player
    Actor.__init__(self, self.playerini)

    self.name = self.player.split(".ini")[0]
    self.race = self.playerini.race.split(".ini")[0] 
    self.raceini = Configuration(os.path.join(actorPath, "Races", self.race + ".ini")).race

    self.levelcurve = self.raceini.__getattr__("levelcurve").replace(" ", "").split(",")
    for i, num in enumerate(self.levelcurve):
      self.levelcurve[i] = float(num)

    self.playerclass = self.playerini.playerclass.split(".ini")[0] 
    self.classini = Configuration(os.path.join(actorPath, "Classes", str(self.playerini.playerclass))).defclass
    self.classcurve = self.classini.__getattr__("levelcurve").replace(" ", "").split(",")
    for i, num in enumerate(self.levelcurve):
      self.classcurve[i] = float(num)

    self.classpic = None
    if os.path.exists(os.path.join(actorPath, "Classes", self.playerclass + ".png")) == True:
      self.classpic = GameEngine().loadImage(os.path.join(actorPath, "Classes", self.playerclass + ".png"))

    self.lvl = self.playerini.__getattr__("lvl", "int")

    self.hp += int(self.levelcurve[0]*(self.lvl-1)) + int(self.classcurve[0]*(self.lvl-1))
    self.currenthp = self.playerini.__getattr__("currenthp", "int")
    if self.currenthp > self.hp:
      self.currenthp = self.hp
      self.playerini.save()

    self.sp += int(self.levelcurve[1]*(self.lvl-1)) + int(self.classcurve[1]*(self.lvl-1))
    self.currentsp = self.playerini.__getattr__("currentsp", "int")
    if self.currentsp > self.sp:
      self.currentsp = self.sp
      self.playerini.save()

    self.atk  += int(self.levelcurve[2]*(self.lvl-1)) + int(self.classcurve[2]*(self.lvl-1))
    self.defn += int(self.levelcurve[3]*(self.lvl-1)) + int(self.classcurve[3]*(self.lvl-1))
    self.spd  += int(self.levelcurve[4]*(self.lvl-1)) + int(self.classcurve[4]*(self.lvl-1))
    self.mag  += int(self.levelcurve[5]*(self.lvl-1)) + int(self.classcurve[5]*(self.lvl-1))
    self.evd  += int(self.levelcurve[6]*(self.lvl-1)) + int(self.classcurve[6]*(self.lvl-1))

    self.weapon = self.playerini.weapon
    self.armor = self.playerini.armor
    self.explvl = 15*int(self.lvl**2)
    self.inventory = self.playerini.__getattr__("inventory").replace(" ", "").split(",")
    if self.playerini.__getattr__("inventory").isspace() == True:
      self.inventory = "None"
    self.monsterskilled = self.playerini.__getattr__("monsterskilled", "int")

    self.gold = self.playerini.__getattr__("gold", "int")
    if self.gold == '':
      self.gold = 0

    #these numbers are for testing reasons, uncomment them if you require it
    #self.name = "AAAAAAAAAAAA"
    #self.exp = self.explvl-1
    #self.hp = int(9999)
    #self.currenthp = int(9999)
    #self.sp = int(999)
    #self.currentsp = int(999)

  def updateINI(self, victory = False, levelup = False):
    self.playerini = Configuration(os.path.join(actorPath, "Players", self.player))

    if self.knockedout == True:
      self.playerini.player.__setattr__("currenthp", int(1))
      self.knockedout = False
    else:
      self.playerini.player.__setattr__("currenthp", self.currenthp)

    self.playerini.player.__setattr__("currentsp", self.currentsp)
    if victory == True:
      self.playerini.player.__setattr__("monsterskilled", self.monsterskilled + 1)
    self.playerini.player.__setattr__("inventory", ", ".join(self.inventory))
    self.playerini.player.__setattr__("gold", self.gold)
    if levelup == True:
      self.playerini.player.__setattr__("lvl", self.lvl+1)
      self.playerini.player.__setattr__("currenthp", self.hp)
      self.playerini.player.__setattr__("currentsp", self.sp)

    self.playerini.save()

    self.playerini = Configuration(os.path.join(actorPath, "Players", self.player)).player

class Enemy(Actor):
  def __init__(self, enemy):
    self.enemyini = Configuration(os.path.join(actorPath, "Enemies", "Info", enemy + ".ini")).enemy

    Actor.__init__(self, self.enemyini)    

    self.name = enemy
    self.image = GameEngine().loadImage(os.path.join(actorPath, "Enemies", "Graphics", self.enemyini.__getattr__("image")))

    #item drops and rate of drop per item
    self.loot = self.enemyini.__getattr__("loot").replace(" ", "").split(",")
    self.lootchances = self.enemyini.__getattr__("lootchances").replace(" ", "").split(",")
    if self.loot == [''] or self.lootchances == ['']:
      self.lootchances = None
      self.loot = None


    #these numbers are for testing reasons, uncomment them if you require it
    #self.name = "AAAAAAAAAAAA"
    #self.hp = int(9999)
    #self.sp = int(999)


