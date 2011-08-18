
from OpenGL.GL import *
from OpenGL.GLU import *

from sysobj import *
import os
    
from Enemy import Formation
            
class Cell(object):
    def __init__(self, engine, path, height):
        self.engine = engine
        
        self.height = height         #height of the cell
        self.hidden = True           #whether or not the player has uncovered it
        self.selected = False        #selected for move space
        
        self.base = Texture(os.path.join(path, "base.png"))
        self.side = Texture(os.path.join(path, "side.png"))
        self.event = None
        
        self.displayList = glGenLists(1)                
        glNewList(self.displayList, GL_COMPILE)
        self.genCube()
        glEndList()  
        
    #events are set post field generation
    def setEvent(self, event):
        self.event = event
        
    def execute(self):
        head = self.event.split(":")[0]
        tail = self.event.split(":")[1]
        if head == "Formation":
            self.engine.formation = Formation(tail)
            self.engine.viewport.pushScene("BattleSystem")
        elif head == "Gold":
            self.engine.family.gold += int(tail)
        elif head == "Item":
            self.engine.family.inventory.addItem(tail.split(",")[0], tail.split(",")[1])
            
    def genCube(self):
        glPushMatrix()
        glScale(64.0,16.0*self.height,64.0)
        self.side.bind(repeat=True)
        glBegin(GL_QUADS)
        #Front Face
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 0.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, 0.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0,  1.0)
        #Back Face
        glTexCoord2f(1.0, 0.0); glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, 0.0, 0.0)
        #Right face
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, 0.0,  1.0)
        #Left Face
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(0.0, 0.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(0.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glEnd()
        
        self.base.bind()
        #Top Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(0.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, 0.0)
        glEnd()
        glPopMatrix()

    def show(self):
        if self.hidden and self.event:
            self.execute()
        self.hidden = False
        
        
    def hide(self):
        self.hidden = True
    
    def draw(self):
        
        glPushMatrix()
        if self.selected:
            glColor4f(1.0,0.0,0.0,1.0)
        elif self.hidden:
            glColor4f(.3,.3,.3,1.0)
        else:
            glColor4f(1.0,1.0,1.0,1.0)
        glCallList(self.displayList)
        glPopMatrix()
        
