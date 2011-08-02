from View import *
from sysobj import *

from Config import Configuration
from Field import Field

class Dungeon(Scene):
    def __init__(self, engine):
        self.engine = engine
        
        name = self.engine.town
        path = os.path.join("places", name)
        self.dungeonini = Configuration(os.path.join("..", "data", path, "dungeon.ini")).dungeon
        
        self.field = Field(path)
        
        w,h = self.engine.w, self.engine.h
        
        self.background = ImgObj(os.path.join(path, "background.png"))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(w/2,h/2)
        
        self.font = FontObj("default.ttf", size = 32)
        self.font.setPosition(w*.5,h*.1)
        
        self.bigFont = FontObj("default.ttf", size = 72)
        self.bigFont.setPosition(w*.8,h*.9)
        
    def render3D(self):
        self.field.render()
    def render(self, visibility):
        self.background.draw()
        
        #self.field.render()
        
        self.bigFont.setText("%iH" % self.field.grid[self.field.playerPos].height)
        self.bigFont.draw()
        
        self.font.setText(self.field.playerPos)
        self.font.draw()

    
