'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
from Actor  import *

import string
import Input

from MenuObj import MenuObj

class Maplist(Scene):
    def __init__(self, engine):
        self.engine = engine

        scenepath = os.path.join("scenes", "maplist")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), self.engine.w/4, 0)
        self.menubutton = ImgObj(Texture(os.path.join(scenepath, "menubutton.png")), boundable = True)
        self.font   = FontObj("default.ttf")

        self.maps   = self.engine.listPath("places", value = "town.ini", flag = "folderDeepSearch")
        self.startIndex = 0
        self.endIndex = min(10, len(self.maps))
        
        commands = ["Up"]
        for i in range(self.startIndex, self.endIndex):
            commands.append(self.maps[i])
        commands.append("Down")
        self.menu   = MenuObj(self, commands, position = (100, 400))
        
        self.fadeIn     = True  #are the windows transitioning in or out

        self.error = False      #was an error thrown
        self.step = 0           #step 0 = naming, step 1 = choose difficulty
        
        self.exists = False

    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char):    
        self.menu.keyPressed(key)   
        
        #opens up the menu
        if key == Input.CButton:
            self.engine.viewport.changeScene("MenuSystem")
             

    def select(self, index):
        #if Up is selected
        if index == 0:
            if len(self.maps) > 0:
                self.startIndex = max(self.startIndex - 10, 0)
        #if Down is selected
        elif index == len(self.menu.commands)-1:
            if len(self.maps) > 10:
                self.startIndex = min(self.startIndex+10, len(self.maps)-11)
            
                
        #if Up or Down is selected, the end index will be corrected as well
        if index == 0 or index == len(self.menu.commands)-1:
            #endIndex will always be 10 ahead of startIndex
            self.endIndex = min(self.startIndex + 10, len(self.maps))
            self.updateCommands()
            
        if index > 0 and index < len(self.menu.commands)-1:
            self.selectedMap = self.maps[self.startIndex + index]
      
    #updates the list of maps
    def updateCommands(self):
        commands = ["Up"]
        for i in range(self.startIndex, self.endIndex):
            commands.append(self.maps[i])
        commands.append("Down")
        
        self.menu.commands = commands
        
    def run(self):
        pass
        
    def next(self):
        if self.step == 0 and not self.name:
            self.error = True
        else:
            self.step += 1

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))
        self.engine.drawImage(self.menubutton, position = (w*.9, h*.1))
        self.menu.render()
