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
from Enemy import Enemy

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
        
        scenepath = os.path.join("scenes", "battlesystem")
        
        #hud back
        self.hudtex = Texture(os.path.join(scenepath, "battlehud.png"))
        self.hudImg = ImgObj(self.hudtex)
        self.hudImg.setAlignment("left")
        self.hudImg.setPosition(self.x, self.y)

        #font used in the hud for displaying HP by number and name of the character
        self.font   = FontObj("default.ttf")
        self.font.setAlignment("left")

        #these are for drawing the HP and FP bars
        #each bar consists of 3 textures
        self.hpBar = [ImgObj(Texture(os.path.join(scenepath, "bottom_bar.png"))),
                      ImgObj(Texture(os.path.join(scenepath, "hp_bar.png"))), 
                      ImgObj(Texture(os.path.join(scenepath, "top_bar.png")))]
        self.fpBar = [ImgObj(Texture(os.path.join(scenepath, "bottom_bar.png"))),
                      ImgObj(Texture(os.path.join(scenepath, "fp_bar.png"))), 
                      ImgObj(Texture(os.path.join(scenepath, "top_bar.png")))]

        self.setPosition(self.x, self.y)
    
        self.scale = scale
        
    def update(self):
        self.hpBar[1].setRect((0, 0, self.character.currentHP/self.character.hp, 1))
        self.fpBar[1].setRect((0, 0, self.character.fp/self.character.maxFP, 1))
       
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
        for bar in self.hpBar:
            bar.setAlignment("left")
            bar.setPosition(200 + x, y - 5)

        for bar in self.fpBar:
            bar.setAlignment("left")
            bar.setPosition(200 + x, y - 25)
        
    def draw(self):
        
        glPushMatrix()
        glScalef(self.scale, self.scale, 1)
        
        self.hudImg.draw()

        self.font.setText(self.character.name)
        self.font.setPosition(self.x + 5, self.y)
        self.font.draw()

        self.font.setText(str(self.character.currentHP) + "/" + str(self.character.hp))        
        self.font.setPosition(self.x + 200, self.y - 5)

        for bar in self.hpBar:
            bar.draw()

        for bar in self.fpBar:
            bar.draw()
        glPopMatrix()
        

class BattleMenu(MenuObj):
    def __init__(self, scene, character):
        self.scene = scene
        self.engine = scene.engine
        self.character = character
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)
        
        #0 = attack menu, 2 = strategic menu, 3 = item menu
        self.commandWin = WinObj(Texture("window.png"), 0, 0)
        self.commandWin.setDimensions(self.engine.w-30, 400)
        self.highlight = ImgObj(Texture("window_selected.png"))
        self.highlight.setScale(self.engine.w/2 - 10, 32.0, inPixels = True)
        
        #the wheel backdrop
        self.back = ImgObj(Texture(os.path.join("scenes", "battlesystem", "commandwheel.png")))
        self.back.setPosition(self.engine.w - self.back.width/2, self.back.height/2)
        
        self.command = 0        #command selected
        self.index = 0          #index selected in the window
        self.step = 0           #menu showing
        
        self.basicCommands = ["Attack", "Spell/Technique", "Tactical", "Item"] #basic command menu
        self.attackCommands = ["Normal", "Strong", "Accurate"] #attack menu
        self.tactCommands = ["Boost", "Defend", "Flee"]     #tactical menu
        self.itemCommands = self.engine.family.inventory    #item menu
        self.techCommands = character.skills                #character's list of skills
        
    def keyPressed(self, key):
        
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
            #to go down a row you have to add 2
            if self.step == 3 or self.step == 4:
                if self.step == 3:
                    commands = self.itemCommands
                else:
                    commands = self.techCommands
                if self.index + 2 < len(commands):
                    self.index += 2
            else:
                if self.step == 0:
                    commands = self.attackCommands
                else:
                    commands = self.basicCommands
                if self.index + 1< len(self.basicCommands):
                    self.index += 1
            
                
        #overrides default a button pressing
        if key == Input.AButton:
            if self.step == 0:
                if self.index == 0:
                    self.step = 1       #attacking menu
                elif self.index == 1:
                    self.step = 2       #tactical menu
                elif self.index == 2:
                    self.step = 3       #item menu
                elif self.index == 3:
                    self.step = 4       #skill menu
                self.index = 0
                
            elif self.step == 1:
                if self.index == 1:     #strong attack
                    self.character.power = 1
                elif self.index == 2:   #accurate attack
                    self.character.power = 2
                else:                   #normal attack
                    self.character.power = 0
                self.character.attacking = True
                self.scene.selectTarget()

            elif self.step == 2:
                if self.index == 0:     #boost
                    self.character.boost = True
                elif self.index == 1:   #defend
                    self.character.defend = True
                elif self.index == 2:   #flee
                    self.scene.flee()
            elif self.step == 3:
                self.character.command = self.itemCommands[self.index]
                self.scene.generateTargets(self.character)
                self.scene.targeting = True
            elif self.step == 4:
                self.character.command = self.techCommands[self.index]
                self.scene.generateTargets(self.character)
                self.scene.targeting = True
        
        if key == Input.BButton:
            self.step = 0
            self.index = 0
        
    def render(self, visibility):
        
        if self.step == 3 or self.step == 4:
            if self.step == 3:
                commands = self.itemCommands
            elif self.step == 4:
                commands = self.techCommands
                
            self.commandWin.draw()
            
            for i, item in enumerate(commands):
                position = ((self.engine.w/2 * i%2) + 10, 32.0 * int(i/2))
                
                if i == self.index:
                    self.highlight.setPosition(position[0], position[1])
                    
                self.text.setText(item.name)
                self.text.setPosition(position[0], position[1])
                self.text.scaleHeight(28.0)
                self.text.draw()
                
            self.highlight.draw()
         
        else:
            self.back.draw()
            
            if self.step == 0:
                commands = self.basicCommands
            elif self.step == 1:
                commands = self.attackCommands
            elif self.step == 2:
                commands = self.tactCommands
                
            self.text.setText(commands[self.index])
            self.text.setPosition(self.back.position[0],self.back.position[1])
            self.text.scaleHeight(24.0)
            self.text.draw()
        
        
        
        
    
#unlike most other scenes in this game, the battle scene 
#is completely controlled by the keyboard instead of mouse
class BattleSystem(Scene):
    def __init__(self, engine):

        self.engine = engine
        w, h = self.engine.w, self.engine.h

        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle, size = 32.0)

        self.party = self.engine.family.party
        self.formation = self.engine.formation.enemies

        self.incapParty = 0     #keeps track of how many in the party are incapacitated
                                #when all members are then the battle is over
        
        self.background = self.engine.formation.terrain
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        #self.start = ImgObj(Texture("start.png"))
        #self.start.setPosition(self.engine.w / 2, self.engine.h / 2)

        self.huds = [BattleHUDCharacter(character) for character in self.party]
        self.commandWheel = BattleMenu(self, self.party[0])
        self.inMenu = False

        self.active = 0         #which character is currently selecting commands
        self.battling = False   #are commands being selected or is fighting occuring?

        self.turn = 0           #whose turn is it
        self.turns = {}
        for character in self.party:
            character.initForBattle()
            self.turns[character] = 0
            
        for enemy in self.formation:
            enemy.initForBattle()
            self.turns[enemy] = 0
            
        self.order = []

        self.targetMenu = None
        self.targeting = False
        
        self.displayDelay = 0   #little delay ticker for displaying damage dealt upon a target

        self.victory = False    #win battle
        self.flee = False       #lose battle or retreat
        
    def keyPressed(self, key, char):
        if self.battling:
            return
            
        if self.targeting:
            self.targetMenu.keyPressed(key)
            if key == Input.BButton:
                self.targeting = False
        else:
            if key == Input.BButton:
                if self.commandWheel.step == 0:
                    self.active -= 1
                    if self.active < 0:
                        self.active = 0
                    self.commandWheel = BattleMenu(self, self.party[self.active])
                    
            self.commandWheel.keyPressed(key)
    
    def select(self, index):
        self.party[self.active].target = self.formation[index]
        self.next()
               
    def run(self):
        for hud in self.huds:
            hud.update()
            
        for character in self.party:
            if character.currentHP <= 0:
                character.currentHP = 0
                character.incap = True
            else:
                character.incap = False
        
        for enemy in self.formation:
            if enemy.currentHP <= 0:
                self.formation.remove(enemy)
                
        if len(self.formation):
            self.victory = True
        elif self.incapParty == len(self.party):
            self.flee = True
        
        
    #organizes all the turns for order of execution
    def battleStart(self):
        self.turn = 0
        
        #this needs to be called in case an enemy or actor has died
        self.turns = {}
        for character in self.party:
            if not character.incap:
                self.turns[character] = 0
            
        for enemy in self.formation:
            self.turns[enemy] = 0


        for character in self.party:
            if not (character.boost or character.defend):
                self.turns[character] = random.randint(0, 50) + character.spd

        for enemy in self.formation:
            if not (enemy.boost or enemy.defend):
                self.turns[enemy] = random.randint(0, 50) + enemy.spd
                enemy.getCommand(self.generateEnemyTargets(enemy))  #gets enemy's command and target
        
        self.order = sorted(self.turns.items(), key=itemgetter(1))
        print self.order
    
        self.battling = True
        
    #executes all of the commands
    def execute(self):
        print self.displayDelay
        
        actor = self.order[self.turn][0]
        
        if self.displayDelay == 0:
            actor.turnStart()
            
        if actor.target != None:
            #if the actor's target was knocked out during this phase then a new target
            # is automatically selected and damage is recalculated
            if actor.target.incap:
                actor.target = random.choice(self.generatePartyTargets(actor))
                actor.calculateDamage()
                
            pos = actor.target.getSprite().position    
            #draws the damage on screen
            bounce = lambda t:(-.0023*t**2 + .00134*t + pos[1])+50
            y = bounce(self.displayDelay-150)
            if self.displayDelay > 150:
                color = (1,1,1, (250 - self.displayDelay)/250.0)
            else:
                color = (1,1,1,1)
            self.engine.drawText(self.text, actor.damage, position = (pos[0], y), color = color)
            self.displayDelay += 5
            
            if self.displayDelay >= 300:
                actor.target.currentHP -= actor.damage
                if isinstance(actor.target, Character) and actor.target.currentHP <= 0:
                    self.incapParty += 1
                self.next()
        else:
            self.next()

    #generates the target list for enemies and auto-targetting
    def generateEnemyTargets(self, actor):
        targets = []
        if isinstance(actor, Character):
            targetGroup = self.formation
        else:
            targetGroup = self.party
        for t in targetGroup:
            if not t.incap:
                targets.append(t)
        return targets
       
    #generates the target list/menu for allies
    def generateTargets(self, actor):

        if actor.attacking or actor.cast:
            targets = [enemy.name for enemy in self.formation]
        else:
            targets= [member.name for member in self.party]

        position = (self.engine.w - 150, self.engine.h/2 + 30*len(targets)/2)
        targetMenu = MenuObj(self, targets, position, window = os.path.join("scenes", "battlesystem", "window.png"))
        return targetMenu
    
    def selectTarget(self):
        self.targetMenu = self.generateTargets(self.party[self.active])
        self.targeting = True
        
    #advances the character for command selection
    def next(self):
        if self.battling:
            self.order[self.active][0].turnEnd()
            self.displayDelay = 0
            self.turn += 1
            if self.turn >= len(self.order):
                self.battling = False
                self.turn = 0
                self.active = -1
                self.next()
        else:
            self.active += 1
            if self.active < len(self.party):
                self.commandWheel = BattleMenu(self, self.party[self.active])
            else:
                self.commandWheel = None
                self.battleStart()
            self.targeting = False
    
    def render(self, visibility):
        self.background.draw()
        
        #commenting out due to lack of image
        for i, hud in enumerate(self.huds):
            if len(self.party)>1 and self.active < len(self.party):
                if self.party[self.active]:
                    hud.scale = 1.0
                    hud.setPosition(0, self.engine.h - 60)
                else:
                    hud.scale = .5
                    hud.setPosition(0, self.engine.h - 30*i - 60)
            else:
                hud.scale = .5
                hud.setPosition(0, self.engine.h - 30*i)
            hud.draw()
        
        for i, member in enumerate(self.party):
            member.getSprite().setPosition(self.engine.w*.8 - 20*i, self.engine.h*.4 + 80*i)
            self.engine.drawAnimation(member.getSprite(), loop = True, reverse = False, delay = 20)
            
        self.engine.formation.draw()
        
        if not self.battling:
            if self.active < len(self.party):
                if self.targeting:
                    self.targetMenu.render(visibility)
                else:
                    self.commandWheel.render(visibility)
        else:
            self.execute()
            
    def victory(self):
        self.engine.changeScene("VictoryScene")
        
    def flee(self):
        self.engine.changeScene("Maplist")
        
        
