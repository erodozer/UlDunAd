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
import os
import sys
import View

w, h = GameEngine.w, GameEngine.h

def initMenu(buttonimg, activebuttonimg):
  button = GameEngine.loadImage(buttonimg)
  activebutton = GameEngine.loadImage(activebuttonimg)

  return button, activebutton
  
def drawMainMenu(scene, choices, buttonimg, activebuttonimg):
  for i, choice in enumerate(choices):
    button = GameEngine.drawImage(buttonimg, coord= (220, 200+(60*i)), scale = (150,45))
    active, flag = GameEngine.mousecol(button)
    if active == True:
      button = GameEngine.drawImage(activebuttonimg, coord= (220, 200+(60*i)), scale = (150,45))
      if flag == True:
        if i == 0:
          from CharacterCreator import CharacterCreator
          View.removescene(scene)
          View.addscene(CharacterCreator())
        if i == 1:
          playerpath = os.path.join("Data", "Players")
          players = []
          allplayers = os.listdir(playerpath)
          for name in allplayers:
            if os.path.splitext(name)[1].lower() == ".ini":
              players.append(name)

          if players != []:
            from Playerlist import Playerlist
            View.removescene(scene)
            View.addscene(Playerlist())

        elif i == 2:
           GameEngine.finished = True
    buttonfont = GameEngine.renderFont("default.ttf", str(choice), (220, 200+(60*i)))

def drawPlayerMenu(scene, choices, buttonimg, activebuttonimg):
  button = choices
  buttonfont = choices

  for i, choice in enumerate(choices):
    button[i] = GameEngine.drawImage(buttonimg, coord= (320, 64+(48*i)), scale = (200,32))
    active, flag = GameEngine.mousecol(button[i])
    if active == True:
      button[i] = GameEngine.drawImage(activebuttonimg, coord= (320, 64+(48*i)), scale = (200,32))
      if flag == True:
        from Maplist import Maplist
        View.removescene(scene)
        View.addscene(Maplist())
        GameEngine.player = choice
    buttonfont[i] = GameEngine.renderFont("menu.ttf", str(choice), (320, 64+(48*i)), size = 24)

def drawMapMenu(scene, choices, buttonimg, activebuttonimg):

  button = choices
  buttonfont = choices

  for i, choice in enumerate(choices):
    button[i] = GameEngine.drawImage(buttonimg, coord= (320, 64+(48*i)), scale = (200,32))
    active, flag = GameEngine.mousecol(button[i])
    if active == True:
      button[i] = GameEngine.drawImage(activebuttonimg, coord= (320, 64+(48*i)), scale = (200,32))
      if flag == True:
        GameEngine.town = choice
        import Towns
        View.removescene(scene)
        View.addscene(Towns.Towns())
        flag, active == False, False
    buttonfont[i] = GameEngine.renderFont("menu.ttf", str(choice), (320, 64+(48*i)), size = 24)
    

