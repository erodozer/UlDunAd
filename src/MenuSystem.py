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

class Menu(MenuObj):
    def __init__(self, scene, commands, position):
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands = commands

        scenepath = os.path.join("scenes", "menusystem")
        self.button = WinObj(Texture(os.path.join(scenepath, "button.png")))
        self.button.transitionTime = 0.0
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)

        #which keys select the next or previous button
        self.moveKeys = [Input.RtButton, Input.LtButton]
        
        #the texture used for the buttons and the buttons themselves
        self.buttons  = [0 for n in range(len(self.commands))]
                         
        self.position = position
            
        self.index = 0                  #which button is selected
        
       
    #renders the menu
    def render(self, visibility = 1.0):
        
        position = self.position[0]
        for i, button in enumerate(self.buttons):
            self.text.setText(self.commands[i])
            self.text.scaleHeight(24.0)
            self.text.setPosition(position + self.text.pixelSize[0]/2 + 20, self.position[1])
            position += self.text.pixelSize[0] + 20
            
            if i == self.index:
                self.button.setDimensions(self.text.pixelSize[0]+10.0, 48.0)
                self.button.setPosition(self.text.position[0], self.text.position[1])
                self.button.draw()
            
            self.text.draw()
    
class MenuSystem(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        scenepath = os.path.join("scenes", "menusystem")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.font   = FontObj("default.ttf")

        #self.members = self.family.members
        #self.startIndex = 0
        #self.endIndex = min(4, len(self.members))
        
        self.choices = ["Character",
                        "Settings", 
                        "Quit Game", 
                        "Exit Menu"]
        self.charChoices = ["Inventory", "Spells", "Equipment", "Status"]
        #helps captions for each menu choice
        #explains the purpose of each menu before selecting
        self.help = ["Show what items you currently possess", 
                     "Plan your next battle by examining your arsenal of spells",
                     "Equip your character with armor and weapons to give him/her the edge in battle", 
                     "Not sure about your character's stats?  Want to know how to improve what with which item?",
                     "Don't like the current feel of gameplay?  Change it up a bit to your preference",
                     "I guess you've had enough for today I suppose", "Return to your game"]
        self.menu   = Menu(self, self.choices, position = (0, 24.0))
        self.charMenu = Menu(self, self.charChoices, position = (0,72.0))
        
        self.menuButton = ImgObj(Texture(os.path.join(scenepath, "button.png")), frameY = 2)

        self.dimension = 0  #this defines which sub-level of the menu you are on
        #self.statusbox = self.engine.loadImage(os.path.join("Data", "statusbox.png"))

    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char): 
        if self.dimension == 1:
            self.charMenu.keyPressed(key)
        
            #close the character submenu
            if key == Input.BButton:
                self.dimension = 0
        else:
            self.menu.keyPressed(key)
        
            #close the menu scene
            if key == Input.BButton:
                self.engine.viewport.changeScene("Maplist")
            
        
                                        

    def select(self, index):
        if index == 0 and self.dimension == 0:
            self.dimension = 1
        
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))
        
        if self.dimension == 1:
            self.charMenu.render()
            self.engine.drawText(self.font, self.charChoices[self.charMenu.index], (w*.5, h*.65))
        else:
            self.engine.drawText(self.font, self.choices[self.menu.index], (w*.5, h*.65))
        
        self.menu.render()
        
        
        

