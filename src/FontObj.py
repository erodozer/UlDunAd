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

import string

LEFT   = 0
CENTER = 1
RIGHT  = 2

#creates a texture from a font and string
# it's an extension of the ImgObj class just so I can 
# save on lines of code for the various attribute
# changing methods
class FontObj:
    def __init__(self, path, text = "", size = 32, shadow = True):
        self.font = pygame.font.Font(os.path.join("..", "data", "fonts", path), size)
        self.texture = Texture()

        #attributes
        self.scale     = (1.0, 1.0)             #image bounds (width, height)
        self.position  = (0,0)                  #where in the window it should render
        self.angle     = 0                      #angle which the image is drawn
        self.color     = (255,255,255,255)      #colour of the image
        self.rect      = (0.0,0.0,1.0,1.0)      #left, top, right, bottom, crops the texture
        self.alignment = 1                      #alignment of the text (left, center , right)
        self.shadow = True                      #does the font project a shadow
        self.text = ""
        
        self.setText(text)                      #it is not necessary to enter a string upon initialization, 
                                                #but it is upon time of rendering
        
    def getDimensions(self):
        self.width = self.pixelSize[0]*self.scale[0]
        self.height = self.pixelSize[1]*self.scale[1]

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = np.zeros((4,3), dtype=float32)
        self.texArray = np.zeros((4,2), dtype=float32)

        self.createVerts()
        self.createTex()
        self.getDimensions()
        
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

        if type(text) == list:
            text = string.join(text, '')
        else:
            text = str(text)       #converts any passed value into a string
        
        #don't create new texture if the text is the same
        if text == self.text:
            return
        
        self.text = text
        self.texture.changeTexture(self.font.render(self.text, True, (255,255,255)))
        self.pixelSize = self.texture.pixelSize
        self.setScale(1,1)  #makes sure the surface is resized because 
                            #the text is now different

        self.rect      = (0.0,0.0,1.0,1.0)
        self.createArrays()

    def setAlignment(self, alignment):
        alignment = alignment.upper()
        self.alignment = eval(alignment)
        
    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)

    #moves the image from its current position by x and y
    def slide(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    #changes the size of the image and scales the surface
    def setScale(self, width, height):
        if self.scale[0] != width and self.scale[1] != height:
            if (width >= 0 and width <= 1) and (height >= 0 and height <= 1):
                self.scale = (width,height)
            else:
                self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
            self.getDimensions()
        
    def scaleWidth(self, width, keep_aspect_ratio = True):
        height = self.scale[1]
        if keep_aspect_ratio:
            height = self.scale[1] * (width/self.pixelSize[0])
        self.scale = (width/self.pixelSize[0], height)
        self.getDimensions()
        
    def scaleHeight(self, height, keep_aspect_ratio = True):
        width = self.scale[0]
        if keep_aspect_ratio:
            width = self.scale[0] * (height/self.pixelSize[1])
        self.setScale(width, height/self.pixelSize[1])
        self.getDimensions()
        
    #rotates the image to the angle
    def setAngle(self, angle):
        self.angle = angle

    #rotates the image
    def rotate(self, angle):
        self.angle += angle
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        self.color = list(self.color)
        for i in range(len(color)):
            self.color[i] = color[i]

    #fades from the current color to the new color in the set amount of time
    # remember that the color must be in RGBA format
    def fade(self, color, milliseconds):
        color = [float(c) for c in color]   #makes sure the color is an array of floats
        if list(self.color) != color:
            for i in range(len(self.color)):
                self.color[i] = self.color[i] + (color[i] - self.color[i])/milliseconds
            return True
        return False
        
    #finally draws the image to the screen
    def draw(self):
        def render(position = self.position, scale = self.scale, angle = self.angle, color = self.color):
            
            glPushMatrix()

            x = position[0]
            if self.alignment == 0:
                x += float(self.pixelSize[0])/2.0
            elif self.alignment == 2:
                x -= float(self.pixelSize[0])/2.0

            glTranslatef(x, position[1],-.1)
            glScalef(scale[0], -scale[1], 1.0)
            glRotatef(angle, 0, 0, 1)
            glColor4f(*color)

            self.texture.bind()

            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointerf(self.vtxArray)
            glTexCoordPointerf(self.texArray)
            glDrawArrays(GL_QUADS, 0, self.vtxArray.shape[0])
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            glPopMatrix()
            
            
        if self.shadow:
            render(position = (self.position[0] + 1, self.position[1] - 2), color = (0,0,0,self.color[3]))
        render()    

