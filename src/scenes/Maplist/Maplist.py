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
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), self.engine.w/4, 0)
        self.menuButton = ImgObj(Texture(os.path.join(scenepath, "menubutton.png")), boundable = True)
        self.font   = FontObj("default.ttf")

        self.towns = self.engine.listPath("places", value = "town.ini", flag = "folderDeepSearch")
        self.dungeons = self.engine.listPath("places", value = "dungeon.ini", flag = "folderDeepSearch")
        self.maps = self.towns + self.dungeons
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
        self.selectedMap = None

    def buttonClicked(self, image):
        if image == self.menuButton:
            self.engine.viewport.changeScene("MenuSystem")
        
    def keyPressed(self, key, char):    
        #opens up the menu
        if key == Input.CButton:
            self.engine.viewport.changeScene("MenuSystem")
            
        #creates a test battle scene
        if key == Input.DButton and len(self.engine.family.members) > 0:
            from Enemy import Formation
            self.engine.formation = Formation("formation001")
            self.engine.viewport.changeScene("BattleSystem")
        
        self.menu.keyPressed(key)   
             

    def select(self, index):
        #if Up is selected
        if index == 0:
            if len(self.maps) > 0:
                self.startIndex = max(self.startIndex - 10, 0)
        #if Down is selected
        elif index == len(self.menu.commands)-1:
            if len(self.maps) > 10:
                self.startIndex = min(self.startIndex+10, len(self.maps)-11)
        else:
            if self.selectedMap == self.maps[self.startIndex + index-1]:
                self.engine.town = self.selectedMap
                if self.selectedMap in self.towns:
                    self.engine.viewport.changeScene("Town")
                elif self.selectedMap in self.dungeons:
                    self.engine.viewport.changeScene("Dungeon")
            else:
                self.selectedMap = self.maps[self.startIndex + index - 1]
               
        #if Up or Down is selected, the end index will be corrected as well
        if index == 0 or index == len(self.menu.commands)-1:
            #endIndex will always be 10 ahead of startIndex
            self.endIndex = min(self.startIndex + 10, len(self.maps))
            self.updateCommands()
      
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

        self.background.draw()
        self.engine.drawImage(self.menuButton, position = (w*.9, h*.1))
        self.menu.render()
        
        self.engine.drawText(self.font, "%s:%i" % (self.engine.family.name, len(self.engine.family.members)),
                             position = (self.engine.w*.8, self.engine.h*.8))

        self.engine.drawText(self.font, "Party:%i" % (self.engine.family.party.size),
                             position = (self.engine.w*.8, self.engine.h*.6))
