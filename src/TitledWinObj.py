'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from numpy import array, float32

import array

from math import *

from WinObj import WinObj
from BarObj import BarObj
from FontObj import FontObj

#a window created to be used as a background for images
class TitledWinObj:
    def __init__(self, window, font, caption, width = 64, height = 64, bar = None):
        
        self.window = window
        self.font = font
        
        self.bar = bar
        if isinstance(bar, BarObj):
            self.bar.setAlignment("center")
        
        #attributes
        self.scale       = [width, height]          #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.window.transitionTime = 0
        self.setPosition(0,0)
        self.setCaption(caption)
        self.setDimensions(width, height)
    
    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)
        self.window.setPosition(x, y)
        if isinstance(self.bar, BarObj):
            self.bar.setPosition(self.window.position[0], 
                                 self.window.position[1] + self.window.scale[1]/2 + 
                                                self.bar.pixelSize[1]/2)
            self.font.setPosition(self.bar.position[0], self.bar.position[1])
        else:
            self.font.setPosition(x, y + self.window.scale[1]/2 - self.font.height/2 - 5)
        
    def setCaption(self, caption):
        self.font.setText(caption)
        self.caption = caption
        
    #changes the size of the image and scales the surface
    def setDimensions(self, width, height):
        self.window.setDimensions(width, height)
        if isinstance(self.bar, BarObj):
            self.bar.setLength(self.window.scale[0])
            self.bar.setPosition(self.window.position[0], 
                                 self.window.position[1] + self.window.scale[1]/2 + 
                                            self.bar.pixelSize[1]/2)
        if self.window.scale[0] == width and self.window.scale[1] == height:
            if isinstance(self.bar, BarObj):
                self.font.scaleHeight(self.bar.pixelSize[1]-10.0)
                self.font.setPosition(self.bar.position[0], self.bar.position[1])
            else:
                self.font.scaleHeight(self.window.pixelSize[1]/3 - 10.0)
                self.font.setPosition(self.window.position[0], 
                                      self.window.position[1] + self.window.scale[1]/2 - self.font.height/2 - 5)
                
    #finally draws the image to the screen
    def draw(self):
        self.window.draw()
        if isinstance(self.bar, BarObj):
            self.bar.draw()
        self.font.draw()
