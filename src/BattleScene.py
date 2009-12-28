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
from Object import Spell, Item

from View import *

import os
from sys import *

import math
import random

from Config import *
import pygame

from VictoryScene import VictoryScene

import Input

class BattleScene(Layer):
  def __init__(self, formation):

    Engine.inbattle = True

    self.engine = GameEngine()
    self.party = [Player(partymember) for partymember in Actor.party]
    self.partyactive = self.party[:]
    
    self.formation = formation
    self.formationini = Configuration(os.path.join("Data", "Actors", "Enemies", "Formations", self.formation)).formation
    self.enemies = self.formationini.enemies.split(", ")  
    self.enemy = [Enemy(enemy) for enemy in self.enemies]
    self.enemyactive = self.enemy[:]
    self.enemysprite = [enemy.image for enemy in self.enemy]
    self.formationcoord = [coord.split(", ") for coord in self.formationini.coord.split(";")]
    self.formationscale = self.formationini.scale.split(";")

    self.engine.inbattle = True

    terrain = self.formationini.terrain

    try:
      self.background = self.engine.loadImage(os.path.join("Data", "Places", "Terrains", terrain + ".png"), returnnone = False)
    except:
      self.background = self.engine.loadImage(os.path.join("Data", "Places", "Terrains", terrain + ".jpg"), returnnone = True)

    self.hue = None
    if os.path.isfile(os.path.join("Data", "Terrains", terrain + ".ini")):
      terrainini = Configuration(os.path.join("Data", "Terrains", terrain + ".ini")).terrain
      self.hue = terrainini.__getattr__("hue").split(",")

    self.bar = self.engine.loadImage(os.path.join("Data", "Interface", "bars.png"))
    self.hud = self.engine.loadImage(os.path.join("Data", "Interface", "Battle", "charbattlebase.png"))
    self.moralbar = self.engine.loadImage(os.path.join("Data", "Interface", "Battle", "moral.png"))

    self.attackcircle = self.engine.loadImage(os.path.join("Data", "Interface", "Battle", "battlecircle.png"))

    self.battle = False

    self.fade = False
    self.stop = False
    self.spacehit = False

    self.activemember = None
    self.activeenemy = None

    self.moral = 100.0
    self.selectingspell = False
    self.selectingtarget = False
    self.selectingitem = False
    self.index = 0

    self.command = None
    self.enemycommand = None
    self.target = None
    self.attacker = None
 
    self.timer = 0
    self.rotatestart = 0
    self.textpop = 0

    Input.resetKeyPresses()

    self.initMenu()

  def initMenu(self, menu = "basic"):
    choices = ["Attack", "Defend", "Spells", "Items", "Flee"]

    if menu == "spells":
      choices = [spell for spell in self.activemember.spells[self.index:self.index+6]]
    elif menu == "items":
      choices = [item for item in self.activemember.inventory[self.index:self.index+6]]
    elif menu == "target:enemy":
      choices = [enemy.name for enemy in self.enemyactive]
    elif menu == "target:ally":
      choices = [player.name for player in self.partyactive]

    self.menu = self.engine.createMenu(self.engine.data.menuWindow, self.engine.data.menuwindowbutton, choices, (90, 240), 200, 34)


  def showCommands(self):
    buttons = self.engine.drawMenu(self.menu)
    for i, button in enumerate(buttons):
      if button[1] == True:
        self.command = i
        if i == 0:
          self.selectingtarget = True
          self.initMenu("target:enemy")
        elif i == 1:
          self.target = self.activemember
          self.attacker = self.activemember
          self.battle = True
        elif i == 2:
          if self.activemember.spells != "None":
            self.selectingspell = True
            self.index = 0
            self.initMenu("spells")
          else:
            self.command = None
        elif i == 3:
          if self.activemember.inventory != "None":
            self.selectingitem = True
            self.index = 0
            self.initMenu("items")
          else:
            self.command = None
        elif i == 4:
          self.endscene("flee")

  def showSpells(self):
    buttons = self.engine.drawMenu(self.menu)
    active, flag = self.engine.drawButton(self.engine.data.battlebutton, "default.ttf", "Return", size = 32, coord= (540, 120), scale = (100, 32))
    for i, spell in enumerate(buttons):
      if spell[1] == True:
        self.object = Spell(self.activemember.spells[i])
        self.selectingspells = False
        self.selectingtarget = True
        if self.object.function[0] == "Heal":
          self.initMenu("target:ally")
        else:
          self.initMenu("target:enemy")

    if flag == True:
      self.selectingspells = False

    maxindex = len(self.activemember.spells)
    for key, char in Input.getKeyPresses():
      if key == K_LEFT:
        if self.index - 5 >= 0:
          self.index -= 5
          self.initMenu("spells")
      if key == K_RIGHT:
        if self.index + 5 < maxindex:
          self.index += 5
          self.initMenu("spells")

  def showItems(self):
    buttons = self.engine.drawMenu(self.menu)
    active, flag = self.engine.drawButton(self.engine.data.battlebutton, "default.ttf", "Return", size = 18, coord= (90, 120), scale = (200, 34))
    for i, item in enumerate(buttons):
      if item[1] == True:
        self.object = Item(self.activemember.inventory.pop[i])
        self.selectingitems = False
        self.selectingtarget = True
        if self.object.function[0] == "Heal":
          self.initMenu("target:ally")
        else:
          self.initMenu("target:enemy")

    if flag == True:
      self.selectingitems = False

    maxindex = len(self.activemember.inventory)
    for key, char in Input.getKeyPresses():
      if key == K_LEFT:
        if self.index - 5 >= 0:
          self.index -= 5
          self.initMenu("items")
      if key == K_RIGHT:
        if self.index + 5 < maxindex:
          self.index += 5
          self.initMenu("items")

  def showTargets(self):
    buttons = self.engine.drawMenu(self.menu)
    for button in buttons:
      if button[1] == True:
        self.target = self.enemyactive[buttons.index(button)]
        if self.command == 2 or self.command == 3:
          if self.object.function[0] == "Heal":
            self.target = self.party[buttons.index(button)]
        if self.command == 0 or self.command == 1:
          self.rotatestart = random.randint(0, 359)
        self.attacker = self.activemember
        self.selectingtarget = False
        self.battle = True

  def battleCommand(self, command, target, attacker):
    attacker.currentATB = 0

    if command == 0:
      if attacker == self.activemember:
        self.renderHit("attack", target)
      else:
        self.showDamage(target, attacker.atk)
    elif command == 1:
      if attacker == self.activemember:
        self.renderHit("defend", target)
      else:
        target.defending = True
        self.clearVars("Enemy")
    elif command == 2:
      if target in self.party:
        self.showDamage(target)
      else:
        stop = self.object.render(self.timer, (320, 240))
        if stop == False:
          self.timer += self.object.speed
        else:
          self.showDamage(target)
    elif command == 3:
      self.showDamage(target, self.object.function[2])

  def renderHit(self, command, target):
    if self.stop == False:
      var = random.randint(30,90)
      self.timer += var
      rotate = self.rotatestart + ((self.timer/7))
      self.engine.renderFont("default.ttf", "Press Space to Stop", (320, 64), size = 24)
      self.engine.renderFont("default.ttf", command, (320, 96), size = 24) 
      if command == "attack":
        self.engine.drawImage(self.attackcircle, coord = (float(int(self.formationcoord[self.enemy.index(target)][0])), 
                            float(int(self.formationcoord[self.enemy.index(target)][1]))), 
                            scale = (150,150), direction = "Horizontal", frames = 2, currentframe = 1)
        self.engine.drawImage(self.attackcircle, coord = (float(int(self.formationcoord[self.enemy.index(target)][0])), 
                            float(int(self.formationcoord[self.enemy.index(target)][1]))), 
                            scale = (150*(float(1800-self.timer)/900.0),150*(float(1800-self.timer)/900.0)), 
                            rot = -rotate, direction = "Horizontal", frames = 2, currentframe = 2)
      else:
        self.engine.drawImage(self.attackcircle, (320, 240), scale = (150,150), direction = "Horizontal", 
                            frames = 2, currentframe = 1)
        self.engine.drawImage(self.attackcircle, (320, 240), 
                            scale = (150*(float(1800-self.timer)/900.0),150*(float(1800-self.timer)/900.0)), 
                            rot = -rotate,  direction = "Horizontal", frames = 2, currentframe = 2)
    else:
      var = 0

    if self.spacehit == True:
      if int(1800-self.timer) in range(600, 900):
        if command == "defend":
          target.defending = True
          self.clearVars("Actor")
        else:
          self.showDamage(self.target, self.activemember.atk)
      else:
        self.showDamage(self.target, "Miss")
      self.stop = True

    if self.timer >= 1800:
      if command == "defend":
        target.defending = False
        self.clearVars("Actor")
      else:
        self.showDamage(self.target, "Miss")


  def showDamage(self, target, damage = 0):
    self.textpop += .4
    if target in self.partyactive:
      if self.command == 2 or self.command == 3:
        if self.object.function[0] == "Heal":
          color = (0, 255, 0)
        else:
          color = (255, 0, 0)
        self.engine.renderFont("default.ttf", self.object.function[1] + ": " + str(damage), coord = (108+(self.party.index(target)*213), 320 - self.textpop), size = 18, color = color)
      else:
        color = (255, 0, 0)
        self.engine.renderFont("default.ttf", "HP: " + str(damage), coord = (108+(self.party.index(target)*213), 320 - self.textpop), size = 18, color = color)

    elif target in self.enemyactive:
      if self.command == 2 or self.command == 3:
        if self.object.function[0] == "Heal":
          color = (0, 255, 0)
        else:
          color = (255, 0, 0)
        self.engine.renderFont("default.ttf", self.object.function[0] + ": " + str(damage), (int(self.formationcoord[self.enemy.index(target)][0]), int(self.formationcoord[self.enemy.index(target)][1]) - self.textpop), size = 18, color = color)
      else:
        color = (255, 0, 0)

        self.engine.renderFont("default.ttf", "HP: " + str(damage), coord = (int(self.formationcoord[self.enemy.index(target)][0]), int(self.formationcoord[self.enemy.index(target)][1]) - self.textpop), size = 18, color = color)

    if self.textpop >= 20:
      if self.command == 2 or self.command == 3:
        self.object.action(target)
      else:
        if damage != "Miss":
          if target.currenthp - damage < 0:
            target.currenthp = 0
          else:
            target.currenthp -= damage

      if self.attacker in self.party:
        self.clearVars("Actor")
      elif self.attacker in self.enemy:
        self.clearVars("Enemy")

  def updateATB(self):
    for enemy in self.enemy:
      if enemy.currentATB < 300:
        enemy.currentATB += enemy.spd*.2
      else:
        enemy.currentATB = 300
        if self.activeenemy == None:
          self.activeenemy = enemy

    for player in self.partyactive:
      if player.currentATB < 300:
        player.currentATB += player.spd*.2
      else:
        player.currentATB = 300
        if self.activemember == None:
          self.activemember = player

    if self.activeenemy != None:
      self.attacker = self.activeenemy
      self.enemycommand = random.randint(0,1)
      if self.enemycommand == 0:
        self.target = random.choice(self.partyactive)
      else:
        self.target = self.attacker
      self.battle = True

    self.timer = 0
    self.stop = False
    self.spacehit = False

  def clearVars(self, who):
    if self.attacker in self.party:
      self.initMenu()

    self.battle = False
    self.fade = False

    self.target = None
    self.attacker = None

    if who == "Actor":
      self.activemember = None
      self.command = None
      self.selectingspell = False
      self.selectingtarget = False
      self.selectingitem = False
      self.moral -= 2
    else:
      self.activeenemy = None
      if self.enemycommand != 1:
        self.moral -= 4
      self.enemycommand = None

    self.textpop = 0

  def update(self):

    if self.background != None:
      self.engine.drawImage(self.background, scale = (640,480))
    if self.fade == True:
      self.engine.screenfade((0,0,0,175))

    for i, enemy in enumerate(self.enemy):
      if enemy in self.enemyactive:
        self.engine.drawImage(self.enemysprite[i], coord = (float(int(self.formationcoord[i][0])), float(int(self.formationcoord[i][1]))), scaleper = int(self.formationscale[i]))


    self.engine.drawBar(self.moralbar, (340, 40), scale = (300, 75), frames = 3, currentframe = 3, direction = "Vertical")
    self.engine.drawBar(self.moralbar, (340, 40), scale = (300, 75), barcrop = self.moral/100.0, frames = 3, currentframe = 2, direction = "Vertical")
    self.engine.drawBar(self.moralbar, (340, 40), scale = (300, 75), frames = 3, currentframe = 1, direction = "Vertical")

    if self.hue != None:
      self.engine.screenfade((int(self.hue[0]),int(self.hue[1]),int(self.hue[2]),50))

    for i, player in enumerate(self.party):
      if self.activemember == player:
        self.engine.drawImage(self.hud, (108+(i*213),418), scale = (212, 124), frames = 2, currentframe = 2)
      else:
        self.engine.drawImage(self.hud, (108+(i*213),418), scale = (212, 124), frames = 2, currentframe = 1)

      if player not in self.partyactive:
        self.engine.renderFont("default.ttf", str(player.name), (110+(i*213), 465), size = 16, flags = "Shadow", color = (255,0,0))
      else:
        self.engine.renderFont("default.ttf", str(player.name), (110+(i*213), 465), size = 16, flags = "Shadow")

      #ATB Bar
      self.engine.drawBar(self.bar, (18+(i*213), 442), scale = (175,15), frames = 6, currentframe = 5)
      self.engine.drawBar(self.bar, (18+(i*213), 442), scale = (175,15), barcrop = float(player.currentATB)/int(300), frames = 6, currentframe = 6)

      #HP Bar
      self.engine.drawBar(self.bar, (45+(i*213), 395), scale = (150,15), frames = 6, currentframe = 1)
      self.engine.drawBar(self.bar, (45+(i*213), 395), scale = (150,15), barcrop = (float(player.currenthp)/int(player.hp)), frames = 6, currentframe = 2)

      self.engine.renderFont("default.ttf", str(player.currenthp) + "/" + str(player.hp), (128+(i*213), 395), size = 14, flags = "Shadow", alignment = 0)
      self.engine.renderFont("default.ttf", "HP", (25+(i*213), 395), size = 14, flags = "Shadow", alignment = 1)

      #SP Bar
      self.engine.drawBar(self.bar, (45+(i*213), 410), scale = (150,15), frames = 6, currentframe = 3)
      self.engine.drawBar(self.bar, (45+(i*213), 410), scale = (150,15), barcrop = (float(player.currentsp)/int(player.sp)), frames = 6, currentframe = 4)

      self.engine.renderFont("default.ttf", str(player.currentsp) + "/" + str(player.sp), (128+(i*213), 410), size = 14, flags = "Shadow", alignment = 0)
      self.engine.renderFont("default.ttf", "SP", (25+(i*213), 410), size = 14, flags = "Shadow", alignment = 1)


    for key, char in Input.getKeyPresses():
      if key == K_SPACE and self.battle == True:
        self.spacehit = True

    if self.battle == False:

      for player in self.partyactive:
        if player.currenthp <= 0:
          player.currenthp = 0
          player.currentATB = 0
          player.knockedout = True
          self.partyactive.remove(player)
          self.moral -= 20
          if player == self.activemember:
            self.activemember = None

      for i, enemy in enumerate(self.enemyactive):
        if enemy.currenthp <= 0:
          enemy.currenthp = 0
          self.enemyactive.pop(i)
          self.moral += 10

      self.updateATB()
      if len(self.partyactive) == 0:
        self.endscene("flee")

      if not len(self.enemyactive) == 0:
        self.fade = False
        if self.activemember != None:
          if self.selectingspell == True:
            self.showSpells()
          elif self.selectingitem == True:
            self.showItems()
          elif self.selectingtarget == True:
            self.showTargets()
          else:
            self.showCommands()
      else:
        self.endscene("victory")
    else:
      self.fade = True
      if self.attacker in self.enemy:
        self.battleCommand(self.enemycommand, self.target, self.attacker)
      else:
        self.battleCommand(self.command, self.target, self.attacker)

  def endscene(self, condition):
    for player in self.party:
      victory = False
      if condition == "victory":
        victory = True

      player.updateINI(victory)

    if condition == "victory":
      self.engine.changescene(self, VictoryScene(75.0 + self.moral, self.formation))

    elif condition == "flee":
      self.engine.inbattle = False
      pygame.mixer.music.fadeout(400)
      if Engine.town != None:
        if Engine.cells == None:
          from Towns import Towns
          self.engine.changescene(self, Towns())
        else:
          from Dungeon import Dungeon
          self.engine.changescene(self, Dungeon())
      else:
        from Maplist import Maplist
        self.engine.changescene(self, Maplist())

    Engine.inbattle = False
