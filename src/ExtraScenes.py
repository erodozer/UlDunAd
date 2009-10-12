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
#they are, however, required for the game to run and look cool.
#Who knows, maybe in the future some of these will become
#important scenes for the game

from GameEngine import *
import random

from View import *

class LoadingScene(Layer): #simple loading screen, time wasting but stylish
  def __init__(self, phrase = "", time = 5.0):
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
    self.bar = self.engine.loadImage(os.path.join("Data", "bars.png"))
  def update(self):
    w, h = GameEngine.w, GameEngine.h
    self.engine.screenfade((0,0,0,255))
    if self.rotate < 360:
      self.rotate += 10
    else:
      self.rotate = 0

    self.engine.drawBar(self.bar, (45, 460), scale = (450,15), frames = 6, currentframe = 5)
    self.engine.drawBar(self.bar, (45, 460), scale = (450,15), barcrop = (float(self.timer)/int(self.time * 60)), frames = 6, currentframe = 6)

    if self.loadingImage is not None:
      self.engine.drawImage(self.loadingImage, coord = (550, 390), scale = (90,90), rot = -self.rotate) 
    self.engine.renderFont("default.ttf", self.phrase, coord = (320, 432), size = 24)

    if self.timer < (self.time * 60) and self.engine.loadingscreen == True:
      self.timer += random.randint(0, 4)
    else:
      View.removescene(self)
      pygame.mixer.music.fadeout(400)
      pygame.mixer.music.unpause()

class TitleScreen(Layer): #title screen to pop up when game starts
  def __init__(self, phrase = "", time = 2.0):
    self.engine = GameEngine
    self.time = time

    self.titleImage = Drawing().loadImage(os.path.join("Data","titlescreen.png"))

    self.timer = 5.0
    self.audio = Sound().loadAudio("main.mp3")

    self.spacehit = False

  def update(self):

    if self.timer > 1.0 and self.spacehit == False:
      self.timer -= 0.1
    elif self.timer <= 4.0 and self.spacehit == True:
      self.timer += 0.1
    if self.timer < 1.0:
      self.timer = 1.0


    if self.titleImage is not None:
      self.engine.drawImage(self.titleImage, coord = (320, 240), scale = (640,480))

    self.engine.screenfade((0,0,0,255-(255*(2-self.timer))))
    if self.timer == 1.0:
      self.engine.renderFont("default.ttf", "Press SPACE", coord = (320, 432), size = 32, flags = "Shadow")

    for key, char in GameEngine.getKeyPresses():
      if key == K_SPACE and self.timer <= 1.1:
        self.spacehit = True

    if self.timer >= 4.0 and self.spacehit == True:
      View.removescene(self)
      pygame.mixer.music.unpause()
