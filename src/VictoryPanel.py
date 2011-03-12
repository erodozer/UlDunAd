from sysobj import *
import Input
        
class VictoryPanel:
    def __init__(self, scene, turns):
        self.scene = scene
        self.engine = scene.engine
        
        battlepath = os.path.join("scenes", "battlesystem")
        
        self.background = ImgObj(Texture(os.path.join(battlepath, "victorypanel.png")))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        self.diffStar = ImgObj(Texture(os.path.join(battlepath, "star.png")))
        
        self.font = FontObj("default.ttf", size = 16)
        
        self.turns = turns    #total number of player turns used in battle
        
        self.formation = self.engine.formation
        self.family = self.engine.family
        self.party = self.engine.family.party 
        
        self.difficulty = self.formation.getDifficulty(self.party)
        #dropped items
        self.items = []
        
        self.exp = 0
        self.gold = 0
        self.bonusExp = 0
        self.bonusGold = 0
        
        for enemy in self.formation.enemies:
            self.exp += enemy.exp
            self.gold += enemy.gold
            if enemy.drop:
                if random.randint(0, 100/enemy.dropChance - 1) == 0:
                    self.items.append(enemy.drop)
        
        #figure out bonus amounts
        self.bonusExp = self.exp * self.difficulty
        self.bonusExp *= (len(self.formation.enemies)*((self.difficulty-1)*3))/self.turns
        
        self.exp /= len(self.party)
        self.bonusExp /= len(self.party)
        
        self.bonusGold = self.gold * self.difficulty
        self.bonusGold *= (len(self.formation.enemies)*((self.difficulty-1)*3))/self.turns
        
        self.alpha = 0.0
        
        self.levelUp = [False for i in self.party]
        
    def keyPressed(self, key):
        if key == Input.AButton:
            self.finish()
    
    #saves all the character data and returns to the previous scene
    def finish(self):
        if any(self.levelUp):
            self.scene.end()
            
        self.family.gold += int(self.gold + self.bonusGold)
        
        for item in self.items:
            self.family.inventory.append(item)
        self.family.update()
            
        for member in self.party:
            member.exp += int((self.exp + self.bonusExp)/len(self.party))
            member.update()
            
        for i, member in enumerate(self.party):
            self.levelUp[i] = member.levelUp()

        if not any(self.levelUp):
            self.scene.end()
        
    def render(self):
        self.background.setColor((1,1,1,self.alpha))
        self.background.draw()
        
        self.font.setAlignment("right")
        
        self.font.setColor((1,1,1,self.alpha))
        
        #difficulty
        self.font.setText("%i" % self.difficulty)
        self.font.setPosition(self.engine.w/2, 425)
        self.font.draw()
        
        #time
        self.font.setText("%i Turns" % (self.turns))
        self.font.setPosition(self.engine.w/2, 350)
        self.font.draw()
        
        #gold
        self.font.setText("%i + %i = %i" % (self.gold, self.bonusGold, (self.gold+self.bonusGold)))
        self.font.setPosition(self.engine.w/2, 275)
        self.font.draw()
        
        #exp
        self.font.setText("(%i + %i) / %i = %i" % (self.exp, self.bonusExp, len(self.party), (self.exp+self.bonusExp)/len(self.party)))
        self.font.setPosition(self.engine.w/2, 200)
        self.font.draw()
        
        for i, lU in enumerate(self.levelUp):
            if lU:
                self.font.setText("%s Leveled Up!" % (self.party[i].name))
                self.font.setPosition(self.engine.w*.9 - 20*(i+1), 175 - 30*(i+1))
                self.font.draw()
        
        self.alpha = min(1.0, self.alpha+.1)
        
        
 
