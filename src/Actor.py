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

from Item import *
        
#this class contains the basic variables and methods for characters and enemies
#most shared variables and methods are just for battle since enemies are supposed
#to have just as many options as characters to create a far fight and flexibility
class Actor(object):
    def __init__(self, name):

        #base stats
        self.hp   = 1  #hit points
        self.str  = 1  #strength
        self.defn = 1  #defense
        self.spd  = 1  #speed
        self.evd  = 1  #evasion
        self.mag  = 1  #magic strength 
        self.res  = 1  #magic defense (resistance)

        #used in battle
        self.maxFP = 100
        self.fp = 0
        self.currentHP = self.hp
        self.incap = False      #actors become incapacitated when their hp reaches 0
        
        self.command = None
        
        #are they casting a spell or technique, if they are, which one
        self.cast = False
        self.spell = None
        
        #the enemy or ally being targeted
        self.target = None
        
        self.damage = 0
        
    def initForBattle(self):
        self.currentHP = self.hp
        self.fp = min(self.maxFP/3 + random.randint(0, self.maxFP), self.maxFP)
        self.active = False

    def turnStart(self):
        self.command.execute()

    #ends the enemy's turn
    def turnEnd(self):
        self.fp += self.maxFP / 5

        #resets defense
        self.command.reset()
        
        self.fp = min(self.fp, self.maxFP)

        self.target = None
        self.command = None
        self.power = 0
