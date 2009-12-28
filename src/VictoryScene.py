#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

import Engine
from Engine import GameEngine

import Actor
from Actor import Player, Enemy
from Object import Item

from View import *
import os

from sys import *

import math
import random

from Config import *
import pygame

import Input

class VictoryScene(Layer):
  def __init__(self, multiplier, formation):

    self.engine = GameEngine()
    self.party = [Player(partymember) for partymember in Actor.party]
    self.levelup = [False for i in range(len(Actor.party))]

    self.formation = formation
    self.formationini = Configuration(os.path.join("Data", "Actors", "Enemies", "Formations", self.formation)).formation
    self.enemies = self.formationini.enemies.split(",")  
    self.enemy = [Enemy(enemy.strip()) for enemy in self.enemies]
    
    self.items = []
    for i, enemy in enumerate(self.enemy):
      if enemy.loot != None and enemy.lootchances != None:
        for i, item in enumerate(enemy.loot):
          chance = random.randint(0, 100)
          if chance >= 0 and chance <= int(enemy.lootchances[i]):
            self.items.append(item)

    self.bar = self.engine.loadImage(os.path.join("Data", "Interface", "bars.png"))

    self.background = self.engine.loadImage(os.path.join("Data", "Interface", "Battle", "victorybackground.png"))
    self.statusbox = self.engine.loadImage(os.path.join("Data", "Interface", "Battle", "victorystatusbox.png"))

    self.button = self.engine.data.defaultbutton
    self.secondarybutton = self.engine.data.secondarymenubutton

    self.enemyexp = 0
    self.enemyavglvl = 0
    for enemy in self.enemy:
      self.enemyexp += int((enemy.exp/len(self.party))*(multiplier/100))

    self.countdownexp = False
    self.finishupcounting = False
    self.finished = False

    self.notokay = False

    Input.resetKeyPresses()

  def update(self):
    for key, char in Input.getKeyPresses():
      if key == K_SPACE:
        if self.countdownexp == False:
          self.countdownexp = True
        elif self.countdownexp == True and self.enemyexp > 0:
          self.finishupcounting = True

    self.engine.drawImage(self.background, scale = (640,480))
    
    if self.countdownexp == True and self.enemyexp == 0:  
      active, flag = self.engine.drawButton(self.button, coord= (530, 425), scale = (150,45))
      if flag == True:
        self.finished = True
      self.engine.renderFont("default.ttf", "Finished", (530, 425))

    self.engine.renderFont("menu.ttf", "Loot and Drops", (20, 96), size = 28, flags = "Shadow", alignment = 1)
    for i, item in enumerate(self.items):
      itemini = Item(item)
      self.engine.renderFont("default.ttf", itemini.name, (20, 128+24*i), size = 20, flags = "Shadow", alignment = 1)

    self.engine.renderFont("menu.ttf", "Status", (620, 70), size = 32, flags = "Shadow", alignment = 2)

    for i, player in enumerate(self.party):

      self.engine.drawImage(self.statusbox, coord = ((640-150), 130+(i*100)), scale = (345, 80))

      self.engine.renderFont("default.ttf", str(player.name), (350, 110+(i*100)), size = 20, flags = "Shadow", alignment = 1)
      self.engine.renderFont("default.ttf", "Lvl:" + str(player.lvl), (620, 110 + (i*100)), size = 20, flags = "Shadow", alignment = 2)

      self.engine.renderFont("default.ttf", str(player.exp) + "/" + str(player.explvl), (620, 140 + (i*100)), size = 16, flags = "Shadow", alignment = 2)
      self.engine.renderFont("default.ttf", str(self.enemyexp), (350, 140 + (i*100)), size = 24, flags = "Shadow", alignment = 1)


      self.engine.drawBar(self.bar, (350, 155 + (i*100)), scale = (260, 15), frames = 6, currentframe = 5)
      self.engine.drawBar(self.bar, (350, 155 + (i*100)), scale = (260, 15), barcrop = (float(player.exp)/float(player.explvl)), frames = 6, currentframe = 6)

      if self.countdownexp == True:
        if self.enemyexp > 0:
          if self.finishupcounting == True:
            playerexp += self.enemyexp
          else:
            player.exp += 1
        else:
          self.enemyexp = 0
          self.countdown = False

    
      if player.exp >= player.explvl:
        self.levelup[i] = True
      
      if self.levelup[i] == True:
        self.engine.renderFont("default.ttf", "Level Up!", (480, 155 + (i*100)), size = 30)
        if player.exp >= player.explvl:
          player.exp = player.exp - player.explvl

    if self.countdownexp == True:
      if self.enemyexp > 0:
        if self.finishupcounting == True:
          self.enemyexp = 0
        else:
          self.enemyexp -= 1
      else:
        self.enemyexp = 0
        self.countdown = False

    if self.finished == True:
      for i, player in enumerate(self.party):
        for item in self.items:
          if i == 0:
            if len(player.inventory) < 20:
              player.inventory.append(item)
            elif len(player.inventory) >= 20 and i+1 < len(self.party):
              self.party[i+1].inventory.append(item)
          if i+1 >= len(self.party) and len(player.inventory) >= 20:
            self.notokay = True

      if self.notokay == True:
        self.engine.screenfade((0,0,0,120))

        active, flag = self.engine.drawButton(self.secondarybutton, coord= (320, 280), scale = (100,48))
        if flag == True:
          self.notokay = False

        buttonfont = self.engine.renderFont("default.ttf", "OK", (320, 280), size = 16)
        self.engine.renderMultipleFont("default.ttf", ("Your inventory is full!", "Some items were not picked up"), (320, 212), size = 20, flags = "Shadow")

      else:
        self.engine.inbattle = False
        pygame.mixer.music.fadeout(400)
        for player in self.party:
          player.updateINI(self.levelup[i])

        if Engine.town != None:
          if Engine.cells == None:  
            from Towns import Towns
            self.engine.changescene(self, Towns())
          else:
            from Dungeon import Dungeon
            self.engine.changescene(self, Dungeon())
            Engine.currentcell += 1
        else:
          from Maplist import Maplist
          self.engine.changescene(self, Maplist())


