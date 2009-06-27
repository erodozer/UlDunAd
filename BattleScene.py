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

from Player import Player

from View import *
import os

from sys import *

from Enemy import Enemy

import math
import random

from Config import *
import pygame

class BattleScene(Layer):
  def __init__(self, terrain = "grasslands.png"):

    self.engine = GameEngine
    self.party = []
    for i, partymember in enumerate(self.engine.party):
      self.party.append(Player(partymember))
      
    self.enemy = Enemy()

    if os.path.isfile(os.path.join("Data", "Audio", "battle.mp3")):
      self.audio = self.engine.loadAudio("battle.mp3")
    else:
      self.audio = None

    self.background = self.engine.loadImage(os.path.join("Data", "Terrains", terrain))

    self.enemysprite = self.engine.loadImage(os.path.join("Data",  "Enemies", self.enemy.image))

    self.button = self.engine.loadImage(os.path.join("Data", "battlebutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "battlebuttonactive.png"))

    self.atb = self.engine.loadImage(os.path.join("Data", "atb.png"))
    self.atbback = self.engine.loadImage(os.path.join("Data", "atbback.png"))

    self.hpbar = self.engine.loadImage(os.path.join("Data", "hpbar.png"))
    self.hpback = self.engine.loadImage(os.path.join("Data", "hpbarback.png"))

    self.hud = self.engine.loadImage(os.path.join("Data", "battlehud.png"))
    self.attackcb = self.engine.loadImage(os.path.join("Data", "battlecirclebottom.png"))
    self.attackct = self.engine.loadImage(os.path.join("Data", "battlecircletop.png"))

    self.battle = False

    self.playercommand = 0
    self.enemycommand = 1

    self.displaydamage = 0
    self.timer = 0.0
    self.rotatestart = 0
    self.fade = False
    self.stop = False
    self.spacehit = False
    self.defend = False

    self.barframe = 1

    self.activemember = None
    self.roll = 1
    self.playertargeted = 0

    GameEngine.resetKeyPresses()

  def fight(self, playercommand, enemycommand, roll, partymember = None):
    if roll == 0:
      if self.enemycommand == 1:
        self.attack(0, partymember)

    if roll == 1:
      if self.playercommand == 1 or self.playercommand == 2:
        self.renderbattlecircle(self.activemember)
      elif self.playercommand == 3:
        self.castspell(self.activemember)
        #self.attack(1)

  def renderbattlecircle(self, partymember):
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
          self.party[partymember].defending = True
          self.spacehit = False
          self.clearvariables(self.playercommand)
      else:
        self.displayturn("Miss", 1, partymember)
    else:
      self.engine.drawImage(self.attackcb, (int(self.enemy.coord[0]), int(self.enemy.coord[1])), scale = (200*(.25*math.sin(time+.5)+1),200*(.25*math.sin(time+.5)+1)))
      self.engine.drawImage(self.attackct, (int(self.enemy.coord[0]), int(self.enemy.coord[1])), scale = (200*(.25*math.sin(time+.5)+1),200*(.25*math.sin(time+.5)+1)), rot = -rotate)

  def attack(self, who, partymember = 0):
    if who == 0:
      if self.party[partymember].defending == True:
        damage = (self.enemy.atk*3)/(self.party[partymember].defn*2)
      else:
        damage = (self.enemy.atk*3)/self.party[partymember].defn
    elif who == 1:
      damage = (self.party[partymember].atk*3)/self.enemy.defn

    self.displayturn(damage, who, partymember)

  def castspell(self, partymember):
    speed = 60/float(self.spellini.frames)
    if self.stop == False:
      if self.timer <= float(self.spellini.frames):
        self.timer += (float(self.spellini.frames)/speed)
        self.engine.drawImage(self.spellanimation, (int(self.enemy.coord[0]), int(self.enemy.coord[1])), frames = int(self.spellini.frames), currentframe = self.timer, direction = self.spellini.direction)
      else:
        self.stop = True
    else:
      self.timer = 0
      self.displayturn(self.spelldamage, 1, partymember)

  def displayturn(self, damage, who, partymember):
    self.displaydamage = self.displaydamage + 20
    if who == 1:
      self.engine.screenfade((255,255,255,255-(self.displaydamage*5)))
      self.engine.renderFont("default.ttf", str(damage), (int(self.enemy.coord[0]) - (self.displaydamage/20), int(self.enemy.coord[1])), size = 24, flags = "Shadow")
      if self.playercommand == 3:
        self.engine.renderFont("default.ttf", self.spellini.cost, (450, 380+(partymember*20)), size = 18, flags = "Shadow")
    else:
      self.engine.renderFont("default.ttf", str(damage), (450 + (self.displaydamage/20), 380+(partymember*30)), size = 16, flags = "Shadow")

    if self.displaydamage >= 500:
      if damage == "Miss":
        damage = 0
      if who == 0:
        self.party[partymember].currenthp -= damage
      else:
        self.enemy.currenthp -= damage
        if self.playercommand == 3:
          self.party[partymember].currentsp -= int(self.spellini.cost)
      self.displaydamage = 0
      self.spacehit = False

      self.clearvariables(self.playercommand)

  def clearvariables(self, i):
    self.battle = False
    self.stop = True
    self.timer = 0
    self.displaydamage = 0
    if self.roll == 0:
      self.enemy.currentatb = 0
    else:
      self.party[self.activemember].currentatb = 0
      self.activemember = None

    if i == 1 or i == 2:
      self.rotatestart = 0
      self.spacehit = False
      if i == 2:
        self.defend = False
    if i == 3:
      self.spell = None
      self.spellini = None
      self.spellanimation = None
      self.spelldamage = None

  def battlecommand(self, i, partymember = 0):
    if i == 2:
      self.spell = "fire.ini"
      self.spellini = Configuration(os.path.join("Data", "Spells", self.spell)).spell
      self.spellanimation = self.engine.loadImage(os.path.join("Data", "Animations", self.spellini.animation))
      self.spelldamage = int(self.spellini.damage) + random.randint(0, int(self.spellini.variance))
      if self.party[partymember].currentsp < int(self.spellini.cost): #if player sp is less than the cost of the spell then stop the command
        return

    self.battle = True
    self.roll = 1
    self.timer = 0
    self.displaydamage = 0
    self.stop = False

    self.party[partymember].defending = False

    if i == 0 or i == 1:
      self.rotatestart = random.randint(0, 359)

  def enemybattlecommand(self):
    self.battle = True
    self.roll = 0
    self.displaydamage = 0
    self.playertargeted = random.randint(0, len(self.party)-1)

  def update(self):

    if self.enemy.currenthp <= 0:
      self.enemy.currenthp = 0

    self.engine.drawImage(self.background, scale = (640,480))
    if self.fade == True:
      self.engine.screenfade((150,150,150,175))
    self.engine.drawImage(self.enemysprite, (int(self.enemy.coord[0]), int(self.enemy.coord[1])))

    for i, player in enumerate(self.party):
      if player.currenthp <= 0:
        player.currenthp = 0

      self.engine.drawBar(self.atbback, (10, 390+(i*30)), scale = (200,6))
      self.engine.drawBar(self.atb, (10, 390+(i*30)), scale = (200,6), barcrop = (float(player.currentatb)/int(300)))

      self.engine.drawBar(self.hpback, (335, 390+(i*30)), scale = (95,6))
      self.engine.drawBar(self.hpbar, (335, 390+(i*30)), scale = (95,180), barcrop = (float(player.currentsp)/int(player.sp)), frames = 30, currentframe = self.barframe)

      self.engine.drawBar(self.hpback, (215, 390+(i*30)), scale = (115,6))
      self.engine.drawBar(self.hpbar, (215, 390+(i*30)), scale = (115,180), barcrop = (float(player.currenthp)/int(player.hp)), frames = 30, currentframe = self.barframe)

      self.engine.renderFont("default.ttf", str(player.currenthp) + "/" + str(player.hp), (330, 380+(i*30)), size = 18, flags = "Shadow", alignment = 2)
      self.engine.renderFont("default.ttf", "HP", (215, 380+(i*30)), size = 18, flags = "Shadow", alignment = 1)

      self.engine.renderFont("default.ttf", str(player.currentsp) + "/" + str(player.sp), (430, 380+(i*30)), size = 18, flags = "Shadow", alignment = 2)
      self.engine.renderFont("default.ttf", "SP", (335, 380+(i*30)), size = 18, flags = "Shadow", alignment = 1)

      self.engine.renderFont("default.ttf", str(player.name), (10, 380+(i*30)), size = 18, flags = "Shadow", alignment = 1)

    for key, char in GameEngine.getKeyPresses():
      if key == K_SPACE and self.battle == True:
        self.spacehit = True

        enemytarget = random.randint(0, len(self.party)-1)

    commands = ["Attack", "Defend", "Skills", "Item", "Flee"]
    if self.battle == False:
      if self.barframe < 30:
        self.barframe += .5
      else:
        self.barframe = 1

      for i, player in enumerate(self.party):
        if player.currentatb < 300 and self.enemy.currentatb < 300:
          if (self.activemember == None and self.engine.battlemode == "wait") or self.engine.battlemode == "active":
            div = random.randint(4, 7)
            player.currentatb += (player.spd/div)
            self.enemy.currentatb += (self.enemy.spd/div)
        elif player.currentatb >= 300:
          if (self.activemember == None and self.engine.battlemode == "active") or self.engine.battlemode == "wait":
            player.currentatb = 300
            self.activemember = i
        elif self.enemy.currentatb >= 300:
          self.enemybattlecommand()

      if self.enemy.currenthp > 0:
        self.fade = False
        if self.activemember != None:
          for i, choice in enumerate(commands):
            button = self.engine.drawImage(self.button, coord= (550, 340 + (30*i)), scale = (150,25))
            active, flag = self.engine.mousecol(button)
            if active == True:
              button = self.engine.drawImage(self.buttonactive, coord= (550, 340 + (30*i)), scale = (150,25))
              if flag == True: 
                if i < 3: #this is temporary until the item system is implemented
                  self.playercommand = i+1
                  self.battlecommand(i)
                elif i == 4:
                  for player in self.party:
                    player.playerini.player.__setattr__("currenthp", player.currenthp)
                    player.playerini.player.__setattr__("currentsp", player.currentsp)
                    player.playerini.player.__setattr__("monsterskilled", player.monsterskilled + 1)
                    player.playerini.save()
                  from Maplist import Maplist
                  View.removescene(self)
                  View.addscene(Maplist())
                  GameEngine.enemy = None

            buttonfont = self.engine.renderFont("default.ttf", choice, (550, 340 + (30*i)))

      else:
        for player in self.party:
          player.playerini.player.__setattr__("currenthp", player.currenthp)
          player.playerini.player.__setattr__("currentsp", player.currentsp)
          player.playerini.player.__setattr__("monsterskilled", player.monsterskilled + 1)
          player.playerini.save()
        View.removescene(self)
        View.addscene(VictoryScene())

    else:
      self.fade = True
      if self.roll == 1:
        self.fight(self.playercommand, self.enemycommand, self.roll, self.activemember)
      else:
        self.fight(self.playercommand, self.enemycommand, self.roll, self.playertargeted)

  def clearscene(self):

    del self.displaydamage, self.timer, self.rotatestart, self.fade, self.stop, self.spacehit
    del self.attackcb, self.attackct, self.battle, self.playercommand, self.enemycommand
    del self.button, self.buttonactive, self.hpbar, self.hpback, self.atb, self.atbback, self.background
    if self.audio != None:
      self.engine.stopmusic()
    del self.audio, self.party, self.enemy, self.engine

class VictoryScene(Layer):
  def __init__(self, multiplier):

    self.engine = GameEngine
    self.party = []
    self.levelup = []
    for i, partymember in enumerate(self.engine.party):
      self.party.append(Player(partymember))
      self.levelup.append("False")

    self.enemy = Enemy()
    self.expbar = self.engine.loadImage(os.path.join("Data", "expbar.png"))
    self.barback = self.engine.loadImage(os.path.join("Data", "barback.png"))

    self.background = self.engine.loadImage(os.path.join("Data", "characterbackground.png"))

    self.enemyexp = int((self.enemy.exp/len(self.party))*multiplier)
    self.enemylvl = self.enemy.lvl


    self.countdownexp = False
    self.finishupcounting = False
    self.finished = False


    GameEngine.resetKeyPresses()

  def update(self):
    for key, char in GameEngine.getKeyPresses():
      if key == K_SPACE:
        if self.countdownexp == False:
          self.countdownexp = True
        elif self.countdownexp == True and self.enemyexp > 0:
          self.finishupcounting = True
        elif self.countdownexp == True and self.enemyexp == 0:
          for i, player in enumerate(self.party):
            if player.exp >= player.explvl:
              self.levelup[i] = "True"
            else:
              self.finished = True

    self.engine.drawImage(self.background, (320,240), scale = (640,480))

    for i, player in enumerate(self.party):

      self.engine.renderFont("default.ttf", str(player.name), (150, 96 + (i*100)), size = 32)

      self.engine.renderFont("default.ttf", str(player.exp) + "/" + str(player.explvl), (280, 120 + (i*100)), size = 24)
      self.engine.renderFont("default.ttf", str(self.enemyexp), (100, 120 + (i*100)), size = 24)

      self.engine.drawBar(self.barback, (275, 125 + (i*100)), scale = (260,15))
      self.engine.drawBar(self.expbar, (280, 125 + (i*100)), scale = ((float(player.exp)/float(player.explvl))*260,5))

      if self.countdownexp == True:
        if self.enemyexp > 0:
          if self.finishupcounting == True:
            playerexp += self.enemyexp
            self.enemyexp = 0
          else:
            self.enemyexp -= 1
            player.exp += 1
        else:
          self.enemyexp = 0
          self.countdown = False

    
      if player.exp >= player.explvl:
        self.engine.renderFont("default.ttf", "Level Up!", (300, 96 + (i*100)), size = 42)
        if self.levelup[i] == "True":
          if player.exp > player.explvl:
            player.exp = player.exp - player.explvl
          else:
            player.exp = 0        
          player.playerini.player.__setattr__("lvl", player.lvl + 1)
          player.playerini.player.__setattr__("currenthp", player.hp)
          player.playerini.player.__setattr__("currenthp", player.sp)
          self.levelup[i] = "False"

    if self.finished == True:
      for player in self.party:
        player.playerini.player.__setattr__("exp", player.exp)
        player.playerini.save()
      from Maplist import Maplist
      View.removescene(self)
      View.addscene(Maplist())

  def clearscene(self):
    del self.levelup, self.finished, self.finishupcounting, self.countdownexp, self.enemylvl
    del self.enemyexp, self.background, self.barback, self.expbar, self.engine

