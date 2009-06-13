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
enemy = None
finished = False

mousepos = (0, 0)
clicks = []
keypresses = []

class Drawing(pygame.sprite.Sprite):

  def loadImage(self, ImgData):
    pygame.sprite.Sprite.__init__(self)

    image = pygame.image.load(ImgData).convert_alpha()
    return image
    
  def drawImage(self, image, coord = (640/2, 480/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal"):
    pygame.sprite.Sprite.__init__(self)

    if scale != None:
      image = pygame.transform.smoothscale(image, (scale[0], scale[1]))
    if rot != None:
      image = pygame.transform.rotate(image, rot)
    width,height = image.get_size()
    if direction == "Vertical":
      start = (int(currentframe)-1)*(height/frames)
      end = (height/frames)
      image = image.subsurface((0, start, width, end))
      width,height = image.get_size()
    else:
      start = (int(currentframe)-1)*(width/frames)
      end = (width/frames)
      image = image.subsurface((start, 0, end, height))
      width,height = image.get_size()

    rect = image.get_rect(topleft=(coord[0] - width/2, coord[1]-height/2))

    screen.blit(image, (coord[0] - width/2, coord[1]-height/2))

    return rect

  def drawBar(self, image, coord = (640/2, 480/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
    pygame.sprite.Sprite.__init__(self)

    if scale != None:
      image = pygame.transform.smoothscale(image, (scale[0], scale[1]))
    if rot != None:
      image = pygame.transform.rotate(image, rot)
    width,height = image.get_size()

    if direction == "Vertical":
      start = (int(currentframe)-1)*(height/frames)
      end = (height/frames)
      image = image.subsurface((0, start, width*barcrop, end))
      width,height = image.get_size()
    else:
      start = (int(currentframe)-1)*(width/frames)
      end = (width/frames)
      image = image.subsurface((start, 0, end, height))
      width,height = image.get_size()

    rect = image.get_rect(topleft=(coord[0], coord[1]-height/2))

    screen.blit(image, (coord[0], coord[1]-height/2))

    return rect

def loadImage(ImgData):
  image = Drawing().loadImage(ImgData)
  return image

def drawImage(ImgData, coord = (640/2, 480/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal"):
  rect = Drawing().drawImage(ImgData, coord, scale, rot, frames, currentframe, direction)
  return rect

def drawBar(ImgData, coord = (640/2, 480/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
  rect = Drawing().drawBar(ImgData, coord, scale, rot, frames, currentframe, direction, barcrop)
  return rect
       
def loadAudio(AudioFile):
  pygame.mixer.music.load(os.path.join("Data", "Audio", AudioFile))
  pygame.mixer.music.play()

def stopmusic():
  pygame.mixer.music.stop()

def renderFont(font, text, coord = (w/2,h/2), size = 12, flags = None, alignment = 0):
  textfont = pygame.font.Font(os.path.join("Data", font), size)
  width, height = textfont.size(text)
  if flags == "Shadow":
    renderedfont = textfont.render(text, True, (0,0,0))
    screen.blit(renderedfont, ((coord[0] - width/2)+2, (coord[1]-height/2)+2))
  renderedfont = textfont.render(text, True, (255,255,255))
  if alignment == 1:
    screen.blit(renderedfont, (coord[0], coord[1]-height/2))
  elif alignment == 2:
    screen.blit(renderedfont, (coord[0] - width, coord[1]-height/2))
  else:
    screen.blit(renderedfont, (coord[0] - width/2, coord[1]-height/2))

def renderMultipleFont(font, text, coord = (w/2,h/2), size = 12):
  textfont = pygame.font.Font(os.path.join("Data", font), size)
  for i, textline in enumerate(text):
    width, height = textfont.size(textline)
    renderedfont = textfont.render(textline, True, (255,255,255))
    screen.blit(renderedfont, (coord[0] - width/2, coord[1]-height/2+((size+3)*i)))

def screenfade(color):
  surface = pygame.Surface((w, h))
  surface.set_colorkey((color[0],color[1],color[2]))
  alpha = color[3]
  if color[3] < 0:
    alpha = 0
  elif color[3] > 255:
    alpha = 255
  surface.set_alpha(alpha)

  screen.blit(surface,(0,0))

def mousecol(rect): #for use in a scene's update command

  active = rect.collidepoint(*mousepos)
  flag = any(rect.collidepoint(clickx, clicky) for clickx, clicky in clicks)

  return active, flag

def processMouseMove(newpos):
  global mousepos
  mousepos = newpos

def processClick():
  clicks.append(mousepos)

def resetClick():
  clicks[:] = []

def processKeyPress(press):
  global finished
  if press.key == K_ESCAPE:
    finished = True
    return
  keypresses.append((press.key, press.unicode))

def getKeyPresses():
  while len(keypresses):
    yield keypresses.pop(0)

def resetKeyPresses():
  keypresses[:] = []

