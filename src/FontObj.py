'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''
import os
import sys

import pygame, pygame.image
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from numpy import array, float32

from Texture import Texture

#creates a texture from a font and string
# it's an extension of the ImgObj class just so I can 
# save on lines of code for the various attribute
# changing methods
class FontObj:
    def __init__(self, path, text = "", size = 32):
        self.font = pygame.font.Font(os.path.join("..", "data", "fonts", path), size)
        self.texture = Texture()

        #attributes
        self.scale     = (1.0, 1.0)             #image bounds (width, height)
        self.position  = (0,0)                  #where in the window it should render
        self.angle     = 0                      #angle which the image is drawn
        self.color     = (1.0,1.0,1.0,1.0)      #colour of the image
        self.rect      = (0.0,0.0,1.0,1.0)      #left, top, right, bottom, crops the texture
        self.alignment = "center"               #alignment of the text (left, center, right)

        self.setText(text)                      #it is not necessary to enter a string upon initialization, 
                                                #but it is upon time of rendering

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = np.zeros((4,3), dtype=float32)
        self.texArray = np.zeros((4,2), dtype=float32)

        self.createVerts()
        self.createTex()

    #set up vertex coordinates
    def createVerts(self):
        vtxArray = self.vtxArray

        #top left, top right, bottom right, bottom left

        #vertices
        # by using these numbers pictures are now moved by the center
        # coordinate instead of the top left.  I, personally, find it
        # easier to use.
        halfPS = (float(self.pixelSize[0])/2.0, float(self.pixelSize[1])/2.0)
        
        if (self.alignment == "left") or (self.alignment == "right"):
            vtxArray[0,0] = 0;                 vtxArray[0,1] =  halfPS[1]
            vtxArray[1,0] = self.pixelSize[0]; vtxArray[1,1] =  halfPS[1]
            vtxArray[2,0] = self.pixelSize[0]; vtxArray[2,1] = -halfPS[1]
            vtxArray[3,0] = 0;                 vtxArray[3,1] = -halfPS[1]
        else:
            vtxArray[0,0] = -halfPS[0]; vtxArray[0,1] =  halfPS[1]
            vtxArray[1,0] =  halfPS[0]; vtxArray[1,1] =  halfPS[1]
            vtxArray[2,0] =  halfPS[0]; vtxArray[2,1] = -halfPS[1]
            vtxArray[3,0] = -halfPS[0]; vtxArray[3,1] = -halfPS[1]

    #set up texture coordinates
    def createTex(self):
        rect = self.rect    #not really necessary, it just saves on some typing
                            #because I got sick of typing "self." all the time
       
        texArray = self.texArray

        #top left, top right, bottom right, bottom left

        #texture coordinates
        texArray[0,0] = rect[0]; texArray[0,1] = rect[3]
        texArray[1,0] = rect[2]; texArray[1,1] = rect[3]
        texArray[2,0] = rect[2]; texArray[2,1] = rect[1]
        texArray[3,0] = rect[0]; texArray[3,1] = rect[1]

    #changes what the font is supposed to say
    def setText(self, text):
        self.text = text
        
        self.texture.changeTexture(self.font.render(self.text, True, (255,255,255)))
        self.pixelSize = self.texture.pixelSize
        self.setScale(1,1)  #makes sure the surface is resized because 
                            #the text is now different

        self.rect      = (0.0,0.0,1.0,1.0)
        self.createArrays()

    def setAlignment(self, alignment):
        self.alignment = alignment.lower()

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)

    #moves the image from its current position by x and y
    def slide(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    #changes the size of the image and scales the surface
    def setScale(self, width, height):
        if (width >= 0 and width <= 1) and (height >= 0 and height <= 1):
                self.scale = (width,height)
        else:
            self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))

    def scaleWidth(self, width, keep_aspect_ratio = True):
        height = self.scale[1]
        if keep_aspect_ratio:
            height = self.scale[1] * (width/self.pixelSize[0])
        self.scale = (width/self.pixelSize[0], height)

    def scaleHeight(self, height, keep_aspect_ratio = True):
        width = self.scale[0]
        if keep_aspect_ratio:
            width = self.scale[0] * (height/self.pixelSize[1])
        self.scale = (width, height/self.pixelSize[1])
        
    #rotates the image to the angle
    def setAngle(self, angle):
        self.angle = angle

    #rotates the image
    def rotate(self, angle):
        self.angle += angle
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(self.color)):
            self.color[i] = color[i]

    #finally draws the image to the screen
    def draw(self):
        glPushMatrix()

        if self.alignment == "right":
            x = self.position[0] - self.pixelSize[0]
        else:
            x = self.position[0]
        glTranslatef(x, self.position[1],-.1)
        glScalef(self.scale[0], -self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)
        glColor4f(*self.color)

        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawArrays(GL_QUADS, 0, self.vtxArray.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()
