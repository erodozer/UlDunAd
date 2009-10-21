#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# UlDunAd - Ultimate Dungeon Adventure                              #
# Copyright (C) 2009 Blazingamer|n_hydock@comcast.net               #
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
import random

import wx
import Config
import shutil

windows = []

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

class drawMainWindow(wx.Frame):
  def __init__(self, title):
    wx.Frame.__init__(self, None, -1, title, size=(490, 360), style = wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX)    

    #stats
    self.sliders = []
    self.statsliders = ["atk", "defn", "spd", "mag", "evd"]

    wx.StaticBox(self, -1, pos = (230,10), size = (250,290), label = "   Enemy Stats    ")

    self.sliders.append((wx.Slider(self, -1, minValue = 1, maxValue = 9999, pos = (250, 60), size = (220, 20), name = "hp"), wx.StaticText(self, -1, pos = (250, 46), label = "hp")))
    wx.StaticText(self, -1, pos = (400, 46), label = "(1...9999)")

    self.sliders.append((wx.Slider(self, -1, minValue = 1, maxValue = 999, pos = (250, 92), size = (220, 20), name = "sp"), wx.StaticText(self, -1, pos = (250, 78), label = "sp")))
    wx.StaticText(self, -1, pos = (400, 78), label = "(1...999)")

    for i in range(5):
      self.sliders.append((wx.Slider(self, -1, minValue = 0, maxValue = 255, pos = (250, 145 + 32*i), size = (220, 20), name = self.statsliders[i]), wx.StaticText(self, -1, pos = (250, 132 + 32*i), label = (self.statsliders[i]))))
      wx.StaticText(self, -1, pos = (400, 132 + 32*i), label = "(0...255)")

    #name
    self.name = wx.TextCtrl(self, -1, pos = (10, 40), size = (200, 24))
    wx.StaticText(self, -1, pos = (10, 20), label = "Name")

    #image
    self.image = wx.FilePickerCtrl(self, -1, pos = (10, 90), size = (200, 30), message = "Choose an image to use for the enemy", wildcard = "*.png")
    wx.StaticText(self, -1, pos = (10, 70), label = "Image")

    #rewards
    wx.StaticBox(self, -1, pos = (10,140), size = (200,160), label = "   Rewards    ")


    self.loot = wx.ComboBox(self, -1, pos = (25, 178), size = (160, 26), choices = listpath(os.path.join("Data", "Items"), flag = "filename"))
    #self.loot = wx.TextCtrl(self, -1, pos = (25, 180), size = (160, 24))
    wx.StaticText(self, -1, pos = (25, 158), label = "Items")

    self.lootchance = wx.Slider(self, -1, minValue = 0, maxValue = 100, pos = (25, 225), size = (160, 20))
    #self.lootchance = wx.TextCtrl(self, -1, pos = (25, 225), size = (160, 24))
    wx.StaticText(self, -1, pos = (25, 205), label = "Drop Rate    (0%...100%)")

    self.exp = wx.Slider(self, -1, minValue = 0, maxValue = 1000, pos = (25, 265), size = (160, 20), name = "exp")
    wx.StaticText(self, -1, pos = (25, 250), label = "Experience    (0...1000)")

    self.createButton = wx.Button(self, -1, pos = (10,315), size = (80,32), label = "Create")
    self.createButton.Bind(wx.EVT_BUTTON, self.createEnemy)
    self.cancelButton = wx.Button(self, -1, pos = (100,315), size = (80,32), label = "Cancel")
    self.cancelButton.Bind(wx.EVT_BUTTON, self.close)
    self.aboutButton = wx.Button(self, -1, pos = (390,315), size = (80,32), label = "About")
    self.aboutButton.Bind(wx.EVT_BUTTON, self.showAbout)

    self.Centre()
    self.Show(True)
      

  def createEnemy(self, event):
    name = self.name.GetValue()

    if name.strip() != "":
      enemypath = os.path.join("..", "Data", "Enemies")
      Config.Configuration(os.path.join(enemypath, "Info", name + ".ini")).save()
      enemyini = Config.Configuration(os.path.join(enemypath, "Info", name + ".ini"))

      shutil.copy(self.image.GetPath(), os.path.join(enemypath, "Graphics"))
      enemyini.enemy.__setattr__("image", os.path.basename(self.image.GetPath()))

      for i in range(len(self.sliders)):
        enemyini.enemy.__setattr__(self.sliders[i][1].GetLabel(), self.sliders[i][0].GetValue())

      enemyini.enemy.__setattr__("loot", self.loot.GetValue())
      enemyini.enemy.__setattr__("lootchances", self.lootchance.GetValue())
      enemyini.enemy.__setattr__("exp", self.exp.GetValue())

      enemyini.save()
      
  def close(self, event):
    global windows
    for window in windows:
      window.Close(True)

  def showAbout(self, event):
    global windows
    window = drawAbout("About")
    windows.append(window)
    
class drawAbout(wx.Frame):
  def __init__(self, title):
    wx.Frame.__init__(self, None, -1, title, size=(300, 340), style = wx.CAPTION | wx.CLOSE_BOX)    

    abouttext = "UlDunAd Enemy Creator \n Licensed under the GNU GPL V3 \n Copyright (C) 2009 Nicholas Hydock"
    wx.StaticBitmap(self, -1, wx.Bitmap("logoec.bmp"), pos= (10, 10))
    wx.StaticLine(self, -1, pos = (10, 190), size = (280, -1))
    wx.StaticText(self, -1, pos = (35, 210), size = (230, -1), label = abouttext, style = wx.ALIGN_CENTRE)

    self.SetFocus()
    def close(event):
      global windows
      windows.remove(self)
      self.Close(True)

    ok = wx.Button(self, -1, pos = (100, 280), size = (100, 32), label = "Close")
    ok.Bind(wx.EVT_BUTTON, close)

    self.Centre()
    self.Show(True)

app = wx.App(0)
windows.append(drawMainWindow("UlDunAd Enemy Creator"))
app.MainLoop()
