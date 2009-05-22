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


import os
import sys
import pygame
from pygame.locals import *

import math

w, h = 640, 480
screen = None
player = None

class Drawing(pygame.sprite.Sprite):

  def loadImage(self, ImgData):
    pygame.sprite.Sprite.__init__(self)

    image = pygame.image.load(ImgData).convert_alpha()
    return image
    
  def drawImage(self, image, coord = (640/2, 480/2), scale = None):
    pygame.sprite.Sprite.__init__(self)

    if scale != None:
      image = pygame.transform.scale(image, (int(scale[0]), int(scale[1])))
    width,height = image.get_size()
    rect = image.get_rect(topleft=(coord[0] - width/2, coord[1]-height/2))

    screen.blit(image, (coord[0] - width/2, coord[1]-height/2))

    return rect

def loadImage(ImgData):
  image = Drawing().loadImage(ImgData)
  return image

def drawImage(ImgData, coord = (640/2, 480/2), scale = None):
  rect = Drawing().drawImage(ImgData, coord, scale)
  return rect
       
def loadAudio(AudioFile):
  pygame.mixer.music.load(os.path.join("Data", "Audio", AudioFile))
  pygame.mixer.music.play()

def stopmusic():
  pygame.mixer.music.stop()

def renderFont(font, text, coord = (w/2,h/2), size = 12):
  textfont = pygame.font.Font(os.path.join("Data", font), size)
  width, height = textfont.size(text)
  renderedfont = textfont.render(text, True, (255,255,255))
  screen.blit(renderedfont, (coord[0] - width/2, coord[1]-height/2))

def mousecol(rect): #for use in a scene's update command
  pygame.event.pump()
  mouseinput = pygame.mouse.get_pressed()
  mouseposx, mouseposy = pygame.mouse.get_pos()

  active = False
  flag = False
  if rect.collidepoint(mouseposx, mouseposy) == True:
    active = True
    if mouseinput[0] == 1:
      flag = True

  return active, flag
