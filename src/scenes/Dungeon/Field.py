
from OpenGL.GL import *
from OpenGL.GLU import *

from Cell import Cell
    
from sysobj import *

import os

from operator import itemgetter

_encounterMin = .5    #percentage of cells that must be encounters

#grid for the dungeon
# this reads in the data file and creates a collection of cells and other values
class Field(object):
    def __init__(self, scene, path):
        file = open(os.path.join("..", "data", path, "field.udaf"))
                                            #udaf standard for uldunad field files
        
        self.grid = {}                      #the grid of cells
        self.displayList = None             #the grid saved as an opengl list
        self.playerPos = None               #player's position in the map
        self.bossPos = None                 #boss's position in the map
        self.dimensions = None              #grid's dimensions
        self.selected = None                #the currently selected cell
        self.highestPoint = 0               #the highest point on the map
        self.rotY = 35                      #the rotate angle along the x axis
        self.angle = 45                     #the angle at which the user is viewing it along its y axis
        self.center = (0,0)                 #the map's center point


        #player icon
        self.angel = ImgObj(os.path.join("scenes", "dungeon", "angel.png"))
                
        #boss icon
        self.devil = ImgObj(os.path.join("scenes", "dungeon", "devil.png"))
        
                
        #gets the height value from the character passed
        #height ranges from 0-9 then a-f (lowercase)
        def getHeight(h):
            try:
                h = int(h)
            except:
                h = ord(h) - 87
            if h > self.highestPoint:
               self.highestPoint = h
            return h
            
        #reads the field file
        for y, line in enumerate(file.readlines()):
            #first line reads in the dimensions of the grid
            if y == 0:
                self.dimensions = [int(i) for i in line.split("x")]
            #skip one line, then the next y amount of lines is the grid
            elif y > 1 and y < self.dimensions[1]+2:
                for x in range(self.dimensions[0]):
                    h = getHeight(line[x])
                    if h > 0:
                        self.grid[(x+1,y-1)] = Cell(scene.engine, path, h)
            #2 lines after the grid is the player's position
            elif y == self.dimensions[1] + 3:
                self.playerPos = tuple([int(i) for i in line.split(",")])
            #3 lines after the grid is the boss's position
            elif y == self.dimensions[1] + 4:
                self.bossPos = tuple([int(i) for i in line.split(",")])
        self.grid[self.playerPos].show()      #make sure the player's cell is not hidden
        self.grid[self.bossPos].show()        #make sure the boss's cell is not hidden
              
        requiredEncounter = len(self) * _encounterMin
        encounterCells = 0
        
        cellsNeedingEvents = self.grid.keys()[:]
        cellsNeedingEvents.remove(self.playerPos)
        cellsNeedingEvents.remove(self.bossPos)
        while len(cellsNeedingEvents) > 0:
            cell = random.choice(cellsNeedingEvents)
            #place encounters first
            if encounterCells < requiredEncounter:
                self.grid[cell].setEvent("Formation:" + random.choice(scene.formations))
            #then other random events
            else:
                #greater chance to get in an encounter than to find an item/gold
                if random.randint(0, 50) < 35 or len(scene.otherevents) == 0:
                    self.grid[cell].setEvent("Formation:" + random.choice(scene.formations))
                else:
                    self.grid[cell].setEvent(random.choice(scene.otherevents))
            cellsNeedingEvents.remove(cell)
            print cellsNeedingEvents
                
        self.setCenter()
        self.updateList()
        
    #sets which cell is the center of the map focus
    def setCenter(self, cell = None):
        if cell:
            self.center = cell
        else:
            self.center = self.playerPos
        
    ###For movement selection
    #deselects all tiles
    def deselect(self):
        self.selected = None
        
    #highlights the currently selected tile
    def setSelected(self, position):
        if self.selected is not tuple(position):
            self.selected = tuple(position)
            self.updateList()
  
    #smoothly rotates the map to a new angle along its y-axis
    def rotateTo(self, newangle):
        if self.angle is not newangle:
            if abs(newangle - self.angle) > .5:
                self.angle += (newangle-self.angle)*.05
            else:
                self.angle = newangle
            return True
        return False
        
    #generates a glList of all the cubes so it only has to recall the list whenever it has to render
    def updateList(self):
        self.displayList = glGenLists(1)                
        glNewList(self.displayList, GL_COMPILE)
        for cell in self.grid.keys():
            if self.selected:
                if self.selected[0] == cell[0] and self.selected[1] == cell[1]:
                    self.grid[cell].selected = True
                else:
                    self.grid[cell].selected = False
            else:
                self.grid[cell].selected = False
            glPushMatrix()
            glTranslatef(64.0*cell[0],0,64.0*cell[1])
            self.grid[cell].draw()
            glPopMatrix()
        glEndList()        
        
    def render(self):
        
        glPushMatrix()
        
        #angles the grid
        glRotatef(self.rotY,1,0,0)
        glRotatef(-self.angle,0,1,0)
        #centers the grid
        glTranslatef(-64.0*self.center[0], 0, -64.0*self.center[1])
        
        #renders the generated opengl grid
        glPushMatrix()
        glCallList(self.displayList)
        glPopMatrix()
        
        #renders the player's position
        glPushMatrix()
        cell = self.playerPos
        glTranslatef(64.0*cell[0]+32.0-16.0*(self.playerPos==self.bossPos), 16.0*self.grid[cell].height+32.0,64.0*cell[1]+32.0-16.0*(self.playerPos==self.bossPos))
        glScalef(.25,.25,0)
        self.angel.draw()
        glPopMatrix()
        
        #renders the boss's position
        glPushMatrix()
        cell = self.bossPos
        #glScalef(32.0,32.0,0)
        glTranslatef(64.0*cell[0]+32.0+16.0*(self.playerPos==self.bossPos), 16.0*self.grid[cell].height+32.0,64.0*cell[1]+32.0+16.0*(self.playerPos==self.bossPos))
        glScalef(.25,.25,0)
        self.devil.draw()
        glPopMatrix()
        
        glPopMatrix()
        
    def __len__(self):
        return len(self.grid.keys())-1
