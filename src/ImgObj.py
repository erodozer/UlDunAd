'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from numpy import array, float32

import array

from math import *

LEFT   = 0
CENTER = 1
RIGHT  = 2

#an Image Object for rendering and collision detection (mouse)
class ImgObj:
    clickableObjs = []  #images that are clickable
    
    def __init__(self, texture, boundable = False, frameX = 1, frameY = 1):
        self.texture = texture

        #attributes
        self.scale       = (1.0, 1.0)               #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.angle       = 0                        #angle which the image is drawn
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.frameSize   = (1.0/float(frameX),1.0/float(frameY))
                                                    #the size of each cell when divided into frames
        self.rect        = (0.0,0.0,self.frameSize[0],self.frameSize[1])
                                                    #left, top, right, bottom, crops the texture
        self.alignment  = CENTER                   #alignment of the vertices for placement
        self.pixelSize   = (self.texture.pixelSize[0]/frameX,
                            self.texture.pixelSize[1]/frameY)   
                                                    #the actual size of the image in pixels
                                                    
        self.width, self.height = self.pixelSize    #the width and height after transformations
                                                    # are taken into account

        self.isBoundable = boundable                #is the picture one that can be read for mouse detection
        if self.isBoundable:                        #if it is then append to the list of clickable objects
            ImgObj.clickableObjs.append(self)
            
        self.bounds  = (0.0, 1.0, 0.0, 1.0)         #the bounds of the picture
        self.tBounds = []

        self.createArrays()
        
        #first is position, second is angle
        self.rates = [[0.0,0.0, 100.0],
					   [0.0, 100.0]]
        self.targets = [[0.0,0.0],
						[0.0]]
                        
        #for animation purposes
        self.frames = [frameX, frameY]      #number of frames (x axis, y axis)
        self.currentFrame = [0, 0]          #current frame
                                            #will reverse the animation when looping
        self.reverseH = False               #   reverse along frameX
        self.reverseV = False               #   reverse along frameY
        
        self.transformed = False                    #did the image's attributes change

    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = np.zeros((4,3), dtype=float32)
        self.texArray = np.zeros((4,2), dtype=float32)
        self.indexArray = [0,1,2,3]

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
        texArray[0,0] = rect[0]; texArray[0,1] = rect[1]
        texArray[1,0] = rect[2]; texArray[1,1] = rect[1]
        texArray[2,0] = rect[2]; texArray[2,1] = rect[3]
        texArray[3,0] = rect[0]; texArray[3,1] = rect[3]

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        if not self.position == (x, y):
            self.position = (x, y)
            self.transformed = True

    #=====FUNCTIONING BUT SLOW, CALCULATIONS NEED FIXING=====
    #calculates the rates for sliding and spinning
    def calculateRates(self):
        calcRate = self.rates[0][2]
        if self.currentFrame < self.rates[0][2]:
            calcRate = self.rates[0][2] - self.currentFrame[0]
        else:
            self.currentFrame[0] = 0
        self.rates[0][0] = (self.targets[0][0] - self.position[0])/calcRate
        self.rates[0][1] = (self.targets[0][1] - self.position[1])/calcRate 
        
        calcRate = self.rates[1][1]
        if self.currentFrame < self.rates[1][1]:
            calcRate = self.rates[1][1] - self.currentFrame[1]
        else:
            self.currentFrame[1] = 0
        self.rates[1][0] = (self.targets[1] - self.angle)/calcRate

    #moves the image from its current position by x and y
    # milliseconds defines how long you want it to take to
    # slide to the new position.		
    def slide(self, x, y, milliseconds = 32.0):
        if self.targets[0] != [x,y]:
            self.targets[0] = [x,y]
            self.rates[0][2] = milliseconds
            self.calculateRates()
        else:
            if self.currentFrame[0] < self.rates[0][2]:
                self.position = (self.position[0] + self.rates[0][0],
								 self.position[1] + self.rates[0][1])
                self.currentFrame[0] += 1
            else:
                self.position = (x, y)
    #smoothly rotates the image to this angle in this many frames
    def spin(self, angle, milliseconds = 32.0):

        if self.targets[1] != angle:
            self.targets[1] = angle
            self.rates[1][1] = milliseconds
            self.calculateRates()
        else:
            if self.currentFrame[1] < self.rates[1][1]:
                self.angle += self.rates[1][0]
                self.currentFrame[1] += 1
            else:
                self.angle = angle
                    
    #changes the size of the image and scales the surface
    def setScale(self, width = 1.0, height = 1.0, inPixels = False):
        if not inPixels:
            if not self.scale == (width, height):
                self.scale = (width,height)
                self.transformed = True
                self.width = self.scale[0] * self.pixelSize[0]
                self.height = self.scale[1] * self.pixelSize[1]
        else:
            if not self.scale == (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1])):
                self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
                self.transformed = True
                self.width = width
                self.height = height

    #scales the image size by only the width
    # if keep_aspect_ratio is true it will scale the height
    # as well in order to maintain the aspect ratio
    def scaleWidth(self, width, keep_aspect_ratio = True):
        height = self.scale[1]
        if keep_aspect_ratio:
            height = self.scale[1] * (width/self.pixelSize[0])
        if not self.scale == (width/self.pixelSize[0], height):
            self.scale = (width/self.pixelSize[0], height)
            self.transformed = True
            self.width = width*self.pixelSize[0]
            
    #same as scaleWidth except that the value passed
    #is the height of the image instead of the width
    def scaleHeight(self, height, keep_aspect_ratio = True):
        width = self.scale[0]
        if keep_aspect_ratio:
            width = self.scale[0] * (height/self.pixelSize[1])
        if not self.scale == (width, height/self.pixelSize[1]):
            self.scale = (width, height/self.pixelSize[1])
            self.transformed = True
            self.height = height
            
    #rotates the image to the angle
    def setAngle(self, angle):
        if not self.angle == angle:
            self.angle = angle
            self.transformed = True

    #rotates the image
    def rotate(self, angle):
        if not self.angle == (self.angle + angle):
            self.angle += angle
            self.transformed = True
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(self.color)):
            self.color[i] = float(color[i])

    #fades from the current color to the new color in the set amount of time
    # remember that the color must be in RGBA format
    def fade(self, color, milliseconds):
        color = [float(c) for c in color]   #makes sure the color is an array of floats
        if list(self.color) != color:
            for i in range(len(self.color)):
                self.color[i] = self.color[i] + (color[i] - self.color[i])/milliseconds
            return True
        return False
        
    #change whether or not the image can be treated as a button
    def setBoundable(self, boundable):
        self.isBoundable = boundable

    #changes the frame number of the image
    def setFrame(self, x = 1, y = 1):
        self.currentFrame = [x, y]
        self.setRect((float(int(x)-1)*self.frameSize[0], float(int(y)-1)*self.frameSize[1], 
                      float(int(x))*self.frameSize[0], float(int(y))*self.frameSize[1]))

    #crops the texture
    def setRect(self, rect):
        self.rect = rect
        self.createTex()
        
    #sets where the image is anchored (left, center, or right)
    def setAlignment(self, alignment):
        alignment = alignment.upper()
        self.alignment = eval(alignment)

    #very simple collision detection
    #does not work with rotations
    def getCollision(self, point):
        
        if self.alignment == 0:     #left
            x1 = self.position[0]
        elif self.alignment == 2:   #right
            x1 = self.position[0] - self.width
        else:                       #center
            x1 = self.position[0] - self.width/2.0
        x2 = x1 + self.width
        y = self.position[1] - self.height/2.0
        
        #print (x1, y2, x2-x1, y2-y1)
        #print (x1, x2, y1, y2)
        rect = pygame.Rect(x1, y, x2-x1, y+self.height)
        
        return rect.collidepoint(point)
        
    #finally draws the image to the screen
    def draw(self):

        glPushMatrix()

        glColor4f(*self.color)

        x = self.position[0]
        if self.alignment == 0:
            x += float(self.pixelSize[0])/2.0
        elif self.alignment == 2:
            x -= float(self.pixelSize[0])/2.0
        glTranslatef(x, self.position[1], -.1)
            
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(-self.angle, 0, 0, 1)
        
        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArray), GL_UNSIGNED_BYTE, self.indexArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

