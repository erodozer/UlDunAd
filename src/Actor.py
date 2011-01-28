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

        #used in battle
        self.maxFP = 100
        self.currentHP = self.hp
        
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

        self.fp = min(self.fp, self.maxFP)

        self.boost = False
        self.defend = False

#the player's family
#this class holds the code responsible for the amount of gold the family has
#the inventory of the family, the difficulty of the game, and the members in
#the family.  It is very important and one of the main gameplay additions
#to UlDunAd.  No longer are you loading individual characters, you are now
#loading families.

from Character import Character #import character after Actor class has been defined

class Family:
    def __init__(self, name):

        #does not try loading a family if name is not passed
        # ONLY do this during family creation
        if not name:
            return

        path = os.path.join("data", "actors", "families", name)
        familyini = Configuration(os.path.join("..", path, "family.ini")).family

        #family's last name, all members of the family will have this last name
        self.name = name

        #all the members in your party
        path = os.path.join("..", path)
        members = [n.split("/")[-1] for n in glob.glob(os.path.join(path, "*.ini"))]
        if "family.ini" in members:
            members.remove("family.ini")
        
        self.members = [Character(name, n.replace(".ini", "")) for n in members]

        #the party used in battle is the first 3 members you have ordered
        if len(self.members) >= 3:
            self.party = self.members[0:2]
        else:
            self.party = self.members[0:len(self.members)]

        #the items your family has
        items = [n.strip() for n in familyini.__getattr__("inventory").split(",")]
        self.inventory = []
        for item in items:
            path = os.path.join("..", "data", "items", item)
            if os.path.exists(path):
                ini = Configuration(os.path.join("..", "data", "items", name, "item.ini"))
                #detecting what type of item it is
                if ini.parser.has_section("weapon"):
                    items.append(Weapon(item))
                elif ini.parser.has_section("armor"):
                    items.append(Armor(item))
                else:
                    items.append(Item(item))
                
            
        #amount of money your family possesses
        self.gold = familyini.__getattr__("gold", int)
        #gameplay difficulty (0 - easy, 1- normal, 2 - hard)
        self.difficulty = familyini.__getattr__("difficulty", int)  
       
    #creates a new family .ini 
    def create(self, name, difficulty):
        path = os.path.join("..", "data", "actors", "families", name)
        os.mkdir(path)
        Configuration(os.path.join(path, "family.ini")).save()
        familyini = Configuration(os.path.join(path, "family.ini"))
        familyini.family.__setattr__("difficulty", difficulty)
        
        familyini.family.__setattr__("gold", 0)
        familyini.family.__setattr__("inventory", "")
        
        familyini.family.__setattr__("members", "")

        familyini.save()

    #this updates the family's .ini file
    def updateFile(self):
        path = os.path.join("..", "data", "actors", "families", self.name)
        Configuration(path).save()
        familyini = Configuration(os.path.join(path,"family.ini")).family

        familyini.__setattr__("difficulty", self.difficulty)
        familyini.__setattr__("gold",       self.gold)
        familyini.__setattr__("inventory",  string.join(self.inventory, ","))

        familyini.save()
        
    def refresh(self):
        self.__init__(self.name)

#party for battle has a few specifics for conditions
#depending on members present in it
class Party:
    def __init__(self, members):
        self.members = members
        
        
        self.shepardPresent = False
        self.treasureHunterPresent = False
        self.piratePresent = False
        for mem in self.members:
            if isInstance(mem, Shepard):
                self.shepardPresent = True
            elif isInstance(mem, TreasureHunter):
                self.treasureHunterPresent = True
            elif isInstance(mem, Pirate):
                self.piratePresent = True
            
        
