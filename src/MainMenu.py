'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View import *

from MenuObj import MenuObj

class MainMenu(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.menu       = MenuObj(self, commands = ["New Game", "Continue", "Exit"], 
                                  position = (150, 75), horizontal = True)
        self.background = ImgObj(Texture("mainbg.png"))
        
        self.window     = WinObj(Texture("window.png"), 300, 128)
        self.size       = 0
        
        self.test       = [ImgObj(Texture("test.png")), 0, 0]
        
        self.music = BGMObj("test.mp3")
        
        self.selected = 0
        
    def buttonClicked(self, image):
        self.menu.buttonClicked(image)
                
    def keyPressed(self, key, char):
        if key == K_SPACE:
            if self.size < 4:
                self.size += 1
            else:
                self.size = 0
            print self.size
        elif key == K_z:
            if self.test[1] < 2:
                self.test[1] += 1
            else:
                self.test[1] = 0
            print self.test[1]
        elif key == K_UP:
            self.test[2] += 45
            print self.test[0].angle
        elif key == K_DOWN:
            self.test[2] -= 45
            print self.test[0].angle
            
            
            
        self.menu.keyPressed(key)
        
    def select(self, index):
        if index == 0:
            self.engine.viewport.changeScene("CreateFamily")
        elif index == 1:
            self.engine.viewport.changeScene("FamilyList")
        
    def run(self):
        pass
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))        
        
        self.menu.render(visibility)
            
        self.window.setPosition(w*.5, h*.5)
        if self.size == 1:
            self.window.setDimensions(500, 320)
        elif self.size == 2:
            self.window.setDimensions(200, 200)
        elif self.size == 3:
            self.window.setDimensions(128, 450)
        elif self.size == 4:
            self.window.setDimensions(700, 500)
        else:
            self.window.setDimensions(300, 128)
        self.window.setColor((1.0,1.0,1.0,.4))
        self.window.draw()
        
        self.test[0].spin(self.test[2])
        
        if self.test[1] == 1:
            self.test[0].slide(w*.8, h*.25)
        elif self.test[1] == 2:
            self.test[0].slide(w*.2, h*.75)
        else:
            self.test[0].slide(w*.5, h*.5)
        self.test[0].draw()

