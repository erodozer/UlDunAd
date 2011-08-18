'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from operator import itemgetter

from View   import *
from Actor  import *
from Character import *
from Enemy import *

import string
import Input

from MenuObj import MenuObj

from BattleHUDCharacter import BattleHUDCharacter
from BattleHUDEnemy import BattleHUDEnemy
from BattleHUDEngage import BattleHUDEngage
from BattleHUDAddition import BattleHUDAddition
from BattleMenu import BattleMenu
from VictoryPanel import VictoryPanel
   
from Command import *

#scene graphics handling for the battle
#terrains consist of a backdrop and platforms for characters to stand on
class Terrain:
    def __init__(self, scene, name):
        self.scene = scene
        self.engine = scene.engine
        
        self.background = ImgObj(Texture(os.path.join("terrain", name, "background.png")))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)

        self.hue = (1.0,1.0,1.0,1.0)
        self.background.setColor(self.hue)
        
    def drawBackground(self):
        self.background.draw()
        
#unlike most other scenes in this game, the battle scene 
#is completely controlled by the keyboard instead of mouse
class BattleSystem(Scene):
    def __init__(self, engine):

        self.engine = engine
        self.camera = self.engine.viewport.camera   #for simplicity's sake
        
        w, h = self.engine.w, self.engine.h

        musicpath = os.path.join("audio", "music", "battle")
        battleSongs = self.engine.listPath(musicpath, "ogg|mp3")
        musicpath = os.path.join("audio", "music", "victory")
        victorySongs = self.engine.listPath(musicpath, "ogg|mp3")
        
        if len(battleSongs) > 0:
            self.battleSong = os.path.join("battle", random.choice(battleSongs))
            
        if len(victorySongs) > 0:
            self.victorySong = os.path.join("victory", random.choice(victorySongs))
            
        if not pygame.mixer.music.get_busy():
            self.music = BGMObj(self.battleSong)
        
        battlepath = os.path.join("scenes", "battlesystem")
        self.activeHighlight = ImgObj(Texture(os.path.join(battlepath, "active_highlight.png")))
        
        self.diffStar = ImgObj(Texture(os.path.join(battlepath, "star.png")))
        
        self.header = ImgObj(os.path.join(battlepath, "header.png"))
        self.footer = ImgObj(os.path.join(battlepath, "footer.png"))
        self.infohud = ImgObj(os.path.join(battlepath, "infohud.png"))
        self.vs = ImgObj(os.path.join(battlepath, "vs.png"))
        self.boost = ImgObj(os.path.join(battlepath, "boost.png"))
        self.defend = ImgObj(os.path.join(battlepath, "defend.png"))
        
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle, size = 32)
        self.smtext = FontObj(fontStyle, size = 14)
        self.bigText = FontObj(fontStyle, size = 64)

        self.party = [m for m in self.engine.family.party.members]
        self.formation = [e for e in self.engine.formation.enemies]

        self.terrain = Terrain(self, self.engine.formation.terrain)
        
        self.incapParty = 0     #keeps track of how many in the party are incapacitated
                                #when all members are then the battle is over
        
        #self.start = ImgObj(Texture("start.png"))
        #self.start.setPosition(self.engine.w / 2, self.engine.h / 2)

        self.huds = [BattleHUDCharacter(character, scale = .5) for character in self.party] #player huds
        self.eHuds = [BattleHUDEnemy(enemy) for enemy in self.formation]        #enemy hud
        self.engageHud = None                                                   #battle engage hud
        self.commandMenu = BattleMenu(self, self.party[0])                     #player's commands
        self.inMenu = False

        self.active = 0         #which character is currently selecting commands
        self.activeActor = None #which character/enemy is currently performing an action
        self.battling = False   #are commands being selected or is fighting occuring?

        #turn order lists
        self.turn = 0           #whose turn is it
        self.totalTurns = 0     #keeps track of how many player turns it has taken to defeat the enemy group
        self.turns = {}
        for character in self.party:
            character.initForBattle()
            self.turns[character] = 0
            
        for enemy in self.formation:
            enemy.initForBattle()
            self.turns[enemy] = 0
            
        self.order = []

        #target selection
        self.targetMenu = None
        self.targeting = False
        self.pointer = ImgObj(Texture(os.path.join(battlepath, "pointer.png")), frameX = 2)
        
        self.displayDelay = 0   #little delay ticker for displaying damage dealt upon a target
        self.introDelay = 100   #little intro rendering
        self.fade = ImgObj(Texture(surface = pygame.Surface((self.engine.w, self.engine.h))))
    
        #battle lost
        self.lose = False       
        self.loseMenu = MenuObj(self, ["Retry", "Give Up"], position = (self.engine.w/2, self.engine.h/2))
        
        #victory!
        self.victoryPanel = None
        
        self.additionHUD = None
        
        self.numbers = ImgObj(Texture(os.path.join(battlepath, "numbers.png")), frameX = 10)
        self.hitImg = ImgObj(Texture(os.path.join(battlepath, "hit.png")))
        self.hitImg.setAlignment("right")
        self.hitImg.setPosition(self.engine.w*.9, self.engine.h*.8)
        
        self.fade = 0
        
    #make the additionHUD if the active actor has selected to perform an addition
    def makeAdditionHUD(self):
        if isinstance(self.activeActor, Character):
            if isinstance(self.activeActor.command, ComboAttack):
                self.additionHUD = BattleHUDAddition(self.engine, self.activeActor)

    #process key input for the scene
    def keyPressed(self, key, char):
        if self.introDelay > 0: #disable input during the intro
            return
            
        if self.lose:
            self.loseMenu.keyPressed(key)
        elif self.victoryPanel:
            self.victoryPanel.keyPressed(key)
        elif self.battling:
            if self.additionHUD:
                if not self.additionHUD.end:
                    self.additionHUD.keyPressed(key)
        else:
            if key == Input.BButton:
                if self.commandMenu.step == 0:
                    self.active -= 1
                    if self.active < 0:
                        self.active = 0
                    self.commandMenu = BattleMenu(self, self.party[self.active])
                if self.targeting:
                    self.targeting = False
                    
            self.commandMenu.keyPressed(key)
    
    def select(self, index):
        if self.lose:
            if index == 0:
                self.engine.changeScene("BattleSystem")
            else:
                self.flee()
        elif self.targeting:
            self.party[self.active].target = self.formation[index]
            self.next()
               
    def run(self):
        for hud in self.huds:
            hud.update()
            
        #win battle
        if len(self.formation) == 0 and not self.victoryPanel:
            self.victory()
            
        #lose battle
        elif self.incapParty == len(self.party):
            self.lose = True
        
        if self.battling:
            if self.additionHUD is not None:
                if not self.additionHUD.end:
                    self.additionHUD.run()
                else:
                    self.additionHUD = None
            else:
                self.execute()
        
    #organizes all the turns for order of execution
    def battleStart(self):
        self.turn = 0
        
        #this needs to be called in case an enemy or actor has died
        self.turns = {}
        for character in self.party:
            if not character.incap:
                self.turns[character] = 0
            
        for enemy in self.formation:
            self.turns[enemy] = 0

        for character in self.party:
            self.turns[character] = random.randint(0, 50) + character.spd

        for enemy in self.formation:
            self.turns[enemy] = random.randint(0, 50) + enemy.spd
            enemy.getCommand(self.generateEnemyTargets(enemy))  #gets enemy's command and target
        
        #automatically puts actors who are defending or boosting first in order
        for actor in self.turns.keys():
            if isinstance(actor, Defend) or isinstance(actor, Boost):
                self.turns[actor] = 1000
                
        self.order = sorted(self.turns.items(), key=itemgetter(1))
    
        self.activeActor = self.order[self.turn][0]
        self.battling = True
        
        self.makeAdditionHUD()
            
    #executes all of the commands
    def execute(self):
        actor = self.activeActor
        if actor.incap:
            self.next()
        
        '''
        if self.displayDelay >= 100:
            actor.turnStart()
            anim = actor.command.animation
            if anim:
                self.displayDelay = 100
            else:
                self.displayDelay = 110
        '''    
        if self.displayDelay <= 110:
            return
        if self.displayDelay >= 360:
            if actor.target != None:
                if not actor.damage == "Miss":
                    actor.target.currentHP -= actor.damage
                if actor.target.currentHP <= 0:
                    if isinstance(actor.target, Character):
                        self.incapParty += 1
                    if isinstance(actor.target, Enemy):
                        self.formation.remove(actor.target)
                    actor.target.incap = True
                    #makes sure to remove the target from the order so they 
                    #don't attack if they die before their turn
                    for i, target in enumerate(self.order):
                        if target[0] == actor.target:
                            self.order.pop(i)
                            if i < self.turn:
                                self.turn -= 1
                            break
                self.next()
            else:
                if isinstance(actor.command, Flee):
                    if actor.command.success:
                        self.end()
                self.next()

    #generates the target list for enemies and auto-targetting
    def generateEnemyTargets(self, actor):
        targets = []
        if isinstance(actor, Character):
            targetGroup = self.formation
        else:
            targetGroup = self.party
        for t in targetGroup:
            if not t.incap:
                targets.append(t)
        return targets
       
    #generates the target list for allies
    def generateTargets(self, actor):

        if isinstance(actor, Character):
            targets = [enemy.name for enemy in self.formation]
        else:
            targets= [member.name for member in self.party]

        position = (self.engine.w - 150, self.engine.h/2 + 30*len(targets)/2)
        return targets
    
    #creates the menu for target selection and activates targeting
    def selectTarget(self):
        self.targetMenu = self.generateTargets(self.party[self.active])
        self.targeting = True
        
    #advances the character for command selection
    def next(self):
        if self.battling:
            self.additionHUD = None
            #if a character in the user's party just acted, then increment the number of total turns
            if isinstance(self.activeActor, Character):
                self.totalTurns += 1
            self.displayDelay = 0
            self.turn += 1
            if self.turn >= len(self.order) or len(self.formation) == 0:
                self.battling = False
                self.active = -1
                for actor in self.party:
                    actor.turnEnd()
                for actor in self.formation:
                    actor.turnEnd()
                self.activeActor = None
                self.engageHud = None
                self.next()
                return
            self.activeActor = self.order[self.turn][0]
            
            #should be performed before the turn officially executes
            if self.activeActor.target != None:
                #if the actor's target was knocked out during this phase then a new target
                # is automatically selected and damage is recalculated
                if self.activeActor.target.incap:
                    targets = self.generateEnemyTargets(self.activeActor)
                    if len(targets) < 1:
                        self.next()
                        return
                    self.activeActor.target = random.choice(targets)

            self.makeAdditionHUD()
            if self.activeActor.target:
                self.engageHud = BattleHUDEngage(self.activeActor)
            else:
                self.engageHud = None
        else:
            self.active += 1
            if self.active < len(self.party):
                self.commandMenu = BattleMenu(self, self.party[self.active])
            else:
                self.commandMenu = None
                self.battleStart()
            self.targeting = False
       
    def renderBase(self, visibility):
        self.header.setPosition(self.engine.w/2, self.engine.h-self.header.height/2)
        self.header.draw()
        
        if self.battling:
            self.text.setText("Fight it out")
        elif self.targeting:
            self.text.setText("Select your target")
        else:
            self.text.setText("Choose a command")
        
        self.text.setAlignment("left")
        self.text.setPosition(32.0, self.engine.h-self.header.height/2)
        self.text.draw()
        
        self.footer.setPosition(self.engine.w/2, self.footer.height/2)
        self.footer.draw()
    
    def renderBattleInterface(self, visibility):
        actor = self.activeActor
        target = actor.target
        
        y = self.footer.height/2
        
        self.text.setAlignment("center")
        self.text.setText(actor.name)
        self.text.setPosition(self.engine.w/8, y+16)
        self.text.draw()
        self.text.setText("HP: %s" % actor.hp)
        self.text.setPosition(self.engine.w/8+16, y-24)
        self.text.draw()
        
        if target is not actor and target is not None:
            self.text.setText(target.name)
            self.text.setPosition(self.engine.w/8*7, y+16)
            self.text.draw()
            self.text.setText("HP: %s" % actor.hp)
            self.text.setPosition(self.engine.w/8*7-16, y-24)
            self.text.draw()
            
            self.vs.setPosition(self.engine.w/2, self.footer.height/2)
            self.vs.draw()
        else:
            if isinstance(actor.command, Boost):
                self.boost.setPosition(self.engine.w/8*5, y)
                self.boost.draw()
            elif isinstance(actor.command, Defend):
                self.defend.setPosition(self.engine.w/8*5, y)
                self.defend.draw()
            
    def renderCommandInterface(self, visibility):
        actor = self.party[self.active]
        sprite = actor.getSprite()
        
        if self.targeting:
            actor = self.formation[self.commandMenu.index]
            sprite = actor.getSprite()
            align = "right"
            x = self.engine.w
            y = self.footer.height+self.infohud.height/2
                
            self.infohud.setAlignment(align)
            self.infohud.setPosition(x, y)
            self.infohud.setScale(1,1)
            self.infohud.draw()
        
            self.smtext.setText(actor.name)
            self.smtext.setAlignment(align)
            self.smtext.setPosition(x, y+16)
            self.smtext.draw()
            self.smtext.setText("HP: %s" % actor.hp)
            self.smtext.setAlignment(align)
            self.smtext.setPosition(x, y)
            self.smtext.draw()

        for i, hud in enumerate(self.huds):
            hud.setPosition(20, self.engine.h - self.header.height - 50 - 110*i)
            hud.draw()
            
        self.commandMenu.render(visibility)
            
    #renders the spiffy intro animation
    def renderIntro(self, visibility):
      
        for i, member in enumerate(self.party):
            sprite = member.getSprite()
            sprite.setPosition(self.engine.w*.8 + 15*i, self.engine.h*.6 - 45*i)
            self.engine.drawAnimation(sprite, loop = True, reverse = False, delay = 20)
        
        for enemy in self.formation:
            sprite = enemy.getSprite()
            sprite.draw()
            
        self.bigText.setText(self.engine.formation.name)
        self.bigText.setPosition(self.engine.w/2, self.engine.h/2 + 30)
        if self.introDelay < 20:
            self.bigText.fade((1,1,1,0), 20)
        else:
            self.bigText.fade((1,1,1,1), 60)
        self.bigText.draw()
         
        difficulty = self.engine.formation.getSelfDifficulty(self.party)
        if difficulty > 0:
            for i in range(int(difficulty)):
                pos = (self.engine.w/2 - (self.diffStar.width/2 + 10)*(difficulty-1) + (self.diffStar.width + 10) * i,
                        self.engine.h/2 - 30)
                self.engine.drawImage(self.diffStar, position = pos)
        self.introDelay -= 2
        
    def renderBattle(self, visibility):
        actor = self.activeActor
        target = actor.target
        spriteA = actor.getSprite()
        spriteA.setPosition(self.engine.w*.25+20*min(self.displayDelay/100.0,1), self.engine.h*.5)
        spriteA.setScale(-1,1)
        spriteA.setColor((1,1,1,self.displayDelay/100.0))
        self.engine.drawAnimation(spriteA)

        if target is not actor and target is not None:
            spriteB = target.getSprite()
            spriteB.setPosition(self.engine.w*.75-20*min(self.displayDelay/100.0,1), self.engine.h*.5)
            spriteB.setScale(1,1)
            spriteB.setColor((1,1,1,self.displayDelay/100.0))
            self.engine.drawAnimation(spriteB)
        else:
            spriteB = spriteA
            
        self.displayDelay += 5
        '''
        if self.displayDelay >= 100 and self.displayDelay < 110:
            if actor.command.draw():
                self.displayDelay = 100
                return
            else:
                self.displayDelay = 110
        '''
        if target != None and self.displayDelay >= 110:
            
            #draws the damage on screen
            if self.displayDelay > 300:
                a = (360 - self.displayDelay)/60.0
            else:
                a = 1

            d = str(actor.damage)
            if d is not "Miss":
                x = self.hitImg.position[0]
                y = self.hitImg.position[1]
                for i, n in enumerate(d[::-1]):
                    self.engine.drawImage(self.numbers, position = (x - self.hitImg.width - 3 + (self.numbers.width-25)*i+2, y-2), frameX = int(n), color = (0,0,0,a))
                    self.engine.drawImage(self.numbers, position = (x - self.hitImg.width - 3 + (self.numbers.width-25)*i, y), frameX = int(n), color = (1,1,1,a))
                self.engine.drawImage(self.hitImg, position = (x+2, y-2), color = (0,0,0,a))
                self.engine.drawImage(self.hitImg, position = (x, y), color = (1,1,1,a))

    def render(self, visibility):
        self.terrain.drawBackground()
        
        #if the battle is lost nothing else needs to be drawn or processed
        if self.lose:
            self.loseMenu.render(visibility)
            return
            
        #if the battle is won nothing else needs to be drawn
        if self.victoryPanel:
            self.victoryPanel.render()
            return
            
        if self.introDelay <= 0:
            self.renderBase(visibility)
            if self.battling:
                self.renderBattle(visibility)
                self.renderBattleInterface(visibility)
            else:
                self.renderCommandInterface(visibility)
        else:
            self.renderIntro(visibility)
    
    #show the victory screen
    def victory(self):
        self.victoryPanel = VictoryPanel(self, self.totalTurns)
        self.music = BGMObj(self.victorySong)
                
    def end(self):
        self.music.fadeToStop()
        self.engine.viewport.pop(self)
        
