'''

2010-11 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
import Character
from Character  import *

from Item import *
import string
import Input

from MenuObj import MenuObj

_pageSize = 10

class InventoryMenu(MenuObj):
    def __init__(self, scene, inventory, type = None):
        self.scene    = scene
        self.engine   = scene.engine   
        self.inventory = inventory 
        self.type = type
        
        scenepath = os.path.join("scenes", "menusystem", "inventory")

        #items are organized by pages with 10 different items on each page,
        #the user can switch between the pages by either clicking these buttons or
        #by pressing left or right
        self.buttonTex = os.path.join("scenes", "menusystem", "inventory", "button.png")
        self.nextButton = ImgObj(os.path.join(scenepath, "nextButton.png"))
        self.lastButton = ImgObj(os.path.join(scenepath, "lastButton.png"))
        
        self.nextButton.setPosition(self.engine.w - self.nextButton.width/2,
                                    self.engine.h - 96 - self.nextButton.height/2)
        self.lastButton.setPosition(self.engine.w - self.lastButton.width/2,
                                    self.lastButton.height/2)
                                    
        self.win = WinObj(Texture(os.path.join(scenepath, "window.png")), 
                          width = self.engine.w/2 - self.nextButton.width/2, height = self.engine.h - 96)
        self.win.setPosition(self.engine.w-self.win.scale[0]/2-self.nextButton.width, self.win.scale[1]/2)
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle, size = 24)
            
        self.updateCommands()
        
        self.active = False
        
        
    def updateCommands(self):
        self.commands = self.inventory.getByType(self.type).values()
        self.buttons  = [ImgObj(self.buttonTex, boundable = True, frameY = 2)
                         for n in range(min(_pageSize, len(self.commands)))]
        
        for i, button in enumerate(self.buttons):
            button.setPosition(self.win.position[0], self.win.position[1] + self.win.scale[1]/2 - 24.0 - (self.win.scale[1]/_pageSize * i + 5))
            button.setScale(self.win.scale[0] - _pageSize, self.win.scale[1]/_pageSize - 5, inPixels = True)
            button.setFrame(y = 2)
        
        self.index = 0                          #which button is selected
        self.page = 0
        self.maxPage = len(self.commands)/_pageSize
                    
    def keyPressed(self, key):
        if key == Input.UpButton:
            self.index -= 1
            if self.index < 0:
                self.index = _pageSize
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
            n = (self.page*_pageSize) + i
            if i == self.index and self.active:
                button.draw()
            
            #item 
            self.engine.drawText(self.text, self.commands[i][0].name, position = (button.position[0] - button.width/2 + 5, button.position[1]),
                                 alignment = "left")
            #item quantity
            self.engine.drawText(self.text, self.commands[i][1], position = (button.position[0] + button.width/2 - 5, button.position[1]),
                                 alignment = "right")
            
class SortMenu(MenuObj):
    def __init__(self, scene):
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands = [None, Usable, Food, Weapon, Armor, None]

        scenepath = os.path.join("scenes", "menusystem", "inventory")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle, size = 16)

        #the texture used for the buttons and the buttons themselves
        self.buttons  = [ImgObj(os.path.join(scenepath, "sortbuttons.png"), frameX = len(self.commands)) for i in self.commands]
        self.highlight = ImgObj(os.path.join(scenepath, "button.png"), frameY = 2)
        self.highlight.setFrame(y = 2)
        self.highlight.setScale(120, 68, True)
        for i in range(len(self.commands)):
            self.buttons[i].setFrame(x=i+1)
                                    
        for i, button in enumerate(self.buttons):
            button.setPosition(self.engine.w/len(self.buttons)*i+64, self.engine.h-48)
            button.setScale(64, 64, True)
            
        self.index = 0                          #which button is selected
        self.active = False
        
    def keyPressed(self, key):
        if key == Input.LtButton:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.buttons)-1
            self.scene.sortType = self.commands[self.index]
            
        elif key == Input.RtButton:
            self.index += 1
            if self.index >= len(self.buttons):
                self.index = 0 
            self.scene.sortType = self.commands[self.index]
                
        elif key == Input.AButton:
			self.scene.select(self.index)
			
    #renders the menu
    def render(self, visibility = 1.0):
        
        if self.active:
            self.highlight.setPosition(self.buttons[self.index].position[0], self.buttons[self.index].position[1])
            self.highlight.draw()
			
        for i, button in enumerate(self.buttons):
			button.draw()


                                 
class InventoryScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        self.inventory = self.family.inventory
        
        scenepath = os.path.join("scenes", "menusystem", "inventory")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.font   = FontObj("default.ttf")

        self.itemList = InventoryMenu(self, self.inventory, type = None)
        self.sortMenu = SortMenu(self)
        
        self.win = WinObj(Texture(os.path.join(scenepath, "window.png")), width = self.engine.w/2 - 32, height = self.engine.h - 96)
        self.win.setPosition(self.win.scale[0]/2, self.win.scale[1]/2)
        
        self.step = 0                       #0 = sort type
                                            #1 = item menu control
        
        self.sortType = None
                     
    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char): 
        if self.step == 0:
            self.sortMenu.keyPressed(key)
            self.itemList.type = self.sortType
            self.itemList.updateCommands()
        else:        
            self.itemList.keyPressed(key)
        
        #close the menu scene
        if key == Input.BButton:
            if self.step == 0:
                self.engine.viewport.changeScene("MenuSystem")
            elif self.step == 1:
                self.step = 0
                
    def select(self, index):
        if self.step == 0:
			self.step = 1
			
                
    def run(self):
        if self.step == 0:
            self.sortMenu.active = True
            self.itemList.active = False
        else:
            self.sortMenu.active = False
            self.itemList.active = True
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        self.sortMenu.render()
        self.itemList.render()
        self.win.draw()
        
        
        

