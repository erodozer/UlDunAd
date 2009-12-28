#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

import Log

import os
import sys
import pygame
from pygame.locals import *
import os
import random
import Config

from Resources import *

from View import View
import Engine
from Engine import GameEngine
import Input
import Actor

FPS = 60
video_flags = 0
caption = 'UlDunAd - Ultimate Dungeon Adventure'

class Main(object):
  def __init__(self, caption, flags):

    pygame.mixer.pre_init(44100)

    pygame.init()

    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

    GameEngine().__init__()

    self.fpsClock = pygame.time.Clock()


    songpaths = ["Dungeon", "Town"]
    self.songs = []
    self.songs.extend(GameEngine().listpath(os.path.join("Data", "Audio"), "splitfiletype", "audio"))
    self.songs.extend(GameEngine().listpath(os.path.join("Data", "Audio", songpaths[0]), "splitfiletype", "audio"))
    self.songs.extend(GameEngine().listpath(os.path.join("Data", "Audio", songpaths[1]), "splitfiletype", "audio"))
    self.battlesongs = GameEngine().listpath(os.path.join("Data", "Audio", "Battle"), "splitfiletype", "audio")

    View().startup(caption, flags)

  def run(self):
    # main event loop
    Input.update()
    GameEngine().finished = Input.finished

    pygame.mixer.music.set_endevent(USEREVENT)
    if (pygame.event.poll().type == USEREVENT or pygame.mixer.music.get_busy() == False) and Actor.party != []:

      if Engine.inbattle == True:
        Sound().loadAudio(random.choice(self.battlesongs))
      else:
        if self.songs != []:
          Sound().loadAudio(random.choice(self.songs))

    View().update()

    pygame.display.update()
    Input.resetClick()

    self.fpsClock.tick(FPS)

game = Main(caption, video_flags)
while not GameEngine().finished:
  game.run()


