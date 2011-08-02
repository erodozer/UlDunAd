
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
        print path
        self.base = Texture(os.path.join(path, "base.png"))
        self.side = Texture(os.path.join(path, "side.png"))
        
    def show(self):
        self.hidden = False
        
    def hide(self):
        self.hidden = True
    
    def draw(self):
        
        """
        glPushMatrix()
        glScale(64.0,16.0*self.height,64.0)
        
        self.side.bind()
        
        for i in range(4):
            glBegin (GL_QUADS);
            glTexCoord2f (0.0, 0.0);
            glVertex3fv(_vertices[_indices[i*4+0]])
            glTexCoord2f (1.0, 0.0);
            glVertex3fv(_vertices[_indices[i*4+1]])
            glTexCoord2f (1.0, 1.0);
            glVertex3fv(_vertices[_indices[i*4+2]])
            glTexCoord2f (0.0, 1.0);
            glVertex3fv(_vertices[_indices[i*4+3]])
            glEnd ();
        glPopMatrix()
        
        glPushMatrix()
        glScale(64.0,1.0,64.0)
        
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
        glPopMatrix()
        """
        glDisable(GL_TEXTURE_2D)
        
        glPushMatrix()
        glColor4f(1.0,1.0,1.0,.8)
        #glTranslatef(0,16.0*float(self.height),0)
        glScalef(64.0,16.0*self.height,64.0)
        
        #glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, _vertices)
        #glTexCoordPointerf(_texArray)
        #self.side.bind(True)
        glDrawRangeElements(GL_QUADS, 0,16,16, GL_UNSIGNED_BYTE, _indices[:16])
        #self.base.bind()
        glDrawRangeElements(GL_QUADS, 16,20,4, GL_UNSIGNED_BYTE, _indices[16:])
        glDisableClientState(GL_VERTEX_ARRAY)
        #glDisableClientState(GL_TEXTURE_COORD_ARRAY) 
        glPopMatrix()
        
        
        glEnable(GL_TEXTURE_2D)
