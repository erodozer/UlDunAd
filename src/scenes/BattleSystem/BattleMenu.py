from sysobj import *
import Input

from MenuObj import MenuObj
from Command import *

#Bottom right corner command menu circle thing
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
        
        self.basicCommands = ["Attack", "Tactical", "Item", "Spell/Tech"] #basic command menu
        self.attackCommands = {"Normal"  :Attack(self.character, 0), 
                               "Accurate":Attack(self.character, 1),
                               "Strong"  :Attack(self.character, 2)} #attack menu
        
        if character.equipment[character.hand].attack:
            self.attackCommands["Combo"] = ComboAttack(self.character)
            
        self.tactCommands = {"Boost" :Boost(self.character),
                             "Defend":Defend(self.character),
                             "Flee"  :None} #tactical menu
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
                if self.step == 1:
                    commands = self.attackCommands
                elif self.step == 2:
                    commands = self.tactCommands
                elif self.step == 5:
                    commands = self.scene.targetMenu
                else:
                    commands = self.basicCommands
                
                if self.index + 1 < len(commands):
                    self.index += 1
            
                
        #overrides default a button pressing
        if key == Input.AButton:
            if self.step == 0:
                self.step = self.index + 1
                #1 - attacking menu
                #2 - tactical menu
                #3 - item menu
                #4 - skill menu
            elif self.step == 1:
                self.character.command = list(self.attackCommands.values())[self.index]
                
                #if the cost is more than the character can spend then prevent the action
                if self.character.command.fpCost > self.character.fp:
                    self.character.command = None
                    return
                self.scene.selectTarget()
                self.step = 5
            elif self.step == 2:
                if self.index == 2:   #flee
                    self.scene.flee()
                else:
                    self.character.command = list(self.tactCommands.values())[self.index]
                self.scene.next()
            elif self.step == 3:
                self.character.command = self.itemCommands[self.index]
                self.scene.selectTarget()
                self.step = 5
            elif self.step == 4:
                self.character.command = self.techCommands[self.index]
                self.scene.selectTarget()
                self.step = 5
            elif self.step == 5:
                self.scene.select(self.index)
            self.index = 0
                
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
            elif self.step == 5:
                commands = self.scene.targetMenu
            
            if isinstance(commands, dict):
                commands = list(commands.keys())
                
            self.text.setText(commands[self.index])
            self.text.setPosition(self.back.position[0],self.back.position[1])
            self.text.scaleHeight(24.0)
            self.text.draw()
        
