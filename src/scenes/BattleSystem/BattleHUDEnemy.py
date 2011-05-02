from sysobj import *
        
#this is the hud that displays the enemy's basic information (hp, lvl)
class BattleHUDEnemy:
    def __init__(self, enemy):
        self.enemy = enemy

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
        self.hpBar[1].setLength(self.hpBar[0].width*(float(self.enemy.currentHP)/float(self.enemy.hp)))
        
        self.setPosition(0, 15)
       
    def update(self):
        self.hpBar[1].setLength(self.hpBar[0].width*(float(self.enemy.currentHP)/float(self.enemy.hp)))
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
        for bar in self.hpBar:
            bar.setPosition(x + 10, y - 5)

    def draw(self):

        for bar in self.hpBar:
            bar.draw()

        self.font.setText(self.enemy.name)
        self.font.setAlignment('left')
        self.font.scaleHeight(32.0)
        self.font.setPosition(self.x + 5, self.y + 15)
        self.font.draw()

