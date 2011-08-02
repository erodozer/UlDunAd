from View import *
from sysobj import *

from Config import Configuration
from Field import Field

class Dungeon(Scene):
    def __init__(self, engine):
        self.engine = engine
        
        name = self.engine.town
        path = os.path.join("..", "data", "places", name)
        self.dungeonini = Configuration(os.path.join(path, "dungeon.ini")).dungeon
        
        self.field = Field(path)
        
        self.background = ImgObj(os.path.join("places", name, "background.png"))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(.5,.5)
        
        self.font = FontObj("default.ttf", size = 32)
        self.bigFont = FontObj("default.ttf", size = 72)
        self.bigFont.setPosition(.8,.9)
        
    def render(self, visibility):
        self.background.draw()
        
        self.field.render()
        
        self.bigFont.setText("%iH" % self.field.grid[self.field.playerPos].height)
        self.bigFont.draw()
        
        self.font.setText(self.field.playerPos)
        self.font.draw()

    
