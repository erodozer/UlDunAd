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
    
class PlayerStats:
    def __init__(self, scene, character, position):
        self.scene = scene
        self.engine = scene.engine
        
        self.character = character
        self.position = position
        
        scenepath = os.path.join("scenes", "menusystem")
        self.back = WinObj(Texture(os.path.join(scenepath, "window.png")), self.engine.w, self.engine.h*.1)
        self.back.setPosition(self.engine.w/2, self.position)
        
        
        self.font = FontObj("default.ttf", size = 16)
        self.bigFont = FontObj("default.ttf", size = 32)
        
        length = 200
        self.bars = [BarObj(Texture(os.path.join(scenepath, "bar_bottom.png")), length),
                     BarObj(Texture(os.path.join(scenepath, "exp_bar.png")), length*(character.exp/float(Character._expCalc(character.level)))),
                     BarObj(Texture(os.path.join(scenepath, "bar_top.png")), length)]
        for bar in self.bars:
            bar.setPosition(self.engine.w - 10 - length, self.position-10)
        
    def render(self):
        self.back.draw()
        
        character = self.character
        
        width = self.back.scale[0]
        height = self.back.scale[1]
        y = self.position
        
        #name
        self.engine.drawText(self.font, character.name, position = (10, y), alignment = "left")
        
        #level
        self.engine.drawText(self.font, "Level: %i" % (character.level), position = (self.engine.w/4, y), alignment = "left")
        
        #hp
        self.engine.drawText(self.font, "HP: %i" % character.hp, position = (self.engine.w/2, y), alignment = "left")
        
        #exp
        for bar in self.bars:
            bar.draw()
        self.engine.drawText(self.font, "EXP: %i/%i" % (character.exp, Character._expCalc(character.level)),
                             position = (self.engine.w - 10, y), alignment = "right")
        
class MenuSystem(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        scenepath = os.path.join("scenes", "menusystem")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.font   = FontObj("default.ttf")

        #self.members = self.family.members
        #self.startIndex = 0
        #self.endIndex = min(4, len(self.members))
        
        self.choices = ["Family",
                        "Character",
                        "Settings", 
                        "Quit Game", 
                        "Exit Menu"]
        self.familyChoices = ["Inventory", "Bestiary", "Order"]
        self.charChoices = ["Spells", "Equipment", "Status"]
        #helps captions for each menu choice
        #explains the purpose of each menu before selecting
        self.help = ["Show what items you currently possess", 
                     "Plan your next battle by examining your arsenal of spells",
                     "Equip your character with armor and weapons to give him/her the edge in battle", 
                     "Not sure about your character's stats?  Want to know how to improve what with which item?",
                     "Don't like the current feel of gameplay?  Change it up a bit to your preference",
                     "I guess you've had enough for today I suppose", "Return to your game"]
        self.menu   = Menu(self, self.choices, position = (0, self.engine.h - 24.0))
        self.familyMenu = Menu(self, self.familyChoices, position = (0,self.engine.h-72.0))
        self.charMenu = Menu(self, self.charChoices, position = (0,self.engine.h-72.0))
        self.quitPrompt = MenuObj(self, ["No", "Yes"], position = (self.engine.w/2, self.engine.h/2))
        
        self.menuButton = ImgObj(Texture(os.path.join(scenepath, "button.png")), frameY = 2)

        self.playerWin = [PlayerStats(self, char, self.engine.h/4 + (self.engine.h/10 * i))
                          for i, char in enumerate(self.family.party.members)]

        self.dimension = 0  #this defines which sub-level of the menu you are on
        #self.statusbox = self.engine.loadImage(os.path.join("Data", "statusbox.png"))

    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char):
        if self.dimension == 1:
            self.familyMenu.keyPressed(key)
        
            #close the character submenu
            if key == Input.BButton:
                self.dimension = 0
        elif self.dimension == 2:
            self.charMenu.keyPressed(key)
        
            #close the character submenu
            if key == Input.BButton:
                self.dimension = 0
        elif self.dimension == 3:
            self.quitPrompt.keyPressed(key)
            
            if key == Input.BButton:
                self.dimension = 0
        else:
            self.menu.keyPressed(key)
        
            #close the menu scene
            if key == Input.BButton:
                self.engine.viewport.changeScene("Maplist")

    def select(self, index):
        if self.dimension == 0:
            if index == 0:      #family
                self.dimension = 1
            elif index == 1:    #character
                self.dimension = 2
            elif index == 2:    #settings
                self.engine.viewport.changeScene("SettingsScene")
            elif index == 3:    #quit game
                self.dimension = 3
            elif index == 4:    #exit menu
                self.engine.viewport.changeScene("Maplist")
        elif self.dimension == 1:
            if index == 0:      #inventory
                self.engine.viewport.changeScene("InventoryScene")
            elif index == 1:    #bestiary
                self.engine.viewport.changeScene("BestiaryScene")
            elif index == 2:    #order
                self.engine.viewport.changeScene("OrderScene")
        elif self.dimension == 2:
            if index == 0:      #spells/techniques
                self.engine.viewport.changeScene("SpellScene")
            elif index == 1:    #equipment
                self.engine.viewport.changeScene("EquipmentScene")
            elif index == 2:    #status
                self.engine.viewport.changeScene("Status")
        elif self.dimension == 3:
            if index == 0:   #no
                self.dimension = 0
            elif index == 1: #yes
                self.engine.finished = True
                
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        if self.dimension == 1:
            self.familyMenu.render()
        elif self.dimension == 2:
            self.charMenu.render()
        
        self.menu.render()
        
        for win in self.playerWin:
            win.render()
            
        self.engine.drawText(self.font, "%i Available Characters" % (len(self.family.members)), (w*.5, 24.0)) 
        
        if self.dimension == 3:
            self.font.setText("Are you sure you wish to quit the game?")
            self.font.setPosition(self.engine.w/2, self.engine.h/2 + 40)
            self.font.draw()
            self.quitPrompt.render()
        
        

