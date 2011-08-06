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
        
        name = self.engine.dungeon                    #name of the dungeon
        path = os.path.join("places", name)           #path to the dungeon
        
        self.dungeonini = Configuration(os.path.join("..", "data", path, "dungeon.ini")).dungeon
                                                      #config file
        
        self.field = Field(path)                      #the field data (grid)
        
        w,h = self.engine.w, self.engine.h        
        
        #background image
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
        
        self.selectedPos = self.field.playerPos       #selected position for movement
        self.distance = 0
        
        #camera controls
        self.position = [w/2,h/2]
        self.panX = w/2
        self.panY = h/2
        self.cameraMotion = False
        self.angle = 135.0
        if self.field.playerPos[0] > self.field.dimensions[0]/2:
            if self.field.playerPos[1] > self.field.dimensions[1]/2:
                self.angle = 225.0
            else:
                self.angle = 135.0
        else:
            if self.field.playerPos[1] > self.field.dimensions[1]/2:
                self.angle = 45.0
            else:
                self.angle = 315.0
          
        
        self.mode = 0                                 #0 = view, 1 = action menu, 2 = move
        
        self.actionMenu = MenuObj(self, ["Move", "Menu", "Escape"], (w*.8, h*.25), window = "window.png")
        
        self.moveKeys = {}                            #keys used for tile selection
        self.updateKeys()
        
        
    #makes sure to flip input keys for selecting a tile when the map is rotated
    # so it makes sense
    # down is towards the camera, up is away
    def updateKeys(self):
        if self.angle == 45.0 or self.angle == 305.0:
            self.moveKeys[Input.DnButton] = [(self.selectedPos[0], self.selectedPos[1] + 1), 1]
            self.moveKeys[Input.UpButton] = [(self.selectedPos[0], self.selectedPos[1] - 1),-1]
        else:
            self.moveKeys[Input.UpButton] = [(self.selectedPos[0], self.selectedPos[1] + 1), 1]
            self.moveKeys[Input.DnButton] = [(self.selectedPos[0], self.selectedPos[1] - 1),-1]
        
        if self.angle == 45.0 or self.angle == 215.0:
            self.moveKeys[Input.RtButton] = [(self.selectedPos[0] + 1, self.selectedPos[1]), 1]
            self.moveKeys[Input.LtButton] = [(self.selectedPos[0] - 1, self.selectedPos[1]),-1]
        else:
            self.moveKeys[Input.LtButton] = [(self.selectedPos[0] + 1, self.selectedPos[1]), 1]
            self.moveKeys[Input.RtButton] = [(self.selectedPos[0] - 1, self.selectedPos[1]),-1]
          
        
    def keyPressed(self, key, char):
      
        #view mode
        #  allows panning and rotating of the map
        if self.mode == 0:
            if key == Input.CButton:
                self.angle += 90.0
                self.updateKeys()
            
            if key == Input.DButton:
                self.angle -= 90.0
                self.updateKeys()
            
            if key == Input.RtButton:
                self.panX += _panRate
            if key == Input.LtButton:
                self.panX -= _panRate
            if key == Input.UpButton:
                self.panY += _panRate
            if key == Input.DnButton:
                self.panY -= _panRate
            
            
            #open action menu
            if key == Input.AButton:
                self.mode = 1
                
            #resets pan position to center
            if key == Input.BButton:
                self.panX = w/2
                self.panY = h/2
                                
        #selecting action
        elif self.mode == 1:
            self.actionMenu.keyPressed(key)
            
            if key == Input.BButton:
                self.mode = 0
                
        #selecting tile to move to
        elif self.mode == 2:
            if key in self.moveKeys.keys():
                try:
                    heightdiff = self.field.grid[self.moveKeys[key][0]].height - self.field.grid[self.field.playerPos].height
                    newDistance = self.distance + self.moveKeys[key][1]
                    if not (abs(heightdiff) > 1 or abs(newDistance) > 1):
                        self.selectedPos = self.moveKeys[key][0]
                        self.distance = newDistance
                except:
                    return
                
            self.field.setSelected(self.selectedPos)
            self.field.updateList()
            self.updateKeys()
                               
            #move player to selected position
            if key == Input.AButton:
                self.distance = 0
                self.field.playerPos = self.selectedPos
                self.field.grid[self.field.playerPos].show()
                self.field.deselect()
                self.field.updateList()
                self.mode = 0
                
            #cancel movement
            if key == Input.BButton:
                self.selectedPos = self.field.playerPos
                self.field.deselect()
                self.field.updateList()
                self.mode = 1

    #menu input
    def select(self, index):
        if index == 0:
            self.mode = 2
            self.field.setSelected(self.selectedPos)
            self.field.updateList()
            
        #leave dungeon
        elif index == 2:
            self.engine.dungeon = None
            self.engine.viewport.changeScene("Maplist")
            
    def panTo(self, newPosition):
        #maker sure new position is a list, not tuple
        newPosition = list(newPosition)
        
        #force to new position when selecting tiles
        if self.mode == 2:
            self.position = newPosition
            
        self.cameraMotion = False
        if self.position[0] is not newPosition[0]:
            if abs(newPosition[0] - self.position[0]) > .5:
              self.position[0] += (newPosition[0]-self.position[0])*.05
            else:
              self.position[0] = newPosition[0]
            self.cameraMotion = True
        if self.position[1] is not newPosition[1]:
            if abs(newPosition[1] - self.position[1]) > .5:
                self.position[1] += (newPosition[1]-self.position[1])*.05
            else:
                self.position[1] = newPosition[1]
            self.cameraMotion = True
        
    def render(self, visibility):
        w,h = self.engine.w, self.engine.h        
        
        self.panTo((self.panX, self.panY))
        if not self.mode == 0:
            self.panX = w/2
            self.panY = h/2
        if self.mode == 2:
            self.field.setCenter(self.selectedPos)
        else:
            self.field.setCenter()
                
        glPushMatrix()
        glTranslatef(1,1,-1000)
        self.background.draw()
        glPopMatrix()
                
        glPushMatrix()
        glTranslatef(self.position[0],self.position[1],-32.0*(max(self.field.dimensions[0],self.field.dimensions[1])+max(self.field.playerPos[0], self.field.playerPos[1])))
        if not self.field.rotateTo(self.angle):
            if self.angle > 360:
                self.angle %= 360
                self.field.angle = self.angle
            if self.angle < 0:
                self.angle += 360
                self.field.angle = self.angle
        else:
            self.cameraMotion = True
        self.field.render()
        glPopMatrix()
        
        self.bigFont.setText("%iH" % self.field.grid[self.selectedPos].height)
        self.bigFont.draw()
        
        '''Debug Position
        if self.mode == 2:
            location = "%s > %s" % (str(self.field.playerPos), str(self.selectedPos))
        else:
            location = "%s" % str(self.field.playerPos)
        self.font.setText(location)
        self.font.draw()
        '''
        
        self.compassbase.draw()
        self.compass.setAngle(self.field.angle)
        self.compass.draw()
        
        if self.mode == 1:
            self.actionMenu.render()

