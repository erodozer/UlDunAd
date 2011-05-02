from sysobj import *
from OpenGL.GL import glPushMatrix, glPopMatrix, glScalef

#this is the hud that displays the character information
#it's not one big window, instead it is 1-3 little windows
#arranged to save space in an efficent manner when more or
#less characters are present in your party
class BattleHUDCharacter:
    def __init__(self, character, position = (0,0), scale = 1.0):
        self.character = character

        self.x, self.y = position
        
        scenepath = os.path.join("scenes", "battlesystem")

        #font used in the hud for displaying HP by number and name of the character
        self.font   = FontObj("default.ttf")
        self.font.setAlignment("left")

        #these are for drawing the HP and FP bars
        #each bar consists of 3 textures
        self.hpBar = [ImgObj(Texture(os.path.join(scenepath, "bottom_bar.png"))),
                      BarObj(Texture(os.path.join(scenepath, "hp_bar.png"))), 
                      ImgObj(Texture(os.path.join(scenepath, "top_bar.png")))]
        self.fpBar = [ImgObj(Texture(os.path.join(scenepath, "bottom_bar.png"))),
                      BarObj(Texture(os.path.join(scenepath, "fp_bar.png"))), 
                      ImgObj(Texture(os.path.join(scenepath, "top_bar.png")))]

        self.hpBar[0].setAlignment("left")
        self.hpBar[2].setAlignment("left")
        self.fpBar[0].setAlignment("left")
        self.fpBar[2].setAlignment("left")
        
        self.setPosition(self.x, self.y)
    
        self.scale = scale
        
    def update(self):
        self.hpBar[1].setLength(self.hpBar[0].width*(float(self.character.currentHP)/float(self.character.hp)))
        self.fpBar[1].setLength(self.fpBar[0].width*(float(self.character.fp)/float(self.character.maxFP)))
       
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
        for bar in self.hpBar:
            bar.setPosition(100 + x, y - 5)

        for bar in self.fpBar:
            bar.setPosition(100 + x, y - 25)
        
    def draw(self):
        
        glPushMatrix()
        glScalef(self.scale, self.scale, 1)
        #self.hudImg.draw()

        for bar in self.hpBar:
            bar.draw()

        for bar in self.fpBar:
            bar.draw()
        
        self.font.setText(self.character.name)
        self.font.setAlignment('left')
        self.font.scaleHeight(32.0)
        self.font.setPosition(self.x + 5, self.y)
        self.font.draw()

        self.font.setText(str(self.character.currentHP) + "/" + str(self.character.hp))
        self.font.setAlignment('right')        
        self.font.scaleHeight(24.0)
        self.font.setPosition(self.x + self.hpBar[0].width-20, self.y + 15)
        self.font.draw()
        
        glPopMatrix()
