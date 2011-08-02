
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
        file = open(os.path.join(path, "field.udaf"))
                                            #udaf standard for uldunad field files
        
        self.grid = {}                      #cells (8x8 grid)
        self.playerPos = None               #player's position in the map
        self.bossPos = None                 #boss's position in the map
        self.dimensions = None
        for y, line in enumerate(file.readlines()):
            #first line reads in the dimensions of the grid
            if y == 0:
                self.dimensions = [int(i) for i in line.split("x")]
            #skip one line, then the next y amount of lines is the grid
            elif y > 1 and y < self.dimensions[1]+2:
                for x in range(self.dimensions[0]):
                    self.grid[(x+1,y-1)] = Cell(path, line[x])
            #2 lines after the grid is the player's position
            elif y == self.dimensions[1] + 3:
                self.playerPos = tuple([int(i) for i in line.split(",")])
            #3 lines after the grid is the boss's position
            elif y == self.dimensions[1] + 4:
                self.bossPos = tuple([int(i) for i in line.split(",")])
             
        print self.grid
        
        #player icon
        self.angel = ImgObj(os.path.join("scenes", "dungeon", "angel.png"))
        self.angel.setPosition(.5,.5)       #always in the center of the screen
                
        #boss icon
        self.devil = ImgObj(os.path.join("scenes", "dungeon", "devil.png"))
        self.devil.setPosition(64.0*self.bossPos[0],16.0*self.bossPos[1])       
                                            #depends on cell location
        
    def render(self):
        
        glPushMatrix()
        glTranslatef(64.0*self.playerPos[0], 16.0*self.grid[self.playerPos].height, 64.0*self.playerPos[1])
        for cell in self.grid.keys():
            glPushMatrix()
            glTranslatef(64.0*cell[0],0,64.0*cell[1])
            self.grid[cell].draw()
            glPopMatrix()
        self.devil.draw()
        glPopMatrix()
        self.angel.draw()
