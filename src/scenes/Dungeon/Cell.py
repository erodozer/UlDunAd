
from OpenGL.GL import *
from OpenGL.GLU import *

from sysobj import *
import os

class Cell(object):
    def __init__(self, path, height):
        #gets the height value from the character passed
        #height ranges from 0-9 then a-f (lowercase)
        def getHeight(h):
            h = ord(h)
            if h >= 97:
                h -= 87
            return h
        
        self.height = getHeight(height)         #height of the cell
        self.hidden = True
        self.base = Texture(os.path.join(path, "base.png"))
        self.side = Texture(os.path.join(path, "side.png"))
        
        self.vtxArray = [[0.0,0.0,0.0],
                         [0.0,1.0,0.0],
                         [1.0,1.0,0.0],
                         [1.0,0.0,0.0],
                         [0.0,0.0,1.0],
                         [0.0,1.0,1.0],
                         [1.0,1.0,1.0],
                         [1.0,0.0,1.0]]
        self.texArray = [[0.0, 0.0], [0.0,1.0], [1.0,1.0], [1.0,0.0]]
        self.indexArraySides = [0,1,5,4,
                                1,2,6,5,
                                2,3,7,6,
                                3,0,4,7]
        self.indexArrayTop = [0,1,2,3]
        
    def show(self):
        self.hidden = False
        
    def hide(self):
        self.hidden = True
    
    def draw(self):
        
        glPushMatrix()
        if self.hidden:
            glColor4f(.5,.5,.5,1.0)
        else:
            glColor4f(1.0,1.0,1.0,1.0)
        glPushMatrix()
        glScale(64.0,16.0*self.height,64.0)
        
        self.side.bind()
        
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArraySides), GL_UNSIGNED_BYTE, self.indexArraySides)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY) 
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0,16.0*self.height,0)
        glScalef(64.0,1.0,64.0)
        
        self.base.bind()
        
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArrayTop), GL_UNSIGNED_BYTE, self.indexArrayTop)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY) 
        glPopMatrix()

        glPopMatrix()
