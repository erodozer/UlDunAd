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
            
        self.music = BGMObj(self.battleSong)
        
        battlepath = os.path.join("scenes", "battlesystem")
        self.activeHighlight = ImgObj(Texture(os.path.join(battlepath, "active_highlight.png")))
        
        self.diffStar = ImgObj(Texture(os.path.join(battlepath, "star.png")))
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle, size = 32)
        self.bigText = FontObj(fontStyle, size = 64)

        self.party = [m for m in self.engine.family.party.members]
        self.formation = [e for e in self.engine.formation.enemies]

        self.terrain = Terrain(self, self.engine.formation.terrain)
        
        self.incapParty = 0     #keeps track of how many in the party are incapacitated
                                #when all members are then the battle is over
        
        #self.start = ImgObj(Texture("start.png"))
        #self.start.setPosition(self.engine.w / 2, self.engine.h / 2)

        self.huds = [BattleHUDCharacter(character) for character in self.party] #player huds
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
        
        if self.displayDelay == 0:
            actor.turnStart()
            anim = actor.command.animation
            if anim:
                self.displayDelay = 1
            else:
                self.displayDelay = 5
            
        if self.displayDelay == 1:
            return
        
        if actor.target != None:
            self.displayDelay += 5
            
            if self.displayDelay >= 100:
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
    
    #renders the character huds
    def renderHUDS(self, visibility):
        huds = [h for h in self.huds]

        if self.battling:
            for i, hud in enumerate(huds):
                hud.scale = .5
                hud.setPosition(self.engine.w*.7 + self.engine.w*.1*i, self.engine.h*.115)
                hud.draw()
        else:
            if self.active < len(self.party):
                hud = huds.pop(self.active)
                hud.scale = 1.0
                hud.setPosition(self.engine.w*.875, self.engine.h*.125)
                hud.draw()
                
            for i, hud in enumerate(huds):
                hud.scale = .5
                hud.setPosition(self.engine.w*.7 + self.engine.w*.04*i, self.engine.h*.11 + (self.engine.h*.13)*i)
                hud.draw()
           
    #draws the pointer arrows and the command menus
    def renderInterface(self, visibility):
        if self.active < len(self.party):
            sprite = self.party[self.active].getSprite()
            self.pointer.setScale(32,32,inPixels = True)
            self.pointer.setPosition(sprite.position[0], sprite.position[1] + sprite.height/2 + 20)
            self.pointer.setFrame(x = 1)
            self.pointer.draw()
                
            if self.targeting:
                self.eHuds[self.commandMenu.index].update()
                self.eHuds[self.commandMenu.index].draw()
                target = self.formation[self.commandMenu.index].getSprite()
                self.pointer.setPosition(target.position[0], target.position[1] + target.height/2 + 20)
                self.pointer.setFrame(x = 2)
                self.pointer.draw()
            self.commandMenu.render(visibility)
            
    #renders the active highlight and damage
    def renderBattle(self, visibility):
        #draws order of the next 2 turns
        for i in range(min(3, len(self.order)-self.turn)):
            self.engine.drawText(self.text, self.order[self.turn+i][0].name, position = (self.engine.w*.75, self.engine.h *.9 - 45*i), color = (1,1,1,1-(.33*i)))

        actor = self.activeActor
            
        #eyecandy highlight for who is currently attacking
        pos = (actor.getSprite().position[0], actor.getSprite().position[1] - actor.getSprite().height/2)
        self.activeHighlight.setPosition(pos[0], pos[1])
        self.activeHighlight.setScale(actor.getSprite().width, 16, True)
        self.activeHighlight.draw()
            
      
        if self.engageHud:
            self.engageHud.draw()
            
        if self.additionHUD:
            self.additionHUD.draw()
            return
            
        if self.displayDelay == 1:
            if actor.command.draw():
                return
            else:
                self.displayDelay = 5

        if actor.target != None and self.displayDelay < 100:
            pos = actor.target.getSprite().position    
            #draws the damage on screen
            bounce = lambda t:(-.017*t**2 + .0134*t + pos[1])+50
            y = bounce(self.displayDelay-25)
            if self.displayDelay > 50:
                a = (250 - self.displayDelay)/250.0
            else:
                a = 1

            d = str(actor.damage)
            if d is not "Miss":
                for i, n in enumerate(d[::-1]):
                    self.engine.drawImage(self.numbers, position = (pos[0]+3 + (self.numbers.width-25)*i, y-2), frameX = int(n), color = (0,0,0,a))
                    self.engine.drawImage(self.numbers, position = (pos[0] + (self.numbers.width-25)*i, y), frameX = int(n), color = (1,1,1,a))
                self.hitImg.draw()
                
    #renders the spiffy intro animation
    def renderIntro(self, visibility):
        alpha = 1.0
        if self.introDelay < 20:
            alpha = self.introDelay/20.0
        self.engine.drawText(self.bigText, self.engine.formation.name, (self.engine.w/2, self.engine.h/2 + 30),
                                color = (1,1,1,alpha)) 
        difficulty = self.engine.formation.getSelfDifficulty(self.party)
        if difficulty > 0:
            for i in range(int(difficulty)):
                pos = (self.engine.w/2 - (self.diffStar.width/2 + 10)*(difficulty-1) + (self.diffStar.width + 10) * i,
                        self.engine.h/2 - 30)
                self.engine.drawImage(self.diffStar, position = pos)
        self.introDelay -= 2
        
    def render(self, visibility):
        self.terrain.drawBackground()
        
        if self.introDelay < 450 and self.introDelay > 400:
            alpha = (450.0-self.introDelay)/50.0
        elif self.introDelay >= 450:
            alpha = 0.0
        else:
            alpha = 1.0
            
        for i, member in enumerate(self.party):
            sprite = member.getSprite()
            sprite.setPosition(self.engine.w*.8 + 15*i, self.engine.h*.6 - 45*i)
            sprite.setColor((1,1,1, alpha))
            self.engine.drawAnimation(sprite, loop = True, reverse = False, delay = 20)
        
        if self.introDelay < 250 and self.introDelay > 200:
            alpha = (250.0-self.introDelay)/50.0
        elif self.introDelay >= 250:
            alpha = 0.0
        else:
            alpha = 1.0
        for enemy in self.formation:
            sprite = enemy.getSprite()
            sprite.setColor((1,1,1,alpha))
            sprite.draw()
            
        #if the battle is lost nothing else needs to be drawn or processed
        if self.lose:
            self.loseMenu.render(visibility)
            return
            
        #if the battle is won nothing else needs to be drawn
        if self.victoryPanel:
            self.victoryPanel.render()
            return
            
        if self.introDelay <= 0:
            if not self.battling:
                self.renderInterface(visibility)
            else:
                self.renderBattle(visibility)
            self.renderHUDS(visibility)
        else:
            self.renderIntro(visibility)
    
    #show the victory screen
    def victory(self):
        self.victoryPanel = VictoryPanel(self, self.totalTurns)
        self.music = BGMObj(self.victorySong)
        
    def flee(self):
        #chance of fleeing should be determined by comparing party's stat's to the formations
        #it should be harder to flee when the party is almost dead and easier to flee when the
        #enemies formation is almost vanquished
        diff = Formation.getDifficulty(self.formation, self.party.getAlive())
        chance = random.randint(self.party.avgSpd, 100) / diff 
        if chance > 50: #successful escape
            self.end()
        
    def end(self):
        if self.engine.town:
            self.engine.viewport.changeScene("Town")
        else:
            self.engine.viewport.changeScene("Maplist")
        self.music.fadeToStop()
