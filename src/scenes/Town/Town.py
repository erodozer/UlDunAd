'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from View   import *
from Config import Configuration

from sysobj import *
from MenuObj import MenuObj

from Enemy import Formation

import random

class Town(Scene):
    def __init__(self, engine):

        self.engine = engine
        self.townname = self.engine.town

        townpath = os.path.join("places", self.townname)
        self.townini = Configuration(os.path.join("..", "data", townpath, "town.ini")).town

        self.background = ImgObj(Texture(os.path.join(townpath, "background.png")))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.font = FontObj("default.ttf", size = 32.0)
        self.audio = BGMObj(os.path.join(townpath, "bgm.mp3"))

        self.choices = [choice.strip() for choice in self.townini.choices.split(",")]
        self.choices.append("Return")

        self.menu = MenuObj(self, self.choices, buttonStyle = Texture(os.path.join(townpath, "button.png")),
                            position = (100, 500))

        self.enemies = [formation.strip() for formation in self.townini.enemylist.split(",")]

    def buttonClicked(self, image):
        self.menu.buttonClicked(image)
        
    def keyPressed(self, key, char):
        self.menu.keyPressed(key)
        
        #leave town
        if key == Input.BButton:
            self.engine.town = None
            self.engine.viewport.changeScene("Maplist")
                
    def select(self, index):
        if self.choices[index] == "Wilderness":
            self.engine.formation = Formation(random.choice(self.enemies))
            self.engine.viewport.changeScene("BattleSystem")
        if index == len(self.choices)-1:
            self.engine.town = None
            self.engine.viewport.changeScene("Maplist")
        #else:
        #    self.engine.subTown = self.choices[index]
        #    self.engine.viewport.changeScene("Shop")
            
    def render(self, visibility):
        self.background.draw()
        
        self.menu.render()
   
        self.engine.drawText(self.font, self.townname, (430, 64))
