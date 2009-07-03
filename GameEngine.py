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
import Config

if not os.path.exists(os.path.join("uldunad.ini")):
  Config.Configuration(os.path.join("uldunad.ini")).save()
  uldunadini = Config.Configuration(os.path.join("uldunad.ini"))
  uldunadini.video.__setattr__("resolution", str(640) + str("x") + str(480))
  uldunadini.audio.__setattr__("volume", str(10))
  uldunadini.audio.__setattr__("battlevolume", str(10))
  uldunadini.audio.__setattr__("townvolume", str(10))
  uldunadini.gameplay.__setattr__("battlemode", str("wait"))
  uldunadini.save()
else:
  uldunadini = Config.Configuration(os.path.join("uldunad.ini"))

w, h = uldunadini.video.__getattr__("resolution").split("x")
resolution = uldunadini.video.__getattr__("resolution")
battlemode = uldunadini.gameplay.__getattr__("battlemode")
volume = uldunadini.audio.__getattr__("volume")
battlevolume = uldunadini.audio.__getattr__("battlevolume")
townvolume = uldunadini.audio.__getattr__("townvolume")

w, h = int(w), int(h)

screen = None
party = []
enemy = None
finished = False
town = None

defaultsettings = False

mousepos = (0, 0)
clicks = []
keypresses = []

class Drawing(pygame.sprite.Sprite):

  def loadImage(self, ImgData):
    pygame.sprite.Sprite.__init__(self)

    image = pygame.image.load(ImgData).convert_alpha()
    return image
    
  def drawImage(self, image, coord = (w/2, h/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal"):
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

  def drawBar(self, image, coord = (w/2, h/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
    pygame.sprite.Sprite.__init__(self)

    if scale != None:
      image = pygame.transform.smoothscale(image, (scale[0], scale[1]))
    if rot != None:
      image = pygame.transform.rotate(image, rot)
    width,height = image.get_size()

    if barcrop > 1:
      barcrop = 1

    if direction == "Vertical":
      start = (int(currentframe)-1)*(height/frames)
      end = (height/frames)
      image = image.subsurface((0, start, width*barcrop, end))
      width,height = image.get_size()
    else:
      start = (int(currentframe)-1)*(width/frames)
      end = (width/frames)
      image = image.subsurface((start, 0, end, height*barcrop))
      width,height = image.get_size()

    rect = image.get_rect(topleft=(coord[0], coord[1]-height/2))

    if direction == "Vertical":
      screen.blit(image, (coord[0], coord[1]-height/2))
    else:
      screen.blit(image, (coord[0]-width/2, coord[1]))

    return rect

def loadImage(ImgData):
  image = Drawing().loadImage(ImgData)
  return image

def drawImage(ImgData, coord = (w/2, h/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal"):
  rect = Drawing().drawImage(ImgData, coord, scale, rot, frames, currentframe, direction)
  return rect

def drawBar(ImgData, coord = (w/2, h/2), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
  rect = Drawing().drawBar(ImgData, coord, scale, rot, frames, currentframe, direction, barcrop)
  return rect
       
def loadAudio(AudioFile, queue = False):
  if queue == True:
    pygame.mixer.music.queue(os.path.join("Data", "Audio", AudioFile))
  else:
    pygame.mixer.music.load(os.path.join("Data", "Audio", AudioFile))
  pygame.mixer.music.play()

def stopmusic():
  pygame.mixer.music.stop()

def renderFont(font, text, coord = (w/2,h/2), size = 12, flags = None, alignment = 0, color = (255,255,255)):
  textfont = pygame.font.Font(os.path.join("Data", font), size)
  width, height = textfont.size(text)
  if flags == "Shadow":
    renderedfont = textfont.render(text, True, (0,0,0))
    if alignment == 1:
      screen.blit(renderedfont, ((coord[0])+2, (coord[1]-height/2)+2))
    elif alignment == 2:
      screen.blit(renderedfont, ((coord[0] - width)+2, (coord[1]-height/2)+2))
    else:
      screen.blit(renderedfont, ((coord[0] - width/2)+2, (coord[1]-height/2)+2))
  renderedfont = textfont.render(text, True, color)
  if alignment == 1:
    screen.blit(renderedfont, (coord[0], coord[1]-height/2))
  elif alignment == 2:
    screen.blit(renderedfont, (coord[0] - width, coord[1]-height/2))
  else:
    screen.blit(renderedfont, (coord[0] - width/2, coord[1]-height/2))

def renderMultipleFont(font, text, coord = (w/2,h/2), size = 12, opacity = 255):
  textfont = pygame.font.Font(os.path.join("Data", font), size)
  for i, textline in enumerate(text):
    width, height = textfont.size(textline)
    renderedfont = textfont.render(textline, True, (255,255,255))
    renderedfont.set_alpha(opacity)
    screen.blit(renderedfont, (coord[0] - width/2, coord[1]-height/2+((size+3)*i)))

def renderTextbox(font, text, size = 12):
  textbox = loadImage(os.path.join("Data", "textbox.png"))
  drawImage(textbox, coord = (320, 400), scale = (w, 160))
  for i, textline in enumerate(text):
    renderFont(font, textline, coord = (30, 350+((size+3)*i)), size = size, flags = "Soft Shadow", alignment = 1)

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

