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
        
        self.combo = self.character.command
        self.end = False
        
        #images used for displaying the input combo 
        self.inputButtons = [ImgObj(Texture("inputButtons.png"), frameY = 5) for i in self.combo.keys]
        for i, button in enumerate(self.inputButtons):
            frame, angle = self.getButtonImage(self.addition[i])
            button.setFrame(y = frame)
            button.setAngle(angle)
            button.setScale(96,96, inPixels = True)

    def keyPressed(self, key):
        if self.combo.runKey(key):
            self.end = True
            
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
        if self.combo.runTimer(self.engine.clock.get_time()):
           self.end = True
                
    def draw(self):
        y = self.engine.h/2
        for i in range(len(self.combo.keys)):
            x = self.engine.w/2 - (self.inputButtons[0].width + 10.0) * (i - self.combo.keyIndex)
            if i == self.combo.keyIndex:
                col = (1,1,1,1)
            else:
                col = (1,1,1,.5)
            
            self.engine.drawImage(self.inputButtons[i], position = (x, y), color = col)
        
        self.engine.drawText(self.font, "%3d" % self.comboTimer, position = (self.engine.w/2, self.engine.h/2 - 100))
