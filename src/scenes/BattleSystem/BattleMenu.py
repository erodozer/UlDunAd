from sysobj import *
import Input

from MenuObj import MenuObj
from Command import *

pageLength = 5     #length of each set of commands
    
#Bottom right corner command menu circle thing
class BattleMenu(MenuObj):
    def __init__(self, scene, character):
        self.scene = scene
        self.engine = scene.engine
        self.character = character
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)
        
        #0 = attack menu, 2 = strategic menu, 3 = item menu
        self.highlight = ImgObj(Texture("window_selected.png"))
        
        self.command = 0        #command selected
        self.index = 0          #index selected in the window
        self.step = 0           #menu showing
        
        self.page = 0           #offset index for grouping commands in sets
        
        self.basicCommands = ["Attack", "Tactical", "Item", "Spell/Tech"] #basic command menu
        weapon = self.character.equipment[character.hand]
        
        #attack menu
        if weapon.type == "gun" or weapon.type == "bow":
            self.attackCommands = [["Single", Shoot(self.character, 0)]]
            if "double" in weapon.firingMode:
                self.attackCommands.append(["Double", Shoot(self.character, 1)])
            else:
                if weapon.type == "gun":
                    if "burst" in weapon.firingMode:
                        self.attackCommands.append(["Burst", Shoot(self.character, 2)])
                    if "auto" in weapon.firingMode:
                        self.attackCommands.append(["Auto", Shoot(self.character, 3)])
        else:
            self.attackCommands = [["Normal"  ,Attack(self.character, 0)], 
                                   ["Accurate",Attack(self.character, 1)],
                                   ["Strong"  ,Attack(self.character, 2)]]
        
            if weapon.attack:
                self.attackCommands.append(["Combo", ComboAttack(self.character)])
            
        self.tactCommands = [["Boost" ,Boost(self.character)],
                             ["Defend",Defend(self.character)],
                             ["Flee"  ,None]] #tactical menu
        self.itemCommands = self.engine.family.inventory    #item menu
        self.techCommands = character.skills                #character's list of skills
        
        self.activeCommands = self.basicCommands
        
        self.pos = (self.engine.w*.25, self.engine.h*.3)
        
        self.makeMenu()
        
    def makeMenu(self):
        commands = self.activeCommands
        self.commandWin = WinObj(Texture("window.png"), 200, 32 * min(5,len(commands)-self.page)+8)
        self.commandWin.setPosition(self.pos[0] - (self.commandWin.scale[0]/2 + 10),
                                    self.pos[1] - self.commandWin.scale[1]/2 + 10)
        self.highlight.setScale(self.commandWin.scale[0] - 10, 32.0, inPixels = True)
        
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
            if self.step == 0:
                self.step = self.index + 1
                #1 - attacking menu
                #2 - tactical menu
                #3 - item menu
                #4 - skill menu
                if self.step == 0:
                    self.activeCommands = self.basicCommands
                elif self.step == 1:
                    self.activeCommands = self.attackCommands
                elif self.step == 2:
                    self.activeCommands = self.tactCommands
                elif self.step == 3:
                    self.activeCommands = self.itemCommands
                elif self.step == 4:
                    self.activeCommands = self.techCommands
            elif self.step == 1:
                self.character.command = self.attackCommands[self.index][1]
                
                #if the cost is more than the character can spend then prevent the action
                if self.character.command.fpCost > self.character.fp:
                    self.character.command = None
                    return
                self.scene.selectTarget()
                self.step = 5
                self.activeCommands = self.scene.targetMenu
            elif self.step == 2:
                if self.index == 2:   #flee
                    self.scene.flee()
                else:
                    self.character.command = self.tactCommands[self.index][1]
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
            self.page = 0
            self.index = 0
            self.makeMenu()
                
        if key == Input.BButton:
            self.step = 0
            self.index = 0
            self.page = 0
            self.activeCommands = self.basicCommands
            self.makeMenu()
        
        
    def render(self, visibility):
        
        self.commandWin.draw()
        
        commands = self.activeCommands
        
        for i, item in enumerate(commands[self.page:min(self.page+pageLength,len(commands))]):
            position = (self.commandWin.position[0], self.commandWin.position[1] + (self.commandWin.scale[1]/2 - 20) - 32.0 * i)
                
            if i == self.index:
                self.highlight.setPosition(position[0], position[1])
                self.highlight.draw()
        
            if self.step == 0 or self.step == 5:
                self.text.setText(item)
            elif self.step == 3 or self.step == 4:
                self.text.setText("%02d:%s" % (item[1], item[0].name))
            else:
                self.text.setText(item[0])     
            self.text.setAlignment("center")
            self.text.setPosition(position[0], position[1])
            self.text.scaleHeight(28.0)
            self.text.setScale(min(self.commandWin.scale[0], self.text.width), self.text.height)
            self.text.draw()
                
        directions = ""
        if len(commands) > self.page+pageLength:
            directions += "^"
        if self.page > 0:
            directions += "v"
            
        self.text.setText(directions)
        self.text.setPosition(self.commandWin.position[0], self.commandWin.position[1] + (self.commandWin.scale[1]/2 + 20))
        self.text.draw()
              
            
