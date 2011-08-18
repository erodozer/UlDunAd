from sysobj import *

import math

#this is the hud that displays the character information
#it's not one big window, instead it is 1-3 little windows
#arranged to save space in an efficent manner when more or
#less characters are present in your party
class BattleHUDCharacter:
    def __init__(self, character, position = (0,0), scale = 1.0):
        self.character = character

        self.x, self.y = position
        
        scenepath = os.path.join("scenes", "battlesystem")
        
        self.setPosition(self.x, self.y)
    
        self.scale = scale
        
        self.drawing = ImgObj(Texture(os.path.join(scenepath, "circle.png")))
    
        self.back = ImgObj(os.path.join(scenepath, "hud.png"))
        self.face = self.character.sprites['face']
        self.font = FontObj("default.ttf", size = 24)
        
    def update(self):
        pass
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        
        s = self.scale
        
        self.back.setAlignment("left")
        self.back.setPosition(self.x-20, self.y)
        self.back.draw()
        
        self.face.setPosition(self.x+180, self.y)
        self.face.setScale(80, 80, inPixels = True)
        self.face.draw()
        
        self.font.setAlignment("left")
        
        self.font.setColor((1,1,1,1))
        self.font.setText(self.character.name)
        self.font.setPosition(self.x, self.y-24)
        self.font.draw()
        self.font.setColor((.65,.5,0,1.0))
        self.font.setText("HP")
        self.font.setPosition(self.x+5, self.y+10)
        self.font.draw()
        self.font.setText("/%4i" % self.character.hp)
        self.font.setPosition(self.x + 110, self.y+10)
        self.font.draw()
        if (self.character.currentHP < self.character.hp):
            self.font.setColor((1,1,1,1))
        self.font.setText(self.character.currentHP)
        self.font.setPosition(self.x+60, self.y+10)
        self.font.draw()
        
