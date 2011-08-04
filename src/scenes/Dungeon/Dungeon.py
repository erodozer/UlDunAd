from View import *
from sysobj import *
from Input import *

from Config import Configuration
from Field import Field

class Dungeon(Scene):
    def __init__(self, engine):
        self.engine = engine
        
        name = self.engine.town
        path = os.path.join("places", name)
        
        self.dungeonini = Configuration(os.path.join("..", "data", path, "dungeon.ini")).dungeon
                                                    #config file
        
        self.field = Field(path)                    #the field data (grid)
        
        w,h = self.engine.w, self.engine.h        
        
        self.background = ImgObj(os.path.join(path, "background.png"))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(w/2,h/2)
        
        #displays the current map direction
        self.compassbase = ImgObj(os.path.join("scenes", "dungeon", "compassbase.png"))
        self.compassbase.setPosition(w*.1, h*.1)
        self.compassbase.setScale(256, 256, True)
        self.compass = ImgObj(os.path.join("scenes", "dungeon", "compass.png"))
        self.compass.setPosition(w*.1, h*.1)
        self.compass.setScale(256, 256, True)
        
        #displays coordinates of the player
        self.font = FontObj("default.ttf", size = 32)
        self.font.setPosition(w*.5,h*.1)
        
        #displays player height
        self.bigFont = FontObj("default.ttf", size = 72)
        self.bigFont.setPosition(w*.8,h*.9)
        
        self.angle = 45.0
        
    def keyPressed(self, key, char):
        if key == Input.RtButton:
            self.angle += 90.0
        
        
        if key == Input.LtButton:
            self.angle -= 90.0
          
        #leave dungeon
        if key == Input.BButton:
            self.engine.town = None
            self.engine.viewport.changeScene("Maplist")
            
    def render(self, visibility):
        w,h = self.engine.w, self.engine.h        
        
        self.background.draw()
                
        self.bigFont.setText("%iH" % self.field.grid[self.field.playerPos].height)
        self.bigFont.draw()
        
        self.font.setText(self.field.playerPos)
        self.font.draw()

        self.compassbase.draw()
        self.compass.setAngle(self.field.angle)
        self.compass.draw()
        
        self.engine.viewport.setOrthoProjection()
        glTranslatef(w/2,h/2,1)
        glScalef(1,1,1)
        if not self.field.rotateTo(self.angle):
            if self.angle > 360:
                self.angle %= 360
                self.field.angle = self.angle
            if self.angle < 0:
                self.angle += 360
                self.field.angle = self.angle
        self.field.render()
        self.engine.viewport.resetProjection()
