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
class Actor:
    def __init__(self, name):

        #base stats
        self.hp   = 0  #hit points
        self.str  = 0  #strength
        self.defn = 0  #defense
        self.spd  = 0  #speed
        self.evd  = 0  #evasion
        self.mag  = 0  #magic strength 
        self.res  = 0  #magic defense (resistance)

        #used in battle
        self.maxFP = 100
        self.fp = 0
        self.currentHP = self.hp
        self.incap = False      #actors become incapacitated when their hp reaches 0
        
        #is the character attacking
        self.attacking = False
        self.power = 0          #0 = normal attack, 1 = strong attack, 2 = accurate attack
        
        #are they casting a spell or technique, if they are, which one
        self.cast = False
        self.command = None
        
        #when an enemy boosts instead of defends,
        #their def is halved but they get full FP the next turn
        self.boost = False
        
        #when a character defends they gain the normal amount of FP per turn (20%)
        #but their def is multiplied by 250%
        self.defend = False        

        #the enemy or ally being targeted
        self.target = None
        
        self.damage = 0
        
    def initForBattle(self):
        self.currentHP = self.hp
        self.fp = min(self.maxFP/3 + random.randint(0, self.maxFP), self.maxFP)
        self.active = False

    def turnStart(self):
        if self.boost:
            self.defn /= 2
        elif self.defend:
            self.defn *= 2.5
        elif self.cast or self.attacking:
            self.calculateDamage()
           
    #calculates and returns the cost of doing an action
    def getFPCost(self):
        if self.attacking:
            #strong attack takes more fp
            if self.power == 1:
                return 45.0
            else:
                return 35.0
        elif self.cast:
            return self.command.cost
            
    #calculates the amount of damage towards a target
    def calculateDamage(self):
        pass
        
    #ends the enemy's turn
    def turnEnd(self):
        self.fp += self.maxFP / 5

        #resets defense
        if self.boost:
            self.fp = self.maxFP
            self.defn *= 2
        elif self.defend:
            self.defn /= 2.5
        elif self.attacking or self.cast:
            self.fp -= self.getFPCost()

        self.fp = min(self.fp, self.maxFP)

        self.boost = False
        self.defend = False
        self.attacking = False
        self.target = None
        self.cast = False
        self.command = None
        self.power = 0
