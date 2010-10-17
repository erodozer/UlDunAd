from sysobj import *

#creates a little button menu
class MenuObj:
    def __init__(self, scene, commands, position = (0, 0), fontStyle = None,
                 buttonStyle = None, window = False, horizontal = False):
    
        self.scene    = scene
        self.engine   = scene.engine
        self.commands = commands
        self.direction = horizontal
                
        if fontStyle == None:
            fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)

        if self.direction:
            self.moveKeys = [K_RIGHT, K_LEFT]
        else:
            self.moveKeys = [K_DOWN, K_UP]
        
        if buttonStyle == None:
            buttonStyle = self.engine.data.defaultButton  
        self.buttons  = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                         for n in range(len(self.commands))]
        self.position = position
        
        for i, button in enumerate(self.buttons):
            if self.direction:
                pos = [self.position[0] + ((button.width + 5) * i), self.position[1]]
            else:
                pos = [self.position[0], self.position[1] + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])
            
        self.index = 0
        
    def keyPressed(self, key):
        if key == K_RETURN:
            self.scene.select(self.index)
            
        if key == self.moveKeys[0]:
            if self.index + 1 < len(self.commands):
                self.index += 1
            else:
                self.index = 0
                
        elif key == self.moveKeys[1]:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.commands) - 1
                
        return None
        
    def buttonClicked(self, image):
        if (image in self.buttons):
            i = self.buttons.index(image)
            if not self.index == i:
                self.index = i
            else:
                self.scene.select(self.index)
                
    def render(self, visibility):
        

        for i, button in enumerate(self.buttons):
            if i == self.index:
                button.setFrame(y = 2)
            else:
                button.setFrame(y = 1)
            button.draw()
            
            self.text.setText(self.commands[i]) 
            self.text.setPosition(button.position[0], button.position[1])
            self.text.scaleHeight(36.0)
            self.text.draw()
        
                
                
