from sysobj import *
from View   import *
from Character  import *

import Input          

from MenuObj import MenuObj

class FamilyMenu(MenuObj):
    def __init__(self, scene, families):
        self.scene = scene
        self.engine = scene.engine
        self.commands = families
        self.moveKeys = [Input.DnButton, Input.UpButton]
        
        scenepath = os.path.join("scenes", "familylist")
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        
        buttonStyle  = Texture(os.path.join(scenepath, "highlight.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
                        
        self.position = (self.engine.w/10, self.engine.h - self.buttons[0].height)
        for i, button in enumerate(self.buttons):
            button.setScale(self.engine.w*.80, self.engine.h/6, inPixels = True)
            button.setPosition(self.position[0], self.position[1] - ((button.height + 10) * i))
            button.setAlignment("left")
        self.slideRate = 150.0/512.0
        
        self.index = 0
        self.startIndex = 0
        self.endIndex = min(4, len(self.commands))

    def keyPressed(self, key):
        if key == Input.AButton:
            self.scene.select(self.index)
            
        if key == self.moveKeys[0]:
            if self.index + 1 == self.endIndex:
                if len(self.commands) > 4:
                    self.startIndex = min(self.startIndex+4, len(self.commands)-4)
            else:
                if self.index + 1 < len(self.commands):
                    self.index += 1
                else:
                    self.index = 0
                    self.startIndex = 0
                
        elif key == self.moveKeys[1]:
            if self.index - 1 == self.startIndex-1:
                if len(self.commands) > 0:
                    self.startIndex = max(self.startIndex - 4, 0)
            else:
                if self.index > 0:
                    self.index -= 1
                else:
                    self.index = len(self.commands) - 1 
                    self.startIndex = len(self.commands) - 4       
            
        self.endIndex = min(self.startIndex + 4, len(self.commands))

    def buttonClicked(self, image):
        if (image in self.buttons[:(self.endIndex-self.startIndex)]):
            i = self.buttons.index(image)
            if not self.index == i + self.startIndex:
                self.index = i + self.startIndex
            else:
                self.scene.select(self.index)
    
    #renders the menu
    def render(self, visibility = 1.0):

        families = self.commands[self.startIndex:self.endIndex]
        
        #rendersthe buttons
        for i, button in enumerate(self.buttons[:(self.endIndex-self.startIndex)]):
            family = families[i]
        
            if i == self.index%4:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
        
            self.engine.drawImage(button)
        
            #renders family name
            self.text.setText(family.name) 
            self.text.setPosition(button.position[0] - self.engine.w/10, button.position[1])
            self.text.scaleHeight(36.0)
            self.text.setAlignment("left")
            self.text.draw()
            
            #renders the number of members in the family
            self.text.setPosition(button.position[0] + button.width - self.engine.w/10, button.position[1])
            self.text.setText("Members:%i" % len(family.members)) 
            self.text.scaleHeight(36.0)
            self.text.setAlignment("right")
            self.text.draw()
  
