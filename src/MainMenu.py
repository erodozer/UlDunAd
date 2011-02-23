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
        commands = ["New Game", "Exit"]
        self.continueEnabled = bool(len(self.engine.listPath(path = os.path.join("actors", "families"), 
                                   value = "family.ini", flag = "folderDeepSearch")) > 0)
        if self.continueEnabled:
            commands.insert(1, "Continue")
            
        self.menu       = MenuObj(self, commands, 
                                  position = (150, 200))
        self.background = ImgObj(Texture("mainbg.png"))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.music = BGMObj("test.mp3")
        
        self.selected = 0
        
        
    def buttonClicked(self, image):
        self.menu.buttonClicked(image)
                
    def keyPressed(self, key, char):
        self.menu.keyPressed(key)
        
    def select(self, index):
        if index == 0:
            self.engine.viewport.changeScene("CreateFamily")
        elif index == 1 and self.continueEnabled:
            #forcing for testing purposes
            #self.engine.family = Family("default")
            #self.engine.viewport.changeScene("MapList")
            self.engine.viewport.changeScene("FamilyList")
        else:
            self.engine.finished = True
        
    def run(self):
        pass
        
    def render(self, visibility):
        self.background.draw()     
        
        self.menu.render(visibility)
