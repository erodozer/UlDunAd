import string
import Input

from sysobj import *
from MenuObj import MenuObj
        
#custom menu for character creation
class CreationMenu(MenuObj):
    def __init__(self, scene, scenepath):
    
        self.scene    = scene
        self.engine   = scene.engine
        w, h = self.engine.w, self.engine.h    
        
        #where on the screen should the menu be displayed
        position = (w*.25, h*.5)
        
        self.commands = ["Name:", "Job: ", "Sprite: ", "Stat Distribution", "Create"]
                                        #the commands to choose from (are drawn on the buttons)
        self.direction = False          #are the buttons in order vertically or horizontally
            
        self.name = self.scene.name
        if len(self.scene.sprites) > 0:
            sprite = self.scene.sprites[self.scene.selectedSprite]
        else:
            sprite = "None"
        self.values = [self.name, self.scene.job.name, sprite]
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), w*.45, h)
        self.window.setPosition(position[0], position[1])
        
        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)

        #the texture used for the buttons and the buttons themselves
        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
                         
        for i, button in enumerate(self.buttons):
            button.setScale(self.window.scale[0]-10, 64, inPixels = True)
            
            if i == len(self.buttons) - 1:
                pos = [position[0], position[1] - self.window.scale[1]/2 + 50]
            else:
                pos = [position[0], (position[1] + self.window.scale[1]/2 - 50) + (-(button.height + 5) * i)]
            
            
            button.setPosition(pos[0], pos[1])
            
        self.index = 0                  #which button is selected

    def refresh(self):
        if len(self.scene.sprites) > 0:
            sprite = self.scene.sprites[self.scene.selectedSprite]
        else:
            sprite = "None"
        self.values = [string.join(self.name, ''), self.scene.job.name, sprite]
    
    #arrow keys select which button it is
    #enter/return performs the scene's set action for that button
    def keyPressed(self, key):
            
        if key == Input.DnButton:
            if self.index + 1 < len(self.commands):
                self.index += 1
            else:
                self.index = 0
                
        elif key == Input.UpButton:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.commands) - 1
                
            
        if key == Input.LtButton:
            if self.index == 1:
                if self.scene.jobSelect > 0:
                    self.scene.jobSelect -= 1
                else:
                    self.scene.jobSelect = len(self.scene.jobs) - 1
                self.refresh()
            elif self.index == 2:
                if len(self.scene.sprites) > 0:
                    self.scene.selectedSprite = max(0, self.scene.selectedSprite - 1)
                
        elif key == Input.RtButton:
            if self.index == 1:
                if self.scene.jobSelect > len(self.scene.jobs) - 1:
                    self.scene.jobSelect += 1
                else:
                    self.scene.jobSelect = 0
                self.refresh()
            elif self.index == 2:
                self.scene.selectedSprite = min(len(self.scene.sprites)-1, self.scene.selectedSprite + 1)
                
                    
        elif key == Input.AButton:
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
            
            if i < 3:
                self.text.setText(self.values[i]) 
                self.text.setPosition(button.position[0] + button.width/2 - 5, button.position[1])
                self.text.scaleHeight(36.0)
                self.text.setAlignment("right")
                self.text.draw()
            
        for i, stat in enumerate(self.scene.stats):            
            self.text.setText(self.scene.stats[i]) 
            self.text.setPosition(self.buttons[3].position[0] - self.window.scale[0]/2 + 30,
                                  self.buttons[3].position[1] - 45 - 34*i)
            self.text.scaleHeight(32.0)
            self.text.setAlignment("left")
            self.text.draw()
            
            self.text.setText(self.scene.job.stats[i] + self.scene.distAreas[i]) 
            self.text.setPosition(self.buttons[3].position[0] + self.window.scale[0]/2 - 20,
                                  self.buttons[3].position[1] - 45 - 34*i)
            self.text.scaleHeight(32.0)
            self.text.setAlignment("right")
            self.text.draw()
            
