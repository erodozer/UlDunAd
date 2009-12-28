#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

import os
import sys
import pygame
from pygame.locals import *

screen = pygame.Surface((0,0))
w, h = 0, 0

class Data:
  def __init__(self):

    path = os.path.join("Data", "Interface")
    self.battlebutton = Drawing().loadImage(os.path.join(path, "battlebutton.png"))
    self.mapbutton = Drawing().loadImage(os.path.join(path, "mapmenubutton.png"))
    self.secondarybutton = Drawing().loadImage(os.path.join(path, "secondarybutton.png"))
    self.defaultbutton = Drawing().loadImage(os.path.join(path, "defaultbutton.png"))
    self.menubutton = Drawing().loadImage(os.path.join(path, "menubutton.png"))
    self.secondarymenubutton = Drawing().loadImage(os.path.join(path, "secondarymenubutton.png"))
    self.textbutton = Drawing().loadImage(os.path.join(path, "textbutton.png"))
    self.bigtextbutton = Drawing().loadImage(os.path.join(path, "bigtextbutton.png"))
    self.menuwindowbutton = Drawing().loadImage(os.path.join(path, "menuWindowbutton.png"))

    self.window = Drawing().loadImage(os.path.join(path, "window.png"))
    self.menuWindow = Drawing().loadImage(os.path.join(path, "menuWindow.png"))

class Drawing:
  def loadImage(self, ImgData, returnnone = True):
    if returnnone == True:
      if os.path.exists(os.path.join("..", ImgData)):
        image = pygame.image.load(os.path.join("..", ImgData)).convert_alpha()
      else:
        image = None
    else:
      image = pygame.image.load(os.path.join("..", ImgData)).convert_alpha()

    return image
    
  def drawImage(self, image, coord = (320, 240), scale = None, scaleper = None, rot = None, frames = 1, currentframe = 1, direction = "Horizontal", blit = True):

    if image == None:
      return

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

    if blit == True and screen != None:
      screen.blit(image, (int(x), int(y)))

    return rect

  def drawBar(self, image, coord = (320, 240), scale = None, rot = None, frames = 1, currentframe = 1, direction = "Vertical", barcrop = 1):

    if barcrop > 1:
      barcrop = 1

    width,height = image.get_size()

    if scale < 0:
      scale = 0
    if barcrop < 0:
      barcrop = 0

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
      x = float(coord[0])*w*0.0015625
      y = float(coord[1])*h*0.002083333 - height*.5
    else:
      x = float(coord[0])*w*0.0015625 - width*.5
      y = float(coord[1])*h*0.002083333

    rect = image.get_rect(topleft=(int(x), int(y)))
    if screen != None:
      screen.blit(image, (int(x), int(y)))

    return rect

  def makeWindow(self, scale, image = None):

    if image == None:
      image = self.loadImage(os.path.join("Data", "Interface", "window.png"))

    width,height = image.get_size()

    windowrect = pygame.Surface((scale[0],scale[1]))
    ssurfaces = []
    ssurfacepos = [[32, 32], #center 
                   [32, 0], #top
                   [32, scale[1]-32], #bottom
                   [0, 32], #left
                   [scale[0]-32, 32], #right
                   [0,0], #tl corner
                   [0, scale[1]-32], #bl corner
                   [scale[0]-32, 0], #tr corner
                   [scale[0]-32, scale[1]-32]] #br corner

    wid = (0, width*.33333, width*.66666)
    hgt = (0, height*.33333, height*.66666)

    #center
    ssurfaces.append(image.subsurface((wid[1], hgt[1], width*.33333, height*.33333)))

    #top
    ssurfaces.append(image.subsurface((wid[1], hgt[0], width*.33333, height*.33333)))
    #bottom
    ssurfaces.append(image.subsurface((wid[1], hgt[2], width*.33333, height*.33333)))

    #left side
    ssurfaces.append(image.subsurface((wid[0], hgt[1], width*.33333, height*.33333)))
    #right side
    ssurfaces.append(image.subsurface((wid[2], hgt[1], width*.33333, height*.33333)))

    #top-left corner
    ssurfaces.append(image.subsurface((wid[0], hgt[0], width*.33333, height*.33333)))
    #bottom-left corner
    ssurfaces.append(image.subsurface((wid[0], hgt[2], width*.33333, height*.33333)))
    #top-right corner
    ssurfaces.append(image.subsurface((wid[2], hgt[0], width*.33333, height*.33333)))
    #bottom-right corner
    ssurfaces.append(image.subsurface((wid[2], hgt[2], width*.33333, height*.33333)))

    scalex, scaley = scale
    if scale[0] - 64 < 0:
      scalex = 64
    if scale[1] - 64 < 0:
      scaley = 64
    
    for i in range(9):

      if i == 0:#center
        ssurfaces[i] = pygame.transform.smoothscale(ssurfaces[i], (scalex - 64, scaley - 64))
      elif i <= 2 and i > 0: #left and right sides
        ssurfaces[i] = pygame.transform.smoothscale(ssurfaces[i], (scalex - 64, 32))
      elif i <= 4 and i > 2: #top and bottom sides
        ssurfaces[i] = pygame.transform.smoothscale(ssurfaces[i], (32, scaley - 64))
      else: #corners
        ssurfaces[i] = pygame.transform.smoothscale(ssurfaces[i], (32, 32))

      windowrect.blit(ssurfaces[i], (ssurfacepos[i][0], ssurfacepos[i][1]))

    return windowrect

  def drawWindow(self, window, coord):
    image = window
    width,height = image.get_size()

    width = int(float(width)*w*0.0015625)
    height = int(float(height)*h*0.002083333)
    image = pygame.transform.smoothscale(image, (width, height))

    x = float(coord[0])*w*0.0015625 - width*.5
    y = float(coord[1])*h*0.002083333 - height*.5
    rect = image.get_rect(topleft=(int(x), int(y)))

    if screen != None:
      screen.blit(image, (int(x), int(y)))

  def screenfade(self, color):
    surface = pygame.Surface((w, h))
    alpha = color[3]
    if color[3] < 0:
      alpha = 0
    elif color[3] > 255:
      alpha = 255
    surface.set_alpha(alpha)
    surface.fill((color[0],color[1],color[2]))

    screen.blit(surface,(0,0))

class Sound:
  def __init__(self):
    self.inbattle = False
    self.vol = 10

  def loadAudio(self, AudioFile, queue = False, volume = None):
    audiopath = os.path.join("..", AudioFile)

    if volume != None:
      self.volume(volume/10)
    
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
    textfont = pygame.font.Font(os.path.join("..", "Data", "Interface", "Fonts", font), size+2)
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
    textbox = Drawing().makeWindow((640, 150))
    Drawing().drawWindow(textbox, (320,405))

    self.renderMultipleFont(font, text, coord = (30, 360), size = size, flags = "Shadow", alignment = 1)

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
