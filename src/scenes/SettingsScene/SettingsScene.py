'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
import Character
from Character  import *

import pygame

import string
import Input

from MenuObj import MenuObj

class ResolutionMenu(MenuObj):
    def __init__(self, scene):
        
        self.scene    = scene
        self.engine   = scene.engine    
        
        scenepath = os.path.join("scenes", "menusystem", "settings")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        self.smallText = FontObj("default.ttf", size = 18)
        
        self.commands  = [[320,240], [640,480], [800,600], [1024,768]]
        self.index = self.commands.index([self.engine.changedW, self.engine.changedH])
        
        self.res = WinObj(Texture(os.path.join(scenepath, "res.png")))
        self.res.transitionTime = 16.0
        self.res.setPosition(self.engine.w/2, self.engine.h/2)
        self.res.setColor((1.0,0.0,0.0))
        
        self.resBack = WinObj(Texture(os.path.join(scenepath, "res.png")), 320, 240)
        self.resBack.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.moveKeys = [Input.LtButton, Input.RtButton]
        
        self.resolution = self.commands[self.index]
        self.fullscreen = self.engine.changedF
        
        self.scene.resolution = self.resolution
        self.scene.fullscreen = self.fullscreen
    
        self.helpButtons = [[self.moveKeys[0], "Decrease resolution"],
                          [self.moveKeys[1], "Increase resolution"],
                          [Input.CButton, "Fullscreen toggle"]]
                          
    def keyPressed(self, key):
        if key == self.moveKeys[0]:
            self.index = max(0, self.index-1)
        elif key == self.moveKeys[1]:
            self.index = min(self.index + 1, len(self.commands)-1)
    
        self.resolution = self.commands[self.index]
            
        if key == Input.CButton:
            self.fullscreen = not self.fullscreen
            
    def render(self):
        
        self.resBack.draw()
        w = float(self.commands[self.index][0])/self.engine.viewport.resolution[0]
        h = float(self.commands[self.index][1])/self.engine.viewport.resolution[1]
        
        self.res.setDimensions(320.0 * w, 240.0 * h)
        self.res.draw()
        
        self.engine.drawText(self.text, "%ix%i" % (self.commands[self.index][0], self.commands[self.index][1]),
                             position = (self.engine.w/2, self.engine.h/2))
        
        if self.fullscreen:
            text = "Fullscreen"
        else:
            text = "Windowed"
        self.engine.drawText(self.text, text, position = (self.engine.w/2, self.engine.h*.2))

        self.engine.drawText(self.smallText, "Changes to resolution will be applied after the game is restarted.", 
                             position = (self.engine.w/2, 64.0))

class VolumeMenu(MenuObj):
    def __init__(self, scene):
        
        self.scene    = scene
        self.engine   = scene.engine    
        
        scenepath = os.path.join("scenes", "menusystem", "settings")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        
        self.volume = self.engine.volume
        self.scene.volume = self.volume
        
        self.volimg = ImgObj(Texture(os.path.join(scenepath, "volume.png")), frameY = 10)
        self.volimg.setPosition(self.engine.w/2, self.engine.h*.6)
        
        self.moveKeys = [Input.LtButton, Input.RtButton]
        
        self.helpButtons = [[self.moveKeys[0], "Decrease Volume"],
                          [self.moveKeys[1], "Increase Volume"]]
                          
    def keyPressed(self, key):
        if key == self.moveKeys[0]:
            self.volume = max(0, self.volume-1)
        elif key == self.moveKeys[1]:
            self.volume = min(self.volume + 1, 10)
    
    def render(self):
        
        self.volimg.setFrame(y = self.volume)
        self.volimg.draw()
        
        self.engine.drawText(self.text, "Volume: %i" % self.volume, 
                             position = (self.engine.w/2, self.engine.h*.45))

        
class InputMenu(MenuObj):
    def __init__(self, scene):
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commandStrings = ["Up", "Down", "Left", "Right", "A", "B", "C", "D"]
        
        scenepath = os.path.join("scenes", "menusystem", "settings")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        self.inputMessage = FontObj(fontStyle, "Press a key", size = 48.0)
        self.inputMessage.setPosition(self.engine.w/2, self.engine.h - 48.0)
        

        self.keys = [Input.UpButton, Input.DnButton, Input.LtButton, Input.RtButton,
                     Input.AButton, Input.BButton, Input.CButton, Input.DButton]
        self.scene.keys = [key for key in self.keys]

        self.moveKeys = [Input.DnButton, Input.UpButton]
        
        self.buttons  = [0 for i in self.keys]
        self.button = WinObj(Texture(os.path.join(scenepath, "button.png")))
        self.button.transitionTime = 0.0
                                 
        self.position = (self.engine.w/2, self.engine.h*.9)
            
        self.index = 0                  #which button is selected
        
        self.active = False
     
        self.helpButtons = [[self.moveKeys[0], "Scroll Up"],
                          [self.moveKeys[1], "Scroll Down"],
                          [Input.AButton, "Select button to change"]]

    def keyPressed(self, key):
        if self.active:
            self.keys[self.index] = key
            self.active = False
        else:
            
            if key == Input.AButton:
                self.active = True
            
            if key == self.moveKeys[0]:
                if self.index + 1 < len(self.keys):
                    self.index += 1
                else:
                    self.index = 0
                
            elif key == self.moveKeys[1]:
                if self.index > 0:
                    self.index -= 1
                else:
                    self.index = len(self.keys) - 1
              
    #renders the menu
    def render(self, visibility = 1.0):
        
        position = self.position[1]
        for i, button in enumerate(self.buttons):
            self.text.setText("%s: %s" % (self.commandStrings[i], pygame.key.name(self.keys[i])))
            self.text.scaleHeight(24.0)
            self.text.setPosition(self.position[0], position - (self.text.pixelSize[1]/2 + 16.0))
            position -= self.text.pixelSize[1] + 16.0
            
            if i == self.index:
                self.button.setDimensions(self.engine.w/3, 24.0)
                self.button.setPosition(self.position[0], self.text.position[1])
                self.button.draw()
            
            self.text.draw()
        if self.active:
            self.inputMessage.draw()
            
class SettingsScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        scenepath = os.path.join("scenes", "menusystem", "settings")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle, size = 18)
        
        self.choices = ["Resolution",
                        "Volume",
                        "Controls"]
                        
        self.inputMenu = InputMenu(self)
        self.resMenu = ResolutionMenu(self)
        self.volMenu = VolumeMenu(self)
        self.menu   = MenuObj(self, self.choices, position = (self.engine.w/2, self.engine.h/2))
        
        self.menuButton = ImgObj(Texture(os.path.join(scenepath, "button.png")), frameY = 2)

        self.dimension = 0  #this defines which sub-level of the menu you are on

        self.helpButtons = []
        
    def run(self):
        if self.dimension == 3:
            self.helpButtons = self.inputMenu.helpButtons
        elif self.dimension == 2:
            self.helpButtons = self.volMenu.helpButtons
        elif self.dimension == 1:
            self.helpButtons = self.resMenu.helpButtons
        else:
            self.helpButtons = [[Input.AButton, "Select option"],
                              [Input.UpButton, "Scroll up"],
                              [Input.DnButton, "Scroll down"]]
                              
    def buttonClicked(self, image):
        if self.dimension == 0:
            self.menu.buttonClicked(image)
        
    def keyPressed(self, key, char): 
        if self.dimension != 0:
            if key == Input.BButton:
                if self.dimension == 3:
                    self.keys = self.inputMenu.keys
                elif self.dimension == 2:
                    self.volume = self.volMenu.volume
                elif self.dimension == 1:
                    self.resolution = self.resMenu.resolution
                    self.fullscreen = self.resMenu.fullscreen
                self.dimension = 0
                return
            
        if self.dimension == 1:
            self.resMenu.keyPressed(key)
        elif self.dimension == 2:
            self.volMenu.keyPressed(key)
        elif self.dimension == 3:
            self.inputMenu.keyPressed(key)
        else:
            self.menu.keyPressed(key)
            #close the menu scene
            if key == Input.BButton:
                self.end()

    def select(self, index):
        if self.dimension == 0:
            self.dimension = index + 1

    #closes the scene and saves options to the uldunad.ini
    def end(self):
        Configuration(os.path.join("..", "uldunad.ini")).save()
        runini = Configuration(os.path.join("..", "uldunad.ini"))
        if self.fullscreen:
            f = "F"
        else:
            f = "W"
        runini.video.__setattr__("resolution", str(self.resolution[0]) + "x" + str(self.resolution[1]) + "x" + f)
        runini.audio.__setattr__("volume", str(self.volume))
        runini.save()
        Input.create(runini, self.keys)
        
        Input.load(runini)
        self.engine.changedW, self.engine.changedH, self.engine.changedF = self.resolution[0], self.resolution[1], self.fullscreen
        self.engine.volume = self.volume
        
        self.engine.viewport.changeScene("MenuSystem")
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        if self.dimension == 3:
            self.inputMenu.render()
        elif self.dimension == 2:
            self.volMenu.render()
        elif self.dimension == 1:
            self.resMenu.render()
        else:
            self.menu.render()
        
