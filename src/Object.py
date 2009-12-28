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

from Config import *
import os
import math

class Object:
  def __init__(self, objini):
    self.name = objini.__getattr__("name")                        #obviously the name of the object
    self.function = objini.__getattr__("function").split(".")     #what the object does

    #these deal with the object's animation in battle,
    #do not touch unless you are also editing the animation
    #handling code in the BattleScene.py
    self.frames = objini.__getattr__("frames", "int")             #number of frames
    self.speed = objini.__getattr__("speed", "int")              #how fast the animation should play
    self.direction = objini.__getattr__("direction", "int")       #what direction the picture should be split

    self.aniimage = None
    if objini.__getattr__("animation") != '':
      if os.path.exists(os.path.join("..", "Data", "Animations", objini.__getattr__("animation"))):
        self.aniimage = GameEngine().loadImage(os.path.join("Data", "Animations", objini.__getattr__("animation")))


  #Handles action that the object can do in battle or in the menu
  #1. only items with the function of healing may be used in the menu
  #2. objects can either heal or do damage to either HP or SP of the target
  def action(self, target):
    if self.function[0] == "Heal":
      if self.function[1] == "HP":
        target.hp += self.function[2]
      elif self.function[1] == "SP":
        target.sp += self.function[2]
      else:
        target.hp += 10
    elif self.function[1] == "Damage":
      if self.function[1] == "HP":
        target.hp -= self.function[2]
      elif self.function[1] == "SP":
        target.sp -= self.function[2]
      else:
        target.hp -= 10
      
  def render(self, timer, coord):
    self.stop = True
    if self.aniimage != None:
      self.stop = False
      if self.timer <= self.frames:
        GameEngine().drawImage(self.animimage, (coord[0], coord[1]), frames = self.frames, currentframe = int(self.timer), direction = self.direction)
      else:
        self.stop = True

    return stop

class Item(Object):
  def __init__(self, item):
    self.itemini = Configuration(os.path.join("Data", "Objects", "Items", "Info", item + ".ini")).item

    Object.__init__(self, self.itemini)

    self.type = self.itemini.__getattr__("type")               #defines whether the item is an armor, weapon, or useable
    self.worth = self.itemini.__getattr__("worth", "int")      #how much you have to pay for the item (sell price = worth/2)

    self.image = None
    #item image, used in shops and menu
    if os.path.exists(os.path.join("..", "Data", "Objects", "Items", "Image", item + ".png")) == True:
      self.image = GameEngine().loadImage(os.path.join("Data", "Objects", "Items", "Image", item + ".png"))  


class Spell(Object):
  def __init__(self, spell):
    self.spellini = Configuration(os.path.join("Data", "Objects", "Spells", spell + ".ini")).spell

    Object.__init__(self, self.spellini)

    self.cost = self.spellini.__getattr__("cost", "int")                 #how much sp the spell uses
    self.variance = self.spellini.__getattr__("variance", "int")         #how much damage caused the spell can vary
