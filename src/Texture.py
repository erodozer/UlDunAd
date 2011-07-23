import os
import sys

import pygame, pygame.image
from pygame.locals import *

from PIL import Image, ImageDraw

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

from Cache import Cache

textureCache = Cache(256)

#cached texture loading
def loadTexture(path = "", surface = pygame.Surface((1,1)), flip = True, fallback = None):
    if path.strip() is "":
        try:
            return textureCache.get(surface)
        except KeyError:
            textureCache.add(surface, Texture(path, surface, flip, fallback))
            print 'cache not used'
            return textureCache.get(surface)
    else:
        try:
            return textureCache.get(path)
        except KeyError:
            textureCache.add(path, Texture(path, surface, flip, fallback))
            print 'cache not used'
            return Texture(path, surface, flip, fallback)
    
#texture for the ImgObj
# this is separate so then multiple objects
# can be made using the same texture and use
# less ram
class Texture:
    def __init__(self, path = "", surface = pygame.Surface((1,1)), flip = True, fallback = None):
    
        self.id = glGenTextures(1)
        
        self.path = os.path.join("..", "data", path)
        
        if path != "":
            path = os.path.join("..", "data", path)
            #using pygame to load the image because it already is opengl friendly
            if not os.path.isfile(path):
                #fallback texture support
                #value passed for fallback must be a valid texture, not a path
                if isinstance(fallback, Texture):
                    print "Image %s was not found, using fallback image instead" % path
                    self.textureSurface = fallback.textureSurface
                else:
                    print "Image %s was not found, creating pygame surface in its place" % path
                    self.textureSurface = surface
            else:
                self.textureSurface = pygame.image.load(path)
        
        else:
            self.textureSurface = surface
        
        
        self.changeTexture(self.textureSurface, flip)

    #changes the texture without creating a new id to save on memory
    def changeTexture(self, texture, flip = True):
        self.textureSurface = texture
        
        #converts PIL images to pygame surfaces
        if isinstance(texture, Image.Image):
          self.textureSurface = pygame.image.fromstring(self.textureSurface.tostring('raw', 'RGBA', 0, -1), self.textureSurface.size, 'RGBA')
        
        self.pixelSize = self.textureSurface.get_size()
        
        self.finalSurface = self.makePOT(flip)
        self.textureData = pygame.image.tostring(self.finalSurface, "RGBA", 1)

        self.bind()
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, self.finalSurface.get_width(), self.finalSurface.get_height(),
                      0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)
        
    #makes sure the texture is a power of two for compatibilies sake
    def makePOT(self, flip = True):
        wid = 2**ceil(log(self.pixelSize[0], 2))         #makes the width of the surface a power of two
        hgt = 2**ceil(log(self.pixelSize[1], 2))         #makes the height of the surface a power of two

        #scales the texture to the new power of two size
        surface = pygame.transform.smoothscale(self.textureSurface, (int(wid),int(hgt)))
        surface = pygame.transform.flip(surface, False, flip)

        return surface 

    #binds the texture to the 3d plane
    def bind(self):

        glBindTexture(GL_TEXTURE_2D, self.id)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    #deletes the OpenGL texture
    def __del__(self):
        glDeleteTextures(self.id)
