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
        
        self.commands  = ["320x240", "640x480", "800x600", "1024x768"]
        self.index = 1
        
        self.resolution = [float(r) for r in self.commands[self.index].split("x")]
        self.fullscreen= False
    
        self.res = WinObj(Texture(os.path.join(scenepath, "res.png")))
        self.res.transitionTime = 16.0
        self.res.setPosition(self.engine.w/2, self.engine.h/2)
        self.res.setColor((1.0,0.0,0.0))
        
        self.resBack = WinObj(Texture(os.path.join(scenepath, "res.png")), 320, 240)
        self.resBack.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.moveKeys = [Input.LtButton, Input.RtButton]
        
    def update(self):
        self.resolution = [float(r) for r in self.commands[self.index].split("x")]
        
    def keyPressed(self, key):
        if key == self.moveKeys[0]:
            self.index = max(0, self.index-1)
        elif key == self.moveKeys[1]:
            self.index = min(self.index + 1, len(self.commands)-1)
    
    def render(self):
        
        self.resBack.draw()
        w = self.resolution[0]/self.engine.w
        h = self.resolution[1]/self.engine.h
        
        self.res.setDimensions(320.0 * w, 240.0 * h)
        self.res.draw()
        
        self.text.setText(self.commands[self.index])
        self.text.setPosition(self.engine.w/2, self.engine.h/2)
        self.text.draw()
        
        
class InputMenu(MenuObj):
    def __init__(self, scene):
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands  = [Input.UpButton, Input.DnButton, Input.LtButton, Input.RtButton,
                          Input.AButton, Input.BButton, Input.CButton, Input.DButton]
        self.commandStrings = ["Up", "Down", "Left", "Right", "A", "B", "C", "D"]
        
        scenepath = os.path.join("scenes", "menusystem", "settings")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        self.text.setAlignment("left")
        self.inputMessage = FontObj(fontStyle, "Press a key", size = 48.0)
        self.inputMessage.setPosition(self.engine.w/2, self.engine.h - 48.0)
        
        self.moveKeys = [Input.DnButton, Input.UpButton]
        
        self.buttons  = [0 for i in self.commands]
        self.button = WinObj(Texture(os.path.join(scenepath, "button.png")))
        self.button.transitionTime = 0.0
                                 
        self.position = (self.engine.w/2, self.engine.h*.8)
            
        self.index = 0                  #which button is selected
        
        self.active = False
     
    def update(self):
        self.commands  = [Input.UpButton, Input.DnButton, Input.LtButton, Input.RtButton,
                          Input.AButton, Input.BButton, Input.CButton, Input.DButton]
        
    def keyPressed(self, key):
        if self.active:
            if self.index == 0:   Input.UpButton = key
            elif self.index == 1: Input.DnButton = key
            elif self.index == 2: Input.LtButton = key
            elif self.index == 3: Input.RtButton = key
            elif self.index == 4: Input.AButton  = key
            elif self.index == 5: Input.BButton  = key
            elif self.index == 6: Input.CButton  = key
            elif self.index == 7: Input.DButton  = key
            self.active = False
        else:
            
            if key == Input.AButton:
                self.active = True
            
            if key == self.moveKeys[0]:
                if self.index + 1 < len(self.commands):
                    self.index += 1
                else:
                    self.index = 0
                
            elif key == self.moveKeys[1]:
                if self.index > 0:
                    self.index -= 1
                else:
                    self.index = len(self.commands) - 1
              
    #renders the menu
    def render(self, visibility = 1.0):
        
        position = self.position[1]
        for i, button in enumerate(self.buttons):
            self.text.setText("%s:   %s" % (self.commandStrings[i], pygame.key.name(self.commands[i])))
            self.text.scaleHeight(24.0)
            self.text.setPosition(self.position[0], position - (self.text.pixelSize[1]/2 + 16.0))
            position -= self.text.pixelSize[1] + 16.0
            
            if i == self.index:
                self.button.setDimensions(self.engine.w/3, 24.0)
                self.button.setPosition(self.text.position[0], self.text.position[1])
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

        self.choices = ["Resolution",
                        "Volume",
                        "Controls"]
                        
        self.inputMenu = InputMenu(self)
        self.resMenu = ResolutionMenu(self)
        self.menu   = MenuObj(self, self.choices, position = (self.engine.w/2, self.engine.h/2))
        
        self.menuButton = ImgObj(Texture(os.path.join(scenepath, "button.png")), frameY = 2)

        self.dimension = 0  #this defines which sub-level of the menu you are on

    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char): 
        if self.dimension == 1:
            if key == Input.BButton:
                self.dimension = 0
                return
            self.resMenu.keyPressed(key)
        elif self.dimension == 3:
            if key == Input.BButton and not self.inputMenu.active:
                self.dimension = 0
                return
            self.inputMenu.keyPressed(key)
        else:
            self.menu.keyPressed(key)
            #close the menu scene
            if key == Input.BButton:
                self.engine.viewport.changeScene("MenuSystem")

    def select(self, index):
        if self.dimension == 0:
            if index == 2:
                self.dimension = 3
            if index == 0:
                self.dimension = 1
        
    def run(self):
        if self.dimension == 3:
            self.inputMenu.update()
        elif self.dimension == 1:
            self.resMenu.update()
        

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        if self.dimension == 3:
            self.inputMenu.render()
        elif self.dimension == 2:
            pass
        elif self.dimension == 1:
            self.resMenu.render()
        else:
            self.menu.render()
        
