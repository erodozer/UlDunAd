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

from Player import Player

from Config import *
      
class MenuSystem(Layer):
  def __init__(self):
    self.engine = GameEngine

    self.party = []
    for i, partymember in enumerate(self.engine.party):
      self.party.append(Player(partymember))

    self.choices = ["Inventory", "Spells", "Equipment", "Status", "Change Character", "Settings", "Quit Game", "Exit Menu"]
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
    self.changeactive = False

    self.optionselected = False
    self.whichoption = 0

  def showInventory(self):
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

    self.engine.drawImage(self.background, scale = (640,480))

    partyinv = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(partyinv.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character inventories", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    if partyinv.inventory[0] != 'None':
      maxindex = len(partyinv.inventory)
      for i in range(self.index, 10+self.index):
        if i < maxindex:
          itemini = Configuration(os.path.join("..", "Data", "Items", str(partyinv.inventory[i])+".ini")).item
          active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
          if active == True:
            itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(partyinv.inventory[i])+".png"))
            if itemimage != None:
              self.engine.drawImage(itemimage, coord= (465, 165), scale = (150,150))
            if flag == True:
              pass
    
          buttonfont = self.engine.renderFont("default.ttf", itemini.__getattr__("name"), (120, 128 + (26*(i-self.index))))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 132 + (26*10)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index + 10 < maxindex:
          self.index += 10
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (120, 132 + (26*10)))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 128 + (30*-1)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index - 10 >= 0:
          self.index -= 10
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (120, 128 + (30*-1)))

    mainchoices = ["Sort", "Return"]
    for i, choice in enumerate(mainchoices):
      active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (240 + (180*i), 448), scale = (160,32))
      if active == True:
        if flag == True:
          if i == 0:
            partyinv.inventory.sort()
          elif i == 1:
            self.currentlayer = "Main"
            self.updatescene = None
            partyinv.playerini.player.__setattr__("inventory", ", ".join(partyinv.inventory))
            partyinv.playerini.save()
    
      buttonfont = self.engine.renderFont("default.ttf", choice, (240 + (180*i), 448))

  def showSpells(self):
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

    self.engine.drawImage(self.background, scale = (640,480))

    partyspell = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(partyspell.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character spell lists", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    if partyspell.spells != "None":
      maxindex = len(partyspell.spells)
      for i in range(self.index, 6+self.index):
        if i < maxindex:
          spellini = Configuration(os.path.join("..", "Data", "Spells", str(partyspell.spells[i])+".ini")).spell
          active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 128 + (38*(i-self.index))), scale = (220,36))
          if active == True:
            if os.path.exists(os.path.join("..", "Data", "Spells", spellini.__getattr__("element")+".png")):
              spellimage = self.engine.loadImage(os.path.join("Data", "Spells", str(spellini.__getattr__("element"))+".png"))
              self.engine.drawImage(spellimage, coord= (465, 165), scale = (150,150))
            self.engine.renderWrapText("default.ttf", spellini.__getattr__("description"), (120, 128 + (38*(i-self.index))))
    
          buttonfont = self.engine.renderFont("default.ttf", str(partyspell.spells[i]), (120, 128 + (38*(i-self.index))))
    else:
      self.engine.renderMultipleFont("default.ttf", (str(partyspell.name), "has no spells"), (120, 240), size = 24)

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 132 + (26*10)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index + 6 < maxindex:
          self.index += 6
    
    buttonfont = self.engine.renderFont("default.ttf", "Down", (120, 132 + (26*10)))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 128 + (30*-1)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index - 6 >= 0:
          self.index -= 6
    
    buttonfont = self.engine.renderFont("default.ttf", "Up", (120, 128 + (30*-1)))

    active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (320, 448), scale = (160,32))
    if active == True:
      if flag == True:
        self.currentlayer = "Main"
        self.updatescene = None
    
    buttonfont = self.engine.renderFont("default.ttf", "Return", (320, 448))

  def showSettings(self):
    self.engine.drawImage(self.background, scale = (640,480))

    self.engine.renderFont("menu.ttf", "Select an option and press LEFT or RIGHT to change its value.", (630, 56), size = 20, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "All changes (including changing to default) will take effect after program restart", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    choices = ['Resolution', 'Volume', 'Town Volume', 'Battle Volume', 'Battle Mode']
    choicehelp = ['Size of the game window (W for windowed mode, F for Fullscreen)', 'How loud the music plays', 'How loud the music is in town', 'How loud the music is in battle', 'Decides whether to wait for player command (Wait) or have anything go whenever (Active)']
    choiceoptions = [["640x480xW", "800x600xW", "1024x768xW", "640x480xF", "800x600xF", "1024x768xF"],
                     ['0','1','2','3','4','5','6','7','8','9','10'],
                     ['0','1','2','3','4','5','6','7','8','9','10'],
                     ['0','1','2','3','4','5','6','7','8','9','10'],
                     ["wait", "active"]]
    correspondingoptions = [self.engine.resolution, self.engine.volume, self.engine.townvolume, self.engine.battlevolume, self.engine.battlemode]
    for i, choice in enumerate(choices):
      active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (120, 128 + (52*i)), scale = (220,48))
      if ((active == True and self.optionselected == False) or (self.whichoption == i and self.optionselected == True)) and self.engine.defaultsettings == False:
        renderhelpfont = self.engine.renderFont("default.ttf", choicehelp[i], (630, 408), alignment = 2)
        if flag == True and self.optionselected == False:
          self.optionselected = True
          self.whichoption = i
    
      buttonfont = self.engine.renderFont("default.ttf", choice, (120, 128 + (52*i)), size = 20)
      self.engine.renderFont("default.ttf", str(choiceoptions[i][choiceoptions[i].index(correspondingoptions[i])]), (450, 128 + (52*i)), size = 20)

    if choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1 > -1 and self.optionselected == True:
      self.engine.renderFont("default.ttf", "<", (350, 128 + (52*self.whichoption)), size = 20)
    if choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1 < len(choiceoptions[self.whichoption]) and self.optionselected == True:
      self.engine.renderFont("default.ttf", ">", (550, 128 + (52*self.whichoption)), size = 20)
    if self.optionselected == True:
      self.engine.renderFont("default.ttf", "Press SPACE when you are satisfied with the current value selected", (10, 424), alignment = 1)
    if self.engine.defaultsettings == True:
      self.engine.renderFont("default.ttf", "Default settings has been hit, you must restart before you can change settings again.", (320, 408))


    mainchoices = ["Default", "Return"]
    for i, choice in enumerate(mainchoices):
      active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (240 + (180*i), 448), scale = (160,32))
      if (active == True and self.optionselected == False):
        if i == 0 and self.engine.defaultsettings == False:
          self.engine.renderFont("default.ttf", "Once default is hit you may not change the options until UlDunAd is restarted", (320, 408))
        if flag == True:
          if i == 0:
            self.engine.uldunadini.video.__setattr__("resolution", str(640) + str("x") + str(480))
            self.engine.uldunadini.audio.__setattr__("volume", str(10))
            self.engine.uldunadini.audio.__setattr__("battlevolume", str(10))
            self.engine.uldunadini.audio.__setattr__("townvolume", str(10))
            self.engine.uldunadini.gameplay.__setattr__("battlemode", str("wait"))
            self.engine.uldunadini.save()
            self.engine.defaultsettings = True
          elif i == 1:
            if self.engine.defaultsettings == False:
              self.engine.uldunadini.video.__setattr__("resolution", str(self.engine.resolution))
              self.engine.uldunadini.audio.__setattr__("volume", str(self.engine.volume))
              self.engine.uldunadini.audio.__setattr__("battlevolume", str(self.engine.battlevolume))
              self.engine.uldunadini.audio.__setattr__("townvolume", str(self.engine.townvolume))
              self.engine.uldunadini.gameplay.__setattr__("battlemode", str(self.engine.battlemode))
              self.engine.uldunadini.save()
            self.currentlayer = "Main"
            self.updatescene = None

      buttonfont = self.engine.renderFont("default.ttf", choice, (240 + (180*i), 448)) 

    for key, char in GameEngine.getKeyPresses():
      if self.optionselected == True:
        if key == K_LEFT and (choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1 > -1 and self.optionselected == True):
          if self.whichoption == 0:
            self.engine.resolution = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1]
          elif self.whichoption == 1:
            self.engine.volume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1]
          elif self.whichoption == 2:
            self.engine.townvolume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1]
          elif self.whichoption == 3:
            self.engine.battlevolume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1]
          elif self.whichoption == 4:
            self.engine.battlemode = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1]
        if key == K_RIGHT and (choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1 < len(choiceoptions[self.whichoption]) and self.optionselected == True):
          if self.whichoption == 0:
            self.engine.resolution = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1]
          elif self.whichoption == 1:
            self.engine.volume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1]
          elif self.whichoption == 2:
            self.engine.townvolume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1]
          elif self.whichoption == 3:
            self.engine.battlevolume = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1]
          elif self.whichoption == 4:
            self.engine.battlemode = choiceoptions[self.whichoption][choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1]
        if key == K_SPACE:
          self.optionselected = False    
      
  def update(self):
    
    if self.updatescene != None:
      if self.updatescene == 0:
        self.showInventory()
      elif self.updatescene == 1:
        self.showSpells()
      elif self.updatescene == 5:
        self.showSettings()
    else:
      self.engine.drawImage(self.background, scale = (640,480))

      for i, player in enumerate(self.party):
        self.engine.drawImage(self.statusbox, coord = ((640-172), 130+(i*100)), scale = (345, 80))

        if player.classpic != None:
          self.engine.drawImage(player.classpic, coord = (350, 130+(i*100)), scale = (65, 65))

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
        active, flag = self.engine.drawButton(self.button, self.buttonactive, coord= (90, 96+(40*i)), scale = (180,32))
        if active == True and self.quitactive == False:
          renderhelpfont = self.engine.renderFont("default.ttf", self.help[i], (630, 448), alignment = 2)
          if flag == True:
            if i == 0:
              self.updatescene = i
              self.currentlayer = "Inventory"
            elif i == 1:
              self.updatescene = i
              self.currentlayer = "Spells"
            elif i == 4:
              self.changeactive = True
            elif i == 5:
              self.updatescene = i
              self.currentlayer = "Settings"
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
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              GameEngine.finished = True
            else:
              self.quitactive = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you want to quit?", (320, 230), size = 20, flags = "Shadow")

    if self.changeactive == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarybutton, self.secondarybuttonactive, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              from Playerlist import Playerlist
              View.removescene(self)
              View.addscene(Playerlist())
            else:
              self.changeactive = False
    
        buttonfont = self.engine.renderFont("default.ttf", choice, (265+(120*i), 280), size = 16)
        self.engine.renderFont("default.ttf", "Are you sure you wish to change characters?", (320, 230), size = 20, flags = "Shadow")

