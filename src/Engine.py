#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

#This class defines all the methods used throughout for performing tasks
#from loading and drawing images to playing music.  Basically all it
#does is add shortcuts for me to use throughout the game's code

import os
import sys
import pygame
from pygame.locals import *

import math
import Config

from Resources import *

import Input

data = None

if not os.path.exists(os.path.join("..", "uldunad.ini")):
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


#battle
inbattle = None
    
#dungeon and location
town = None
cells = None
currentcell = 1

defaultsettings = False

class GameEngine:
  def __init__(self):
    self.finished = Input.finished

    self.w, self.h, self.fullscreen = uldunadini.video.__getattr__("resolution").split("x")
    self.resolution = uldunadini.video.__getattr__("resolution")
    self.battlemode = uldunadini.gameplay.__getattr__("battlemode")
    self.loadingscreen = uldunadini.gameplay.__getattr__("loadingscreen", "bool")
    self.volume = uldunadini.audio.__getattr__("volume")
    self.battlevolume = uldunadini.audio.__getattr__("battlevolume")
    self.townvolume = uldunadini.audio.__getattr__("townvolume")

    self.w, self.h = int(self.w), int(self.h)

  
  def loadAudio(self, AudioFile, queue = False, volume = None):
    Sound().loadAudio(AudioFile, queue, volume)

  def loadImage(self, ImgData, returnnone = True):
    image = Drawing().loadImage(ImgData, returnnone)
    return image

  def drawImage(self, ImgData, coord = (320, 240), scale = None, scaleper = None, rot = None, frames = 1, 
                currentframe = 1, direction = "Horizontal", blit = True):

    rect = Drawing().drawImage(ImgData, coord, scale, scaleper, rot, frames, currentframe, direction, blit)
    return rect

  def drawBar(self, ImgData, coord = (320, 240), scale = None, rot = None, frames = 1, currentframe = 1, 
              direction = "Vertical", barcrop = 1):

    rect = Drawing().drawBar(ImgData, coord, scale, rot, frames, currentframe, direction, barcrop)
    return rect

  def drawButton(self, ImgData, font = "default.ttf", text = "", coord = (320, 240), scale = None, size = 12, 
                 rot = None, buttons = 1, index = 1, direction = "Vertical", activeshift = 0):

    whichimgdata = ImgData

    rect = Drawing().drawImage(ImgData, coord, scale, 100, rot, buttons, index, direction, blit = False)

    active, flag = Input.mousecol(rect)
    if active == True:
      Drawing().drawImage(ImgData, (coord[0]+activeshift, coord[1]), scale, rot, frames = 2, currentframe = 2, direction = direction)
    else:
      Drawing().drawImage(ImgData, coord, scale, rot, frames = 2, currentframe = 1, direction = direction)

    self.renderFont(font, text, coord, size)
    return active, flag

  def makeWindow(self, scale, image = None):
    window = Drawing().makeWindow(scale, image)
    return window

  def drawWindow(self, window, coord):
    Drawing().drawWindow(window, coord)

  def renderFont(self, font = "default.ttf", text = "", coord = (320,240), size = 12, flags = None, 
                 alignment = 0, color = (255,255,255)):
    Font().renderFont(font,text,coord,size,flags,alignment,color)

  def renderMultipleFont(self, font, text, coord = (320,240), size = 12, flags = None):
    Font().renderMultipleFont(font,text,coord,size,flags)

  def renderTextbox(self, font, text, size = 12):
    Font().renderTextbox(font,text,size)

  def renderWrapText(self, font, text, coord = (320,240), size = 12, width = 320, alignment = 1):
    lines = Font().renderWrapText(font, text, coord, size, width, alignment)
    return lines

  def createMenu(self, ImgData, ButtonImgData, choices, coord, width, spacing = 34):

    scale = (width, len(choices)*spacing + 6)
    if ImgData == None:
      window = None
    else:
      window = self.makeWindow(scale, ImgData)

    menu = [ButtonImgData, window, choices, coord, scale, spacing]

    return menu

  def drawMenu(self, menu):
    if menu[1] != None:
      self.drawWindow(menu[1], menu[3])
    buttons = []
    for i, choice in enumerate(menu[2]):
      xcoord = menu[3][0] - menu[4][0]/2 + (menu[4][0]-5)/2 + 2
      ycoord = (menu[3][1] - menu[4][1]/2) + 18 + (i*menu[5]+2)
      textxcoord = menu[3][0] - menu[4][0]/2 + 20

      rect = Drawing().drawImage(menu[0], coord = (xcoord, ycoord), scale = (menu[4][0]-4, 32), frames = 1, currentframe = 1, direction = "Vertical", blit = False)

      active, flag = Input.mousecol(rect)
      if active == True:
        self.drawImage(menu[0], coord = (xcoord, ycoord), scale = (menu[4][0]-4, 32), frames = 2, currentframe = 2, direction = "Vertical")
        self.renderFont(font = "default.ttf", text = choice, coord = (textxcoord, ycoord), size = 14, color = (255, 255, 255), alignment = 1)
      else:
        self.drawImage(menu[0], coord = (xcoord, ycoord), scale = (menu[4][0]-4, 32), frames = 2, currentframe = 1, direction = "Vertical")
        self.renderFont(font = "default.ttf", text = choice, coord = (textxcoord, ycoord), size = 14, color = (120, 120, 120), alignment = 1)

      buttons.append((active, flag))
    
    return buttons

  def screenfade(self, color):
    Drawing().screenfade(color)

  def listpath(self, path, condition = "splitfiletype", value = ".ini", flag = None):
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

  def changescene(self, currentscene, newscene):
    from View import View

    View().removescene(currentscene)
    View().addscene(newscene)

