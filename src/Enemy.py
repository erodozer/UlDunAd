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
from ImgObj import *
from Texture import *
import os

class Enemy:
    _LevelMax = 20      #this is the current level cap, I will adjust this with the number of content available
    #exp is calculated by enemy level and their stats
    #in the victory scene it is scaled to the player party's average level
    exp = [100]     #good calculation still needs to be found
    
    def __init__(self, name):
        
        #do not try loading a character if name is not passed
        # ONLY do this during creation
        if not name:
            return

        path = os.path.join("actors", "enemies", name)
        enemyini = Configuration(os.path.join("..", "data", path, "enemy.ini"))
        
        #divides the enemy ini into resonable chunks
        baseSection  = enemyini.enemy          #contains basic information about the enemy
        distSection  = enemyini.distribution   #contains stat distribution information

        self.level      = baseSection.__getattr__("level", int)

        #the amount of points added to each field
        # these are set upon the creation of the character
        # and upon leven up when the bonus stat points
        # are distributed
        self.hp   = distSection.__getattr__("hp",  int)
        self.str  = distSection.__getattr__("str", int)
        self.defn = distSection.__getattr__("def", int)
        self.spd  = distSection.__getattr__("spd", int)
        self.evd  = distSection.__getattr__("evd", int)
        self.mag  = distSection.__getattr__("mag", int)
        self.res  = distSection.__getattr__("res", int)
        
        #used in battle
        x = self.level
        self.maxFP = 100
        self.currentHP = self.hp
        
        #is the character attacking
        self.attack = False
        
        #are they casting a spell or technique, if they are, which one
        self.cast = False
        self.command = None
        
        #when an enemy boosts instead of defends,
        #their def is halved but they get full FP the next turn
        self.boost = False
        
        #when a character defends they gain the normal amount of FP per turn (20%)
        #but their def is multiplied by 250%
        self.defend = False

        self.sprites = self.loadSprites(path)
        
        #position and scale are defined in the formation of the enemies and not the enemy.ini
        self.position = (0, 0)
        self.scale = (1, 1)
        
    def loadSprites(self, path):
        normal = Texture(os.path.join(path, "normal.png"))
        sprites =  {'normal':ImgObj(normal)}
                        #at least normal is required, especially as fallback
        
        #these are optional sprites but add some extra flare to the sprites
        sprites['weakened'] = ImgObj(Texture(os.path.join(path, "weakened.png"), fallback = normal))
        sprites['defend'] = ImgObj(Texture(os.path.join(path, "normal.png"), fallback = normal))
        sprites['boost'] = ImgObj(Texture(os.path.join(path, "boost.png"), fallback = normal))
        
        return sprites
        
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
        
    def initForBattle(self):
        self.currentHP = self.hp
        self.fp = min(self.maxFP/3 + random.randInt(0, self.maxFP), self.maxFP)
        self.active = False

    def turnStart(self):
        if self.boost:
            self.defn /= 2
        elif self.defend:
            self.defn *= 2.5
        elif self.attack:
            self.damage = self.str + self.equipment[0].str + (self.str*(self.proficiency/100.0 - 1))
    
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

    #draws the enemy sprite in battle
    def draw(self):
        sprite = self.sprites['normal']
        if self.currentHP < self.hp / 3.0:
            sprite = self.sprites['weakened']
        if self.defend:
            sprite = self.sprites['defending']
        if self.boost:
            sprite = self.sprites['boost']
        
        sprite.setPosition(self.position[0], self.position[1])
        sprite.setScale(self.scale[0], self.scale[1])
        sprite.draw()
        
#an enemy formation
class Formation:
    def __init__(self, name):

        #does not try loading a formation if name is not passed
        if not name:
            return

        path = os.path.join("data", "actors", "formations")
        formationini = Configuration(os.path.join("..", path, name + ".ini")).formation

        #family's last name, all members of the family will have this last name
        self.name = name

        #all the members in your party
        self.enemies = [Enemy(n) for n in formationini.enemies.split("|")]
        
        #assigns the positions and scales to the enemies
        for i, enemy in enumerate(self.enemies):
            n = formationini.__getattr__("coord").split("|")[i]
            x = int(n.split(",")[0])
            y = int(n.split(",")[1])
            enemy.position = (x,y)
            n = formationini.__getattr__("scale").split("|")[i]
            enemy.scale =  float(n)

        self.terrain = ImgObj(Texture(os.path.join("terrains", formationini.__getattr__("terrain"))))
   
    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
