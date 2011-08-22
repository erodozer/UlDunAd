from sysobj import *
import Input

from MenuObj import MenuObj
from Command import *

pageLength = 5     #length of each set of commands

pageWidth = 3      #width for item and skill windows
    
#Bottom right corner command menu circle thing
class BattleMenu(MenuObj):
    def __init__(self, scene, character):
        self.scene = scene
        self.engine = scene.engine
        self.character = character
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle, size = 24)
        
        #0 = attack menu, 2 = strategic menu, 3 = item menu
        
        self.command = 0        #command selected
        self.index = 0          #index selected in the window
        self.step = 0           #menu showing
        
        self.page = 0           #offset index for grouping commands in sets
        
        self.button = ImgObj(os.path.join("scenes", "battlesystem", "button.png"), frameY = 2)
        weapon = self.character.equipment[character.hand]
        
        #attack menu
        if weapon.type == "gun" or weapon.type == "bow":
            self.attackCommands = [Shoot(self.character, 0)]
            if "double" in weapon.firingMode:
                self.attackCommands.append(Shoot(self.character, 1))
            else:
                if weapon.type == "gun":
                    if "burst" in weapon.firingMode:
                        self.attackCommands.append(Shoot(self.character, 2))
                    if "auto" in weapon.firingMode:
                        self.attackCommands.append(Shoot(self.character, 3))
        else:
            self.attackCommands = [Attack(self.character, 0), 
                                   Attack(self.character, 1),
                                   Attack(self.character, 2)]
        
            if weapon.attack:
                self.attackCommands.append(ComboAttack(self.character))
            
        self.tactCommands = [Boost(self.character),
                             Defend(self.character),
                             Flee(self.character, self.scene.party, self.scene.formation)] #tactical menu
        self.itemCommands = self.engine.family.inventory.battle().values()    
                                                            #item menu
        self.techCommands = character.battleSkills          #character's list of skills
        
        #basic command menu
        self.basicCommands = [["Attack", self.attackCommands], ["Tactical", self.tactCommands]]
        if len(self.itemCommands) > 0:
            self.basicCommands.append(["Item", self.itemCommands])
        if len(self.techCommands) > 0:
            self.basicCommands.append(["Spell/Tech", self.techCommands])
            
        self.activeCommands = self.basicCommands
        
        self.pos = (self.engine.w*.075, self.engine.h*.295)
        
    def keyPressed(self, key):
        
        if key == Input.UpButton:
            if self.index % pageLength == 0:
                self.page = max(0, self.page - pageLength)
            self.index = max(self.index-1, 0)

                    
        if key == Input.DnButton:
            commands = self.activeCommands
            self.index = min(self.index + 1, len(commands) - 1)
                    
            if self.index % 5 == 0:
                self.page = min(self.page + pageLength, len(commands) - pageLength)
            
                
        #overrides default a button pressing
        if key == Input.AButton:
            if self.step == 1:
                self.scene.select(self.index)
            elif self.activeCommands == self.basicCommands:
                #1 - attacking menu
                #2 - tactical menu
                #3 - item menu
                #4 - skill menu
                self.activeCommands = self.basicCommands[self.index][1]
            elif self.activeCommands == self.attackCommands:
                self.character.command = self.attackCommands[self.index]
                
                #if the cost is more than the character can spend then prevent the action
                if self.character.command.fpCost > self.character.fp:
                    self.character.command = None
                    return
                self.scene.selectTarget()
                self.step = 1
                self.activeCommands = self.scene.targetMenu
            elif self.activeCommands == self.tactCommands:
                self.character.command = self.tactCommands[self.index]
                self.scene.next()
            elif self.activeCommands == self.itemCommands:
                self.character.command = UseItem(self.character, self.itemCommands[self.index][0])
                self.scene.selectTarget()
                self.step = 1
            elif self.activeCommands == self.techCommands:
                self.character.command = Cast(self.character, self.techCommands[self.index])
                self.scene.selectTarget()
                self.step = 1

            self.page = 0
            self.index = 0
                
        if key == Input.BButton:
            self.step = 0
            self.index = 0
            self.page = 0
            self.activeCommands = self.basicCommands
        
        
    def renderCommands(self, commands):
        for i, item in enumerate(commands[self.page:min(self.page+pageLength,len(commands))]):
            position = (self.pos[0] + 16.0*i, self.pos[1] - 48.0 * i)
                
            if i == self.index:
                self.button.setFrame(y=2)
            else:
                self.button.setFrame(y=1)
            self.button.setAlignment("left")
            self.button.setPosition(position[0]-50.0, position[1])
            self.button.draw()
            
            if commands is self.basicCommands:
                self.text.setText(item[0])
            else:
                self.text.setText(item)
              
            self.text.setAlignment("left")
            self.text.setPosition(*position)
            self.text.draw()
                
    def renderItems(self, commands):
        for i, item in enumerate(commands[self.page:min(self.page+pageLength+pageWidth,len(commands))]):
            position = (self.pos[0] + 16.0*(i%3), self.pos[1] - 48.0 * (i/3))
                
            if i == self.index:
                self.button.setFrame(y=2)
            else:
                self.button.setFrame(y=1)
            self.button.setAlignment("left")
            self.button.setPosition(position[0]-50.0, position[1])
            self.button.draw()
            
            self.text.setText("%s: %02d" % (item[0].name, item[1]))  
              
            self.text.setAlignment("left")
            self.text.setPosition(*position)
            self.text.draw()
                    
    def render(self, visibility):
        commands = self.activeCommands
        
        if commands == self.itemCommands or commands == self.techCommands:
            self.renderItems(commands) 
        else:
            self.renderCommands(commands)
              
        directions = ""
        if len(commands) > self.page+pageLength:
            directions += "^"
        if self.page > 0:
            directions += "v"
            
        self.text.setText(directions)
        self.text.setPosition(self.pos[0], self.pos[1] + 20)
        self.text.draw()
              
            
