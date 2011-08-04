
from OpenGL.GL import *
from OpenGL.GLU import *

from sysobj import *
import os
    
class Cell(object):
    def __init__(self, path, height):
        
        self.height = height         #height of the cell
        self.hidden = True
        
        self.base = Texture(os.path.join(path, "base.png"))
        self.side = Texture(os.path.join(path, "side.png"))

        self.displayList = glGenLists(1)                
        glNewList(self.displayList, GL_COMPILE)
        self.genCube()
        glEndList()  
        
    def genCube(self):
        glPushMatrix()
        glScale(64.0,16.0*self.height,64.0)
        self.side.bind()
        glBegin(GL_QUADS)
        #Front Face
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 0.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, 0.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0,  1.0)
        #Back Face
        glTexCoord2f(1.0, 0.0); glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, 0.0, 0.0)
        #Right face
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, 0.0,  1.0)
        #Left Face
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(0.0, 0.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(0.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glEnd()
        
        self.base.bind()
        #Top Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glEnd()
        glPopMatrix()

    def show(self):
        self.hidden = False
        
    def hide(self):
        self.hidden = True
    
    def draw(self):
        
        glPushMatrix()
        if self.hidden:
            glColor4f(.3,.3,.3,1.0)
        else:
            glColor4f(1.0,1.0,1.0,1.0)
        glCallList(self.displayList)
        glPopMatrix()
        
