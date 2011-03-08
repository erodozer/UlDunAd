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
from numpy import array, float32, int8

from math import *

LEFT = 0
CENTER = 1
RIGHT = 2

UP = 0
HORIZONTAL = 1
DOWN = 2

#a window created to be used as a background for images
class BarObj:
    def __init__(self, texture, length = 96, direction = HORIZONTAL, alignment = LEFT):
        self.texture = texture
        self.texture.changeTexture(texture.textureSurface, False)
        
        #attributes
        self.scale       = length                   #length of the bar
        self.position    = (0,0)                    #where in the window it should render
        
        self.direction = direction    
        self.alignment = alignment
                
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.pixelSize   = self.texture.pixelSize   #the actual size of the image in pixels

        #these are for calculating the smooth transitional scaling
        self.xAdd = None
        self.yAdd = None
        
        self.createArrays()

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = np.zeros((8,3), dtype=float32)
        self.texArray = np.zeros((8,2), dtype=float32)
        
        #  0  1  2  3
        #  4  5  6  7
        self.indexArray = np.array([0,   1,  5,  4,
                                    1,   2,  6,  5,
                                    2,   3,  7,  6], dtype = int8)

        self.createVerts()
        self.createTex()

    #set up vertex coordinates
    def createVerts(self):
        vtxArray = self.vtxArray

        #top left, top right, bottom right, bottom left

        #vertices
        boarderW = self.pixelSize[0]/3
        boarderH = self.pixelSize[1]
        
        xcoord = [0, boarderW, self.scale - boarderW, self.scale]
        ycoord = [0, boarderH]
        index = 0
        for i in range(2):
            for n in range(4):
                vtxArray[index,0] = xcoord[n]
                vtxArray[index,1] = ycoord[i]
                index += 1

    #set up texture coordinates
    def createTex(self):
        texArray = self.texArray

        #top left, top right, bottom right, bottom left

        #texture coordinates
        coordX = [0, 1.0/3.0, 2.0/3.0, 1.0]
        coordY = [0.0, 1.0]
        index = 0
        
        for i in range(2):
            for n in range(4):
                texArray[index,0] = coordX[n]
                texArray[index,1] = coordY[i]
                index += 1

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)
        
    def setLength(self, length = 96):
        self.scale = length
        self.createVerts()        
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(self.color)):
            self.color[i] = color[i]

    #sets where the image is anchored (left, center, or right)
    def setAlignment(self, alignment):
        alignment = eval(alignment.upper())
        if alignment >= LEFT and alignment <= RIGHT:
            self.alignment = alignment

    #sets which direction the bar is filling (up, down, horizontal)
    def setDirection(self, direction):
        direction = eval(direction.upper())
        if direction >= UP and direction <= DOWN:
            self.direction = direction

    #finally draws the image to the screen
    def draw(self):
        glPushMatrix()

        
        if self.direction == UP:
            if self.alignment == RIGHT:
                r = 90
            else:
                r = -90
        elif self.direction == DOWN:
            if self.alignment == RIGHT:
                r = -90
            else:
                r = 90
        else:
            r = 0
        
        if self.direction == HORIZONTAL:
            x = self.position[0]
            if self.alignment == CENTER:
                x -= self.scale/2.0
            elif self.alignment == RIGHT:
                x -= self.scale
            y = self.position[1]-self.pixelSize[1]/2.0
        else:
            x = self.position[0]-self.pixelSize[1]/2.0
            y = self.position[1]
            if self.direction == UP:
                if self.alignment == CENTER:
                    y += self.scale/2.0
                elif self.alignment == RIGHT:
                    y -= self.scale
            else:
                if self.alignment == CENTER:
                    y -= self.scale/2.0
                elif self.alignment == RIGHT:
                    y += self.scale
            
        glTranslatef(x, y,-.1)
        glRotatef(r, 0, 0, 1)
        
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
