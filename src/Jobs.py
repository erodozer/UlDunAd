'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import os

from Config import Configuration
from math import *
import random

import glob

from Skill import *

from ImgObj import *
from Texture import *

class Job:
    def __init__(self):
        
        self.name = ""

        #These stats are what the job starts out with
        # characters can go against the basic stats for example
        # you can create a mage that have high str instead of
        # the default high mag, however, certain skills are learned
        # not on level but on how many stat points are distributed
        # into what categories
        #
        #Recommended total stat points to be distributed when designing
        # a job is 50 points
        
        self.description = ""
        self.hp   = 0
        self.str  = 0
        self.defn = 0
        self.spd  = 0
        self.evd  = 0
        self.mag  = 0
        self.res  = 0
        
        self.stats = [self.hp, self.str, self.defn, self.spd, self.evd, self.mag, self.res]
        
        #skill tree
        self.skills = []

        #jobs have their own weapon proficiency buffs to being with
        self.swordProf  = 0
        self.daggerProf = 0
        self.spearProf  = 0
        self.staffProf  = 0
        self.gunsProf   = 0
        self.fistProf   = 0

    def drawStatGraph(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-self.stats[0],   0)
        glColor3f(1.0, 1.0, 0.0); glVertex2f(-self.stats[1]/2,  self.stats[1]/2)
        glColor3f(1.0, 0.5, 0.0); glVertex2f( self.stats[2]/2,  self.stats[2]/2)
        glColor3f(1.0, 0.0, 1.0); glVertex2f( self.stats[3],   0)
        glColor3f(0.0, 0.5, 1.0); glVertex2f( self.stats[4]/2, -self.stats[4]/2)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(-self.stats[5]/2, -self.stats[5]/2)
        glEnd()

    #searches path for files with filetype or folder
    def loadSprites(self):
        spritePath = os.path.join("..", "data", "actors", "jobs", name, "sprites")
        sprites = os.listdir(spritePath)

        return sprites
        
class Adventurer(Job):
    def __init__(self):
        
        self.name = "Adventurer"

        self.description = "Adventurers are masters of combat and are at a rise.\n" + \
                           "With war at a historical low, people are in search of\n" + \
                           "a thrill for their lives.  Adventuring fills that void\n" + \
                           "by reopening their eyes to the nature and the wild." 
        
        self.hp   = 150
        self.str  = 17
        self.defn = 15
        self.spd  = 6
        self.evd  = 4
        self.mag  = 3
        self.res  = 5
        
        self.stats = [self.hp, self.str, self.defn, self.spd, self.evd, self.mag, self.res]
        
        #jobs have their own weapon proficiency buffs to being with
        self.swordProf  = 300
        self.daggerProf = 100
        self.spearProf  = 200
        self.staffProf  = 0
        self.gunsProf   = 0
        self.fistProf   = 150
        
        self.proficiencies = [self.swordProf, self.daggerProf, self.spearProf, 
                              self.staffProf, self.gunsProf, self.fistProf]
        
        #skill tree
        self.skills = [SwordMastery(self)]
        
        self.state = 'standing'
                
