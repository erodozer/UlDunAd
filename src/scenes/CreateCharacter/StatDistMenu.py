import Input

from MenuObj import MenuObj

class StatDistMenu(MenuObj):
    def __init__(self, scene, scenepath):

        self.scene    = scene
        self.engine   = scene.engine
        w, h = self.engine.w, self.engine.h    

        position = (w*.5, h*.5)
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), w*.5, h)
        self.window.setPosition(position[0], position[1])
        
        self.commands = self.scene.stats

        #font setting for buttons
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle)

        buttonStyle = Texture(os.path.join(scenepath, "button.png"))
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.commands))]
        
        for i, button in enumerate(self.buttons):
            button.setScale(self.window.scale[0]-10, 48, inPixels = True)    
            pos = (position[0], (position[1] + self.window.scale[1]/2 - 50 + (-(button.height + 5) * i)))
            button.setPosition(pos[0], pos[1])

        
        self.statButtons = [[ImgObj(Texture(os.path.join(scenepath, "statdistbutton.png")), boundable = True, frameX = 2)
                             for n in range(2)]
                             for i in range(len(self.buttons))]
                            
        for i, buttons in enumerate(self.statButtons):
            for n, button in enumerate(buttons):
                pos = (position[0] + self.buttons[0].width/2 - (30 + (100*n)), 
                       self.buttons[i].position[1])
                button.setPosition(pos[0], pos[1])
                button.setFrame(x = n+1)
                                    
        self.index = 0
        
    def buttonClicked(self, image):
        
        if image in self.statButtons[:]:
            #click on the plus
            if self.statButtons[:].index(image) == 0:
                if self.scene.distAreas[self.index] > 0:
                    self.scene.distAreas[self.index] -= 1
                    self.scene.distPoints += 1
                else:
                    self.scene.distAreas[self.index] = 0
            #click on the minus
            elif self.statButtons[:].index(image) == 1:
                if self.scene.distPoints > 0:
                    self.scene.distAreas[self.index] += 1
                    self.scene.distPoints -= 1
                else:
                    self.scene.distPoints = 0
        elif image in self.buttons:
            self.index = self.buttons.index(image)
        
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
                
        elif key == Input.LtButton:
            if self.scene.distAreas[self.index] > 0:
                self.scene.distAreas[self.index] -= 1
                self.scene.distPoints += 1
            else:
                self.scene.distAreas[self.index] = 0
                    
        elif key == Input.RtButton:
            if self.scene.distPoints > 0:
                self.scene.distAreas[self.index] += 1
                self.scene.distPoints -= 1
            else:
                self.scene.distPoints = 0
                    
        elif key == Input.AButton or key == Input.BButton:
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
            
            self.engine.drawImage(self.statButtons[i][0])
            self.engine.drawImage(self.statButtons[i][1])
            
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
        
            
            
