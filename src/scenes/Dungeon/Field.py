
from OpenGL.GL import *
from OpenGL.GLU import *

from Cell import Cell
    
from sysobj import *

import os

from operator import itemgetter

#grid for the dungeon
# this reads in the data file and creates a collection of cells and other values
class Field(object):
    def __init__(self, path):
        file = open(os.path.join("..", "data", path, "field.udaf"))
                                            #udaf standard for uldunad field files
        
        self.grid = {}                      #cells (8x8 grid)
        self.playerPos = None               #player's position in the map
        self.bossPos = None                 #boss's position in the map
        self.dimensions = None
        self.highestPoint = 0
        self.displayList = None
        self.rotY = 35
        self.angle = 45
        self.selected = None
        
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
            
        for y, line in enumerate(file.readlines()):
            #first line reads in the dimensions of the grid
            if y == 0:
                self.dimensions = [int(i) for i in line.split("x")]
            #skip one line, then the next y amount of lines is the grid
            elif y > 1 and y < self.dimensions[1]+2:
                for x in range(self.dimensions[0]):
                    h = getHeight(line[x])
                    if h > 0:
                        self.grid[(x+1,y-1)] = Cell(path, h)
            #2 lines after the grid is the player's position
            elif y == self.dimensions[1] + 3:
                self.playerPos = tuple([int(i) for i in line.split(",")])
            #3 lines after the grid is the boss's position
            elif y == self.dimensions[1] + 4:
                self.bossPos = tuple([int(i) for i in line.split(",")])
        self.grid[self.playerPos].show()
        self.grid[self.bossPos].show()
        
        #player icon
        self.angel = ImgObj(os.path.join("scenes", "dungeon", "angel.png"))
                
        #boss icon
        self.devil = ImgObj(os.path.join("scenes", "dungeon", "devil.png"))
        
        self.updateList()
            
    def deselect(self):
        self.selected = None
        
    def setSelected(self, position):
        if self.selected is not tuple(position):
          self.selected = tuple(position)
          self.updateList()
  
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
        glTranslatef(-64.0*self.dimensions[0]/2.0, 0, -64.0*(self.dimensions[1]))
        
        #renders the generated opengl grid
        glPushMatrix()
        glCallList(self.displayList)
        glPopMatrix()
        
        #renders the player's position
        glPushMatrix()
        cell = self.playerPos
        glTranslatef(64.0*cell[0]+32.0, 16.0*self.grid[cell].height+32.0,64.0*cell[1]+32.0)
        glScalef(.25,.25,0)
        self.angel.draw()
        glPopMatrix()
        
        #renders the boss's position
        glPushMatrix()
        cell = self.bossPos
        #glScalef(32.0,32.0,0)
        glTranslatef(64.0*cell[0]+32.0, 16.0*self.grid[cell].height+32.0,64.0*cell[1]+32.0)
        glScalef(.25,.25,0)
        self.devil.draw()
        glPopMatrix()
        
        glPopMatrix()
        
