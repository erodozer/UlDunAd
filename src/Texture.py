import os
import sys

import pygame, pygame.image
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

#texture for the ImgObj
# this is separate so then multiple objects
# can be made using the same texture and use
# less ram
class Texture:
    def __init__(self, path = "", surface = pygame.Surface((1,1))):
    
        self.id = glGenTextures(1)
        
        #using pygame to load the image because it already is opengl friendly
        if path != "":
            self.textureSurface = pygame.image.load(os.path.join("..", "data", path))
        else:
            self.textureSurface = surface
            
        self.changeTexture(self.textureSurface)

    #changes the texture without creating a new id to save on memory
    def changeTexture(self, texture):
        self.textureSurface = texture
        self.pixelSize = self.textureSurface.get_size()
        
        self.finalSurface = self.makePOT()
        self.textureData = pygame.image.tostring(self.finalSurface, "RGBA", 1)

        self.bind()
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, self.finalSurface.get_width(), self.finalSurface.get_height(),
                      0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)
        
    #makes sure the texture is a power of two for compatibilies sake
    def makePOT(self):
        wid = 2**ceil(log(self.pixelSize[0], 2))         #makes the width of the surface a power of two
        hgt = 2**ceil(log(self.pixelSize[1], 2))         #makes the height of the surface a power of two

        #scales the texture to the new power of two size
        surface = pygame.transform.smoothscale(self.textureSurface, (int(wid),int(hgt)))
        surface = pygame.transform.flip(surface, False, True)

        return surface 

    #binds the texture to the 3d plane
    def bind(self):

        glBindTexture(GL_TEXTURE_2D, self.id)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    #deletes the OpenGL texture
    def __del__(self):
        glDeleteTextures(self.id)
