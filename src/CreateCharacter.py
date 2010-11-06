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

class StatDistMenu(MenuObj):
    def __init__(self, scene, scenepath):

        self.scene    = scene
        self.engine   = scene.engine
        w, h = self.engine.w, self.engine.h    

        position = (w*.5, h*.5)
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), w*.6, h*.85)
        self.window.setPosition(position[0], position[1])
        
        self.commands = ["Strength", "Defense", "Agility", "Evasion", "Force", "Resistance"]

        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)

        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
        
        for i, button in enumerate(self.buttons):
            button.setScale(w*.5, 64)
            pos = [position[0], ((position[1] + self.window.scale[1]/2) - 70) + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])

        
        self.statButtons = ImgObj(Texture(os.path.join(scenepath, "statdistbutton.png")), boundable = True, frameX = 2)
                            
        self.index = 0
        
    #arrow keys select which button it is
    #enter/return performs the scene's set action for that button
    def keyPressed(self, key):
          
        distTo = self.scene.distAreas[self.index]
        points = self.scene.distPoints
        
        if key == K_DOWN:
            if self.index + 1 < len(self.commands):
                self.index += 1
            else:
                self.index = 0
                
        elif key == K_UP:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.commands) - 1
                
        elif key == K_LEFT:
            if distTo > 0:
                distTo -= 1
                points += 1
            else:
                distTo = 0
                    
        elif key == K_RIGHT:
            if points > 0:
                distTo += 1
                points -= 1
            else:
                points = 0
                    
        elif key == K_RETURN:
            self.scene.step = -1
                    
        return None
                              
    #renders the menu
    def render(self, visibility = 1.0):
        
        self.window.draw()
        
        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            button.draw()
            
            self.text.setText(self.commands[i]) 
            self.text.setPosition(button.position[0] - button.width/2 + 5, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("left")
            self.text.draw()
            
            self.text.setText(self.scene.distAreas[i]) 
            self.text.setPosition(button.position[0] + button.width/2 - 80, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("center")
            self.text.draw()
            
            self.engine.drawImage(self.statButtons, position = (button.position[0] + button.width/2 - 130, button.position[1]),
                                  scale = (32,32), frameX = 1)
            self.engine.drawImage(self.statButtons, position = (button.position[0] + button.width/2 - 30, button.position[1]),
                                  scale = (32,32), frameX = 2)
                                  
        self.text.setText("Distribution Points: ") 
        self.text.setPosition(self.window.position[0] - self.window.scale[0]/2 + 15 , 
                              self.window.position[1] - self.window.scale[1]/2 + 50)
        self.text.scaleHeight(36.0)
        self.text.setAlignment("left")
        self.text.draw()
            
        self.text.setText(self.scene.distPoints) 
        self.text.setPosition(self.window.position[0] + self.window.scale[0]/2 - 15, 
                              self.window.position[1] - self.window.scale[1]/2 + 50)
        self.text.scaleHeight(36.0)
        self.text.setAlignment("right")
        self.text.draw()
        
            
            
        
#custom menu for character creation
class CreationMenu(MenuObj):
    def __init__(self, scene, scenepath):
    
        self.scene    = scene
        self.engine   = scene.engine
        w, h = self.engine.w, self.engine.h    
        
        #where on the screen should the menu be displayed
        position = (w*.3, h*.5)
        
        self.commands = ["Name:", "Job: ", "Stat Distribution", "Create"]
                                        #the commands to choose from (are drawn on the buttons)
        self.direction = False          #are the buttons in order vertically or horizontally
            
        self.name = self.scene.name
        self.values = [self.name, self.scene.job]
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), w*.6, h*.7)
        self.window.setPosition(position[0], position[1])
        
        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)

        #which keys select the next or previous button
        self.moveKeys = [K_DOWN, K_UP]
        
        #the texture used for the buttons and the buttons themselves
        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
                         
        for i, button in enumerate(self.buttons):
            button.setScale(w*.5, 64)
            pos = [position[0], (position[1] + h*.2) + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])
            
        self.index = 0                  #which button is selected

    def refresh(self):
        self.values = [string.join(self.name, ''), self.scene.job]
    
    #arrow keys select which button it is
    #enter/return performs the scene's set action for that button
    def keyPressed(self, key):
            
        if key == K_DOWN:
            if self.index + 1 < len(self.commands):
                self.index += 1
            else:
                self.index = 0
                
        elif key == K_UP:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.commands) - 1
                
        if self.index == 1:
            
            if key == K_LEFT:
                if self.scene.jobSelect > 0:
                    self.scene.jobSelect -= 1
                else:
                    self.scene.jobSelect = len(self.scene.jobs) - 1
                self.refresh()
                    
            elif key == K_RIGHT:
                if self.scene.jobSelect < len(self.scene.jobs) - 1:
                    self.scene.jobSelect += 1
                else:
                    self.scene.jobSelect = 0
                self.refresh()
                    
        elif key == K_RETURN:
            self.scene.select(self.index)
                    
        return None
        
    #renders the menu
    def render(self, visibility = 1.0):
        
        self.window.draw()
        
        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            button.draw()
            
            self.text.setText(self.commands[i]) 
            self.text.setPosition(button.position[0] - button.width/2 + 5, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("left")
            self.text.draw()
            
            if i < 2:
                self.text.setText(self.values[i]) 
                self.text.setPosition(button.position[0] + button.width/2 - 5, button.position[1])
                self.text.scaleHeight(36.0)
                self.text.setAlignment("right")
                self.text.draw()
            
class CreateCharacter(Scene):
    def __init__(self, engine):
        self.engine = engine
        w, h = self.engine.w, self.engine.h
        
        self.name   = []
        self.job    = None
    
        scenepath = os.path.join("scenes", "creation")
        self.background = ImgObj(Texture(os.path.join(scenepath, "creation.png")))
        
        
        self.nameWindow = WinObj(Texture(os.path.join(scenepath, "window.png")),w*.45,h*.15)
        self.nameButton = ImgObj(Texture("ok.png"), boundable = True, frameX = 2)
        
        self.jobs = self.engine.listPath(os.path.join("actors", "jobs"), flag = "filename")
        self.jobSelect = 0
        self.job = self.jobs[self.jobSelect]
        
        self.statDistMenu = StatDistMenu(self, scenepath)
        self.distPoints = 20
        self.distAreas = [0,0,0,0,0,0]
        
        self.menu = CreationMenu(self, scenepath)
        
        self.font   = FontObj("default.ttf")

        self.error = False      #was an error thrown
        self.step = -1          #step -1 = basic, step 0 = naming, step 1 = choose job

    def run(self):
        self.job = self.jobs[self.jobSelect]
        
    def keyPressed(self, key, char):
        if self.step == -1:
            self.menu.keyPressed(key)
        elif self.step == 0:
            #name is a maximum of 13 letters
            if len(self.name) < 13:
                if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                    self.name.append(char)
                if len(self.name) > 0:  #can not have the first character be a blank
                    if key == K_SPACE:
                        self.name.append(" ")

            if len(self.name) > 0:
                #can only delete letters if there are some to delete
                if key == K_BACKSPACE:
                    self.name.pop(-1)
                if key == K_RETURN:
                    self.menu.name = string.join(self.name, '')
                    self.step = -1
        elif self.step == 1:
            self.statDistMenu.keyPressed(key)
                    

    def select(self, index):
        if self.step == -1:
            if index == 0:
                self.step = 0
            if index == 2:
                self.step = 1
            if index == 3:
                self.create()
       
    def renderNaming(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.nameWindow.setPosition(w*.7, h*.8)
        self.nameWindow.draw()

        if visibility >= 1.0:
            name = string.join(self.name, '')
            self.engine.drawText(self.font, name, (w*.5, h*.8), alignment="left")

            if name:
                self.engine.drawImage(self.nameButton, position = (w*.85, h*.8), scale = (75,75))
            
    def create(self):
        name = string.join(self.name, '')
        character = Character(None)
        character.create(self.family.name, self.name, self.job)
        self.engine.family.refresh()
        self.engine.viewport.changeScene("MapList")
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))
        if not self.step == 1:
            self.menu.render()

        if self.step == 0:
            self.renderNaming(visibility)
        elif self.step == 1:
            self.statDistMenu.render()
        else:
            self.menu.refresh()
        
        if self.error:
            self.engine.showError("You must enter a name")


        
