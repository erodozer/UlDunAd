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
import View
from View import *

from Config import Configuration

from Player import Player

class Shop(Layer):
  def __init__(self, shopini):

    self.engine = GameEngine
    self.shopini = shopini

    self.engine.loadImage(os.path.join("Data", "menubackground.png"))

    self.choices = ["Buy", "Sell", "Exit"]

    self.selectedchoice = 0

    self.party = []
    for partymember in self.engine.party:
      self.party.append(Player(partymember))

    self.items = self.shopini.townchoice.__getattr__("items").replace(" ", "").split(",")
    if self.items == ['']:
      self.items = None

    self.menubutton = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))

    self.secondarybutton = self.engine.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.secondarybuttonactive = self.engine.loadImage(os.path.join("Data", "secondarymenubuttonactive.png"))

    self.windows = self.engine.loadImage(os.path.join("Data", "shop.png"))

    self.index = 0
    self.selecteditem = None
    self.whichcharacter = 0

    self.purchaseflag = False
    self.toomuchflag = False

  def showbuy(self, whichplayer):
    self.engine.drawImage(self.windows)

    self.engine.renderFont("default.ttf", "Buy", coord = (470, 50), size = 24, flags = "Shadow")
    self.engine.renderFont("default.ttf", self.party[whichplayer].name, coord = (470, 80), size = 20, flags = "Shadow")

    self.engine.renderFont("menu.ttf", "Description:", coord = (255, 300), size = 28, flags = "Shadow", alignment = 1)

    self.engine.renderFont("menu.ttf", "Gold:", coord = (390, 200), size = 28, flags = "Shadow", alignment = 1)
    self.engine.renderFont("menu.ttf", str(self.party[whichplayer].gold), coord = (570, 230), size = 28, flags = "Shadow", alignment = 2)

    self.engine.renderFont("menu.ttf", "Inventory:", coord = (390, 150), size = 28, flags = "Shadow", alignment = 1)
    self.engine.renderFont("menu.ttf", str(len(self.party[whichplayer].inventory)) + "/20", coord = (570, 180), size = 28, flags = "Shadow", alignment = 2)

    maxindex = len(self.items)
    highlighted = False
    for i in range(self.index, 5+self.index):
      if i < maxindex:
        itemini = Configuration(os.path.join("..", "Data", "Items", str(self.items[i])+".ini")).item
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 90 + (26*(i-self.index))), scale = (270,24))
        if active == True:
          highlighted = True
          itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(self.items[i])+".png"))
          if itemimage != None:
            self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))
          if flag == True and self.purchaseflag == False:
            self.selecteditem = i
        if self.selecteditem == i:
          self.engine.renderFont("default.ttf", "*", (75, 95 + (26*(i-self.index))), size = 24)

    
        self.engine.renderFont("default.ttf", itemini.__getattr__("name"), (80, 90 + (26*(i-self.index))), size = 16, alignment = 1)
        self.engine.renderFont("default.ttf", itemini.__getattr__("worth") + "G", (335, 90 + (26*(i-self.index))), size = 16, alignment = 2)


    if self.selecteditem != None and highlighted == False:
      itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(self.items[self.selecteditem])+".png"))
      if itemimage != None:
        self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 230), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index + 5 < maxindex:
          self.index += 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (208, 230))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 60), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index - 5 >= 0:
          self.index -= 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (208, 60))

    active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (505, 420), scale = (150,45))
    if active == True:
      if flag == True and self.selecteditem != None and self.purchaseflag == False:
        self.purchaseflag = True    
    buttonfont = self.engine.renderFont("default.ttf", "Purchase", (505, 420))

    if self.purchaseflag == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              if len(self.party[whichplayer].inventory) < 20 and self.party[whichplayer].gold >= itemini.__getattr__("worth", "int"):
                self.party[whichplayer].inventory.append(self.items[self.selecteditem])
                self.party[whichplayer].gold -= itemini.__getattr__("worth", "int")
              else:
                self.toomuchflag = True
              self.purchaseflag = False
              self.selecteditem = None
            else:
              self.purchaseflag = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you wish to purchase this item?", (320, 230), size = 20, flags = "Shadow")
    if self.toomuchflag == True:
      self.engine.screenfade((0,0,0,120))

      active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 280), scale = (100,48))
      if active == True:
        if flag == True:
          self.toomuchflag = False

      buttonfont = self.engine.renderFont("default.ttf", "OK", (320, 280), size = 16)
      self.engine.renderFont("default.ttf", "Your inventory is either too full or you do not have enough gold", (320, 212), size = 20, flags = "Shadow")


  def showsell(self, whichplayer):
    self.engine.drawImage(self.windows)

    self.engine.renderFont("default.ttf", "Sell", coord = (470, 50), size = 24, flags = "Shadow")
    self.engine.renderFont("default.ttf", self.party[whichplayer].name, coord = (470, 80), size = 20, flags = "Shadow")

    self.engine.renderFont("menu.ttf", "Description:", coord = (255, 300), size = 28, flags = "Shadow", alignment = 1)

    self.engine.renderFont("menu.ttf", "Gold:", coord = (390, 200), size = 28, flags = "Shadow", alignment = 1)
    self.engine.renderFont("menu.ttf", str(self.party[whichplayer].gold), coord = (570, 230), size = 28, flags = "Shadow", alignment = 2)

    self.engine.renderFont("menu.ttf", "Inventory:", coord = (390, 150), size = 28, flags = "Shadow", alignment = 1)
    self.engine.renderFont("menu.ttf", str(len(self.party[whichplayer].inventory)) + "/20", coord = (570, 180), size = 28, flags = "Shadow", alignment = 2)

    maxindex = len(self.party[whichplayer].inventory)
    highlighted = False
    for i in range(self.index, 5+self.index):
      if i < maxindex:
        itemini = Configuration(os.path.join("..", "Data", "Items", str(self.party[whichplayer].inventory[i])+".ini")).item
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 90 + (26*(i-self.index))), scale = (270,24))
        if active == True:
          highlighted = True
          itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(self.party[whichplayer].inventory[i])+".png"))
          if itemimage != None:
            self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))
          if flag == True and self.purchaseflag == False:
            self.selecteditem = i
        if self.selecteditem == i:
          self.engine.renderFont("default.ttf", "*", (75, 95 + (26*(i-self.index))), size = 24)

    
        self.engine.renderFont("default.ttf", itemini.__getattr__("name"), (80, 90 + (26*(i-self.index))), size = 16, alignment = 1)
        self.engine.renderFont("default.ttf", str(int(itemini.__getattr__("worth", "int")/2)) + "G", (335, 90 + (26*(i-self.index))), size = 16, alignment = 2)

    if maxindex == 0:
      self.engine.renderFont("default.ttf", "Your inventory is empty", (208, 168), size = 16, alignment = 2)
     
    if self.selecteditem != None and highlighted == False:
      itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(self.party[whichplayer].inventory[self.selecteditem])+".png"))
      if itemimage != None:
        self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 230), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index + 5 < maxindex:
          self.index += 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (208, 230))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (208, 60), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index - 5 >= 0:
          self.index -= 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (208, 60))

    active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord= (505, 420), scale = (150,45))
    if active == True:
      if flag == True and self.selecteditem != None and self.purchaseflag == False:
        self.purchaseflag = True    
    buttonfont = self.engine.renderFont("default.ttf", "Barter", (505, 420))

    if self.purchaseflag == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              self.party[whichplayer].inventory.remove(self.party[whichplayer].inventory[self.selecteditem])
              self.party[whichplayer].gold += (itemini.__getattr__("worth", "int")/2)
              self.purchaseflag = False
              self.selecteditem = None
            else:
              self.purchaseflag = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you wish to sell this item?", (320, 230), size = 20, flags = "Shadow")

  def update(self):
    self.engine.screenfade((0,0,0,255))
    if self.selectedchoice != 0:
      for key, char in GameEngine.getKeyPresses():
        if key == K_LEFT:
          self.index = 0
          if self.whichcharacter - 1 > -1:
            self.whichcharacter -= 1
          else:
            self.whichcharacter = len(self.party)-1
        if key == K_RIGHT:
          self.index = 0
          if self.whichcharacter + 1 < len(self.party):
            self.whichcharacter += 1
          else:
            self.whichcharacter = 0    
        if key == K_BACKSPACE:
          self.selectedchoice = 0
          self.whichcharacter = 0
          self.index = 0
          self.selecteditem = None
          
    if self.selectedchoice == 0:
      self.engine.renderFont("default.ttf", "Welcome", (480,48), size = 32)
      for i, choice in enumerate(self.choices):
        active, flag = self.engine.drawButton(self.menubutton, self.menubuttonactive, coord = (95 + (200*i), 400), scale = (150, 45))
        if active == True:
          if flag == True:
            self.selectedchoice = i+1
        buttonfont = self.engine.renderFont("default.ttf", choice, (95 +(200*i), 400))

    elif self.selectedchoice == 1:
      if self.items != None:
        self.showbuy(self.whichcharacter)
        self.engine.renderFont("default.ttf", "Press BACKSPACE to go back", coord = (630, 465), size = 14, flags = "Shadow", alignment = 2)

      else:
        self.engine.screenfade((0,0,0,120))

        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 280), scale = (100,48))
        if active == True:
          if flag == True:
            self.selectedchoice = 0

        buttonfont = self.engine.renderFont("default.ttf", "OK", (320, 280), size = 16)
        self.engine.renderFont("default.ttf", "There are no items for sale!", (320, 230), size = 20, flags = "Shadow")

    elif self.selectedchoice == 2:
      self.showsell(self.whichcharacter)#selling is not yet set up
      self.engine.renderFont("default.ttf", "Press BACKSPACE to go back", coord = (630, 465), size = 14, flags = "Shadow", alignment = 2)

    elif self.selectedchoice == 3:
      for player in self.party:
        player.playerini.player.__setattr__("inventory", ", ".join(player.inventory))
        player.playerini.player.__setattr__("gold", player.gold)

      import Towns
      View.removescene(self)
      View.addscene(Towns.Towns())

