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

#custom menu for character creation
class JobMenu(MenuObj):
    def __init__(self, scene, scenepath, position):
    
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands = self.engine.listPath(os.path.join("actors", "jobs"), "splitfiletype", ".ini")
        self.direction = False          #are the buttons in order vertically 
            
        self.name = self.scene.name
        self.job = self.scene.job
        self.values = [self.name, self.job]
        
        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)

        #which keys select the next or previous button
        self.moveKeys = [K_DOWN, K_UP]
        
        #the texture used for the buttons and the buttons themselves
        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons  = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                         for n in range(len(self.commands))]
        
        #where on the screen should the menu be displayed
        #  verticle is positioned from the top
        #  horizontal from the left
        self.position = position
        
        self.index = 0                  #which button is selected
        
    #renders the menu
    def render(self, visibility = 1.0):
        
        if self.index >= 10:
            start = self.index-9
            end = self.index
        else:
            start = 0
            end = 9
            
        for i, button in enumerate(self.buttons[start:end]):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
                
            if self.direction:
                pos = [self.position[0] + ((button.width + 5) * i), self.position[1]]
            else:
                pos = [self.position[0], self.position[1] + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])
            button.draw()
            
            self.text.setText(self.commands[i]) 
            self.text.setPosition(button.position[0], button.position[1])
            self.text.scaleHeight(36.0)
            self.text.draw()
            
#custom menu for character creation
class CreationMenu(MenuObj):
    def __init__(self, scene, scenepath, position):
    
        self.scene    = scene
        self.engine   = scene.engine    
        
        self.commands = ["Name:", "Job"]#the commands to choose from (are drawn on the buttons)
        self.direction = False          #are the buttons in order vertically or horizontally
            
        self.name = self.scene.name
        self.job = self.scene.job
        self.values = [self.name, self.job]
        
        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)

        #which keys select the next or previous button
        self.moveKeys = [K_DOWN, K_UP]
        
        #the texture used for the buttons and the buttons themselves
        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons  = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                         for n in range(len(self.commands))]
                         
        #where on the screen should the menu be displayed
        #  verticle is positioned from the top
        #  horizontal from the left
        self.position = position
        
        for i, button in enumerate(self.buttons):
            if self.direction:
                pos = [self.position[0] + ((button.width + 5) * i), self.position[1]]
            else:
                pos = [self.position[0], self.position[1] + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])
            
        self.index = 0                  #which button is selected
        
    #renders the menu
    def render(self, visibility = 1.0):
        
        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            button.draw()
            
            self.text.setText(self.commands[i]) 
            self.text.setPosition(button.position[0] - button.width/2, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("left")
            self.text.draw()
            
            self.text.setText(self.values[i]) 
            self.text.setPosition(button.position[0] + button.width/2, button.position[1])
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
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), w*.4, h*.7)
        self.window.setPosition(w*.5, h*.5)
        
        self.nameWindow = WinObj(Texture(os.path.join(scenepath, "window.png")),0,0)
        self.nameWindow.setPosition(w*.7, h*.8)
        self.nameButton = ImgObj(Texture("ok.png"), boundable = True, frameX = 2)
        
        self.jobWindow = WinObj(Texture(os.path.join(scenepath, "window.png")),0,0)
        self.jobWindow.setPosition(w*.7, h*.8)
        self.jobMenu = JobMenu(self, scenepath, (w*.7, h*.8))
        
        self.menu = CreationMenu(self, scenepath, (w*.4, h*.7))
        
        self.font   = FontObj("default.ttf")

        self.error = False      #was an error thrown
        self.step = -1          #step -1 = basic, step 0 = naming, step 1 = choose job

        Input.resetKeyPresses()

    def run(self):
        pass

    def keyPressed(self, key, char):
        if self.step == -1:
            self.menu.keyPressed(key)
        if self.step == 0:
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
                    self.step = -1
                    
        elif self.step == 1:
                    
            self.jobMenu.keyPressed(key)                

    def select(self, index):
        if self.step == -1:
            if index == 0:
                self.step = 0
            elif index == 1:
                self.step = 1
        elif self.step == 1:
            self.job = index
       
    def renderNaming(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.nameWindow.draw()

        if visibility >= 1.0:
            name = string.join(self.name, '')
            self.engine.drawText(self.font, name, (w*.61, h*.7), alignment="left")

            if name:
                self.engine.drawImage(self.button, position = (w/2, h*.4), scale = (75,75))

    def renderJobs(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.jobWindow.draw()
        self.jobMenu.draw()

    def create(self):
        name = string.join(self.name, '')
        family = Character(None)
        character.create(name, self.diffselected)
        self.engine.family.refresh()
        self.engine.viewport.changeScene("MainMenu")
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))
        self.window.draw()
        
        if self.step == 0:
            self.renderNaming(visibility)
        elif self.step == 1:
            self.renderClass(visibility)
        else:
            self.renderMain(visibility)

        if self.error:
            self.engine.showError("You must enter a name")


        
