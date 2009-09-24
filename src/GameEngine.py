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

from Data import Data

if not os.path.exists(os.path.join("uldunad.ini")):
  Config.Configuration(os.path.join("uldunad.ini")).save()
  uldunadini = Config.Configuration(os.path.join("uldunad.ini"))
  uldunadini.video.__setattr__("resolution", str(640) + str("x") + str(480) + str("x") + str("W"))
  uldunadini.audio.__setattr__("volume", str(10))
  uldunadini.audio.__setattr__("battlevolume", str(10))
  uldunadini.audio.__setattr__("townvolume", str(10))
  uldunadini.gameplay.__setattr__("battlemode", str("wait"))
  uldunadini.gameplay.__setattr__("loadingscreen", str("True"))
  uldunadini.save()
else:
  uldunadini = Config.Configuration(os.path.join("uldunad.ini"))

w, h, fullscreen = uldunadini.video.__getattr__("resolution").split("x")
resolution = uldunadini.video.__getattr__("resolution")
battlemode = uldunadini.gameplay.__getattr__("battlemode")
loadingscreen = uldunadini.gameplay.__getattr__("loadingscreen", "bool")
volume = uldunadini.audio.__getattr__("volume")
battlevolume = uldunadini.audio.__getattr__("battlevolume")
townvolume = uldunadini.audio.__getattr__("townvolume")

w, h = int(w), int(h)

inbattle = None
screen = None
party = []
enemy = None
finished = False
town = None
cells = None
currentcell = 1
battlesongs = []

defaultsettings = False

mousepos = (0, 0)
clicks = []
keypresses = []

data = None

class Drawing(pygame.sprite.Sprite):

  def loadImage(self, ImgData, returnnone = True):
    pygame.sprite.Sprite.__init__(self)
    if returnnone == True:
      if os.path.exists(os.path.join("..", ImgData)):
        image = pygame.image.load(os.path.join("..", ImgData)).convert_alpha()
      else:
        image = None
    else:
      image = pygame.image.load(os.path.join("..", ImgData)).convert_alpha()

    return image
    
  def drawImage(self, image, coord = (320, 240), scale = None, scaleper = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal", blit = True):
    pygame.sprite.Sprite.__init__(self)

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

    if scale != None:
      width = int(float(scale[0])*w*0.0015625)
      height = int(float(scale[1])*h*0.002083333)
      image = pygame.transform.smoothscale(image, (width, height))
    else:
      width = int(float(width)*w*0.0015625)
      height = int(float(height)*h*0.002083333)
      image = pygame.transform.smoothscale(image, (width, height))

    if rot != None:
      image = pygame.transform.rotate(image, rot)
      width,height = image.get_size()
    if scaleper != None and scale == None:
      width = int(float(width*scaleper*.01)*(w*0.0015625))
      height = int(float(height*scaleper*.01)*(h*0.002083333))
      image = pygame.transform.smoothscale(image, (width, height))

    x = float(coord[0])*w*0.0015625 - width*.5
    y = float(coord[1])*h*0.002083333 - height*.5
    rect = image.get_rect(topleft=(int(x), int(y)))

    if blit == True:
      screen.blit(image, (int(x), int(y)))

    return rect

  def drawBar(self, image, coord = (320, 240), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
    pygame.sprite.Sprite.__init__(self)

    if barcrop > 1:
      barcrop = 1

    width,height = image.get_size()

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

    if scale != None:
      if direction == "Vertical":
        width = int(float(scale[0])*w*0.0015625*barcrop)
        height = int(float(scale[1])*h*0.002083333)
      else:
        width = int(float(scale[0])*w*0.0015625)
        height = int(float(scale[1])*h*0.002083333*barcrop)
      image = pygame.transform.smoothscale(image, (width, height))
    if rot != None:
      image = pygame.transform.rotate(image, rot)
      width,height = image.get_size()

    if direction == "Vertical":
      x = float(coord[0])
      y = float(coord[1]) - height*.5
    else:
      x = float(coord[0]) - width*.5
      y = float(coord[1]) - height
    rect = image.get_rect(topleft=(int(x), int(y)))
    screen.blit(image, (int(x), int(y)))

    return rect

class Sound:
  def loadAudio(self, AudioFile, queue = False):
    global inbattle
    audiopath = os.path.join("..", AudioFile)

    if os.path.exists(os.path.join(audiopath)):
      if queue == True:
        pygame.mixer.music.queue(audiopath)
      else:
        pygame.mixer.music.load(audiopath)
      pygame.mixer.music.play()
    else:
      return None
  
  def stop(self):
    pygame.mixer.music.stop()

  def volume(self, volume):
    pygame.mixer.music.set_volume(volume)

class Font:
  def renderFont(self, font, text, coord = (320,240), size = 12, flags = None, alignment = 0, color = (255,255,255)):
    textfont = pygame.font.Font(os.path.join("..", "Data", font), size+2)
    width, height = textfont.size(text)

    width = int(float(width)*float(w/800.0))
    height = int(float(height)*float(h/600.0))

    if alignment == 1:
      x = int(float(coord[0])*w*0.0015625)
    elif alignment == 2:
      x = int(float(coord[0])*w*0.0015625 - width)
    else:
      x = int(float(coord[0])*w*0.0015625 - width/2)
    y = int(float(coord[1])*h*0.002083333-height/2)

    if flags == "Shadow":
      renderedfont = textfont.render(text, True, (0,0,0))
      renderedfont = pygame.transform.smoothscale(renderedfont, (width, height))
      screen.blit(renderedfont, (x+2, y+2))

    renderedfont = textfont.render(text, True, color)
    renderedfont = pygame.transform.smoothscale(renderedfont, (width, height))
    screen.blit(renderedfont, (x, y))

  def renderMultipleFont(self, font, text, coord = (320,240), size = 12, flags = None, alignment = 0):
    for i, textline in enumerate(text):
      self.renderFont(font, textline, coord = (coord[0], coord[1]+((size+3)*i)), size = size, color = (255,255,255), flags = flags, alignment = alignment)

  def renderTextbox(self, font, text, size = 12):
    textbox = Drawing().loadImage(os.path.join("Data", "textbox.png"))
    Drawing().drawImage(textbox, coord = (320, 400), scale = (w, 160))
    for i, textline in enumerate(text):
      self.renderFont(font, textline, coord = (30, 350+((size+3)*i)), size = size, flags = "Soft Shadow", alignment = 1, color = (0,0,0))

  def renderWrapText(self, font, text, coord = (320,240), size = 12, width = 320, alignment = 1):
    x, y = coord
    sentence = ""
    lines = 0
    textfont = pygame.font.Font(os.path.join("..", "Data", font), size)

    for n, word in enumerate(text.split(" ")):
      w, h = textfont.size(sentence + " " + word)
      if x + (320) > x + width or word == "\n":
        w, h = textfont.size(sentence)
        self.renderFont(font, sentence, (x, y), size, alignment = alignment)
        sentence = word
        y += h
        lines += 1
      else:
        if sentence == "" or sentence == "\n":
          sentence = word
        else:
          sentence = sentence + " " + word
    else:
      w, h = textfont.size(sentence)
      self.renderFont(font, sentence, (x, y), size, alignment = alignment)
      y += h
      lines += 1
   
    return lines

def loadImage(ImgData, returnnone = True):
  image = Drawing().loadImage(ImgData, returnnone)
  return image

def drawImage(ImgData, coord = (320, 240), scale = None, scaleper = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal", blit = True):
  rect = Drawing().drawImage(ImgData, coord, scale, scaleper, rot, frames, currentframe, direction, blit)
  return rect

def drawBar(ImgData, coord = (320, 240), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):
  rect = Drawing().drawBar(ImgData, coord, scale, rot, frames, currentframe, direction, barcrop)
  return rect

def drawButton(ImgData, coord = (320, 240), scale = None, rot = None, buttons = 1, index = 1, direction = "Vertical", activeshift = 0):

  whichimgdata = ImgData

  rect = Drawing().drawImage(ImgData, coord, scale, 100, rot, buttons, index, direction, blit = False)

  active = rect.collidepoint(*mousepos)
  flag = any(rect.collidepoint(clickx, clicky) for clickx, clicky in clicks)
  if active == True:
    Drawing().drawImage(ImgData, (coord[0]+activeshift, coord[1]), scale, rot, frames = 2, currentframe = 2, direction = direction)
  else:
    Drawing().drawImage(ImgData, coord, scale, rot, frames = 2, currentframe = 1, direction = direction)

  return active, flag

def renderFont(font, text, coord = (320,240), size = 12, flags = None, alignment = 0, color = (255,255,255)):
  Font().renderFont(font,text,coord,size,flags,alignment,color)

def renderMultipleFont(font, text, coord = (320,240), size = 12, flags = None):
  Font().renderMultipleFont(font,text,coord,size,flags)

def renderTextbox(font, text, size = 12):
  Font().renderTextbox(font,text,size)

def renderWrapText(font, text, coord = (320,240), size = 12, width = 320, alignment = 1):
  lines = Font().renderWrapText(font, text, coord, size, width, alignment)
  return lines

def screenfade(color):
  surface = pygame.Surface((w, h))
  alpha = color[3]
  if color[3] < 0:
    alpha = 0
  elif color[3] > 255:
    alpha = 255
  surface.set_alpha(alpha)
  surface.fill((color[0],color[1],color[2]))

  screen.blit(surface,(0,0))

def listpath(path, condition = "splitfiletype", value = ".ini", flag = None):
  items = []
  listitems = os.listdir(os.path.join("..", path))
  for name in listitems:
    if condition == "splitfiletype":
      if value == "audio":
        if os.path.splitext(name)[1].lower() == ".mp3" or os.path.splitext(name)[1].lower() == ".ogg" or os.path.splitext(name)[1].lower() == ".m4a" or os.path.splitext(name)[1].lower() == ".flac" or os.path.splitext(name)[1].lower() == ".aac":
          items.append(os.path.join(path, name))
      else:
        if os.path.splitext(name)[1].lower() == value:
          if flag == "filename":
            items.append(os.path.splitext(name)[0])
          else:
            items.append(name)
    elif condition == "searchfile":
      if os.path.exists(os.path.join("..", path,name,value)):
        items.append(name)

  return items  

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


