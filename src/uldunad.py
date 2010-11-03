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

from Config import Configuration

from View import *

import sysobj
from sysobj import *

import Input
from Data import Data

#for list files
import glob

FPS = 60
caption = 'UlDunAd - Ultimate Dungeon Adventure'

finished = False

if not os.path.exists(os.path.join("uldunad.ini")):
    Configuration(os.path.join("uldunad.ini")).save()
    runini = Configuration(os.path.join("uldunad.ini"))
    runini.video.__setattr__("resolution", str(800) + "x" + str(600) + "x" + "W")
    runini.audio.__setattr__("volume", str(10))
    runini.save()
    Input().create(runini)
else:
    runini = Configuration(os.path.join("uldunad.ini"))

w, h, fullscreen = runini.video.__getattr__("resolution").split("x")
w, h = float(w), float(h)
resolution = (int(w), int(h))

video_flags = DOUBLEBUF|OPENGL|HWPALETTE|HWSURFACE#|NOFRAME
if fullscreen == "F":
    video_flags |= FULLSCREEN

class Error(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.text = ""
        self.font = FontObj("default.ttf")
        backTex = pygame.Surface((w,h))
        backTex.fill((0,0,0,150))
        self.background = ImgObj(Texture(surface = backTex))

    def setText(self, text):
        if self.text != text:
            self.text = text

    def render(self):
        self.engine.drawImage(self.background)
        self.engine.drawText(self.font, self.text)

class Main:
    def __init__(self, caption, flags):

        pygame.mixer.pre_init(44100)

        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'   #centers the window in the middle of your screen

        self.screen = pygame.display.set_mode(resolution, flags)
        self.viewport = Viewport(self, resolution)
     
        self.clock = pygame.time.Clock()
        self.w, self.h = resolution[0], resolution[1]
        sysobj.w, sysobj.h = resolution[0], resolution[1]

        self.data = Data()

        self.viewport.addScene("MainMenu")

        self.family = None      #your selected family and party

    def run(self):
        global finished

        # main event loop
        Input.update()
        finished = Input.finished

        self.viewport.run()
    
        self.clock.tick()
   
    #allows you to load an image and change the default values for it
    def loadImage(self, path = "", position = None, scale = None, angle = None, color = None, rect = None, frameX = 1, frameY = 1, boundable = False):
        if isinstance(path, Texture):
            tex = path
        else:
            tex = Texture(path)
    
        image = ImgObj(tex, boundable, frameX, frameY)
        if position:
            image.setPosition(position)
        if scale:
            image.setScale(scale)
        if angle:
            image.setAngle(angle)
        if color:
            image.setColor(color)
        if rect:
            image.setRect(rect)

        return image

    #simple method used to quicken the typing process
    def drawImage(self, image, position = (w/2, h/2), scale = (1,1), angle = None, color = None, frameX = None, frameY = None):

        #prevents it from drawing an object that does not exist in the first place
        if not image:
            return

        image.setPosition(position[0], position[1])
        image.setScale(scale[0], scale[1])
        if angle:
            image.setAngle(angle)
        if color:
            image.setColor(color)
        if frameX:
            image.setFrame(x = frameX)
        elif frameY:
            image.setFrame(y = frameY)
        if frameX and frameY:
            image.setFrame(frameX, frameY)

        image.draw()
        if image.isBoundable:
            self.viewport.inputObjects.append(image)

    def drawText(self, font, text, position = (w/2, h/2), scale = None, angle = None, color = None, alignment = "center"):

        #prevents it from drawing if no font exists or text exists
        if not (font or text):
            return

        font.setText(text)
        font.setPosition(position[0], position[1])
        if scale:
            font.setScale(scale[0], scale[1])
        if angle:
            font.setAngle(angle)
        if color:
            font.setColor(color)
        font.setAlignment(alignment)
        font.draw()

 
    def listPath(self, path, value = ".ini", flag = None, exclude = None):
        items = []
        path = os.path.join("..", "data", path)
        if flag == "filename":
            items = [n.split("/")[-1].replace(".ini", "") for n in glob.glob(os.path.join(path, "*." + value))]
        else:
            items = [n.split("/")[-1] for n in glob.glob(os.path.join(path, "*." + value))]
        if exclude:
            items.remove(exclude)
        
        return items

    def showError(self, error):
        self.error.setText(error)
        self.error.render()


#main loop to run the program
game = Main(caption, video_flags)
while not finished:
    game.run()
