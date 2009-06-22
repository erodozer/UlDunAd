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

import Config

class Library(Layer):
  def __init__(self):

    self.engine = GameEngine
    self.townname = self.engine.town

    self.library = os.path.join("Data", "Towns", self.townname, "Library")
    self.libraryback = None
    self.librarian = None
    self.booktex = None
    if os.path.exists(os.path.join(self.library, "library.png")) == True:
      self.libraryback = self.engine.loadImage(os.path.join(self.library, "library.png"))
    if os.path.exists(os.path.join(self.library, "librarian.png")) == True:    
      self.librarian = self.engine.loadImage(os.path.join(self.library, "librarian.png"))
    if os.path.exists(os.path.join(self.library, "book.png")) == True:
      self.booktex = self.engine.loadImage(os.path.join(self.library, "book.png"))
    self.enterdialog = 0

    self.books = []
    allbooks = os.listdir(self.library)
    for name in allbooks:
      if os.path.splitext(name)[1].lower() == ".txt":
        self.books.append(name)

    self.index = 0
    self.spacehit = False

  def showbook(self, book):
    if self.booktex != None:
      self.engine.drawImage(self.booktex)

  def update(self):
    if self.libraryback != None:
      self.engine.drawImage(self.libraryback, scale = (640,480))
    if self.librarian != None:
      self.engine.drawImage(self.librarian, coord = (320,160))
    
    for key, char in self.engine.getKeyPresses():
      if key == K_SPACE:
        self.spacehit = True

    if self.spacehit == True:
      self.enterdialog == 1
      self.spacehit = False

    if self.enterdialog == 0:
      self.engine.renderTextbox("default.ttf", ("Hello, welcome to the library of " + str(self.townname), ""), size = 18)
    elif self.enterdialog == 1:
      self.engine.renderTextbox("default.ttf", ("We have many books here, which would you like to check out?", ""), size = 18)
      if self.books != []:
        maxindex = len(self.books)
        for i in range(self.index, 5+self.index):
          if i < maxindex:
            itemini = Configuration(os.path.join("Data", "Items", str(Player.inventory[i])+".ini")).item
            button = self.engine.drawImage(self.secondarybutton, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
            active, flag = self.engine.mousecol(button)
            if active == True:
              itemimage = self.engine.loadImage(os.path.join("Data", "Items", str(Player.inventory[i])+".png"))
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
            if self.index + 5 < maxindex:
              self.index += 5
    
        buttonfont = self.engine.renderFont("default.ttf", "Down", (120, 132 + (26*10)))

        button = self.engine.drawImage(self.secondarybutton, coord= (120, 128 + (30*-1)), scale = (220,24))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(self.secondarybuttonactive, coord= (120, 128 + (30*-1)), scale = (220,24))
          if flag == True:
            if self.index - 5 >= 0:
              self.index -= 5
    
        buttonfont = self.engine.renderFont("default.ttf", "Up", (120, 128 + (30*-1)))
      else:
        self.engine.renderFont("default.ttf", "There are no books in this library", coord = (120, 240), size = 24)
        
