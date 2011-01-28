'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from Config import Configuration
from math import *
from Jobs import *
from Item import *
import os
from Actor import Actor

class Character(Actor):
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
        
        self.name = name
        
        #divides the character ini into resonable chunks
        baseSection  = playerini.character      #contains basic information about the character
        distSection  = playerini.distribution   #contains stat distribution information
        equipSection = playerini.equipment      #contains all the equipment being worn
        profSection  = playerini.proficiency    #contains information about the character's weapon proficency
        
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

        self.hp   = self.job.hp   + self.hpDist   #hit points
        self.str  = self.job.str  + self.strDist  #strength
        self.defn = self.job.defn + self.defDist  #defense
        self.spd  = self.job.spd  + self.spdDist  #speed
        self.evd  = self.job.evd  + self.evdDist  #evasion
        self.mag  = self.job.mag  + self.magDist  #magic strength 
        self.res  = self.job.res  + self.resDist  #magic defense (resistance)

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
        
        #any character can weild any weapon, to balance things there is a proficency system
        #for equipment.  Every 100 points raises the level of the proficency.  
        #max proficency is 1100 points or SS rank
        
        self.swordProf  = min(self.job.swordProf  + profSection.__getattr__("sword",  int), 1100)
        self.daggerProf = min(self.job.daggerProf + profSection.__getattr__("dagger", int), 1100)
        self.spearProf  = min(self.job.spearProf  + profSection.__getattr__("spear",  int), 1100)
        self.staffProf  = min(self.job.staffProf  + profSection.__getattr__("staff",  int), 1100)
        self.gunsProf   = min(self.job.gunsProf   + profSection.__getattr__("guns",   int), 1100)
        self.fistProf   = min(self.job.fistProf   + profSection.__getattr__("fist",   int), 1100)
        
        self.proficiencies = [self.swordProf, self.daggerProf, self.spearProf, 
                              self.staffProf, self.gunsProf, self.fistProf]
                              
        self.loadProficiency()
        
        self.skills = self.job.skills
        
        #this marks for the end of the battle if the character leveled up
        self.leveledUp = False
        
        self.sprites = self.job.sprites #for now, more work will be done later
        
        Actor.__init__(self, name)

    #figures out the which proficency to use for the dominant hand weapon
    def loadProficiency(self):
        weapon = Weapon(self.equipment[self.hand])
        if (weapon.type == "sword"):
            self.proficiency = self.proficiencies[0]
        elif (weapon.type == "dagger"):
            self.proficiency = self.proficiencies[1]
        elif (weapon.type == "spear"):
            self.proficiency = self.proficiencies[2]
        elif (weapon.type == "staff"):
            self.proficiency = self.proficiencies[3]
        elif (weapon.type == "gun"):
            self.proficiency = self.proficiencies[4]
        else:
            self.proficiency = self.proficiencies[5]
    
    def setEquipment(self, equipment):
        reloadProficiency = False
        if not equipment[self.hand].type == self.equipment[self.hand].type:
            reloadProficiency = True
            
        self.equipment = equipment   
        if reloadProficiency:
            self.loadProficiency()
        
    def levelUp(self):
        if self.exp == Character.exp[self.level-1]:
            self.level += 1
            self.exp = 0
            self.points += 5
            self.leveledUp = True     
            
    #not working, I wish it did, it's supposed to be a pentagon with each vertex further from the
    #center depending on how high the stat is
    def drawStatGraph(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-self.stats[0],   0)
        glColor3f(1.0, 1.0, 0.0); glVertex2f(-self.stats[1]/2, self.stats[1]/2)
        glColor3f(1.0, 0.5, 0.0); glVertex2f( self.stats[2]/2, self.stats[2]/2)
        glColor3f(1.0, 0.0, 1.0); glVertex2f( self.stats[3],   0)
        glColor3f(0.0, 0.5, 1.0); glVertex2f( self.stats[4]/2, -self.stats[4]/2)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(-self.stats[5]/2, -self.stats[5]/2)
        glEnd()

    #proficiency is displayed by letter grade
    def getProfLetter(self, prof = 0):
        grade = int(self.proficencies[prof]/100.0)
        if grade < 4:
            return "F"
        elif grade < 5:
            return "E"
        elif grade < 6:
            return "D"
        elif grade < 7:
            return "C"
        elif grade < 8:
            return "B"
        elif grade < 9:
            return "A"
        elif grade < 10:
            return "A+"
        elif grade < 11:
            return "S"
        else:
            return "SS"

    def calculateDamage(self):
         #first was calculate to see if the actor hits his target
        hit = (self.proficiency*2) - self.target.evd >= self.target.evd*1.5
        if hit:
            if self.cast:
                self.damage = (self.mag + self.command.damage) - (self.target.res * 1.368295)
            elif self.attacking:
                self.damage = self.str - (self.target.defn * 1.368295)
        else:
            self.damage = "Miss"
    
    def getSprite(self):
        sprite = self.sprites['standing']
        return sprite
        
    #saves a new ini for the character to be used
    def create(self, family, name, job, stats, points = 0, equipment = None, proficiency = None):
        Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini")).save()
        ini = Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini"))
        
        #nothing like short-handing
        base = ini.character
        dist = ini.distribution
        eqp  = ini.equipment
        prof = ini.proficiency
        
        if proficiency == None:
            proficiency = eval(job+"()").proficiencies
            print proficiency
        if equipment == None:
            equipment = [None for i in range(10)]
            
        base.__setattr__("job", job)      
        base.__setattr__("level", 1)
        base.__setattr__("exp",   0)
        base.__setattr__("points", points)
        
        dist.__setattr__("hpDist",  stats[0])
        dist.__setattr__("strDist", stats[1])
        dist.__setattr__("defDist", stats[2])
        dist.__setattr__("spdDist", stats[3])
        dist.__setattr__("evdDist", stats[4])
        dist.__setattr__("magDist", stats[5])
        dist.__setattr__("resDist", stats[6])
        
        eqp.__setattr__("left hand",  equipment[0])
        eqp.__setattr__("right hand", equipment[1])
        eqp.__setattr__("helmet",     equipment[2])
        eqp.__setattr__("armor",      equipment[3]) 
        eqp.__setattr__("legs",       equipment[4]) 
        eqp.__setattr__("feet",       equipment[5])
        eqp.__setattr__("gloves",     equipment[6])
        eqp.__setattr__("accessory1", equipment[7])
        eqp.__setattr__("accessory2", equipment[8])
        eqp.__setattr__("accessory3", equipment[9])
        
        prof.__setattr__("sword",  proficiency[0])
        prof.__setattr__("dagger", proficiency[1])
        prof.__setattr__("spear",  proficiency[2])
        prof.__setattr__("staff",  proficiency[3])
        prof.__setattr__("guns",   proficiency[4])
        prof.__setattr__("fist",   proficiency[5])
        
        ini.save()
