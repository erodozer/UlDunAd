'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import os
import sys

w, h = 0, 0                     #width and height of the window

from Camera import Camera
from ImgObj import ImgObj
from WinObj import WinObj
from TitledWinObj import TitledWinObj
from BarObj import BarObj
from Texture import loadTexture as Texture
from FontObj import FontObj
from Audio import *
from Animation import Animation
from Particle import *
