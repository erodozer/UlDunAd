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

from View import *

import Config

import random

class Towns(Layer):
  def __init__(self):

    self.engine = GameEngine()
    self.townname = Engine.town

    self.townpath = os.path.join("Data", "Places", "Towns", self.townname)
    self.townini = Config.Configuration(os.path.join(self.townpath, "town.ini")).town

    self.background = None
    if os.path.exists(os.path.join("..", self.townpath, "background.png")):
      self.background = self.engine.loadImage(os.path.join(self.townpath, "background.png"))
    self.sidebar = self.engine.loadImage(os.path.join("Data", "Interface", "sidemenu.png"))

    self.audio = None
    if self.townini.audio != "None":
      self.audio = self.engine.loadAudio(os.path.join("Town", self.townini.audio), volume = self.engine.townvolume)

    self.choices = self.townini.choices.split(", ")

    if os.path.exists(os.path.join("..", self.townpath, "townbutton.png")) == True:
      self.menubutton = self.engine.loadImage(os.path.join(self.townpath, "townbutton.png"))
    else:
      self.menubutton = self.engine.loadImage(os.path.join("Data", "Interface", "defaultbutton.png"))

    self.enemies = self.townini.enemylist.split(",")

  def update(self):
    self.engine.drawImage(self.background)
    self.engine.drawImage(self.sidebar, coord = (100, 240))

    for i, choice in enumerate(self.choices):
      active, flag = self.engine.drawButton(self.menubutton, coord= (100, 90+(60*i)), scale = (150,45))
      if active == True:
        if flag == True:
          if choice == "Library" or choice == "library":
            from Library import Library
            self.engine.changescene(self, Library())
          elif choice == "Wilderness" or choice == "wilderness":
            pygame.mixer.music.fadeout(400)
            from BattleScene import BattleScene
            self.engine.changescene(self, BattleScene(str(random.choice(self.enemies).strip()+".ini")))
            from ExtraScenes import LoadingScene
            View().addscene(LoadingScene("Preparing Battle", 4.5))
          else:
            choiceini = Config.Configuration(os.path.join(self.townpath, choice+".ini"))
            from Shop import Shop
            self.engine.changescene(self, Shop(choiceini))

      buttonfont = self.engine.renderFont("default.ttf", choice, (100, 90+(60*i)))

    #return button
    active, flag = self.engine.drawButton(self.menubutton, coord= (100, 420), scale = (150,45))
    if active == True:
      if flag == True:
        from Maplist import Maplist
        self.engine.changescene(self, Maplist())
        self.engine.town = None
    returnfont = self.engine.renderFont("default.ttf", "Return", (100, 420))

    self.towntitle = self.engine.renderFont("menu.ttf", self.townname, (430, 64), size = 32)


