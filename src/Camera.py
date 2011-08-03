'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

#system design based on Ian Mallett's glLib for pygame

#an opengl camera object
#it starts out with a view with perspective, 
#but you can make it orthographic with one call
class Camera:
    def __init__(self, pos, zoom = 100):

        self.focusx = pos[0]
        self.focusy = pos[1]
        self.zoom = zoom
        
        self._oldfocusx = self.focusx
        self._oldfocusy = self.focusy
        self._oldzoom = self.zoom
              
    def focus(self, x, y, zoom):
        self._oldfocusx = self.focusx
        self._oldfocusy = self.focusy
        self._oldzoom = self.zoom
        
        self.focusx = x
        self.focusy = y
        self.zoom = zoom

    def resetFocus(self):
        self.focusx = self._oldfocusx
        self.focusy = self._oldfocusy
        self.zoom = self._oldzoom
