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
from Character import Character

from Item import *
        
#the player's family
#this class holds the code responsible for the amount of gold the family has
#the inventory of the family, the difficulty of the game, and the members in
#the family.  It is very important and one of the main gameplay additions
#to UlDunAd.  No longer are you loading individual characters, you are now
#loading families.
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
            self.party = self.members[0:len(self.members)-1]

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
            
        
