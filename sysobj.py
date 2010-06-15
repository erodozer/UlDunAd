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
    def __init__(self, path):
    
        #using pygame to load the image because it already is opengl friendly
        self.textureSurface = pygame.image.load(os.path.join("data", path))
        self.textureData = pygame.image.tostring(self.textureSurface, "RGBA", 1)
        
        #this is necessary for more accurate scaling 
        # of the image to different window resolutions
        self.pixelSize = self.textureSurface.get_size()

    #binds the texture to the 3d plane
    def bind(self):

        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, self.pixelSize[0], self.pixelSize[1], 0,
                      GL_RGBA, GL_UNSIGNED_BYTE, self.textureData );
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

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

    def __init__(self, texture, boundable = False):
        self.texture = texture

        #attributes
        self.scale       = (1.0, 1.0)           #image bounds (width, height)
        self.pixelSize   = (1.0, 1.0)           #the actual size of the image in pixels
        self.position    = (0,0)                #where in the window it should render
        self.angle       = 0                    #angle which the image is drawn
        self.color       = (1.0,1.0,1.0)        #colour of the image
        self.rect        = (0,0,1,1)            #left, top, right, bottom, crops the texture

        self.isBoundable = boundable
        self.createColorID()

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        rect = self.rect    #not really necessary, it just saves on some typing
                            #because I got sick of typing "self." all the time

        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        vtxArray = np.zeros((4,3), dtype=float32)
        texArray = np.zeros((4,2), dtype=float32)

        #top left, top right, bottom right, bottom left

        #vertices
        vtxArray[0,0] = -0.5; vtxArray[0,1] =  0.5
        vtxArray[1,0] =  0.5; vtxArray[1,1] =  0.5
        vtxArray[2,0] =  0.5; vtxArray[2,1] = -0.5
        vtxArray[3,0] = -0.5; vtxArray[3,1] = -0.5

        #texture coordinates
        texArray[0,0] = rect[0]; texArray[0,1] = rect[3]
        texArray[1,0] = rect[2]; texArray[1,1] = rect[3]
        texArray[2,0] = rect[2]; texArray[2,1] = rect[1]
        texArray[3,0] = rect[0]; texArray[3,1] = rect[1]
        
        return vtxArray, texArray

    #gives the image a color ID for mouse detection
    def createColorID(self):
        #this crap needs to be done so that the pick_color isn't actually linked to the ImgObj color ID
        self.pick_color = array.array('B',[ImgObj.gColorID[0],ImgObj.gColorID[1],ImgObj.gColorID[2]])

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
        wScale, hScale = w/800.0, h/600.0
        if width >= 0 and width <= 1:
            wid = self.texture.pixelSize[0]*width*(self.rect[2]-self.rect[0])
        else:
            wid = width*(self.rect[2]-self.rect[0])
            
        if height >= 0 and height <= 1:
            hgt = self.texture.pixelSize[1]*height*(self.rect[3]-self.rect[1])
        else:
            hgt = height*(self.rect[3]-self.rect[1])
        self.scale = (wid * wScale, hgt * hScale)
        
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

    #changes the crop box
    def setRect(self, rect):
        self.rect = rect

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

        vtx, tex = self.createArrays()
        glColor3ub(self.pick_color[0], self.pick_color[1], self.pick_color[2])

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(vtx)
        glDrawArrays(GL_QUADS, 0, vtx.shape[0])
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
        vtx, tex = self.createArrays()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(vtx)
        glTexCoordPointerf(tex)
        glDrawArrays(GL_QUADS, 0, vtx.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

#creates a texture from a font and string
class FontObj(ImgObj):
    def __init__(self, path, text = "", size = 32):

        self.textures = [0,0]

        self.font = pygame.font.Font(os.path.join("data", "fonts", path), size)
        self.text = ""            #it is not necessary to enter a string upon initialization, 
                                    #but it is upon time of rendering
        #attributes
        self.scale       = (1.0, 1.0)           #image bounds (width, height)
        self.pixelSize   = (1.0, 1.0)           #the actual size of the image in pixels
        self.position    = (0,0)                #where in the window it should render
        self.angle       = 0                    #angle which the image is drawn
        self.color       = (255,255,255)        #colour of the image
        self.rect        = (0,0,1,1)            #left, top, right, bottom, crops the texture

    def setText(self, text):
        self.text = text

    #binds the texture to the 3d plane
    def bind(self):
        surface = self.font.render(self.text, True, (255,255,255))
        s_string = pygame.image.tostring(surface, 'RGBA', True)
        self.pixelSize = surface.get_size()
        

        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, self.pixelSize[0], self.pixelSize[1], 0,
                      GL_RGBA, GL_UNSIGNED_BYTE, s_string );
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    #draws the font to the screen
    def draw(self):
        glPushMatrix()

        glTranslatef(self.position[0], self.position[1],-.1)
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)
        glColor3ub(*self.color)

        self.bind()
        vtx, tex = self.createArrays()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(vtx)
        glTexCoordPointerf(tex)
        glDrawArrays(GL_QUADS, 0, vtx.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()
 
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

