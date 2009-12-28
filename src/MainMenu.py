#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

from Engine import GameEngine

from View import *

class MainMenu(Layer):
  def __init__(self):
    self.engine = GameEngine()
    self.background = self.engine.loadImage(os.path.join("Data", "Interface", "mainbackground.png"))
    #self.engine.drawImage(os.path.join("Data", "mapmenu.png"))
    #self.audio = self.engine.loadAudio("Town001.mp3")
    self.choices = ["New Game", "Continue", "Quit"]

    self.button = self.engine.data.secondarymenubutton

    self.bar = self.engine.loadImage(os.path.join("Data", "Interface", "dividerbar.png"))

  def update(self):
    self.engine.drawImage(self.background, scale = (640,480))
    w, h = self.engine.w, self.engine.h

    self.engine.drawImage(self.bar, coord = (320, 100+195), scale = (550, 3))
    self.engine.drawImage(self.bar, coord = (320, 100+285), scale = (550, 3))

    for i, choice in enumerate(self.choices):
      active, flag = self.engine.drawButton(self.button, "default.ttf", str(choice), size = 32, coord= (320, 250 + 90*i), scale = (550, 80))
      if active == True:
        if flag == True:
          if i == 0:
            from CharacterCreator import CharacterCreator
            self.engine.changescene(self, CharacterCreator())
          if i == 1:
            players = self.engine.listpath(os.path.join("Data", "Actors", "Players"), "splitfiletype", ".ini")
            if players != []:
              from Playerlist import Playerlist
              self.engine.changescene(self, Playerlist())

          elif i == 2:
             self.engine.finished = True

