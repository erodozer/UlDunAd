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

class Job:
    def __init__(self, name):
        jobini = Configuration(os.path.join("..", "data", "actors", "jobs", name + ".ini")).job

        #setting up curves is easy!  Just write a simple equation 
        # in terms of x (level) and you're set.  Best of all, all
        # the python math commands are available
        # ex. x**(5/17) + 15  at level 12 will give you a stat of 17
        self.strCurve = jobini.__getattr__("strCurve")
        self.defCurve = jobini.__getattr__("defCurve")
        self.spdCurve = jobini.__getattr__("spdCurve")
        self.evdCurve = jobini.__getattr__("evdCurve")
        self.magCurve = jobini.__getattr__("magCurve")
        self.resCurve = jobini.__getattr__("resCurve")

class Character:
    def __init__(self, name):
        playerini = Configuration(os.path.join("..", "data", "actors", "characters", name + ".ini")).character
        self.job  = Job(playerini.__getattr__("job"))

        self.level      = playerini.__getattr__("level", int)
        self.exp        = playerini.__getattr__("exp",   int)

        #the amount of points added to each field
        # these are set upon the creation of the character
        # when the bonus stat points are distributed
        strDist         = playerini.__getattr__("strDist", int)
        defDist         = playerini.__getattr__("defDist", int)
        spdDist         = playerini.__getattr__("spdDist", int)
        evdDist         = playerini.__getattr__("evdDist", int)
        magDist         = playerini.__getattr__("magDist", int)
        resDist         = playerini.__getattr__("resDist", int)

        x = level
        self.stats = [eval(self.job.strCurve) + strDist,  #strength
                      eval(self.job.defCurve) + defDist,  #defense
                      eval(self.job.spdCurve) + spdDist,  #speed
                      eval(self.job.evdCurve) + evdDist,  #evasion
                      eval(self.job.magCurve) + magDist,  #magic strength
                      eval(self.job.resCurve) + resDist   #magic defense
                      ]

    def create(self, name, job):
        Configuration(os.path.join("data", "actors", "characters", name + ".ini")).save()
        playerini = Configuration(os.path.join("data", "actors", "families", name + ".ini"))
        playerini.player.__setattr__("job", job)        
        playerini.player.__setattr__("level", 1)
        playerini.player.__setattr__("exp", 0)
        playerini.save()
        
 
class Family:
    def __init__(self, name):

        #does not try loading a family if name is not passed
        # ONLY do this during family creation
        if not name:
            return

        familyini = Configuration(os.path.join("..", "data", "actors", "families", name + ".ini")).family

        self.name = name

        #all the members in your party (max of 7)
        self.members = []
        for i in range(7):
            member = familyini.__getattr__("member%s" % i)
            if member != "":
                self.members.append(Character(member))

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
        
    def create(self, name, difficulty):
        path = os.path.join("..", "data", "actors", "families", name + ".ini")
        Configuration(path).save()
        familyini = Configuration(path)
        familyini.family.__setattr__("difficulty", difficulty)
        
        familyini.family.__setattr__("gold", 0)
        familyini.family.__setattr__("inventory", "")
        
        for i in range(7):
            familyini.family.__setattr__("member%s" % i, "")

        familyini.save()


