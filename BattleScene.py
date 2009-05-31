import GameEngine
import Player

from View import *
import os
import sys
import math
import random

import Config

class BattleScene(Layer):
  def __init__(self, enemy = "default", terrain = "grasslands.jpg"):

    self.engine = GameEngine

    self.background = self.engine.loadImage(os.path.join("Data", "Terrains", terrain))

    self.enemyini = Config.Configuration(os.path.join("Data", "Enemies", enemy+".ini")).enemy
    self.enemysprite = self.engine.loadImage(os.path.join("Data",  "Enemies", enemy+".png"))
    self.enemycurrenthp = int(self.enemyini.hp)
    self.enemymaxhp = int(self.enemyini.hp)
    self.enemycoord = self.enemyini.coord.split(",")

    self.playercurrenthp = 50
    self.playermaxhp = Player.hp

    self.button = self.engine.loadImage(os.path.join("Data", "battlebutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "battlebuttonactive.png"))

    self.hpbar = self.engine.loadImage(os.path.join("Data", "hpbar.png"))

    self.hud = self.engine.loadImage(os.path.join("Data", "battlehud.png"))

    self.battle = False
  def attack(self, who):
    if who == 0:
      damage = (self.enemyini.atk*3)/Player.defn
      self.playercurrenthp = self.playercurrenthp - damage
    elif who == 1:
      damage = (Player.atk*3)/self.enemyini.defn
      self.enemycurrenthp = self.enemycurrenthp - damage

    self.displayturn(damage)

  def displayturn(self,damage):
    
    self.engine.renderFont("default.ttf", damage, (280, 240), size = 24)

  def update(self):

    self.engine.drawImage(self.background, scale = (640,480))
    self.engine.drawImage(self.hud, (150, 380))
    self.engine.drawImage(self.hpbar, (200, 360), scale = (300,10))
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
            self.battle = True
            roll = random.randint(0,1)
            #self.attack(roll)
        buttonfont = self.engine.renderFont("default.ttf", choice, (550 - (20*i), 350 + (30*i)))

      button = self.engine.drawImage(self.button, coord= (100, 445), scale = (150,25))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.buttonactive, coord= (100, 445), scale = (150,25))
        if flag == True:
          self.battle = True
          roll = math.randint(0,1)
          self.attack(roll)
      buttonfont = self.engine.renderFont("default.ttf", "Flee", (100, 445))
