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
    def __init__(self, window, bar, font, caption, width = 64, height = 64, ):
        
        self.window = window
        self.bar = bar
        self.font = font
        
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
        self.bar.setPosition(self.window.position[0], 
                             self.window.position[1] + self.window.scale[1]/2 + 
                                            self.bar.pixelSize[1]/2)
        self.font.setPosition(self.bar.position[0], self.bar.position[1])
        
    def setCaption(self, caption):
        self.font.setText(caption)
        self.caption = caption
        
    #changes the size of the image and scales the surface
    def setDimensions(self, width, height):
        self.window.setDimensions(width, height)
        self.bar.setLength(self.window.scale[0])
        self.bar.setPosition(self.window.position[0], 
                             self.window.position[1] + self.window.scale[1]/2 + 
                                        self.bar.pixelSize[1]/2)
        if self.window.scale[0] == width and self.window.scale[1] == height:
            self.font.scaleHeight(self.bar.pixelSize[1]-10.0)
            self.font.setPosition(self.bar.position[0], self.bar.position[1])
                
    #finally draws the image to the screen
    def draw(self):
        self.window.draw()
        self.bar.draw()
        self.font.draw()
