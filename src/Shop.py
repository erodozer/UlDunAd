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

from Config import Configuration

import Actor
from Actor import Player

from Object import Item

import Input

class Shop(Layer):
  def __init__(self, shopini):

    self.engine = GameEngine()
    self.shopini = shopini

    self.engine.loadImage(os.path.join("Data", "menubackground.png"))

    self.choices = ["Buy", "Sell", "Exit"]

    self.selectedchoice = 0

    self.party = [Player(partymember) for partymember in Actor.party]

    self.items = self.shopini.townchoice.__getattr__("items").replace(" ", "").split(",")
    if self.items == ['']:
      self.items = None

    self.menubutton = self.engine.data.defaultbutton
    self.secondarybutton = self.engine.data.secondarymenubutton

    self.windows = self.engine.loadImage(os.path.join("Data", "Interface", "shop.png"))

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
        item = Item(self.items[i])
        active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 90 + (26*(i-self.index))), scale = (270,24))
        if active == True:
          highlighted = True
          if item.image != None:
            self.engine.drawImage(item.image, coord= (155, 360), scale = (150,150))
          if flag == True and self.purchaseflag == False:
            self.selecteditem = i
        if self.selecteditem == i:
          self.engine.renderFont("default.ttf", "*", (75, 95 + (26*(i-self.index))), size = 24)

    
        self.engine.renderFont("default.ttf", item.name, (80, 90 + (26*(i-self.index))), size = 16, alignment = 1)
        self.engine.renderFont("default.ttf", str(item.worth) + "G", (335, 90 + (26*(i-self.index))), size = 16, alignment = 2)


    if self.selecteditem != None and highlighted == False:
      itemimage = Item(self.items[self.selecteditem]).image
      if itemimage != None:
        self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))

    active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 230), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index + 5 < maxindex:
          self.index += 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (208, 230))

    active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 60), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index - 5 >= 0:
          self.index -= 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (208, 60))

    active, flag = self.engine.drawButton(self.menubutton, coord= (505, 420), scale = (150,45))
    if active == True:
      if flag == True and self.selecteditem != None and self.purchaseflag == False:
        self.purchaseflag = True    
    buttonfont = self.engine.renderFont("default.ttf", "Purchase", (505, 420))

    if self.purchaseflag == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarybutton, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              if len(self.party[whichplayer].inventory) < 20 and self.party[whichplayer].gold >= Item(self.items[self.selecteditem]).worth:
                self.party[whichplayer].inventory.append(self.items[self.selecteditem])
                self.party[whichplayer].gold -= Item(self.items[self.selecteditem]).worth
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

      active, flag = self.engine.drawButton(self.secondarybutton, coord= (320, 280), scale = (100,48))
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
        item = Item(str(self.party[whichplayer].inventory[i]))
        active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 90 + (26*(i-self.index))), scale = (270,24))
        if active == True:
          highlighted = True
          if item.image != None:
            self.engine.drawImage(item.image, coord= (155, 360), scale = (150,150))
          if flag == True and self.purchaseflag == False:
            self.selecteditem = i
        if self.selecteditem == i:
          self.engine.renderFont("default.ttf", "*", (75, 95 + (26*(i-self.index))), size = 24)

    
        self.engine.renderFont("default.ttf", item.name, (80, 90 + (26*(i-self.index))), size = 16, alignment = 1)
        self.engine.renderFont("default.ttf", str(item.worth/2) + "G", (335, 90 + (26*(i-self.index))), size = 16, alignment = 2)

    if maxindex == 0:
      self.engine.renderFont("default.ttf", "Your inventory is empty", (208, 168), size = 16, alignment = 2)
     
    if self.selecteditem != None and highlighted == False:
      itemimage = Item(str(self.party[whichplayer].inventory[self.selecteditem])).image
      if itemimage != None:
        self.engine.drawImage(itemimage, coord= (155, 360), scale = (150,150))

    active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 230), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index + 5 < maxindex:
          self.index += 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (208, 230))

    active, flag = self.engine.drawButton(self.secondarybutton, coord= (208, 60), scale = (220,24))
    if active == True:
      if flag == True and self.purchaseflag == False:
        if self.index - 5 >= 0:
          self.index -= 5
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (208, 60))

    active, flag = self.engine.drawButton(self.menubutton, coord= (505, 420), scale = (150,45))
    if active == True:
      if flag == True and self.selecteditem != None and self.purchaseflag == False:
        self.purchaseflag = True    
    buttonfont = self.engine.renderFont("default.ttf", "Barter", (505, 420))

    if self.purchaseflag == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarybutton, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              self.party[whichplayer].gold += (Item(str(self.party[whichplayer].inventory[self.selecteditem])).worth/2)
              self.party[whichplayer].inventory.remove(str(self.party[whichplayer].inventory[self.selecteditem]))
              self.purchaseflag = False
              self.selecteditem = None
            else:
              self.purchaseflag = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you wish to sell this item?", (320, 230), size = 20, flags = "Shadow")

  def update(self):
    self.engine.screenfade((0,0,0,255))
    if self.selectedchoice != 0:
      for key, char in Input.getKeyPresses():
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
        active, flag = self.engine.drawButton(self.menubutton, coord = (95 + (200*i), 400), scale = (150, 45))
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

        active, flag = self.engine.drawButton(self.secondarybutton, coord= (320, 280), scale = (100,48))
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
        player.updateINI()

      from Towns import Towns
      self.engine.changescene(self, Towns())


