'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
from Enemy import Enemy

import Input

from MenuObj import MenuObj
 
class Menu(MenuObj):
    def __init__(self, scene):
        self.scene    = scene
        self.engine   = scene.engine    
        
        bestiary = self.scene.family.bestiary
        self.commands = []
        for i, beast in enumerate(bestiary.beasts):
            name = "%03i: " % (i+1)
            if beast[1] <= 0:
                name += "---------"
                beast[0] = None
            else:
                name += beast[0]
            self.commands.append([name, beast[1], beast[0]])

        scenepath = os.path.join("scenes", "menusystem", "bestiary")
        
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), self.engine.w*.5, self.engine.h-64.0)
        self.window.setPosition(self.engine.w*.5, self.engine.h*.5)
        
        self.button = WinObj(Texture(os.path.join(scenepath, "button.png")),self.engine.w*.5-20, 24.0)
        self.button.transitionTime = 0.0
        
        fontStyle = self.engine.data.defaultFont

        #which keys select the next or previous button
        self.moveKeys = [Input.RtButton, Input.LtButton]
        
        #the texture used for the buttons and the buttons themselves
        self.buttons  = [[FontObj(fontStyle, text = n[0], size = 24), 
                          FontObj(fontStyle, text = n[1], size = 24)] 
                          for n in self.commands]
            
        self.index = 0                  #which button is selected
        
    #renders the menu
    def render(self, visibility = 1.0):
        self.window.draw()
        
        position = self.engine.h-64.0
        for i, button in enumerate(self.buttons[max(0, self.index-4):min(len(self.buttons), self.index+4)]):
            button[0].setAlignment("left")
            button[0].setPosition(self.engine.w*.25 + 20, position)
            button[1].setAlignment("right")
            button[1].setPosition(self.engine.w*.75 - 20, position)
            
            if i == self.index:
                self.button.setPosition(self.engine.w*.5, position)
                self.button.draw()
            button[0].draw()
            button[1].draw()
            position += 48
            

class enemyStats:
    def __init__(self, scene, enemy):
        self.scene = scene
        self.engine = scene.engine
        
        scenepath = os.path.join("scenes", "menusystem", "bestiary")
        self.window = WinObj(Texture(os.path.join(scenepath, "window.png")), self.engine.w*.5, self.engine.h-64.0)
        self.window.setPosition(self.engine.w*.25, self.engine.h*.5)
        
        fontStyle = self.engine.data.defaultFont
        stats = ["HP", "Strength", "Defense", "Speed", "Evasion", "M Pow", "M Def"]
        self.name = FontObj(fontStyle, text = enemy.name, size = 24)
        self.name.setAlignment("left")
        self.name.setPosition(self.engine.w*.1, self.engine.h*.85)
        
        self.stats = [[FontObj(fontStyle, text = "%-10s" % stat, size = 24),
                      FontObj(fontStyle, text = "%2s" % enemy.stats[i], size = 24)]
                      for i, stat in enumerate(stats)]
        self.gold = FontObj(fontStyle, text = "%-10s%i" % ("Gold:", enemy.gold), size = 24)
        self.gold.setAlignment("left")
        self.gold.setPosition(self.engine.w*.15, self.engine.h*.85-48)
        
        self.exp = FontObj(fontStyle, text = "%-10s%i" % ("Exp:", enemy.exp), size = 24)
        self.exp.setAlignment("left")
        self.exp.setPosition(self.engine.w*.15, self.engine.h*.85-80)
        
        position = self.engine.h*.6
        for stat in self.stats:
            stat[0].setAlignment("left")
            stat[0].setPosition(self.engine.w*.1, position)
            stat[1].setPosition(self.engine.w*.25, position)
            position -= 32.0
        
        self.drop = [FontObj(fontStyle, text = enemy.drop, size = 24),
                     FontObj(fontStyle, text = enemy.dropChance, size = 24)]
        position = self.engine.h*.3
        self.drop[0].setAlignment("left")
        self.drop[0].setPosition(self.engine.w*.1, position)
        self.drop[1].setPosition(self.engine.w*.25, position-32.0)

        self.sprite = enemy.sprites['normal']
        self.sprite.setPosition(self.engine.w*.75, self.engine.h*.5)
        
    def keyPressed(self, key):
        if key == Input.BButton:
            return False
        return True
        
    def render(self, visibility = 1.0):
        self.window.draw()
        self.name.draw()
        self.gold.draw()
        self.exp.draw()
        for stat in self.stats:
            stat[0].draw()
            stat[1].draw()
        if self.drop[0].text:
            for drop in self.drop:
                drop.draw()
            
        self.engine.drawAnimation(self.sprite, loop = True, reverse = False, delay = 20)
        
class BestiaryScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.family = self.engine.family
        
        scenepath = os.path.join("scenes", "menusystem")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w,self.engine.h)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.font   = FontObj("default.ttf")

        self.menu   = Menu(self)

        self.enemyStats = None
        self.active = False         #whether or not the enemy stat display window is active
        
    def buttonClicked(self, image):
        pass
        
    def keyPressed(self, key, char): 
        if self.active:
            self.active = self.enemyStats.keyPressed(key)
        else:
            self.menu.keyPressed(key)
        
            #close the menu scene
            if key == Input.BButton:
                self.engine.viewport.changeScene("MenuSystem")

    def select(self, index):
        if self.menu.commands[index][1] is not None:
             self.enemyStats = enemyStats(self, Enemy(self.menu.commands[index][2]))  
             self.active = True  
        
    def run(self):
        pass

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        if self.active:
            self.enemyStats.render()
        else:
            self.menu.render()
        
