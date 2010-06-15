'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import os
import sys
import pygame
from pygame.locals import *

import Config
from View import *
from Main import *

import sysobj
from sysobj import *

FPS = 60
caption = 'UlDunAd - Ultimate Dungeon Adventure'

finished = False

if not os.path.exists(os.path.join("uldunad.ini")):
  Config.Configuration(os.path.join("uldunad.ini")).save()
  runini = Config.Configuration(os.path.join("uldunad.ini"))
  runini.video.__setattr__("resolution", str(800) + "x" + str(600) + "x" + "W")
  runini.audio.__setattr__("volume", str(10))
  runini.save()
else:
  runini = Config.Configuration(os.path.join("uldunad.ini"))

w, h, fullscreen = runini.video.__getattr__("resolution").split("x")
w, h = float(w), float(h)
resolution = (int(w), int(h))

video_flags = DOUBLEBUF|OPENGL|HWPALETTE|HWSURFACE
if fullscreen == "F":
    video_flags = DOUBLEBUF|OPENGL|HWPALETTE|HWSURFACE|FULLSCREEN
 
class Main(object):
  def __init__(self, caption, flags):

    pygame.mixer.pre_init(44100)

    pygame.init()

    pygame.display.set_mode(resolution, video_flags)
    self.viewport = Viewport(resolution)
 
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'   #centers the window in the middle of your screen

    self.fpsClock = pygame.time.Clock()
    self.screen = pygame.display.set_mode(resolution, flags)
    self.w, self.h = resolution[0], resolution[1]
    sysobj.w, sysobj.h = resolution[0], resolution[1]

    self.viewport.addScene(MainMenu(self))

  def run(self):
    global finished

    # main event loop
    event = pygame.event.poll()
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        finished = True

    self.viewport.run()

    self.fpsClock.tick(FPS)

  #simple method used to quicken the typing process
  def drawImage(self, image, position = (w/2, h/2), scale = (1,1), angle = None, color = None, rect = None):
    image.setPosition(position[0], position[1])
    image.setScale(scale[0], scale[1])
    if angle:
      image.setAngle(angle)
    if color:
      image.setColor(color)
    if rect:
      image.setRect(rect)

    if self.viewport.input and image.isBoundable:
        image.drawBoundingBox()
        self.viewport.imageObjects.append(image)
    else:
        image.draw()


#main loop to run the program
game = Main(caption, video_flags)
while not finished:
  game.run()


