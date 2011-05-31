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

import Audio

import Input
from Data import Data

#for list files
import glob

#command line parser, if running python 2.7 use argparse, else fall-back to optparse
try:
    import argparse
except ImportError:
    import optparse as argparse

FPS = 60
caption = 'UlDunAd - Ultimate Dungeon Adventure [FPS: %i]'

if not os.path.exists(os.path.join("..", "uldunad.ini")):
    Configuration(os.path.join("..", "uldunad.ini")).save()
    runini = Configuration(os.path.join("..", "uldunad.ini"))
    runini.video.__setattr__("resolution", str(800) + "x" + str(600) + "x" + "W")
    runini.audio.__setattr__("volume", str(10))
    runini.save()
    Input.create(runini)
    Input.load(runini)
else:
    runini = Configuration(os.path.join("..", "uldunad.ini"))
    Input.load(runini)

w, h, fullscreen = runini.video.__getattr__("resolution").split("x")
w, h = float(w), float(h)
resolution = (int(w), int(h))
volume = int(runini.audio.__getattr__("volume"))

if fullscreen == "F":
    fullscreen = True
else:
    fullscreen = False

video_flags = DOUBLEBUF|OPENGL|HWPALETTE|HWSURFACE#|NOFRAME
if fullscreen:
    video_flags |= FULLSCREEN


startingScene = "MainMenu"
enableSound = True

#sets the starting scene to be TestScene instead of MainMenu    
class testMode(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global startingScene
        startingScene = "TestScene"

#allows you to turn off sound
class disableSound(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global enableSound
        enableSound = False
        
class Main:
    def __init__(self, flags):
        self.finished = False   #is the app done
        
        pygame.mixer.pre_init(44100)

        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'   #centers the window in the middle of your screen

        self.screen = pygame.display.set_mode(resolution, flags)
        self.viewport = Viewport(self, resolution)
        Audio.enabled = enableSound
     
        self.clock = pygame.time.Clock()
        self.currentFPS = 60    #the currentFPS the engine is rendering at
    
        self.w, self.h, self.fullscreen = resolution[0], resolution[1], fullscreen
        self.changedW, self.changedH, self.changedF = self.w, self.h, self.fullscreen
        sysobj.w, sysobj.h = resolution[0], resolution[1]
        self.volume = volume
        
        self.data = Data()

        self.viewport.addScene(startingScene)

        self.family = None      #your selected family and party
        self.formation = None   #current battling formation
        self.town = None        #current town/location
        
    def run(self):
        global finished

        # main event loop
        Input.update()
        self.finished = Input.finished

        self.viewport.run()
        Input.reset()
        self.clock.tick(FPS)
        self.currentFPS = int(self.clock.get_fps())
        
        #fps counter is in the title bar
        pygame.display.set_caption(caption % (self.currentFPS))
        
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
    def drawImage(self, image, position = None, scale = None, angle = None, color = None, frameX = None, frameY = None):

        #prevents it from drawing an object that does not exist in the first place
        if not isinstance(image, ImgObj):
            return
        
        if position:
            image.setPosition(position[0], position[1])
        if scale:
            image.setScale(scale[0], scale[1])
        if angle:
            image.setAngle(angle)
        if color:
            image.setColor(color)
        if frameX and frameY:
            image.setFrame(frameX, frameY)
        elif frameX:
            image.setFrame(x = frameX)
        elif frameY:
            image.setFrame(y = frameY)
        
        image.draw()

    #animates an image with multiple frames
    # direction     image will animate along 0 = frameX, 1 = frameY, 2 = both
    # loop          image will animate continously
    # reverse       image will reverse animation after it hits the end when looping
    #                    (1...n then n...1) (-1 = neither, 0 = frameX, 1 = frameY, 2 = both)
    # delay         millisecond delay for animation
    def drawAnimation(self, image, direction = 0, loop = True, reverse = -1, delay = 20):
        if not isinstance(image, ImgObj):
            return
            
        x = image.currentFrame[0]
        y = image.currentFrame[1]
        
        #adjusts the rate so then it changes at the same rate each frame
        if self.currentFPS/delay < 1.0:
            delay = delay
        else:
            delay = self.currentFPS/delay
        
        if not direction == 1:  #horizontal
            if x >= image.frames[0]:
                if loop:
                    if reverse == 0 or reverse == 2:
                        if not image.reverseH:
                            image.reverseH = True
                        if x <= image.frames[0] + .5:
                            x -= 1.0
                        else:
                            x += 1.0/delay
                    else:
                        x = 1
            elif image.reverseH and x - (1.0/delay) <= 1:
                x = 1
                image.reverseH = False
            else:
                if image.reverseH:
                    x -= 1.0/delay
                else:
                    x += 1.0/delay
                    
        if not direction == 0:  #vertical
            if y >= image.frames[1]:
                if loop:
                    if reverse == 1 or reverse == 2:
                        if not image.reverseV:
                            image.reverseV = True
                        if y <= image.frames[1] + .5:
                            y -= 1.0
                        else:
                            y += 1.0/delay
            elif image.reverseV and y - 1 == 1:
                y = 1
                image.reverseV = False
            else:
                if image.reverseV:
                    y -= 1.0/delay
                else:
                    y += 1.0/delay
                    
        image.setFrame(x, y)
        image.draw()
        
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

 
    #searches path for files with filetype or folder
    def listPath(self, path, value = "ini", flag = None, exclude = None):
        items = []
        searchpath = os.path.join("..", "data", path)
        #returns a list of the folders in the path
        if flag == "folder":
            items = os.listdir(searchpath)
        else:
            #allow for multiple endings when searching
            for val in value.split("|"):
                #retrieve just the file names
                if flag == "filename":
                    item = [n.rsplit("/",1)[1].replace("." + value, "") for n in glob.glob(os.path.join(searchpath, "*." + val))]
                #returns a list of the folders in the path that contain the searched file
                elif flag == "folderDeepSearch":
                    item = [n for n in os.listdir(searchpath) if os.path.isfile(os.path.join(searchpath, n, val))]
                #retrieve the entire filename, extension included
                else:
                    item = [n.rsplit("/",1)[1] for n in glob.glob(os.path.join(searchpath, "*." + val))]
                for i in item:
                    items.append(i)
        #removes this file from list
        if exclude:
            items.remove(exclude)
        
        return items

#extra arguments for running
parser = argparse.ArgumentParser(description='Runs UlDunAd Engine')
parser.add_argument('-t', '--test', nargs = '?', action = testMode,
                   help='Runs the test scene instead of the game')
parser.add_argument('-s', '--sound', nargs = '?', action = disableSound,
                   help='Disables sound')
args = parser.parse_args()

#main loop to run the program
game = Main(video_flags)
while not game.finished:
    game.run()
