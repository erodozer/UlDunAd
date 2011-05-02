from sysobj import *
from View   import *
from Character  import *

import Input          
from FamilyMenu import FamilyMenu         
  
class FamilyList(Scene):
    def __init__(self, engine):
        self.engine     = engine
        self.families   = [Family(n) for n in self.engine.listPath(path = os.path.join("actors", "families"), 
                                                                   value = "family.ini", flag = "folderDeepSearch")]

        self.menu = FamilyMenu(self, self.families)
        
        scenepath = os.path.join("scenes", "familylist")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
                
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
    
    def buttonClicked(self, image):
        self.menu.buttonClicked(image)
        
    def keyPressed(self, key, char):
        self.menu.keyPressed(key)
        
        if key == Input.BButton:
            self.engine.viewport.changeScene("MainMenu")
            
      
    def select(self, index):
        self.engine.family = self.families[index]
        self.engine.viewport.changeScene("Maplist")
        
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        #self.selectwin.draw()
        
        self.engine.drawImage(self.slide_b[0], position = (w*.9, h*.1), frameX = 1)
        self.engine.drawImage(self.slide_b[1], position = (w*.9, h*.9), frameX = 2) 

        self.menu.render(visibility)
        
