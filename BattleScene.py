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

import Player
import Enemy

from View import *
import os
import sys
import math
import random

from Config import *

class BattleScene(Layer):
  def __init__(self, enemy = "default", terrain = "grasslands.jpg"):

    self.engine = GameEngine
    try:
      self.audio = self.engine.loadAudio("battle.mp3")
    except IOError:
      pass

    self.background = self.engine.loadImage(os.path.join("Data", "Terrains", terrain))

    Enemy.enemy = enemy
    self.enemysprite = self.engine.loadImage(os.path.join("Data",  "Enemies", enemy+".png"))
    self.enemycurrenthp = Enemy.hp
    self.enemymaxhp = Enemy.hp
    self.enemycoord = Enemy.coord

    self.playercurrenthp = Player.hp
    self.playermaxhp = Player.hp

    self.button = self.engine.loadImage(os.path.join("Data", "battlebutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "battlebuttonactive.png"))

    self.hpbar = self.engine.loadImage(os.path.join("Data", "hpbar.png"))

    self.hud = self.engine.loadImage(os.path.join("Data", "battlehud.png"))

    self.battle = False

    self.playercommand = 0
    self.enemycommand = 1

    self.displaydamage = False
    self.turnstep = 0
  def fight(self, playercommand, enemycommand, roll):
    self.turnstep = self.turnstep + 1
    if roll == 0:
      if self.enemycommand == 1:
        self.attack(0)

    if roll == 1:
      if self.playercommand == 1:
        self.attack(1)
    
  def attack(self, who):
    if who == 0:
      damage = (Enemy.atk*3)/Player.defn
      self.playercurrenthp = self.playercurrenthp - damage
    elif who == 1:
      damage = (Player.atk*3)/Enemy.defn
      self.enemycurrenthp = self.enemycurrenthp - damage

    self.displaydamage = True
    self.displayturn(damage, who)
    if self.turnstep < 2:
      self.fight(self.playercommand, self.enemycommand, 1-who)
    else:
      self.battle = False
      self.turnstep = 0

  def displayturn(self,damage, who):
    if who == 0:
      self.engine.renderFont("default.ttf", str(damage), (280, 240), size = 24)
    else:
      self.engine.renderFont("default.ttf", str(damage), (290, 350), size = 24)

  def update(self):

    if self.playercurrenthp <= 0:
      self.playercurrenthp = 0
    elif self.enemycurrenthp <= 0:
      self.enemycurrenthp = 0

    self.engine.drawImage(self.background, scale = (640,480))
    self.engine.drawImage(self.hud, (150, 380))
    self.engine.drawImage(self.hpbar, (200, 360), scale = ((self.playercurrenthp/self.playermaxhp)*300,10))
    self.engine.drawImage(self.enemysprite, (int(self.enemycoord[0]), int(self.enemycoord[1])))

    self.engine.renderFont("default.ttf", str(self.playercurrenthp) + "/" + str(self.playermaxhp), (200, 350), size = 24)
    self.engine.renderFont("default.ttf", "HP", (30, 350), size = 24)

    self.engine.renderFont("default.ttf", str(Player.lvl), (33, 297), size = 24)
    self.engine.renderFont("default.ttf", str(Player.name), (250, 297), size = 24)

    commands = ["Attack", "Defend", "Skills", "Item"]
    if self.battle == False:
      for i, choice in enumerate(commands):
        button = self.engine.drawImage(self.button, coord= (550 - (20*i), 350 + (30*i)), scale = (150,25))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(self.buttonactive, coord= (550 - (20*i), 350 + (30*i)), scale = (150,25))
          if flag == True:
            self.playercommand = 1
            self.battle = True
            roll = random.randint(0,1)
            self.fight(self.playercommand, self.enemycommand, roll)
        buttonfont = self.engine.renderFont("default.ttf", choice, (550 - (20*i), 350 + (30*i)))

      button = self.engine.drawImage(self.button, coord= (100, 445), scale = (150,25))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.buttonactive, coord= (100, 445), scale = (150,25))
        if flag == True:
          self.battle = True

          self.attack(roll)
      buttonfont = self.engine.renderFont("default.ttf", "Flee", (100, 445))

    if self.displaydamage == True:
      pass
