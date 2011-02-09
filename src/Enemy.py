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
    exp = lambda x: 100     #good calculation still needs to be found
    
    def __init__(self, name):
        
        #do not try loading a character if name is not passed
        # ONLY do this during creation
        if not name:
            return

        path = os.path.join("actors", "enemies", name)
        enemyini = Configuration(os.path.join("..", "data", path, "enemy.ini"))
        
        self.name = name
        self.exp = Enemy.exp()
        
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
            
        self.gold = baseSection.__getattr__("gold", int)
        
        self.drop = baseSection.__getattr__("item")
        self.dropChance = baseSection.__getattr__("dropChance", int)
        
        path = os.path.join("..", "data", "items", self.drop)
        if os.path.exists(path):
            ini = Configuration(os.path.join("..", "data", "items", self.drop, "item.ini"))
            #detecting what type of item it is
            if ini.parser.has_section("weapon"):
                self.drop = Weapon(item)
            elif ini.parser.has_section("armor"):
                self.drop = Armor(item)
            else:
                self.drop = Item(item)
        else:
            self.drop = None
        
        Actor.__init__(self, name)
     
    def getCommand(self, targets):
        '''commented out due to skills not yet working
        if len(self.skills) > 0:
            command = random.randint(0,2)   #randomly picks attack, tactical, or skill
        else:
            command = random.randint(0,1)   #randomly picks attack, tactical
        '''
        command = random.randint(0,1)   #randomly picks attack or tactical
        #if the enemy does not have enough fp to attack then it must resort to tactical commands
        if self.fp < 35.0 and command == 0:
           command = 1
            
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
            self.damage = max(0, int(self.damage))
        else:
            self.damage = "Miss"
    
    #draws the enemy sprite in battle
    def getSprite(self):
        sprite = self.sprites['normal']
        if self.currentHP < self.hp / 3.0:
            sprite = self.sprites['weakened']
        if self.defend:
            sprite = self.sprites['defend']
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

        #formation's name can come from it's ini or just the filename
        try:
            self.name = formationini.__getattr__("name")
        except AttributeError:
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
   
    def getDifficulty(self, party):
        statsE = [0.0 for i in range(8)]
        statsP = [0.0 for i in range(8)]
        diff   = [0.0 for i in range(8)]
        for enemy in self.enemies:
            statsE[0] += enemy.level
            statsE[1] += enemy.hp
            statsE[2] += enemy.str
            statsE[3] += enemy.defn
            statsE[4] += enemy.spd
            statsE[5] += enemy.evd
            statsE[6] += enemy.mag
            statsE[7] += enemy.res
        for member in party:
            statsP[0] += member.level
            statsP[1] += member.hp
            statsP[2] += member.str
            statsP[3] += member.defn
            statsP[4] += member.spd
            statsP[5] += member.evd
            statsP[6] += member.mag
            statsP[7] += member.res
        
        for i in range(len(diff)):
            diff[i] = max(0.0, ((statsE[i]/len(self.enemies)) - (statsP[i]/len(party)))/255.0)
        difficulty = sum(diff) + 1
        return difficulty
        
    def draw(self, visibility):
        for enemy in self.enemies:
            sprite = enemy.getSprite()
            sprite.setColor((1,1,1,visibility))
            sprite.draw()
