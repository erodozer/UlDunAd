'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View import *

from Character import Family

from MenuObj import MenuObj

class EquipmentButtons(MenuObj):
    def __init__(self, scene):
        self.scene = scene
        self.engine = scene.engine
        self.character = scene.character
        
        scenepath = os.path.join("scenes", "menusystem", "equipment")
        self.buttonTex = Texture(os.path.join(scenepath, "icon.png"))
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), width = self.engine.w/2,
                             height = self.engine.h - 64)
        
        self.commands = ["weapon", "weapon", "accessory", "accessory", "accessory", 
                          "helmet", "armor", "gloves", "legs", "feet"]
        
        self.commandButtons = [ImgObj(Texture(os.path.join(scenepath, "icon.png")), 
                                       boundable = True, frameY = 2)
                                for command in self.commands]
    
        self.activeArea = 0     #0 = bottom, 1 = side
        self.index = 0  
        
        self.position = (0, self.engine.h-64)
        
        self.window.setPosition(self.position[0] + self.window.scale[0]/2, 
                                self.position[1] - self.window.scale[1]/2)
                                
        for i, button in enumerate(self.commandButtons):
            button.setPosition(self.position[0] + self.window.scale[0]/4 + (button.width+10)*(i%5), 
                               self.position[1] - self.window.scale[1] + 96 - (button.height+10)*(i/5))    
        
        
    def buttonClicked(self, image):
        if image in self.commandButtons:
            self.index = self.commandButtons.index(image)
            return True
        return False
    
    def keyPressed(self, key):
        if key == Input.DnButton:
            self.index = min(9, self.index+5)
        if key == Input.UpButton:
            self.index = max(0, self.index-5)
        if key == Input.RtButton:
            self.index = min(9, self.index+1)
        if key == Input.LtButton:
            self.index = max(0, self.index-1)
        if key == Input.AButton:
            self.scene.select(self.index)    
    def render(self, visibility):
        
        self.window.draw()
        
        self.engine.drawImage(self.character.sprites['profile'], 
                              position = (self.position[0] + self.window.scale[0]/2, 
                                          self.position[1] - self.window.scale[1]/2))
        
        for i, button in enumerate(self.commandButtons):
            
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            self.engine.drawImage(button)
 
class ItemMenu(MenuObj):
    def __init__(self, scene):
        self.scene = scene
        self.engine = scene.engine
        self.character = scene.character
        
        scenepath = os.path.join("scenes", "menusystem", "equipment")
        self.buttonTex = Texture(os.path.join(scenepath, "icon.png"))
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), width = self.engine.w/2,
                             height = self.engine.h/2)
        
        self.commandButtons = [ImgObj(Texture(os.path.join(scenepath, "button.png")), 
                                       boundable = True, frameY = 2)
                                for command in self.engine.family.inventory]
    
        self.activeArea = 0     #0 = bottom, 1 = side
        self.index = 0  
        
        self.position = (self.engine.w*.5, self.engine.h-128)
        
        self.window.setPosition(self.position[0] + self.window.scale[0]/2, 
                                self.position[1] - self.window.scale[1]/2)
                                
        for i, button in enumerate(self.commandButtons):
            button.setScale(self.window.scale[0] - 15, 32.0)
            button.setPosition(self.position[0]+self.window.scale[0]/2,
                               self.position[1]+self.window.scale[1]/2 - 10 - 32*i)    
        
        
    def buttonClicked(self, image):
        pass
    
    def keyPressed(self, key):
        if key == Input.DnButton:
            self.index = min(len(self.itemlist), self.index+1)
        if key == Input.UpButton:
            self.index = max(0, self.index-1)
        if key == Input.AButton:
            self.scene.select(self.index)
            
    def render(self, visibility):
        
        self.window.draw()
        
        for i, button in enumerate(self.commandButtons):
            
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            self.engine.drawImage(button)
            self.font.setText(self.family.inventory[i].name)
            self.font.setPosition(self.button.position)
            self.font.draw()

class ItemWindow:
    def __init__(self, scene):
        self.scene = scene
        self.engine = scene.engine
        self.character = scene.character
        
        scenepath = os.path.join("scenes", "menusystem", "equipment")
        self.buttonTex = Texture(os.path.join(scenepath, "icon.png"))
        self.button = ImgObj(self.buttonTex, boundable = True, frameY = 2)
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), width = self.engine.w/2,
                             height = 64)
        self.window.setPosition(self.engine.w*.75, self.engine.h-64-self.window.scale[1]/2)
                             
        self.font = FontObj("default.ttf", size = 32.0)
        self.font.setAlignment("left")
        
    def draw(self):
        self.window.draw()
        
        if not self.scene.activeCat == -1:
            self.engine.drawText(self.font, self.character.equipment[self.scene.activeCat].name, 
                                 position = (self.window.position[0] - 20, self.window.position[1]))
        
        
class EquipmentScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        self.activeChar = 0 #the character being displayed
        self.character = self.family.members[self.activeChar]
        self.activeCat = -1 #the active weapon category
        
        scenepath = os.path.join("scenes", "menusystem", "equipment")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.EquipMenu = EquipmentButtons(self)
        self.ItemWindow = ItemWindow(self)
        self.ItemMenu = ItemMenu(self)
        
        self.step = 0       #0 = equipment selection, 1 = item selection for replacement
        
    def buttonClicked(self, image):
        if self.EquipMenu.buttonClicked(image):
            self.step = 0
        #elif self.ItemMenu.buttonClicked(image):
        #    self.step = 1
                
    def keyPressed(self, key, char):
        if self.step == 0:
            self.EquipMenu.keyPressed(key)
            if key == Input.BButton:
                self.engine.viewport.changeScene("MenuSystem")
        #else:
        #    self.ItemMenu.keyPressed(key)
        #    if key == Input.BButton:
        #        self.step = 1
            
        if key == Input.CButton:
            self.activeChar += 1
            self.refresh()
        elif key == Input.DButton:
            self.activeChar -= 1
            self.refresh()
            
    def select(self, index):
        if self.step == 0:
            self.activeCat = index
            self.step = 1
            
    #refreshes the character info
    def refresh(self):
        if self.activeChar < 0:
            self.activeChar = len(self.family.members) - 1
        elif self.activeChar >= len(self.family.members):
            self.activeChar = 0
            
        self.character = self.family.members[self.activeChar]
        
    def select(self, index):
        pass
        
    def run(self):
        pass
        
    def render(self, visibility):
        self.background.draw()     
        
        self.EquipMenu.render(visibility)
        self.ItemWindow.draw()
        self.ItemMenu.render(visibility)
