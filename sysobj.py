'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import os
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image
from pygame.locals import *

import numpy as np
from numpy import array, float32

from math import *
import array

w, h = 0, 0                     #width and height of the window

#an opengl camera object
#it starts out with a view with perspective, 
#but you can make it orthographic with one call
class Camera:
    def __init__(self, (width, height)):
        self.width = float(width)
        self.height = float(height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*self.width/self.height, .1, 250.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable (GL_DEPTH_TEST)
        glEnable (GL_LIGHTING)
        glEnable (GL_LIGHT0)
        glShadeModel (GL_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    #creates an orthographic projection
    def setOrthoProjection(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()                        
        glOrtho(0, self.width, 0, self.height, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    #resets the projection to have perspective
    def resetProjection(self):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()

#texture for the ImgObj
# this is separate so then multiple objects
# can be made using the same texture and use
# less ram
class Texture:
    def __init__(self, path = "", surface = pygame.Surface((1,1))):
    
        self.texarray = glGenTextures(1)
        
        #using pygame to load the image because it already is opengl friendly
        if path != "":
            self.textureSurface = pygame.image.load(os.path.join("data", path))
        else:
            self.textureSurface = surface

        self.pixelSize = self.textureSurface.get_size()
        
        self.finalSurface = self.makePOT()
        self.textureData = pygame.image.tostring(self.finalSurface, "RGBA", 1)
        
    #makes sure the texture is a power of two for compatibilies sake
    def makePOT(self):
        wid = 2**ceil(log(self.pixelSize[0], 2))         #makes the width of the surface a power of two
        hgt = 2**ceil(log(self.pixelSize[1], 2))         #makes the height of the surface a power of two

        #scales the texture to the new power of two size
        surface = pygame.transform.smoothscale(self.textureSurface, (int(wid),int(hgt)))

        return surface 

    #binds the texture to the 3d plane
    def bind(self):

        glBindTexture(GL_TEXTURE_2D, self.texarray)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, self.finalSurface.get_width(), self.finalSurface.get_height(),
                      0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        #glScale(self.textureSurface.get_width(), self.textureSurface.get_height(), 1)
        
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

#an Image Object for rendering and collision detection (mouse)
class ImgObj:
    #each ImgObj has an ID that is also the color of its bounding box
    #an array object was used to constrain each item to an unsigned byte
    gColorID = array.array('B',[1,0,0])

    def __init__(self, texture, boundable = False, frameX = 1, frameY = 1):
        self.texture = texture

        #attributes
        self.scale       = (1.0, 1.0)               #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.angle       = 0                        #angle which the image is drawn
        self.color       = (1.0,1.0,1.0)            #colour of the image
        

        self.frameSize   = (1.0/float(frameX),1.0/float(frameY))
        self.rect        = (0.0,0.0,self.frameSize[0],self.frameSize[1])
                                                    #left, top, right, bottom, crops the texture

        self.pixelSize   = (self.texture.pixelSize[0]/frameX,
                            self.texture.pixelSize[1]/frameY)   #the actual size of the image in pixels

        self.isBoundable = boundable
        self.createColorID()

        self.createArrays()

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

    #gives the image a color ID for mouse detection
    def createColorID(self):
        #this crap needs to be done so that the pick_color isn't actually linked to the ImgObj color ID
        self.pick_color = array.array('B',ImgObj.gColorID)

	    #if after adding, the value is 0, it rolled over, so add 1 to the next item.
	    #made possible by unsigned bytes (^o^)
        ImgObj.gColorID[0] += 1;
        if(ImgObj.gColorID[0] == 0):
            ImgObj.gColorID[1] += 1
            if(ImgObj.gColorID[1] == 0):
                 ImgObj.gColorID[2] += 1

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)

    #moves the image from its current position by x and y
    def slide(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    #changes the size of the image and scales the surface
    def setScale(self, width, height):
        if width >= 0 and width <= 1:
            if height >= 0 and height <= 1:
                self.scale = (width,height)
        else:
            self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
        
    #rotates the image to the angle
    def setAngle(self, angle):
        self.angle = angle

    #rotates the image
    def rotate(self, angle):
        self.angle += angle
        
    #sets the colour of the image
    def setColor(self, color):
        self.color = color

    #change whether or not the image can be treated as a button
    def setBoundable(self, boundable):
        self.isBoundable = boundable

    #changes the frame number of the image
    def setFrame(self, x = 1, y = 1):
        self.rect = (float(x-1)*self.frameSize[0], float(y-1)*self.frameSize[1], 
                     float(x)*self.frameSize[0], float(y)*self.frameSize[1])
        self.createTex()

    #resets the transformation list
    def reset(self):
        self.transform = []
        
    #draws bounding box
    # when this is called the textures are disabled 
    # and only the color id of the image should be
    # applied to the plane
    def drawBoundingBox(self):
        glPushMatrix()

        glTranslatef(self.position[0], self.position[1],-.1)
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)

        glColor3ub(self.pick_color[0], self.pick_color[1], self.pick_color[2])

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glDrawArrays(GL_QUADS, 0, self.vtxArray.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)

        glPopMatrix()

    #finally draws the image to the screen
    def draw(self):
        glPushMatrix()

        
        glTranslatef(self.position[0], self.position[1],-.1)
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)
        glColor3f(*self.color)

        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawArrays(GL_QUADS, 0, self.vtxArray.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

#creates a texture from a font and string
# it's an extension of the ImgObj class just so I can 
# save on lines of code for the various attribute
# changing methods
class FontObj(ImgObj):
    def __init__(self, path, text = "", size = 32):
        self.texarray = glGenTextures(1)
        
        self.font = pygame.font.Font(os.path.join("data", "fonts", path), size)
        self.setText(text)                      #it is not necessary to enter a string upon initialization, 
                                                #but it is upon time of rendering
        #attributes
        self.scale     = (1.0, 1.0)             #image bounds (width, height)
        self.pixelSize = self.texture.pixelSize #the actual size of the image in pixels
        self.position  = (0,0)                  #where in the window it should render
        self.angle     = 0                      #angle which the image is drawn
        self.color     = (255,255,255)          #colour of the image
        self.rect      = (0,0,1,1)              #left, top, right, bottom, crops the texture
        
        self.createArrays()

    #changes what the font is supposed to say
    def setText(self, text):
        self.text = text
        
        self.texture = Texture("", self.font.render(self.text, True, (255,255,255)))
        self.pixelSize = self.texture.pixelSize
        self.setScale(1,1)  #makes sure the surface is resized because 
                            #the text is now different


 
#an object for sound effects
# do not use this to play music
# use BGMObj for that
class SoundObj:
    def __init__(self, path, loop = -1):
        filePath = os.path.join("data", path)

        #sound object must be wav or it will not work!
        if os.path.splittext(filePath)[1].lower() != ".wav":
            return

        #new sound object
        self.audio = pygame.mixer.Sound(filePath)
        self.volume = 10                	    #volume of the object
        self.loop = loop               		    #how many times it will loop (default = forever)
        self.play()                             #by default it will start playing as soon as it is initialized

    #changes the volume of the audio
    def setVol(self, volume):
        self.volume = volume
        self.audio.set_volume(self.volume)

    #changes how many times the song will loop 
    def setLoop(self, loop):
        self.loop = loop

    #plays the audio
    def play(self):
        self.audio.play(self.loop)

    #stops the audio
    def stop(self):
        self.audio.stop()

#an object for background music
class BGMObj:
    def __init__(self, AudioFile, volume = 10, queue = False):
        #the music file
        audiopath = os.path.join("data", AudioFile)

        self.volume = 10            #volume of the song (0-10 scale)
        self.loop = -1              #how many times it will loop (default = forever)

        #checks if the file exists and if it does then it should play it
        if os.path.exists(os.path.join(audiopath)):
            if queue == True:
                pygame.mixer.music.queue(audiopath)
            else:
                pygame.mixer.music.load(audiopath)
                pygame.mixer.music.play(self.loop)
        else:
            return None
  
    #changes how many times the song will loop
    def setLoop(loop = -1):
        self.loop = loop

    #plays the music
    def play(self):
        pygame.mixer.music.play(self.loop)

    #stops the music
    def stop(self):
        pygame.mixer.music.stop()

    #change the volume
    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume/10)

