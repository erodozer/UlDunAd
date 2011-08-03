
from OpenGL.GL import *
from OpenGL.GLU import *

from sysobj import *
import os

_vertices = [[0,0,0],[1,0,0],[1,1,0],[0,1,0],
             [0,0,1],[1,0,1],[1,1,1],[0,1,1]]
                         
_texArray = [[0.0, 0.0], [0.0,1.0], [1.0,1.0], [1.0,0.0]]
        
_indices = [0,1,2,3,
            1,5,6,2,
            5,4,7,6,
            4,0,3,7,
            4,5,1,0]
    
class Cell(object):
    def __init__(self, path, height):
        
        self.height = height         #height of the cell
        self.hidden = True
        
        self.base = Texture(os.path.join(path, "base.png"))
        self.side = Texture(os.path.join(path, "side.png"))

        self.displayList = glGenLists(1)                
        glNewList(self.displayList, GL_COMPILE)
        self.side.bind()
        
        for i in range(4):
            glBegin(GL_QUADS)
            glTexCoord2f (0.0, 0.0)
            glVertex3fv(_vertices[_indices[i*4+0]])
            glTexCoord2f (1.0, 0.0)
            glVertex3fv(_vertices[_indices[i*4+1]])
            glTexCoord2f (1.0, 1.0)
            glVertex3fv(_vertices[_indices[i*4+2]])
            glTexCoord2f (0.0, 1.0)
            glVertex3fv(_vertices[_indices[i*4+3]])
            glEnd()
            
        self.base.bind()
        
        glBegin(GL_QUADS)
        glTexCoord2f (0.0, 0.0)
        glVertex3fv(_vertices[_indices[16]])
        glTexCoord2f (1.0, 0.0)
        glVertex3fv(_vertices[_indices[17]])
        glTexCoord2f (1.0, 1.0)
        glVertex3fv(_vertices[_indices[18]])
        glTexCoord2f (0.0, 1.0)
        glVertex3fv(_vertices[_indices[19]])
        glEnd()
        glEndList()  
                                
    def show(self):
        self.hidden = False
        
    def hide(self):
        self.hidden = True
    
    def draw(self):
        
        glPushMatrix()
        glScale(64.0,16.0*self.height,64.0)
        glColor4f(1.0,1.0,1.0,1.0)
        glCallList(self.displayList)
        glPopMatrix()

