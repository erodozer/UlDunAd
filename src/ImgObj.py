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

#an Image Object for rendering and collision detection (mouse)
class ImgObj:
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
        self.bounds  = (0.0, 1.0, 0.0, 1.0)         #the bounds of the picture
        self.tBounds = []

        self.createArrays()
        
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
            if not self.scale == (width, height):
                self.scale = (width,height)
                self.transformed = True
        else:
            if not self.scale == (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1])):
                self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
                self.transformed = True

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

    #same as scaleWidth except that the value passed
    #is the height of the image instead of the width
    def scaleHeight(self, height, keep_aspect_ratio = True):
        width = self.scale[0]
        if keep_aspect_ratio:
            width = self.scale[0] * (height/self.pixelSize[1])
        if not self.scale == (width, height/self.pixelSize[1]):
            self.scale = (width, height/self.pixelSize[1])
            self.transformed = True
            
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

    def isColliding(self, mouse):
        mousex, mousey = mouse.get_pos()
        print mousex, mousey
        
        x = [self.tBounds[i][0] for i in range(len(self.tBounds))]
        y = [self.tBounds[i][1] for i in range(len(self.tBounds))]
                
        print x,y
        ax = x[0] - x[2]
        bx = x[1] - x[3]
        ay = y[0] - y[2]
        by = y[1] - y[3]
                
        #if true, us a, else use b
        largestx = bool(abs(ax) == max(abs(ax), abs(bx)))
        largesty = bool(abs(ay) == max(abs(ay), abs(by)))
                
        if largestx:
            x1 = min(x[0], x[2])
            x2 = max(x[0], x[2])
            y1 = min(y[1], y[3])
            y2 = max(y[1], y[3])
        else:
            x1 = min(x[1], x[3])
            x2 = max(x[1], x[3])
            y1 = min(y[0], y[2])
            y2 = max(y[0], y[2])
                    
        print x1, x2, y1, y2
        
        if (mousex >= x1 and mousex <= x2) and \
           (mousey >= y1 and mousey <= y2):
            return True
            
        return False
    
    
    #finally draws the image to the screen
    def draw(self):

        glPushMatrix()

        glColor4f(*self.color)

        glTranslatef(self.position[0], self.position[1],-.1)
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(self.angle, 0, 0, 1)
        
        self.tBounds = [gluProject(coord[0], coord[1], 0) for coord in self.vtxArray]
        
        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArray), GL_UNSIGNED_BYTE, self.indexArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

