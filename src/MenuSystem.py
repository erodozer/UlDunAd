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

import View
from View import *

import Actor
from Actor import Player
from Object import Item

from Config import *
      
import Input

class MenuSystem(Layer):
  def __init__(self):
    self.engine = GameEngine()

    self.party = []
    for i, partymember in enumerate(Actor.party):
      self.party.append(Player(partymember))

    self.choices = ["Inventory", "Spells", "Equipment", "Status", "Change Character", "Settings", "Quit Game", "Exit Menu"]
    self.help = ["Show what items you currently possess", "Plan your next battle by examining your arsenal of spells",
                 "Equip your character with armor and weapons to give him/her the edge in battle", 
                 "Not sure about your character's stats?  Want to know how to improve what with which item?",
                 "Sick of playing with this character?  How about you play a little with another", 
                 "Don't like the current feel of gameplay?  Change it up a bit to your preference",
                 "I guess you've had enough for today I suppose", "Return to your game"]

    self.menu = self.engine.createMenu(self.engine.data.menuWindow, self.engine.data.menuwindowbutton, self.choices, (90, 240), 200, 34)

    self.background = self.engine.loadImage(os.path.join("Data", "Interface", "Menu", "menubackground.png"))

    self.statusbox = self.engine.loadImage(os.path.join("Data", "Interface", "Menu", "statusbox.png"))

    self.button = self.engine.data.menubutton
    self.secondarymenubutton = self.engine.data.secondarymenubutton
    self.secondarybutton = self.engine.data.secondarybutton

    self.bar = self.engine.loadImage(os.path.join("Data", "Interface", "bars.png"))
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

    self.engine.drawImage(self.background, scale = (640,480))

    partyinv = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(partyinv.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character inventories", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    if partyinv.inventory[0] != 'None':
      maxindex = len(partyinv.inventory)
      items = [Item(n) for n in partyinv.inventory]
      for i in range(self.index, 10+self.index):
        if i < maxindex:
          active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", items[i].name, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
          if active == True:
            self.engine.drawImage(items[i].image, coord= (465, 165), scale = (150,150))
            if flag == True:
              pass

    active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", "Down", coord= (120, 132 + (26*10)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index + 10 < maxindex:
          self.index += 10
    
    active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", "Up", coord= (120, 128 + (30*-1)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index - 10 >= 0:
          self.index -= 10

    mainchoices = ["Sort", "Return"]
    for i, choice in enumerate(mainchoices):
      active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", choice, coord= (240 + (180*i), 448), scale = (160,32))
      if active == True:
        if flag == True:
          if i == 0:
            partyinv.inventory.sort()
          elif i == 1:
            self.currentlayer = "Main"
            self.updatescene = None
            partyinv.updateINI()

  def showStatus(self):
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

    self.engine.drawImage(self.background, scale = (640,480))

    player = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(player.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character status lists", (630, 80), size = 18, flags = "Shadow", alignment = 2)
    
    self.statbars = [["HP", player.currenthp, player.hp], ["SP", player.currentsp, player.sp], ["EXP", player.exp, player.explvl]]
    self.stattitles = [["ATK", player.atk], ["DEF", player.defn], ["SPD", player.spd], ["MAG", player.mag], ["EVD", player.evd]]
    self.titles = [["Class", player.playerclass], ["Race", player.race], ["Level", player.lvl]]

    for i in range(len(self.titles)):
      self.engine.renderFont("default.ttf", self.titles[i][0], (20, 128+(i*28)), size = 18, flags = "Shadow", alignment = 1)
      self.engine.renderFont("default.ttf", str(self.titles[i][1]), (200, 128+(i*28)), size = 18, flags = "Shadow", alignment = 2)
    
    for i in range(len(self.statbars)):
      self.engine.drawBar(self.bar, (45, 212+(i*28)), scale = (150,15), frames = 6, currentframe = (2*i)+1)
      self.engine.drawBar(self.bar, (45, 212+(i*28)), scale = (150,15), barcrop = (float(self.statbars[i][1])/int(self.statbars[i][2])), frames = 6, currentframe = (2*i)+2)
      self.engine.renderFont("default.ttf", self.statbars[i][0], (20, 212+(i*28)), size = 18, flags = "Shadow", alignment = 1)
      self.engine.renderFont("default.ttf", str(self.statbars[i][1]) + "/" + str(self.statbars[i][2]), (200, 212+(i*28)), size = 18, flags = "Shadow", alignment = 2)
   
      
    for i in range(len(self.stattitles)):
      self.engine.renderFont("default.ttf", self.stattitles[i][0], (400, 128+(i*28)), size = 18, flags = "Shadow", alignment = 0)
      self.engine.renderFont("default.ttf", str(self.stattitles[i][1]), (600, 128+(i*28)), size = 18, flags = "Shadow", alignment = 2)

    active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", "Return", coord= (500, 448), scale = (160,32))
    if active == True:
      if flag == True:
        self.currentlayer = "Main"
        self.updatescene = None

  def showSpells(self):
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

    self.engine.drawImage(self.background, scale = (640,480))

    partyspell = self.party[self.whichcharacter]

    self.engine.renderFont("menu.ttf", str(partyspell.name), (630, 56), size = 32, flags = "Shadow", alignment = 2)
    self.engine.renderFont("menu.ttf", "Press LEFT or RIGHT to change character spell lists", (630, 80), size = 18, flags = "Shadow", alignment = 2)

    if partyspell.spells != "None":
      maxindex = len(partyspell.spells)
      for i in range(self.index, 6+self.index):
        if i < maxindex:
          spellini = Configuration(os.path.join("..", "Data", "Spells", str(partyspell.spells[i])+".ini")).spell
          active, flag = self.engine.drawButton(self.secondarymenubutton, coord= (120, 128 + (38*(i-self.index))), scale = (220,36))
          if active == True:
            if os.path.exists(os.path.join("..", "Data", "Spells", spellini.__getattr__("element")+".png")):
              spellimage = self.engine.loadImage(os.path.join("Data", "Spells", str(spellini.__getattr__("element"))+".png"))
              self.engine.drawImage(spellimage, coord= (465, 165), scale = (150,150))
            self.engine.renderWrapText("default.ttf", spellini.__getattr__("description"), (120, 128 + (38*(i-self.index))))
    
          buttonfont = self.engine.renderFont("default.ttf", str(partyspell.spells[i]), (120, 128 + (38*(i-self.index))))
    else:
      self.engine.renderMultipleFont("default.ttf", (str(partyspell.name), "has no spells"), (120, 240), size = 24)

    active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", "Down", coord= (120, 132 + (26*10)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index + 6 < maxindex:
          self.index += 6

    active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", "Up", coord= (120, 128 + (30*-1)), scale = (220,24))
    if active == True:
      if flag == True:
        if self.index - 6 >= 0:
          self.index -= 6

    active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", "Return", coord= (320, 448), scale = (160,32))
    if active == True:
      if flag == True:
        self.currentlayer = "Main"
        self.updatescene = None

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
      active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", choice, size = 20, coord= (120, 128 + (52*i)), scale = (220,48))
      if ((active == True and self.optionselected == False) or (self.whichoption == i and self.optionselected == True)) and Engine.defaultsettings == False:
        renderhelpfont = self.engine.renderFont("default.ttf", choicehelp[i], (630, 408), alignment = 2)
        if flag == True and self.optionselected == False:
          self.optionselected = True
          self.whichoption = i
    
      self.engine.renderFont("default.ttf", str(choiceoptions[i][choiceoptions[i].index(correspondingoptions[i])]), (450, 128 + (52*i)), size = 20)

    if choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])-1 > -1 and self.optionselected == True:
      self.engine.renderFont("default.ttf", "<", (350, 128 + (52*self.whichoption)), size = 20)
    if choiceoptions[self.whichoption].index(correspondingoptions[self.whichoption])+1 < len(choiceoptions[self.whichoption]) and self.optionselected == True:
      self.engine.renderFont("default.ttf", ">", (550, 128 + (52*self.whichoption)), size = 20)
    if self.optionselected == True:
      self.engine.renderFont("default.ttf", "Press SPACE when you are satisfied with the current value selected", (10, 424), alignment = 1)
    if Engine.defaultsettings == True:
      self.engine.renderFont("default.ttf", "Default settings has been hit, you must restart before you can change settings again.", (320, 408))


    mainchoices = ["Default", "Return"]
    for i, choice in enumerate(mainchoices):
      active, flag = self.engine.drawButton(self.secondarybutton, "default.ttf", choice, coord= (240 + (180*i), 448), scale = (160,32))
      if (active == True and self.optionselected == False):
        if i == 0 and Engine.defaultsettings == False:
          self.engine.renderFont("default.ttf", "Once default is hit you may not change the options until UlDunAd is restarted", (320, 408))
        if flag == True:
          if i == 0:
            Engine.uldunadini.video.__setattr__("resolution", str(640) + "x" + str(480)+ "x" + "W")
            Engine.uldunadini.audio.__setattr__("volume", str(10))
            Engine.uldunadini.audio.__setattr__("battlevolume", str(10))
            Engine.uldunadini.audio.__setattr__("townvolume", str(10))
            Engine.uldunadini.gameplay.__setattr__("battlemode", str("wait"))
            Engine.uldunadini.save()
            Engine.defaultsettings = True
          elif i == 1:
            if Engine.defaultsettings == False:
              Engine.uldunadini.video.__setattr__("resolution", str(self.engine.resolution))
              Engine.uldunadini.audio.__setattr__("volume", str(self.engine.volume))
              Engine.uldunadini.audio.__setattr__("battlevolume", str(self.engine.battlevolume))
              Engine.uldunadini.audio.__setattr__("townvolume", str(self.engine.townvolume))
              Engine.uldunadini.gameplay.__setattr__("battlemode", str(self.engine.battlemode))
              Engine.uldunadini.save()
            self.currentlayer = "Main"
            self.updatescene = None

    for key, char in Input.getKeyPresses():
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
      elif self.updatescene == 3:
        self.showStatus()
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

        buttons = self.engine.drawMenu(self.menu)
        if self.quitactive == False:
          for i in range(len(buttons)):
            if buttons[i][0]:
              renderhelpfont = self.engine.renderFont("default.ttf", self.help[i], (630, 448), alignment = 2)
          if buttons[0][1]:
            self.updatescene = 0
            self.currentlayer = "Inventory"
          elif buttons[1][1]:
            self.updatescene = 1
            self.currentlayer = "Spells"
          elif buttons[3][1]:
            self.updatescene = 3
            self.currentlayer = "Status"
          elif buttons[4][1]:
            self.changeactive = True
          elif buttons[5][1]:
            self.updatescene = 5
            self.currentlayer = "Settings"
          elif buttons[6][1]:
            self.quitactive = True
          elif buttons[7][1]:
            from Maplist import Maplist
            self.engine.changescene(self, Maplist())

    self.engine.renderFont("menu.ttf", self.currentlayer, (30, 48), size = 48, flags = "Shadow", alignment = 1)

    if self.quitactive == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", choice, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              Input.finished = True
            else:
              self.quitactive = False
    
        self.engine.renderFont("default.ttf", "Are you sure you want to quit?", (320, 230), size = 20, flags = "Shadow")

    if self.changeactive == True:
      self.engine.screenfade((150,150,150,130))

      for i, choice in enumerate(['Yes', 'No']):
        active, flag = self.engine.drawButton(self.secondarymenubutton, "default.ttf", choice, coord= (265+(120*i), 280), scale = (100,48))
        if active == True:
          if flag == True:
            if i == 0:
              from Playerlist import Playerlist
              self.engine.changescene(self, Playerlist())
            else:
              self.changeactive = False
    
        self.engine.renderFont("default.ttf", "Are you sure you wish to change characters?", (320, 230), size = 20, flags = "Shadow")

