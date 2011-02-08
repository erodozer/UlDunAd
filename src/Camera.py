'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

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
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glEnable ( GL_COLOR_MATERIAL )

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        self.resetFocus()
        
    def focus(self, x, y, zoom):
        self.focusX = x*(self.width/800.0)
        self.focusY = y*(self.height/600.0)
        self.focusZ = zoom/100.0
        
    def resetFocus(self):
        self.focus(self.width/2, self.height/2, 100)

    #creates an orthographic projection
    def setOrthoProjection(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()                        
        glScalef(self.focusZ, self.focusZ, 1.0)
        glOrtho(self.focusX, self.width+self.focusX, self.focusY, self.height+self.focusY, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(self.width/2, self.height/2,0.0)
        
    #resets the projection to have perspective
    def resetProjection(self):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()
