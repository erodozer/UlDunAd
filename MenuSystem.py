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
import Menu

from Player import Player

from Config import *
      
class MenuSystem(Layer):
  def __init__(self, originalscene):
    self.engine = GameEngine

    self.party = []
    for i, partymember in enumerate(self.engine.party):
      self.party.append(Player(partymember))

    self.originalscene = originalscene

    self.choices = ["Inventory", "Spells", "Equipment", "Status", "Change Character", "Options", "Quit Game", "Exit Menu"]
    self.help = ["Show what items you currently possess", "Plan your next battle by examining your arsenal of spells",
                 "Equip your character with armor and weapons to give him/her the edge in battle", 
                 "Not sure about your character's stats?  Want to know how to improve what with which item?",
                 "Sick of playing with this character?  How about you play a little with another", 
                 "Don't like the current feel of gameplay?  Change it up a bit to your preference",
                 "I guess you've had enough for today I suppose", "Return to your game"]

    self.background = self.engine.loadImage(os.path.join("Data", "menubackground.png"))

    self.statusbox = self.engine.loadImage(os.path.join("Data", "statusbox.png"))

    self.button = self.engine.loadImage(os.path.join("Data", "menubutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "menubuttonactive.png"))

    self.secondarybutton = self.engine.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.secondarybuttonactive = self.engine.loadImage(os.path.join("Data", "secondarymenubuttonactive.png"))

    self.hpbar = self.engine.loadImage(os.path.join("Data", "hpbar.png"))
    self.hpbarback = self.engine.loadImage(os.path.join("Data", "hpbarback.png"))
    self.barframe = 1

    self.currentlayer = "Main"
    self.updatescene = None
    self.index = 0
    self.whichcharacter = 0

    self.quitactive = False

  def showInventory(self):
    for key, char in GameEngine.getKeyPresses():
      if key == K_LEFT:
        if self.whichcharacter - 1 > -1:
          self.whichcharacter -= 1
        else:
          self.whichcharacter = len(self.party)-1
      if key == K_RIGHT:
        if self.whichcharacter + 1 < len(self.party):
          self.whichcharacter += 1
        else:
          self.whichcharacter = 0    

    self.engine.drawImage(self.background, scale = (640,480))

    partyinv = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(partyinv.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character inventories", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    if partyinv.inventory[0] != 'None':
      maxindex = len(partyinv.inventory)
      for i in range(self.index, 10+self.index):
        if i < maxindex:
          itemini = Configuration(os.path.join("Data", "Items", str(partyinv.inventory[i])+".ini")).item
          button = self.engine.drawImage(self.secondarybutton, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
          active, flag = self.engine.mousecol(button)
          if active == True:
            itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(partyinv.inventory[i])+".png"))
            self.engine.drawImage(itemimage, coord= (465, 165), scale = (150,150))

            button = self.engine.drawImage(self.secondarybuttonactive, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
            if flag == True:
              pass
    
          buttonfont = self.engine.renderFont("default.ttf", itemini.__getattr__("name"), (120, 128 + (26*(i-self.index))))

    button = self.engine.drawImage(self.secondarybutton, coord= (120, 132 + (26*10)), scale = (220,24))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.secondarybuttonactive, coord= (120, 132 + (26*10)), scale = (220,24))
      if flag == True:
        if self.index + 10 < maxindex:
          self.index += 10
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (120, 132 + (26*10)))

    button = self.engine.drawImage(self.secondarybutton, coord= (120, 128 + (30*-1)), scale = (220,24))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.secondarybuttonactive, coord= (120, 128 + (30*-1)), scale = (220,24))
      if flag == True:
        if self.index - 10 >= 0:
          self.index -= 10
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (120, 128 + (30*-1)))

    mainchoices = ["Sort", "Return"]
    for i, choice in enumerate(mainchoices):
      button = self.engine.drawImage(self.secondarybutton, coord= (240 + (180*i), 448), scale = (160,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.secondarybuttonactive, coord= (240 + (180*i), 448), scale = (160,32))
        if flag == True:
          if i == 0:
            partyinv.inventory.sort()
          elif i == 1:
            self.currentlayer = "Main"
            self.updatescene = None
            #saves as an array which for some reason it can not read correctly
            partyinv.playerini.player.__setattr__("inventory", ", ".join(partyinv.inventory))
            partyinv.playerini.save()
    
      buttonfont = self.engine.renderFont("default.ttf", choice, (240 + (180*i), 448))
      
  def update(self):
    
    if self.updatescene != None:
      if self.updatescene == 0:
        self.showInventory()
    else:
      if self.barframe < 30:
        self.barframe += .5
      else:
        self.barframe = 1

      self.engine.drawImage(self.background, scale = (640,480))

      for i, player in enumerate(self.party):
        self.engine.drawImage(self.statusbox, coord = ((640-172), 130+(i*100)), scale = (345, 80))


        self.engine.renderFont("default.ttf", str(player.currenthp) + "/" + str(player.hp), (505, 130+(i*100)), size = 16, flags = "Shadow", alignment = 2)
        self.engine.renderFont("default.ttf", "HP", (390, 130+(i*100)), size = 16, flags = "Shadow", alignment = 1)


        self.engine.renderFont("default.ttf", str(player.currentsp) + "/" + str(player.sp), (505, 150+(i*100)), size = 16, flags = "Shadow", alignment = 2)
        self.engine.renderFont("default.ttf", "SP", (390, 150+(i*100)), size = 16, flags = "Shadow", alignment = 1)

        self.engine.renderFont("default.ttf", str(player.name), (390, 110+(i*100)), size = 20, flags = "Shadow", alignment = 1)

        self.engine.renderFont("default.ttf", str("Lvl:"), (570, 110+(i*100)), size = 16, flags = "Shadow", alignment = 1)
        self.engine.renderFont("default.ttf", str(player.lvl), (630, 110+(i*100)), size = 16, flags = "Shadow", alignment = 2)

        self.engine.renderFont("default.ttf", str("Exp to Lvl:"), (540, 130+(i*100)), size = 16, flags = "Shadow", alignment = 1)
        self.engine.renderFont("default.ttf", str(player.exp) + "/" +str(player.explvl), (630, 150+(i*100)), size = 16, flags = "Shadow", alignment = 2)

      for i, choice in enumerate(self.choices):
        button = self.engine.drawImage(self.button, coord= (90, 96+(40*i)), scale = (180,32))
        active, flag = self.engine.mousecol(button)
        if active == True and self.quitactive == False:
          button = self.engine.drawImage(self.buttonactive, coord= (90, 96+(40*i)), scale = (180,32))
          renderhelpfont = self.engine.renderFont("default.ttf", self.help[i], (630, 448), alignment = 2)
          if flag == True:
            if i == 0:
              self.updatescene = i
              self.currentlayer = "Inventory"
            elif i == 6:
              self.quitactive = True
            elif i == 7:
              from Maplist import Maplist
              View.removescene(self)
              View.addscene(Maplist())
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (80, 96+(40*i)))


    self.engine.renderFont("menu.ttf", self.currentlayer, (30, 48), size = 48, flags = "Shadow", alignment = 1)

    if self.quitactive == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        button = self.engine.drawImage(self.secondarybutton, coord= (265+(120*i), 280), scale = (100,48))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(self.secondarybuttonactive, coord= (265+(120*i), 280), scale = (100,48))
          if flag == True:
            if i == 0:
              GameEngine.finished = True
            else:
              self.quitactive = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you want to quit?", (320, 230), size = 20, flags = "Shadow")

