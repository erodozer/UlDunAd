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
      
class MenuSystem(Layer):
  def __init__(self, originalscene):
    self.engine = GameEngine
    self.originalscene = originalscene

    self.choices = ["Inventory", "Spells", "Equipment", "Status", "Change Character", "Options", "Quit Game", "Exit Menu"]
    self.help = ["Show what items you currently possess", "Plan your next battle by examining your arsenal of spells",
                 "Equip your character armor and weapons to give him the edge in battle", 
                 "Not sure about your character's stats?  Want to know how to improve what with which item?",
                 "Sick of playing with this character, how about you play a little with another", 
                 "Don't like the current feel of gameplay, change it up a bit to your preference",
                 "I guess you've had enough for today I suppose", "Return to your game"]

    self.background = self.engine.loadImage(os.path.join("Data", "menubackground.png"))

    self.button = self.engine.loadImage(os.path.join("Data", "menubutton.png"))
    self.buttonactive = self.engine.loadImage(os.path.join("Data", "menubuttonactive.png"))

    self.currentlayer = "Main"

  def update(self):
    
    self.engine.drawImage(self.background, scale = (640,480))

    for i, choice in enumerate(self.choices):
      button = self.engine.drawImage(self.button, coord= (110, 96+(40*i)), scale = (220,32))
      active, flag = self.engine.mousecol(button)
      if active == True:
        button = self.engine.drawImage(self.buttonactive, coord= (110, 96+(40*i)), scale = (220,32))
        renderhelpfont = self.engine.renderFont("default.ttf", self.help[i], (630, 448), alignment = 2)
        if flag == True:
          if i == 8:
            View.removescene(self)
    
      buttonfont = self.engine.renderFont("default.ttf", choice, (80, 96+(40*i)))

    self.engine.renderFont("menu.ttf", self.currentlayer, (30, 48), size = 48, flags = "Shadow", alignment = 1)
    

