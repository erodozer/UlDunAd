from sysobj import *

#this is the hud that displays the hp and name of the active actor and its target
class BattleHUDEngage:
    def __init__(self, actor):
        self.actor = actor

        scenepath = os.path.join("scenes", "battlesystem")
        
        #font used in the hud for displaying HP by number and name of the character
        self.font   = FontObj("default.ttf")
        self.font.setAlignment("left")

        #these are for drawing the HP and FP bars
        #each bar consists of 3 textures
        self.hpBar = [ImgObj(Texture(os.path.join(scenepath, "bottom_bar.png"))),
                      BarObj(Texture(os.path.join(scenepath, "hp_bar.png"))), 
                      ImgObj(Texture(os.path.join(scenepath, "top_bar.png")))]
        self.hpBar[0].setAlignment("left")
        self.hpBar[2].setAlignment("left")
        
        self.setPosition(0, 15)
       
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
        for bar in self.hpBar:
            bar.setPosition(x + 10, y - 5)

    def draw(self):

        self.hpBar[1].setLength(self.hpBar[0].width*(float(self.actor.currentHP)/float(self.actor.hp)))
        for bar in self.hpBar:
            bar.draw()

        self.font.setText(self.actor.name)
        self.font.setAlignment('left')
        self.font.scaleHeight(32.0)
        self.font.setPosition(self.x + 5, self.y + 15)
        self.font.draw()        

        self.setPosition(self.x + 300, self.y)
        
        self.hpBar[1].setLength(self.hpBar[0].width*(float(self.actor.target.currentHP)/float(self.actor.target.hp)))
        for bar in self.hpBar:
            bar.draw()

        self.font.setText(self.actor.target.name)
        self.font.setAlignment('left')
        self.font.scaleHeight(32.0)
        self.font.setPosition(self.x + 5, self.y + 15)
        self.font.draw()        
