#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# UlDunAd - Ultimate Dungeon Adventure                              #
# Copyright (C) 2009 Blazingamer(n_hydock@comcast.net)              #
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

#these are scenes that aren't entirely neccessary to gameplay
#they are however required for the game to run and look cool
#who knows, maybe in the future some of these will become
#important scenes for the game

from GameEngine import *

from View import *

class LoadingScene(Layer): #simple loading screen, time wasting but stylish
  def __init__(self, phrase = "", time = 2.0):
    self.engine = GameEngine
    self.phrase = phrase
    self.time = time
    if os.path.exists(os.path.join("..", "Data", "loading.png")):
      self.loadingImage = Drawing().loadImage(os.path.join("Data","loading.png"))
    else:
      self.loadingImage = None
    self.rotate = 0
    self.timer = 0
    pygame.mixer.music.pause()
  def update(self):
    w, h = GameEngine.w, GameEngine.h
    self.engine.screenfade((0,0,0,255))
    if self.rotate < 360:
      self.rotate += 10
    else:
      self.rotate = 0

    if self.loadingImage is not None:
      self.engine.drawImage(self.loadingImage, coord = (w/2, h/2), rot = self.rotate) 
    self.engine.renderFont("default.ttf", self.phrase, coord = (w/2, h - h/10), size = 24)

    if self.timer < (self.time * 60) and self.engine.loadingscreen == True:
      self.timer += 1
    else:
      View.removescene(self)
      pygame.mixer.music.unpause()
