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

#a window created to be used as a background for images
class WinObj:
    def __init__(self, texture, width = 64, height = 64):
        self.texture = texture
        self.texture.changeTexture(texture.textureSurface, False)
        
        #attributes
        self.scale       = [width, height]          #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.angle       = 0                        #angle which the image is drawn
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.pixelSize   = self.texture.pixelSize   #the actual size of the image in pixels
        self.currentFrame = 0
        self.transitionTime = 32.0                  #time it takes to change the size of the window

        #these are for calculating the smooth transitional scaling
        self.xAdd = None
        self.yAdd = None
        
        self.createArrays()

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = np.zeros((16,3), dtype=float32)
        self.texArray = np.zeros((16,2), dtype=float32)
        
        #  0  1  2  3
        #  4  5  6  7
        #  8  9 10 11
        # 12 13 14 15
        self.indexArray = [0,   1,  5,  4,
                           1,   2,  6,  5,
                           2,   3,  7,  6,
                           4,   5,  9,  8,
                           5,   6, 10,  9,
                           6,   7, 11, 10,
                           8,   9, 13, 12,
                           9,  10, 14, 13,
                           10, 11, 15, 14]

        self.createVerts()
        self.createTex()

    #set up vertex coordinates
    def createVerts(self):
        vtxArray = self.vtxArray

        #top left, top right, bottom right, bottom left

        #vertices
        boarder = 32
        
        xcoord = [0, boarder, self.scale[0] - boarder, self.scale[0]]
        ycoord = [0, boarder, self.scale[1] - boarder, self.scale[1]]
        index = 0
        for i in range(4):
            for n in range(4):
                vtxArray[index,0] = xcoord[n]
                vtxArray[index,1] = ycoord[i]
                index += 1

    #set up texture coordinates
    def createTex(self):
        texArray = self.texArray

        #top left, top right, bottom right, bottom left

        #texture coordinates
        thirdPS  = (float(self.pixelSize[0])/3.0, float(self.pixelSize[1])/3.0)
        coord = [0, 1.0/3.0, 2.0/3.0, 1.0]
        index = 0
        
        for i in range(4):
            for n in range(4):
                texArray[index,0] = coord[n]
                texArray[index,1] = coord[i]
                index += 1

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)

    def getRates(self, width, height):
        self.currentFrame = 0
        self.xAdd = (width - self.scale[0])/self.transitionTime
        self.yAdd = (height - self.scale[1])/self.transitionTime
        
    #changes the size of the image and scales the surface
    def setDimensions(self, width, height):
        if self.scale == [width, height]:
            self.xAdd = None
            self.yAdd = None
            return
        
        self.scale = list(self.scale)
        
        #if it is 0 then it should be instantaneous
        if self.transitionTime > 0.0: 
            #creates a smooth scaling transition
            if self.xAdd == None and self.yAdd == None:
                self.getRates(width, height)

            if self.currentFrame <= self.transitionTime:
                self.scale[0] += self.xAdd
                self.scale[1] += self.yAdd
                self.currentFrame += 1
            else:
                self.scale = [width, height]
        else:
            self.scale = [width, height]

        self.createVerts()
        
    #rotates the image to the angle
    def setAngle(self, angle):
        self.angle = angle

    #rotates the image
    def rotate(self, angle):
        self.angle += angle
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(color)):
            self.color[i] = color[i]

    #finally draws the image to the screen
    def draw(self):
        glPushMatrix()

        glTranslatef(self.position[0] - self.scale[0]/2.0, self.position[1]-self.scale[1]/2.0,-.1)
        glRotatef(self.angle, 0, 0, 1)
        glColor4f(*self.color)
        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArray), GL_UNSIGNED_BYTE, self.indexArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()
