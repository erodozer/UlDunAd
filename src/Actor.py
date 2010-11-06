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

class Job:
    def __init__(self, name):
        path = os.path.join("data", "actors", "jobs", name)
        jobini = Configuration(os.path.join("..", path, "job.ini")).job
        
        self.name = name

        #These stats are what the job starts out with
        # characters can go against the basic stats for example
        # you can create a mage that have high str instead of
        # the default high mag, however, certain skills are learned
        # not on level but on how many stat points are distributed
        # into what categories
        self.description = jobini.__getattr__("description")
        self.hp   = jobini.__getattr__("hp",  int)
        self.str  = jobini.__getattr__("str", int)
        self.defn = jobini.__getattr__("def", int)
        self.spd  = jobini.__getattr__("spd", int)
        self.evd  = jobini.__getattr__("evd", int)
        self.mag  = jobini.__getattr__("mag", int)
        self.res  = jobini.__getattr__("res", int)
        
        self.stats = [self.str, self.defn, self.spd, self.evd, self.mag, self.res]
        
        self.sprites = [ImgObj(Texture(os.path.join(path, sprite.rsplit["/"][1]))
                        for sprite in glob.glob(os.path.join(path, "*.png"))]

        #this stat is an equation in terms of x with w being the
        # character's level.  It determines the maximum amount
        # of fighting power the character has.
        #self.fightPT  = jobini.__getattr__("fightCurve")

    def drawStatGraph(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-self.stats[0],   0)
        glColor3f(1.0, 1.0, 0.0); glVertex2f(-self.stats[1]/2,  self.stats[1]/2)
        glColor3f(1.0, 0.5, 0.0); glVertex2f( self.stats[2]/2,  self.stats[2]/2)
        glColor3f(1.0, 0.0, 1.0); glVertex2f( self.stats[3],   0)
        glColor3f(0.0, 0.5, 1.0); glVertex2f( self.stats[4]/2, -self.stats[4]/2)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(-self.stats[5]/2, -self.stats[5]/2)
        glEnd()

class Character:
    _LevelMax = 20      #this is the current level cap, I will adjust this with the number of content available
    #these mark the required amount of exp to level up
    #I calculated the curve myself in order to provide a fast, yet balanced
    #equation for leveling up.  There shouldn't be too much grind, but there
    #should be enough that you don't get bored by being over powered too easily
    exp = [int(8.938*x**2.835) for x in range(_LevelMax)]
    
    def __init__(self, family, name):
        playerini = Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini")).character
        self.job  = Job(playerini.__getattr__("job"))

        self.level      = playerini.__getattr__("level", int)
        self.exp        = playerini.__getattr__("exp",   int)

        #the amount of points added to each field
        # these are set upon the creation of the character
        # and upon leven up when the bonus stat points
        # are distributed
        self.hpDist  = playerini.__getattr__("hpDist",  int)
        self.strDist = playerini.__getattr__("strDist", int)
        self.defDist = playerini.__getattr__("defDist", int)
        self.spdDist = playerini.__getattr__("spdDist", int)
        self.evdDist = playerini.__getattr__("evdDist", int)
        self.magDist = playerini.__getattr__("magDist", int)
        self.resDist = playerini.__getattr__("resDist", int)

        #these are the points the character has that are open for
        #distribution amongst his stats
        self.points = playerini.__getattr__("points", int)

        self.currentHp = playerini.__getattr__("currenthp", int)

        self.hp   = self.job.hp   + hpDist,   #hit points
        self.str  = self.job.str  + strDist,  #strength
        self.defn = self.job.defn + defDist,  #defense
        self.spd  = self.job.spd  + spdDist,  #speed
        self.evd  = self.job.evd  + evdDist,  #evasion
        self.mag  = self.job.mag  + magDist,  #magic strength
        self.res  = self.job.res  + resDist   #magic defense

        x = self.level
        self.maxFP = int(eval(self.job.fightPT))
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
        Configuration(os.path.join("data", "actors", "characters", "families", family, name + ".ini")).save()
        playerini = Configuration(os.path.join("data", "actors", "families", family, name + ".ini"))
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
        print members
        
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

