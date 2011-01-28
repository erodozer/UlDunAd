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
from Actor import Actor

import random

class Enemy(Actor):
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
        
        self.name = name
        
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
        
        self.sprites = self.loadSprites(path)
        
        #position and scale are defined in the formation of the enemies and not the enemy.ini
        self.position = (0, 0)
        self.scale = 1
        
        try:
            self.skills = [Skill(s.strip()) for s in baseSection.__getattr__("skills", str).split("|") if s]
        except AttributeError:
            self.skills = []
            
        Actor.__init__(self, name)
     
    def getCommand(self, targets):
        '''commented out due to skills not yet working
        if len(self.skills) > 0:
            command = random.randint(0,2)   #randomly picks attack, tactical, or skill
        else:
            command = random.randint(0,1)   #randomly picks attack, tactical
        '''
        command = random.randint(0,1)   #randomly picks attack or tactical
        if command == 0:    #attack and targeting
            self.attacking = True
            self.target = random.choice(targets)
            self.power = random.randint(0,2)
        elif command == 1:  #tactical/defense choosing
            command = random.randint(0,1)
            if command == 0:
                self.boost = True
            else:
                self.defend = True
        
    def loadSprites(self, path):
        normal = Texture(os.path.join(path, "normal.png"))
        sprites =  {'normal':ImgObj(normal)}
                        #at least normal is required, especially as fallback
        
        #these are optional sprites but add some extra flare to the sprites
        sprites['weakened'] = ImgObj(Texture(os.path.join(path, "weakened.png"), fallback = normal))
        sprites['defend'] = ImgObj(Texture(os.path.join(path, "normal.png"), fallback = normal))
        sprites['boost'] = ImgObj(Texture(os.path.join(path, "boost.png"), fallback = normal))
        
        return sprites

    def calculateDamage(self):
         #first was calculate to see if the actor hits his target
        hit = random.randint(0, 255) - self.target.evd >= self.target.evd*1.5
        if hit:
            if self.cast:
                self.damage = (self.mag + self.command.damage) - (self.target.res * 1.368295)
            elif self.attacking:
                self.damage = self.str - (self.target.defn * 1.368295)
        else:
            self.damage = "Miss"
    
    #draws the enemy sprite in battle
    def getSprite(self):
        sprite = self.sprites['normal']
        if self.currentHP < self.hp / 3.0:
            sprite = self.sprites['weakened']
        if self.defend:
            sprite = self.sprites['defending']
        if self.boost:
            sprite = self.sprites['boost']
        
        sprite.setPosition(self.position[0], self.position[1])
        sprite.setScale(self.scale, self.scale)
        
        return sprite
        
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

        self.terrain = ImgObj(Texture(os.path.join("terrain", formationini.__getattr__("terrain") + ".png")))
   
    def draw(self):
        for enemy in self.enemies:
            enemy.getSprite().draw()
