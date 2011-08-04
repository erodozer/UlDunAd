from View import *
from sysobj import *
from Input import *
from MenuObj import MenuObj

from Config import Configuration
from Field import Field

from math import *

_panRate = 25
        
class Dungeon(Scene):
    def __init__(self, engine):
        self.engine = engine
        
        name = self.engine.dungeon
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
        
        self.angle = 135.0
        
        self.mode = 0     #0 = view, 1 = action menu, 2 = move
        
        self.actionMenu = MenuObj(self, ["Move", "Menu", "Escape"], (w*.8, h*.25), window = "window.png")
        
        self.moveKeys = {}
        
        self.selectedPos = list(self.field.playerPos)    #selected position for movement
        self.position = [w/2,h/2]
        self.panX = w/2
        self.panY = h/2
        self.cameraMotion = False
        
    #makes sure to flip input keys for selecting a tile when the map is rotated
    # so it makes sense
    # down is towards the camera, up is away
    def updateKeys(self):
        if self.angle == 45.0 or self.angle == 305.0:
            self.moveKeys[Input.UpButton] = lambda: self.selectedPos[1] = min(self.selectedPos[1] + 1, self.field.playerPos[1]+1)
            self.moveKeys[Input.DnButton] = lambda: self.selectedPos[1] = max(self.selectedPos[1] - 1, self.field.playerPos[1]-1)
        else:
            self.moveKeys[Input.DnButton] = lambda: self.selectedPos[1] = min(self.selectedPos[1] + 1, self.field.playerPos[1]+1)
            self.moveKeys[Input.UpButton] = lambda: self.selectedPos[1] = max(self.selectedPos[1] - 1, self.field.playerPos[1]-1)
        
        if self.angle == 45.0 or self.angle == 215.0:
            self.moveKeys[Input.RtButton] = lambda: self.selectedPos[0] = min(self.selectedPos[0] + 1, self.field.playerPos[0]+1)
            self.moveKeys[Input.LtButton] = lambda: self.selectedPos[0] = max(self.selectedPos[0] - 1, self.field.playerPos[0]-1)
        else:
            self.moveKeys[Input.LtButton] = lambda: self.selectedPos[0] = min(self.selectedPos[0] + 1, self.field.playerPos[0]+1)
            self.moveKeys[Input.RtButton] = lambda: self.selectedPos[0] = max(self.selectedPos[0] - 1, self.field.playerPos[0]-1)
          
        
    def keyPressed(self, key, char):
        #don't allow input while the map is being transformed
        if self.cameraMotion:
            return
      
        #view mode
        #  allows panning and rotating of the map
        if self.mode == 0:
            if key == Input.CButton:
                self.angle += 90.0
        
            if key == Input.DButton:
                self.angle -= 90.0
            
            if key in self.moveKeys:
                self.pan
            if key == Input.RtButton:
                self.panX += _panRate
            if key == Input.LtButton:
                self.panX -= _panRate
            if key == Input.UpButton:
                self.panY += _panRate
            if key == Input.DnButton:
                self.panY -= _panRate
            
            self.updateKeys()
                
            #open action menu
            if key == Input.AButton:
                self.mode = 1
                
            #leave dungeon
            if key == Input.BButton:
                self.engine.town = None
                self.engine.viewport.changeScene("Maplist")
                
        #selecting action
        elif self.mode == 1:
            self.actionMenu.keyPressed(key)
            
        #selecting tile to move to
        elif self.mode == 2:
            oldpos = self.selectedPos[:]
                
            if key in self.moveKeys.keys():
                self.moveKeys[key]()
            
            #try to detect if the tile exists by checking its properties
            #  if it doesn't reset the selected position to the previously selected one
            try:
                cell = self.field.grid[tuple(self.selectedPos)].height
            except:
                self.selectedPos = oldpos
                return
                
            if cell.height - self.field.grid[self.field.playerPos].height > 1:
                self.selectedPos = oldpos
                return
                
            self.field.setSelected(self.selectedPos)
            self.field.updateList()
                               
            #move player to selected position
            if key == Input.AButton:
                self.field.playerPos = tuple(self.selectedPos)
                self.field.grid[self.field.playerPos].show()
                self.field.deselect()
                self.field.updateList()
                self.mode = 0
                
            #cancel movement
            if key == Input.BButton:
                self.selectedPos = list(self.field.playerPos)
                self.field.deselect()
                self.mode = 1

            
    def select(self, index):
        if index == 0:
            self.mode = 2
        elif index == 1:
            self.engine.viewport.addScene("MenuSystem")
    
    def panTo(self, newPosition):
        self.cameraMotion = False
        if self.position[0] is not newPosition[1]:
            self.position[0] -= (self.position[0]-newPosition[0])*.05
            self.cameraMotion = True
        if self.position[1] is not newPosition[1]:
            self.position[1] -= (self.position[1]-newPosition[1])*.05
            self.cameraMotion = True
        
    def render(self, visibility):
        w,h = self.engine.w, self.engine.h        
        
        self.panTo((self.panX, self.panY))
        
        glPushMatrix()
        glTranslatef(1,1,-1000)
        self.background.draw()
        glPopMatrix()
                
        glPushMatrix()
        glTranslatef(self.position[0],self.position[1],100)
        glScalef(1,1,1)
        if not self.field.rotateTo(self.angle):
            self.cameraMotion = True
            if self.angle > 360:
                self.angle %= 360
                self.field.angle = self.angle
            if self.angle < 0:
                self.angle += 360
                self.field.angle = self.angle
        self.field.render()
        glPopMatrix()
        
        self.bigFont.setText("%iH" % self.field.grid[self.field.playerPos].height)
        self.bigFont.draw()
        
        if self.mode == 2:
            location = "%s > %s" % (str(self.field.playerPos), str(tuple(self.selectedPos)))
        else:
            location = "%s" % str(self.field.playerPos)
        self.font.setText(location)
        self.font.draw()

        self.compassbase.draw()
        self.compass.setAngle(self.field.angle)
        self.compass.draw()
        
        if self.mode == 1:
            self.actionMenu.render()

