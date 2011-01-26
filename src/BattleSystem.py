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
            
        #0 = attack menu, 1 = spell menu, 2 = strategic menu, 3 = item menu
        self.commandWheel = ImgObj(Texture("commands.png"))
        self.commandWheel.setPosition(700, 500)
        self.command = 0

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
        
