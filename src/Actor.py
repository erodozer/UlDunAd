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
import Jobs

class Character:
    _LevelMax = 20      #this is the current level cap, I will adjust this with the number of content available
    #these mark the required amount of exp to level up
    #I calculated the curve myself in order to provide a fast, yet balanced
    #equation for leveling up.  There shouldn't be too much grind, but there
    #should be enough that you don't get bored by being over powered too easily
    exp = [int(8.938*x**2.835) for x in range(_LevelMax)]
    
    def __init__(self, family, name):
        
        #do not try loading a character if name is not passed
        # ONLY do this during creation
        if not name:
            return

        playerini = Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini"))
        
        #divides the character ini into resonable chunks
        baseSection  = playerini.character      #contains basic information about the character
        distSection  = playerini.distribution   #contains stat distribution information
        equipSection = playerini.equipment      #contains all the equipment being worn
        profSection  = playerini.proficency     #contains information about the character's weapon proficency
        
        self.job  = eval(baseSection.__getattr__("job")+"()")

        self.level      = baseSection.__getattr__("level", int)
        self.exp        = baseSection.__getattr__("exp",   int)

        #the amount of points added to each field
        # these are set upon the creation of the character
        # and upon leven up when the bonus stat points
        # are distributed
        self.hpDist  = distSection.__getattr__("hpDist",  int)
        self.strDist = distSection.__getattr__("strDist", int)
        self.defDist = distSection.__getattr__("defDist", int)
        self.spdDist = distSection.__getattr__("spdDist", int)
        self.evdDist = distSection.__getattr__("evdDist", int)
        self.magDist = distSection.__getattr__("magDist", int)
        self.resDist = distSection.__getattr__("resDist", int)

        #these are the points the character has that are open for
        #distribution amongst his stats
        self.points = baseSection.__getattr__("points", int)

        self.currentHp = baseSection.__getattr__("currenthp", int)

        self.hp   = self.job.hp   + hpDist,   #hit points
        self.str  = self.job.str  + strDist,  #strength
        self.defn = self.job.defn + defDist,  #defense
        self.spd  = self.job.spd  + spdDist,  #speed
        self.evd  = self.job.evd  + evdDist,  #evasion
        self.mag  = self.job.mag  + magDist,  #magic strength
        self.res  = self.job.res  + resDist   #magic defense

        #any character can weild any weapon, to balance things there is a proficency system
        #for equipment.  Every 100 points raises the level of the proficency.  
        self.swordProf = self.job.swordProf + profSection.__getattr__("sword", int)
        self.daggerProf = self.job.daggerProf + profSection.__getattr__("dagger", int)
        self.spearProf = self.job.spearProf + profSection.__getattr__("spear", int)
        self.staffProf = self.job.staffProf + profSection.__getattr__("staff", int)
        self.gunsProf = self.job.gunsProf + profSection.__getattr__("guns", int)
        
        #there are 10 pieces of equipment one can wear
        #left hand weapon, right hand weapon, helm, armor, legs, feet, gloves, and 3 accessories
        self.equipment = [equipSection.__getattr__("left hand"),
                          equipSection.__getattr__("right hand"),
                          equipSection.__getattr__("helmet"),
                          equipSection.__getattr__("armor"), 
                          equipSection.__getattr__("legs"), 
                          equipSection.__getattr__("feet"),
                          equipSection.__getattr__("gloves"),
                          equipSection.__getattr__("accessory1"),
                          equipSection.__getattr__("accessory2"),
                          equipSection.__getattr__("accessory3")]
        
        self.hand = 0       #0 = right handed, 1 = left handed
                            #dominant hand determines which weapons gets 
                            #proficency points and damage boost in battle
        
        x = self.level
        self.maxFP = int(eval(self.job.fightPT))
        
        #is the character attacking
        self.attack = False
        
        #are they casting a spell or technique, if they are, which one
        self.cast = False
        self.command = None
        
        #when a character boosts instead of defends,
        #their def is halved but they get full FP the next turn
        self.boost = False
        #when a character defends they gain the normal amount of FP per turn (20%)
        #but their def is multiplied by 250%
        self.defend = False

        #this marks for the end of the battle if the character leveled up
        self.leveledUp = False
        

    def initForBattle(self):
        self.fp = min(self.maxFP/3 + random.randInt(0, self.maxFP), self.maxFP)
        self.active = False

    def turnStart(self):
        if self.boost:
            self.defn /= 2
        elif self.defend:
            self.defn *= 2.5
        elif self.attack:
            self.damage = self.str + self.equipment[0].str + (self.str*
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
            
    def drawStatGraph(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-self.stats[0],   0)
        glColor3f(1.0, 1.0, 0.0); glVertex2f(-self.stats[1]/2, self.stats[1]/2)
        glColor3f(1.0, 0.5, 0.0); glVertex2f( self.stats[2]/2, self.stats[2]/2)
        glColor3f(1.0, 0.0, 1.0); glVertex2f( self.stats[3],   0)
        glColor3f(0.0, 0.5, 1.0); glVertex2f( self.stats[4]/2, -self.stats[4]/2)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(-self.stats[5]/2, -self.stats[5]/2)
        glEnd()

    #
    def levelUp(self):
        if self.exp == Character.exp[self.level-1]:
            self.level += 1
            self.exp = 0
            self.points += 5
            self.leveledUp = True     

    def create(self, family, name, job, stats):
        Configuration(os.path.join("..", "data", "actors", "characters", "families", family, name + ".ini")).save()
        playerini = Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini"))
        playerini.player.__setattr__("job", job)        
        playerini.player.__setattr__("level", 1)
        playerini.player.__setattr__("exp", 0)
        playerini.player.__setattr__("hpDist",  stats[0])
        playerini.player.__setattr__("strDist", stats[1])
        playerini.player.__setattr__("defDist", stats[2])
        playerini.player.__setattr__("spdDist", stats[3])
        playerini.player.__setattr__("evdDist", stats[4])
        playerini.player.__setattr__("magDist", stats[5])
        playerini.player.__setattr__("resDist", stats[6])
        playerini.save()
        
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
        self.inventory = [n.strip() for n in familyini.__getattr__("inventory").split(",")]
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
            
        
