from sysobj import *
from View   import *
from Actor  import *
from MenuObj import MenuObj

import Input

class FamilyMenu(MenuObj):
    def __init__(self, scene, families):
        self.scene = scene
        self.engine = scene.engine
        self.commands = families
        self.moveKeys = [Input.DButton, Input.UButton]
        
        scenepath = os.path.join("scenes", "familylist")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        
        buttonStyle  = Texture(os.path.join(scenepath, "highlight.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
                        
        self.position = (self.engine.w/2, self.engine.h)
        for i, button in enumerate(self.buttons):
            button.setPosition(self.position[0], self.position[1] - (150 * i))
        self.slideRate = 150.0/512.0
        
        self.index = 0
        self.startIndex = 0
        self.endIndex = min(4, len(self.commands))

    def keyPressed(self, key):
        MenuObj.keyPressed(self, key)
        
        #if Up is selected
        if self.index == self.startIndex and key == Input.UButton:
            if len(self.commands) > 0:
                self.startIndex = max(self.startIndex - 4, 0)
        #if Down is selected
        elif self.index == self.endIndex and key == Input.DButton:
            if len(self.commands) > 4:
                self.startIndex = min(self.startIndex+4, len(self.commands)-5)
        self.endIndex = min(self.startIndex + 4, len(self.commands))

    
    #renders the menu
    def render(self, visibility = 1.0):

        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            button.draw()
            
        for i, family in enumerate(self.commands[self.startIndex:self.endIndex]):
            self.text.setText(family.name) 
            self.text.setPosition(button.position[0], button.position[1])
            self.text.scaleHeight(36.0)
            self.text.draw()
            
            self.text.setText("Members:%i" % len(family.members)) 
            self.text.setPosition(button.position[0] + button.width, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("right")
            self.text.draw()
            
            
class FamilyList(Scene):
    def __init__(self, engine):
        self.engine     = engine
        self.families   = [Family(n) for n in self.engine.listPath(path = os.path.join("actors", "families"), 
                                                                   value = "family.ini", flag = "folderDeepSearch")]

        self.menu = FamilyMenu(self, self.families)
        
        scenepath = os.path.join("scenes", "familylist")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        
        self.hlTex      = Texture(os.path.join(scenepath, "highlight.png"))
        self.highlight  = [ImgObj(self.hlTex, boundable = True, frameY = 2)
                           for n in range(4)]
        #self.slider     = ImgObj(Texture("slider.png"))
        self.slide_b    = [ImgObj(Texture(os.path.join(scenepath, "buttons.png")), boundable = True, frameX = 2),
                           ImgObj(Texture(os.path.join(scenepath, "buttons.png")), boundable = True, frameX = 2)]
        self.selectwin  = WinObj(Texture(os.path.join(scenepath, "window.png")), 0, self.engine.h-200)
        self.selectwin.setDimensions(self.engine.w, 200)
        
        self.pos        = 0
        self.newpos     = 0
        self.slideUP    = False
        self.slideDOWN  = False

        self.listlength = self.engine.h*(self.hlTex.pixelSize[1]/2*len(self.highlight))
        
        self.selected   = 0
    
    def keyPressed(self, key, char):
        self.menu.keyPressed(key)
      
    def select(self, index):
        self.engine.family = self.families[index]
        self.engine.viewport.changeScene("MapList")
        
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w, h))

        self.selectwin.draw()

        self.engine.drawImage(self.slide_b[0], position = (w*.9, h*.1), frameX = 1)
        self.engine.drawImage(self.slide_b[1], position = (w*.9, h*.9), frameX = 2) 

        self.menu.render(visibility)
        
