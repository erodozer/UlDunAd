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
        
        #displays coordinates of the player
        self.font = FontObj("default.ttf", size = 32)
        self.font.setPosition(w*.5,h*.1)
        
        #displays player height
        self.bigFont = FontObj("default.ttf", size = 72)
        self.bigFont.setPosition(w*.8,h*.9)
        
        self.angles = [45.0, 135.0, 225.0, 315.0]
        self.selectedAngle = 0
        
    def keyPressed(self, key, char):
        if key == Input.RtButton:
            self.selectedAngle += 1
            if self.selectedAngle >= len(self.angles):
               self.selectedAngle = 0
        
        
        if key == Input.LtButton:
            self.selectedAngle -= 1
            if self.selectedAngle < 0:
               self.selectedAngle = len(self.angles)-1
          
    def render(self, visibility):
        w,h = self.engine.w, self.engine.h        
        
        self.background.draw()
        
        glPushMatrix()
        glTranslatef(w/2,h/2,-.1)
        glScalef(1,1,1)
        self.field.rotateTo(self.angles[self.selectedAngle])
        self.field.render()
        glPopMatrix()
        
        self.bigFont.setText("%iH" % self.field.grid[self.field.playerPos].height)
        self.bigFont.draw()
        
        self.font.setText(self.field.playerPos)
        self.font.draw()

    
