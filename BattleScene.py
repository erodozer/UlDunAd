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

from View import *
import os

from sys import *

import Enemy

import math
import random

from Config import *
import pygame

class BattleScene(Layer):
  def __init__(self, terrain = "desert.png"):

    self.engine = GameEngine
    try:
      self.audio = self.engine.loadAudio("battle.mp3")
    except IOError:
      pass

    self.background = self.engine.loadImage(os.path.join("Data", "Terrains", terrain))

    reload(Enemy)
    self.enemysprite = self.engine.loadImage(os.path.join("Data",  "Enemies", Enemy.image))
    self.enemycurrenthp = Enemy.hp
    self.enemymaxhp = Enemy.hp
    self.enemycoord = Enemy.coord

    self.playercurrenthp = Player.hp
    self.playermaxhp = Player.hp

    self.button = self.engine.loadImage(os.path.join("Data", "battlebutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "battlebuttonactive.png"))

    self.hpbar = self.engine.loadImage(os.path.join("Data", "hpbar.png"))
    self.hpbarback = self.engine.loadImage(os.path.join("Data", "hpbarback.png"))

    self.hud = self.engine.loadImage(os.path.join("Data", "battlehud.png"))
    self.attackcb = self.engine.loadImage(os.path.join("Data", "battlecirclebottom.png"))
    self.attackct = self.engine.loadImage(os.path.join("Data", "battlecircletop.png"))

    self.battle = False

    self.playercommand = 0
    self.enemycommand = 1

    self.displaydamage = 0
    self.turnstep = 0
    self.timer = 0.0
    self.rotatestart = 0
    self.rolled = False
    self.fade = False
    self.stop = False
    self.spacehit = False
    self.defend = False

    self.barframe = 1
    GameEngine.resetKeyPresses()

  def fight(self, playercommand, enemycommand, roll):
    if roll == 0:
      if self.enemycommand == 1:
        self.attack(0)

    if roll == 1:
      if self.playercommand == 1 or self.playercommand == 2:
        self.renderbattlecircle()
        #self.attack(1)

  def renderbattlecircle(self):
    if self.stop == False:
      var = 60
      self.engine.renderFont("default.ttf", "Press Space to Stop", (320, 64), size = 24)
      if self.playercommand == 1: 
        self.engine.renderFont("default.ttf", "Attack", (320, 96), size = 24) 
      elif self.playercommand == 2:
        self.engine.renderFont("default.ttf", "Defend", (320, 96), size = 24) 
    else:
      var = 0
    self.timer = self.timer + var
    time = math.radians(self.timer/3)
    rotate = self.rotatestart + ((self.timer/5))
    rotcount = int(rotate/360)
    rotwatch = rotate - (360*rotcount)
    timer = 3200 - self.timer
    if timer <= 0 or self.spacehit == True:
      self.stop = True
      if not rotwatch in range(46,314):
        if self.playercommand == 1:
          self.attack(1)
        else:
          self.defend = True
          self.turnstep = 2
          self.spacehit = False
      else:
        self.displayturn("Miss", 1)
    else:
      self.engine.drawImage(self.attackcb, (int(self.enemycoord[0]), int(self.enemycoord[1])), scale = (200*(.25*math.sin(time+.5)+1),200*(.25*math.sin(time+.5)+1)))
      self.engine.drawImage(self.attackct, (int(self.enemycoord[0]), int(self.enemycoord[1])), scale = (200*(.25*math.sin(time+.5)+1),200*(.25*math.sin(time+.5)+1)), rot = -rotate)

  def attack(self, who):
    if who == 0:
      if self.defend == True:
        damage = (Enemy.atk*3)/(Player.defn*2)
      else:
        damage = (Enemy.atk*3)/Player.defn
    elif who == 1:
      damage = (Player.atk*3)/Enemy.defn

    self.displayturn(damage, who)

  def displayturn(self, damage, who):
    self.displaydamage = self.displaydamage + 20
    if who == 1:
      self.engine.screenfade((255,255,255,255-(self.displaydamage*5)))
      self.engine.renderFont("default.ttf", str(damage), (int(self.enemycoord[0]) - (self.displaydamage/20), int(self.enemycoord[1])), size = 24, flags = "Shadow")
    else:
      self.engine.renderFont("default.ttf", str(damage), (290 + (self.displaydamage/20), 350), size = 24, flags = "Shadow")
    if self.displaydamage >= 500 and self.turnstep == 1:
      if damage == "Miss":
        damage = 0
      if who == 0:
        self.playercurrenthp = self.playercurrenthp - damage
      else:
        self.enemycurrenthp = self.enemycurrenthp - damage
      self.displaydamage = 0
      self.turnstep = 2
      self.spacehit = False
    elif self.displaydamage >= 500 and self.turnstep == 2:
      if damage == "Miss":
        damage = 0
      if who == 0:
        self.playercurrenthp = self.playercurrenthp - damage
      else:
        self.enemycurrenthp = self.enemycurrenthp - damage
      self.battle = False
      self.turnstep = 0
      self.spacehit = False
      self.defend = False

  def update(self):

    if self.playercurrenthp <= 0:
      self.playercurrenthp = 0
    elif self.enemycurrenthp <= 0:
      self.enemycurrenthp = 0

    self.engine.drawImage(self.background, scale = (640,480))
    if self.fade == True:
      self.engine.screenfade((150,150,150,175))
    self.engine.drawImage(self.enemysprite, (int(self.enemycoord[0]), int(self.enemycoord[1])))

    self.engine.drawImage(self.hud, (150, 380))
    self.engine.drawBar(self.hpbarback, (55, 360), scale = (270,15))
    self.engine.drawBar(self.hpbar, (60, 360), scale = ((float(self.playercurrenthp)/int(self.playermaxhp))*260,150), frames = 30, currentframe = self.barframe)

    self.engine.renderFont("default.ttf", str(self.playercurrenthp) + "/" + str(self.playermaxhp), (200, 350), size = 24, flags = "Shadow")
    self.engine.renderFont("default.ttf", "HP", (30, 350), size = 24, flags = "Shadow")

    self.engine.renderFont("default.ttf", str(Player.lvl), (33, 297), size = 24)
    self.engine.renderFont("default.ttf", str(Player.name), (250, 297), size = 24, flags = "Shadow")

    for key, char in GameEngine.getKeyPresses():
      if key == K_SPACE and self.battle == True:
        self.spacehit = True

    commands = ["Attack", "Defend", "Skills", "Item"]
    if self.battle == False:
      if self.barframe < 30:
        self.barframe += .5
      else:
        self.barframe = 1

      if self.enemycurrenthp > 0:
        self.fade = False
        for i, choice in enumerate(commands):
          button = self.engine.drawImage(self.button, coord= (550 - (20*i), 350 + (30*i)), scale = (150,25))
          active, flag = self.engine.mousecol(button)
          if active == True:
            button = self.engine.drawImage(self.buttonactive, coord= (550 - (20*i), 350 + (30*i)), scale = (150,25))
            if flag == True:
              if i == 0:
                self.playercommand = 1
                self.battle = True
                self.timer = 0
                self.rotatestart = random.randint(0, 359)
                self.turnstep = 1
                self.displaydamage = 0
                self.stop = False
              if i == 1:
                self.playercommand = 2
                self.battle = True
                self.timer = 0
                self.rotatestart = random.randint(0, 359)
                self.turnstep = 1
                self.displaydamage = 0
                self.stop = False
          buttonfont = self.engine.renderFont("default.ttf", choice, (550 - (20*i), 350 + (30*i)))

        button = self.engine.drawImage(self.button, coord= (100, 445), scale = (150,25))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(self.buttonactive, coord= (100, 445), scale = (150,25))
          if flag == True:
            from Maplist import Maplist
            View.removescene(self)
            View.addscene(Maplist())
        buttonfont = self.engine.renderFont("default.ttf", "Flee", (100, 445))
      else:
        View.removescene(self)
        View.addscene(VictoryScene())

    else:
      self.fade = True
      if self.playercommand == 1:
        if Player.spd > Enemy.spd:
          roll = 1
        else:
          roll = 0
      elif self.playercommand == 2:
        roll = 1
      if self.turnstep == 1:
        self.fight(self.playercommand, self.enemycommand, roll)
      elif self.turnstep == 2:
        self.fight(self.playercommand, self.enemycommand, 1 - roll)

  def clearscene(self):

    del self.displaydamage, self.turnstep, self.timer, self.rotatestart, self.rolled, self.fade, self.stop, self.spacehit
    del self.hpbarback, self.hud, self.attackcb, self.attackct, self.battle, self.playercommand, self.enemycommand
    del self.enemycoord, self.playercurrenthp, self.playermaxhp, self.button, self.buttonactive, self.hpbar
    del self.background, self.enemysprite, self.enemycurrenthp, self.enemymaxhp
    self.engine.stopmusic()
    try:
      del self.audio
    except IOError:
      pass
    del self.engine

class VictoryScene(Layer):
  def __init__(self):

    self.engine = GameEngine

    self.expbar = self.engine.loadImage(os.path.join("Data", "expbar.png"))
    self.barback = self.engine.loadImage(os.path.join("Data", "barback.png"))

    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))

    self.enemyexp = Enemy.exp
    self.enemylvl = Enemy.lvl

    self.exp = Player.exp
    self.exptonextlvl = Player.explvl

    self.countdownexp = False
    self.finishupcounting = False
    self.finished = False
    self.levelup = False

    GameEngine.resetKeyPresses()

  def update(self):
    for key, char in GameEngine.getKeyPresses():
      if key == K_SPACE:
        if self.countdownexp == False:
          self.countdownexp = True
        elif self.countdownexp == True and self.enemyexp > 0:
          self.finishupcounting = True
        elif self.countdownexp == True and self.enemyexp == 0:
          if self.exp >= self.exptonextlvl:
            self.levelup = True
          else:
            self.finished = True

    self.engine.drawImage(self.background, (320,240), scale = (640,480))

    self.engine.renderFont("default.ttf", str(Player.name), (150, 96), size = 32)

    self.engine.renderFont("default.ttf", str(self.exp) + "/" + str(self.exptonextlvl), (280, 150), size = 24)
    self.engine.renderFont("default.ttf", str(self.enemyexp), (100, 150), size = 24)

    self.engine.drawBar(self.barback, (275, 190), scale = (260,15))
    self.engine.drawBar(self.expbar, (280, 190), scale = ((float(self.exp)/float(self.exptonextlvl))*260,5))

    if self.countdownexp == True:
      if self.enemyexp > 0:
        if self.finishupcounting == True:
          self.exp += self.enemyexp
          self.enemyexp = 0
        else:
          self.enemyexp -= 1
          self.exp += 1
      else:
        self.enemyexp = 0
        self.countdown = False

    
    if self.exp >= self.exptonextlvl:
      self.engine.renderFont("default.ttf", "Level Up!", (300, 96), size = 42)
      if self.levelup == True:
        Player.playerini.player.__setattr__("lvl", Player.lvl + 1)
        self.exp = 0
        self.levelup = False

    if self.finished == True:
      Player.playerini.player.__setattr__("exp", self.exp)
      Player.playerini.save()
      reload(Player)
      from Maplist import Maplist
      View.removescene(self)
      View.addscene(Maplist())

  def clearscene(self):
    del self.levelup, self.finished, self.finishupcounting, self.countdownexp, self.exptonextlvl, self.exp, self.enemylvl
    del self.enemyexp, self.background, self.barback, self.expbar, self.engine

