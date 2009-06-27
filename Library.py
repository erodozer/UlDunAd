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
    self.bookcover = None

    if os.path.exists(os.path.join(self.library, "library.png")) == True:
      self.libraryback = self.engine.loadImage(os.path.join(self.library, "library.png"))
    if os.path.exists(os.path.join(self.library, "librarian.png")) == True:    
      self.librarian = self.engine.loadImage(os.path.join(self.library, "librarian.png"))
    if os.path.exists(os.path.join(self.library, "book.png")) == True:
      self.booktex = self.engine.loadImage(os.path.join(self.library, "book.png"))
    if os.path.exists(os.path.join(self.library, "bookcover.png")) == True:
      self.bookcover = self.engine.loadImage(os.path.join(self.library, "bookcover.png"))

    self.secondarybutton = self.engine.loadImage(os.path.join("Data", "secondarymenubutton.png"))
    self.secondarybuttonactive = self.engine.loadImage(os.path.join("Data", "secondarymenubuttonactive.png"))
    self.menubutton = self.engine.loadImage(os.path.join("Data", "defaultbutton.png"))
    self.menubuttonactive = self.engine.loadImage(os.path.join("Data", "defaultbuttonactive.png"))

    self.enterdialog = 0

    self.books = []
    allbooks = os.listdir(self.library)
    for name in allbooks:
      if os.path.splitext(name)[1].lower() == ".txt":
        self.books.append(os.path.splitext(name)[0])

    self.index = 0
    self.spacehit = False
    self.active = False

  def showbook(self, book):
    if self.booktex != None:
      self.engine.drawImage(self.booktex)

  def lookatbooks(self):

    if self.bookcover != None:
      self.engine.drawImage(self.bookcover, scale = (640,480))

    maxindex = len(self.books)
   
    buttonfont = self.engine.renderFont("menu.ttf", self.books[self.index], (320, 260), size = 18)

    button = self.engine.drawImage(self.menubutton, coord= (110, 425), scale = (150,45))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.menubuttonactive, coord= (110, 425), scale = (150,45))
      if flag == True:
        self.active = False
    buttonfont = self.engine.renderFont("default.ttf", "Return", (110, 425))

    button = self.engine.drawImage(self.menubutton, coord= (530, 425), scale = (150,45))
    active, flag = self.engine.mousecol(button)
    if active == True:
      button = self.engine.drawImage(self.menubuttonactive, coord= (530, 425), scale = (150,45))
      if flag == True:
        pass
    buttonfont = self.engine.renderFont("default.ttf", "Read", (530, 425))

  def update(self):
    if self.libraryback != None:
      self.engine.drawImage(self.libraryback, scale = (640,480))
    if self.librarian != None:
      self.engine.drawImage(self.librarian, coord = (320,160))
    
    for key, char in self.engine.getKeyPresses():
      if key == K_SPACE:
        self.spacehit = True
      if self.active == True:
        if key == K_LEFT:
          if self.index - 1 >= 0:
            self.index -= 1
        if key == K_RIGHT:
          maxindex = len(self.books)
          if self.index + 1 < maxindex:
            self.index += 1


    if self.spacehit == True:
      self.enterdialog = 1
      self.spacehit = False

    if self.enterdialog == 0:
      self.engine.renderTextbox("default.ttf", ("Hello, welcome to the library of " + str(self.townname), ""), size = 18)
    elif self.enterdialog == 1 and self.active == False:
      self.engine.renderTextbox("default.ttf", ("We have many books here, which would you like to check out?", ""), size = 18)
      for i, choice in enumerate(["Take a Look", "Leave"]):
        button = self.engine.drawImage(self.secondarybutton, coord= (120, 128 + (26*(i-self.index))), scale = (220,24))
        active, flag = self.engine.mousecol(button)
        if active == True:
          button = self.engine.drawImage(self.secondarybuttonactive, coord= (120, 128 + (26*(i-self.index))), scale = (220,24)) 
          if flag == True:
            if i == 0:
              if self.books != []:
                self.active = True
              else:
                self.enterdialog = 2
            else:
              from Towns import Towns
              View.removescene(self)
              View.addscene(Towns())

    
        buttonfont = self.engine.renderFont("default.ttf", choice, (120, 128 + (26*(i-self.index))))


    elif self.enterdialog == 2:
      self.engine.renderTextbox("default.ttf", ("There are no books in this library", ""), size = 18)
    elif self.active == True:
      self.lookatbooks()

        
