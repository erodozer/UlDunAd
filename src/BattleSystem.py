'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from operator import itemgetter

from View   import *
from Actor  import *

import string
import Input

from MenuObj import MenuObj


#this is the hud that displays the character information
#it's not one big window, instead it is 1-3 little windows
#arranged to save space in an efficent manner when more or
#less characters are present in your party
class BattleHUDCharacter:
    def __init__(self, character, position = (0,0), scale = 1.0):
        self.character = character

        self.x, self.y = position

        #hud back
        self.hudtex = Texture("battlehud.png")
        self.hudImg = ImgObj(self.hudtex, frameY = 2)
        self.hudImg.setAlignment("left")
        self.hudImg.setPosition(self.x, self.y)

        #font used in the hud for displaying HP by number and name of the character
        self.font   = FontObj("default.ttf")
        self.font.setAlignment("left")

        #these are for drawing the HP and FP bars
        self.bartex = Texture("bars.png")
        self.bar    = ImgObj(self.bartex, frameY = 2)
        self.barHP  = ImgObj(self.bartex, frameY = 1)
        self.barFP  = ImgObj(self.bartex, frameY = 1)

        self.bar.setAlignment("left")
        self.bar.setPosition(200 + self.x, self.y + 5)

        self.barHP.setAlignment("left")
        self.barHP.setPosition(200 + self.x, self.y + 5)        

        self.barFP.setAlignment("left")
        self.barFP.setPosition(375 + self.x, self.y + 5)        

        self.scale = scale
        
    def draw(self):
        
        glScalef(self.scale, self.scale, 1)
        
        if character.active:
            self.hudImg.setFrame(frameY = 2)
        else:
            self.hudImg.setFrame(frameY = 1)
        self.hudImg.draw()

        self.font.setColor(self.vis)
        self.font.setText(self.character.name)
        self.font.setPosition(self.x + 5, self.y)
        self.font.draw()

        self.font.setText(str(self.character.currentHP) + "/" + str(self.character.hp))        
        self.font.setPosition(self.x + 200, self.y - 5)

        self.barback.draw()

        self.barHP.setRect((0, self.character.currentHP/self.character.HP, .5, 1))
        self.barHP.draw()

class BattleMenu(MenuObj):
    def __init__(self, scene, character):
        self.scene = scene
        self.engine = scene.engine
        self.character = character
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)
        
        #0 = attack menu, 2 = strategic menu, 3 = item menu
        self.commandWin = WinObj(Texture("window.png"), 0, 0)
        self.commandWin.setDimensions(self.engine.w, 400, inPixels = True)
        
        self.command = 0        #command selected
        self.index = 0          #index selected in the window
        self.step = 0           #menu showing
        
        self.basicCommands = ["Attack", "Tactical", "Item"] #basic command menu
        self.attackCommands = ["Weapon", "Spell/Technique"] #attack menu
        self.tactCommands = ["Boost", "Defend", "Flee"]     #tactical menu
        self.itemCommands = self.engine.family.inventory    #item menu
        self.techCommands = character.skills                #character's list of skills
        
    def keyPressed(self, key, char):
        
        if key == Input.UpButton:
            #since item and skill menus have two columns
            #to go up a row you have to subtract 2
            if self.step == 3 or self.step == 4:
                if self.index > 1:
                    self.index -= 2
            else:
                if self.index > 0:
                    self.index -= 1
        if key == Input.DnButton:
            #since item and skill menus have two columns
            #to go up a row you have to subtract 2
            if self.step == 3 or self.step == 4:
                if self.index > 1:
                    self.index -= 2
            else:
                if self.index > 0:
                    self.index -= 1
            
                
        #overrides default a button pressing
        if key == Input.AButton:
            if self.step == 0:
                if self.index == 0:
                    self.step = 1       #attacking menu
                elif self.index == 1:
                    self.step = 2       #tactical menu
                elif self.index == 2:
                    self.step = 3       #item menu
            elif self.step == 1:
                if self.index == 0:     #attack
                    self.scene.selectTarget()
                elif self.index == 1:   #skill menu
                    self.step = 4
            elif self.step == 2:
                if self.index == 0:
                    self.character.boost = True
                elif self.index == 1:
                    self.character.defend = True
                elif self.index == 2:
                    self.scene.flee()
            elif self.step == 3:
                self.character.command = self.itemCommands[index]
                self.scene.selectTarget()
            elif self.step == 4:
                self.character.command = self.techCommands[index]
                self.scene.selectTarget()
        
        if key == Input.BButton:
            if self.step == 1 or self.step == 2 or self.step == 3:
                self.step = 0
            elif self.step == 4:
                self.step = 1
                    
        
    def render(self, visibility):
        
        if self.step == 3:
            for i, item in enumerate(self.itemCommands):
                position = (self.engine.w/2 * i%2) + 10, 32.0 * int(i/2))
                
                if i == self.index:
                    self.highlight.setPosition(position[0], position[1])
                    
                self.text.setText(item.name)
                self.text.setPosition(position[0], position[1])
                self.text.scaleHeight(28.0)
                self.text.draw()
                
            self.highlight.draw()
         
        else:
            self.commandWheel.draw()
            
            self.text.setText(self.basicCommands[self.index])
            self.text.setPosition(700,500)
            self.text.scaleHeight(24.0)
            self.text.draw()
        
        
        
        
    
#unlike most other scenes in this game, the battle scene 
#is completely controlled by the keyboard instead of mouse
class BattleSystem(Scene):
    def __init__(self, engine):

        self.engine = engine
        w, h = self.engine.w, self.engine.h

        self.party = self.engine.family.party
        self.formation = self.engine.formation

        self.background = self.engine.formation.terrain
        self.start = ImgObj(Texture("start.png"))
        self.start.setPosition(self.engine.w / 2, self.engine.h / 2)

        self.huds = [BattleHUDCharacter(character, (0, 575 - 45*i)) for i, character in enumerate(self.party)]
            
        self.inMenu = False

        self.active = 0         #which character is currently selecting commands
        self.battling = False   #are commands being selected or is fighting occuring?

        self.turns = {}
        for character in self.party:
            self.turns[character] = 0
        for enemy in self.formation.enemies:
            self.turns[enemy] = 0
        self.order = []

	self.targetMenu = None

    def run(self):
        if not self.battling:
            character = self.party[self.active]
            character.active = True

            next = False
            back = False
            for key, char in Input.getKeyPresses():
                if key == K_UP:
                    character.command = 0
                    next = True
                elif key == K_RIGHT:
                    character.command = 1
                    next = True
                elif key == K_DOWN:
                    character.command = 2
                    next = True
                elif key == K_LEFT:
                    character.command = 3
                    next = True
                elif key == K_BACKSPACE:
                    back = True

            if next:
                self.active += 1
                self.next = False
            elif back:
                self.active -= 1
                self.back = False

    def turnStart(self):
        for character in self.party:
            if not (character.boost or character.defend):
                self.turns.update(character = random.randInt(0, 50) + character.spd)

        for enemy in self.formation:
            if not (enemy.boost or enemy.defend):
                self.turns.update(enemy = random.randInt(0, 50) + enemy.spd)

        self.order = sorted(self.turns.items(), key=itemgetter(1))
            
    def turnEnd(self):
        for character in self.party:
            character.turnEnd()

    def generateTargets(self, actor):
        targetMenu = []
        if actor.attacking or actor.spell.target == 0:
            targetMenu = MenuObj(self.formation)
        else:
            targetMenu = MenuObj(self.party)
        return targetMenu
        
    def render(self):
        for hud in enumerate(self.huds):
            if active < len(self.party):
                if self.party[active]:
                    hud.scale = 1.0
                else:
                    hud.scale = .5
            else:
                hud.scale = .5
            hud.draw()

        if not self.battling:
            if active < len(self.party):
                self.commandWheel.draw()
            else:
                self.start.draw()
                
    def victory(self):
        self.engine.changeScene("VictoryScene")
        
