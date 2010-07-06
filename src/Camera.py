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
