from Config import Configuration
from math import *
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

        self.currentHp = baseSection.__getattr__("currenthp", int)

        self.hp   = self.job.hp   + hpDist,   #hit points
        self.str  = self.job.str  + strDist,  #strength
        self.defn = self.job.defn + defDist,  #defense
        self.spd  = self.job.spd  + spdDist,  #speed
        self.evd  = self.job.evd  + evdDist,  #evasion
        self.mag  = self.job.mag  + magDist,  #magic strength
        self.res  = self.job.res  + resDist   #magic defense

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
        self.swordProf = self.job.swordProf + profSection.__getattr__("sword", int)
        self.daggerProf = self.job.daggerProf + profSection.__getattr__("dagger", int)
        self.spearProf = self.job.spearProf + profSection.__getattr__("spear", int)
        self.staffProf = self.job.staffProf + profSection.__getattr__("staff", int)
        self.gunsProf = self.job.gunsProf + profSection.__getattr__("guns", int)
        self.fistProf = self.job.fistProf + profSection.__getattr__("fist", int)
        
        self.proficiencies = [self.swordProf, self.daggerProf, self.spearProf, 
                              self.staffProf, self.gunsProf, self.fistProf]
                              
        self.loadProficiency()
        
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
      
    #figures out the which proficency to use for the dominant hand weapon
    def loadProficiency(self):
        weapon = self.equipment[self.hand]
        if (weapon.type = "sword")
            self.proficiency = self.proficiencies[0]
        else if (weapon.type = "dagger")
            self.proficiency = self.proficiencies[1]
        else if (weapon.type = "spear")
            self.proficiency = self.proficiencies[2]
        else if (weapon.type = "staff")
            self.proficiency = self.proficiencies[3]
        else if (weapon.type = "gun")
            self.proficiency = self.proficiencies[4]
        else
            self.proficiency = self.proficiencies[5]
    
    def setEquipment(self, equipment):
        reloadProficiency = False
        if not equipment[self.hand].type == self.equipment[self.hand].type:
            reloadProficiency = True
            
        self.equipment =     
        if reloadProficiency:
            self.loadProficiency()
        
    def initForBattle(self):
        self.fp = min(self.maxFP/3 + random.randInt(0, self.maxFP), self.maxFP)
        self.active = False

    def turnStart(self):
        if self.boost:
            self.defn /= 2
        elif self.defend:
            self.defn *= 2.5
        elif self.attack:
            self.damage = self.str + self.equipment[0].str + 
                          (self.str*(self.proficiency/100.0 - 1))
            
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
            
    #not working, I wish it did
    def drawStatGraph(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-self.stats[0],   0)
        glColor3f(1.0, 1.0, 0.0); glVertex2f(-self.stats[1]/2, self.stats[1]/2)
        glColor3f(1.0, 0.5, 0.0); glVertex2f( self.stats[2]/2, self.stats[2]/2)
        glColor3f(1.0, 0.0, 1.0); glVertex2f( self.stats[3],   0)
        glColor3f(0.0, 0.5, 1.0); glVertex2f( self.stats[4]/2, -self.stats[4]/2)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(-self.stats[5]/2, -self.stats[5]/2)
        glEnd()


    def levelUp(self):
        if self.exp == Character.exp[self.level-1]:
            self.level += 1
            self.exp = 0
            self.points += 5
            self.leveledUp = True     

    #saves a new ini for the character to be used
    def create(self, family, name, job, stats, equipment, proficiency):
        Configuration(os.path.join("..", "data", "actors", "characters", "families", family, name + ".ini")).save()
        ini = Configuration(os.path.join("..", "data", "actors", "families", family, name + ".ini"))
        
        #nothing like short-handing
        base = ini.character
        dist = ini.distribution
        eqp  = ini.equipment
        prof = ini.proficiency
        
        base.__setattr__("job", job)      
        base.__setattr__("level", 1)
        base.__setattr__("exp",   0)
        
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
