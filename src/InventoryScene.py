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

import string
import Input

from MenuObj import MenuObj

class InventoryMenu(MenuObj):
    def __init__(self, scene, commands):
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands = commands

        scenepath = os.path.join("scenes", "menusystem", "inventory")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle, size = 16)

        #the texture used for the buttons and the buttons themselves
        self.buttons  = [ImgObj(Texture(os.path.join(scenepath, "button.png")), boundable = True, frameY = 2)
                         for n in range(min(10, len(self.commands)))]
        
        #items are organized by pages with 10 different items on each page,
        #the user can switch between the pages by either clicking these buttons or
        #by pressing left or right
        self.nextButton = ImgObj(Texture(os.path.join(scenepath, "nextButton.png")))
        self.lastButton = ImgObj(Texture(os.path.join(scenepath, "lastButton.png")))
        
        self.nextButton.setPosition(self.engine.w - self.nextButton.width/2,
                                    self.engine.h - 96 - self.nextButton.height/2)
        self.lastButton.setPosition(self.engine.w - self.lastButton.width/2,
                                    self.lastButton.height/2)
        self.win = WinObj(Texture(os.path.join(scenepath, "window.png")), 
                          width = self.engine.w/2 - self.nextButton.width/2, height = self.engine.h - 96)
        self.win.setPosition(self.engine.w-self.win.scale[0]/2-self.nextButton.width, self.win.scale[1]/2)
        
        for i, button in enumerate(self.buttons):
            button.setPosition(self.win.position[0], self.win.position[1] + self.win.scale[1]/2 - 10.0 - (self.win.scale[1]/10.0 * i + 5))
            button.setScale(self.win.scale[0] - 10, self.win.scale[1]/10 - 5, inPixels = True)
            
        self.index = 0                  #which button is selected
        self.page = 0
        self.maxPage = len(self.commands)/10
        
    def keyPressed(self, key):
        if key == Input.UpButton:
            self.index -= 1
            if self.index < 0:
                self.index = 10
        elif key == Input.DnButton:
            self.index += 1
            if self.index >= len(self.commands):
                self.index = 0
        elif key == Input.LtButton:
            self.page -= 1
            if self.page < 0:
                self.page = self.maxPage
        elif key == Input.RtButton:
            self.page += 1
            if self.page > self.maxPage:
                self.page = 0
       
    #renders the menu
    def render(self, visibility = 1.0):
        
        self.win.draw()
        
        self.nextButton.draw()
        self.lastButton.draw()
        
        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.draw()
            
            #item 
            self.engine.drawText(self.text, self.commands[i][0].name, position = (button.position[0] - button.width/2 + 5, button.position[1]),
                                 alignment = "left")
            #item quantity
            self.engine.drawText(self.text, self.commands[i][1], position = (button.position[0] + button.width/2 - 5, button.position[1]),
                                 alignment = "right")
            
        
class InventoryScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        scenepath = os.path.join("scenes", "menusystem", "inventory")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.font   = FontObj("default.ttf")

        self.itemList = InventoryMenu(self, self.family.inventory)

        self.win = WinObj(Texture(os.path.join(scenepath, "window.png")), width = self.engine.w/2 - 32, height = self.engine.h - 96)
        self.win.setPosition(self.win.scale[0]/2, self.win.scale[1]/2)
        
    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char): 
        self.itemList.keyPressed(key)
        
        #close the menu scene
        if key == Input.BButton:
            self.engine.viewport.changeScene("MenuSystem")

    def select(self, index):
        pass
                
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        self.itemList.render()
        self.win.draw()
        
        
        

