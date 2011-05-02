from sysobj import *
import Input

class BattleHUDAddition:
    def __init__(self, engine, character):
        self.engine = engine
        self.character = character
        self.weapon = self.character.equipment[self.character.hand]
        
        self.font = FontObj("default.ttf", 16)  #used for displaying the time
        
        self.comboIndex = 0
        self.comboTimer = self.weapon.time      #time given to perform the attack
        self.addition = self.weapon.attack      #the list of input keys that need to be hit
        self.success = -1                       #0 is failure, 1 = success
        
        #images used for displaying the input combo 
        self.inputButtons = [ImgObj(Texture("inputButtons.png"), frameY = 5) for i in self.addition]
        for i, button in enumerate(self.inputButtons):
            frame, angle = self.getButtonImage(self.addition[i])
            button.setFrame(y = frame)
            button.setAngle(angle)
            button.setScale(96,96, inPixels = True)

    def keyPressed(self, key):
        if self.comboTimer > 0:
            if key == self.addition[self.comboIndex]:
                self.comboIndex += 1
                if self.comboIndex >= len(self.addition):
                    self.success = 1
                    self.comboIndex = 0
                    self.comboTimer = 0
            else:
                self.comboTimer = 0
                self.success = 0
            
    def getButtonImage(self, key):
        #directional buttons
        if (key == Input.UpButton or
            key == Input.DnButton or
            key == Input.LtButton or
            key == Input.RtButton):
            frame = 5
            if key == Input.UpButton:
                angle = 0
            elif key == Input.RtButton:
                angle = 90
            elif key == Input.DnButton:
                angle = 180
            else:
                angle = 270
        #letter buttons
        else:
            angle = 0
            if key == Input.AButton:
                frame = 1
            elif key == Input.BButton:
                frame = 2
            elif key == Input.CButton:
                frame = 3
            else:
                frame = 4
        return frame, angle
        
    def run(self):
        if self.comboTimer > 0:
            self.comboTimer -= 1
            if self.comboTimer <= 0:
                if self.success == -1:
                    self.success = 0
                
    def draw(self):
        self.engine.drawImage(self.inputButtons[self.comboIndex], position = (self.engine.w/2, self.engine.h/2),
                              color = (1,1,1,1))
        if self.comboIndex + 1 < len(self.addition):
            self.engine.drawImage(self.inputButtons[self.comboIndex+1], position = (self.engine.w/2 + self.inputButtons[0].width + 10.0, self.engine.h/2),
                                  color = (1,1,1,.5))
        self.engine.drawText(self.font, self.comboTimer, position = (self.engine.w/2, self.engine.h/2 - 100))
