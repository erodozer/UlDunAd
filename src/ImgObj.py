
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from numpy import array, float32

import array

from math import *

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
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.frameSize   = (1.0/float(frameX),1.0/float(frameY))
                                                    #the size of each cell when divided into frames
        self.rect        = (0.0,0.0,self.frameSize[0],self.frameSize[1])
                                                    #left, top, right, bottom, crops the texture

        self.pixelSize   = (self.texture.pixelSize[0]/frameX,
                            self.texture.pixelSize[1]/frameY)   
                                                    #the actual size of the image in pixels

        self.isBoundable = boundable                #is the picture one that can be read for mouse detection
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
        texArray[0,0] = rect[0]; texArray[0,1] = rect[1]
        texArray[1,0] = rect[2]; texArray[1,1] = rect[1]
        texArray[2,0] = rect[2]; texArray[2,1] = rect[3]
        texArray[3,0] = rect[0]; texArray[3,1] = rect[3]

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

    #=====IS NOT FUNCTIONING PROPERLY=====
    #moves the image from its current position by x and y
    # milliseconds defines how long you want it to take to
    # slide to the new position.
    def slide(self, x, y, milliseconds = 100.0):
        if list(self.position) != [x,y]:
           self.position = (self.position[0] + (float(x) - self.position[0])/milliseconds, 
                            self.position[1] + (float(y) - self.position[1])/milliseconds)

    #changes the size of the image and scales the surface
    def setScale(self, width, height):
        if (width >= 0 and width <= 1) and (height >= 0 and height <= 1):
                self.scale = (width,height)
        else:
            self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))

    #scales the image size by only the width
    # if keep_aspect_ratio is true it will scale the height
    # as well in order to maintain the aspect ratio
    def scaleWidth(self, width, keep_aspect_ratio = True):
        height = self.scale[1]
        if keep_aspect_ratio:
            height = self.scale[1] * (width/self.pixelSize[0])
        self.scale = (width/self.pixelSize[0], height)

    #same as scaleWidth except that the value passed
    #is the height of the image instead of the width
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

    #fades from the current color to the new color in the set amount of time
    # remember that the color must be in RGBA format
    def fade(self, color, milliseconds):
        color = list(color)
        if list(self.color) != color:
            for i in range(len(self.color)):
                self.color[i] = self.color[i] + (color[i] - self.color[i])/milliseconds

    #change whether or not the image can be treated as a button
    def setBoundable(self, boundable):
        self.isBoundable = boundable

    #changes the frame number of the image
    def setFrame(self, x = 1, y = 1):
        self.rect = (float(x-1)*self.frameSize[0], float(y-1)*self.frameSize[1], 
                     float(x)*self.frameSize[0], float(y)*self.frameSize[1])
        self.createTex()

    def setRect(self, rect):
        self.rect = rect
        self.createTex()

    #draws bounding box
    # when this is called the textures are disabled 
    # and only the color id of the image should be
    # applied to the plane
    def drawBoundingBox(self):
        glPushMatrix()

        glTranslatef(self.position[0], self.position[1],-.1)
        glScalef(self.scale[0], -self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)

        glColor3ub(*self.pick_color)

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
