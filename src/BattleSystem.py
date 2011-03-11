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
from Enemy import Enemy

import string
import Input

from MenuObj import MenuObj

from BattleHUDCharacter import BattleHUDCharacter
from BattleHUDEnemy import BattleHUDEnemy
from BattleHUDEngage import BattleHUDEngage
from BattleHUDAddition import BattleHUDAddition
from BattleMenu import BattleMenu
from VictoryPanel import VictoryPanel
   
#unlike most other scenes in this game, the battle scene 
#is completely controlled by the keyboard instead of mouse
class BattleSystem(Scene):
    def __init__(self, engine):

        self.engine = engine
        self.camera = self.engine.viewport.camera   #for simplicity's sake
        
        w, h = self.engine.w, self.engine.h

        musicpath = os.path.join("audio", "music", "battle")
        songs = self.engine.listPath(musicpath, "ogg")
        songs.append(self.engine.listPath(musicpath, "mp3"))
        if len(songs) > 0:
            song = random.choice(songs)[0]
            print song
            BGMObj(os.path.join("battle", song))
        
        self.background = self.engine.formation.terrain
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        
        battlepath = os.path.join("scenes", "battlesystem")
        self.activeHighlight = ImgObj(Texture(os.path.join(battlepath, "active_highlight.png")))
        
        self.diffStar = ImgObj(Texture(os.path.join(battlepath, "star.png")))
        
        fontStyle = self.engine.data.defaultFont
        self.text = FontObj(fontStyle, size = 32.0)
        self.bigText = FontObj(fontStyle, size = 64.0)

        self.party = [m for m in self.engine.family.party]
        self.formation = [e for e in self.engine.formation.enemies]

        self.incapParty = 0     #keeps track of how many in the party are incapacitated
                                #when all members are then the battle is over
        
        #self.start = ImgObj(Texture("start.png"))
        #self.start.setPosition(self.engine.w / 2, self.engine.h / 2)

        self.huds = [BattleHUDCharacter(character) for character in self.party] #player huds
        self.eHuds = [BattleHUDEnemy(enemy) for enemy in self.formation]        #enemy hud
        self.engageHud = None                                                   #battle engage hud
        self.commandWheel = BattleMenu(self, self.party[0])                     #player's commands
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
        self.introDelay = 500   #little intro rendering
        self.fade = ImgObj(Texture(surface = pygame.Surface((self.engine.w, self.engine.h))))
    
        #battle lost
        self.lose = False       
        self.loseMenu = MenuObj(self, ["Retry", "Give Up"], position = (self.engine.w/2, self.engine.h/2))
        
        #victory!
        self.victoryPanel = None
        
        self.additionHUD = None

    def keyPressed(self, key, char):
        if self.introDelay > 0:
            return
            
        if self.lose:
            self.loseMenu.keyPressed(key)
        elif self.victoryPanel:
            self.victoryPanel.keyPressed(key)
        elif self.battling:
            if self.additionHUD:
                self.additionHUD.keyPressed(key)
            return
            
        else:
            if key == Input.BButton:
                if self.commandWheel.step == 0:
                    self.active -= 1
                    if self.active < 0:
                        self.active = 0
                    self.commandWheel = BattleMenu(self, self.party[self.active])
                if self.targeting:
                    self.targeting = False
                    
            self.commandWheel.keyPressed(key)
    
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
                print self.additionHUD.comboTimer
                if self.additionHUD.comboTimer > 0:
                    self.additionHUD.run()
                else:
                    self.activeActor.comboComplete = self.additionHUD.success
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
            if not (character.boost or character.defend):
                self.turns[character] = random.randint(0, 50) + character.spd

        for enemy in self.formation:
            if not (enemy.boost or enemy.defend):
                self.turns[enemy] = random.randint(0, 50) + enemy.spd
                enemy.getCommand(self.generateEnemyTargets(enemy))  #gets enemy's command and target
        
        self.order = sorted(self.turns.items(), key=itemgetter(1))
    
        self.activeActor = self.order[self.turn][0]
        self.battling = True
        
        if isinstance(self.activeActor, Character):
            if self.activeActor.performingCombo:
                print "made hud"
                self.additionHUD = BattleHUDAddition(self.engine, self.activeActor)
            
    #executes all of the commands
    def execute(self):
        actor = self.activeActor
        if actor.incap:
            self.next()
        
        if self.displayDelay == 0:
            actor.turnStart()
            
        if actor.target != None:
            #if the actor's target was knocked out during this phase then a new target
            # is automatically selected and damage is recalculated
            if actor.target.incap:
                targets = self.generateEnemyTargets(actor)
                if len(targets) < 1:
                    self.next()
                    return
                actor.target = random.choice(targets)
                actor.calculateDamage()
            
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

        if actor.attacking or actor.cast:
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
            self.activeActor.turnEnd()
            #if a character in the user's party just acted, then increment the number of total turns
            if isinstance(self.activeActor, Character):
                self.totalTurns += 1
            self.displayDelay = 0
            self.turn += 1
            if self.turn >= len(self.order) or len(self.formation) == 0:
                self.battling = False
                self.turn = 0
                self.active = -1
                self.next()
            self.activeActor = self.order[self.turn][0]
            if isinstance(self.activeActor, Character):
                if self.activeActor.performingCombo:
                    print "made hud"
                    self.additionHUD = BattleHUDAddition(self.engine, self.activeActor)
            if self.activeActor.target:
                self.engageHud = BattleHUDEngage(self.activeActor)
            else:
                self.engageHud = None
        else:
            self.active += 1
            if self.active < len(self.party):
                self.commandWheel = BattleMenu(self, self.party[self.active])
            else:
                self.commandWheel = None
                self.battleStart()
            self.targeting = False
    
    #renders the character huds
    def renderHUDS(self, visibility):
        huds = [h for h in self.huds]

        if self.battling:
            for i, hud in enumerate(huds):
                hud.scale = .5
                hud.setPosition(0, (self.engine.h-32*i-48)*(1/hud.scale))
                hud.draw()
        else:
            if self.active < len(self.party):
                hud = huds.pop(self.active)
                hud.scale = 1.0
                hud.setPosition(0, self.engine.h - 40)
                hud.draw()
                
            for i, hud in enumerate(huds):
                hud.scale = .5
                hud.setPosition(0, (self.engine.h-32*(i+1)-64)*(1/hud.scale))
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
                self.eHuds[self.commandWheel.index].update()
                self.eHuds[self.commandWheel.index].draw()
                target = self.formation[self.commandWheel.index].getSprite()
                self.pointer.setPosition(target.position[0], target.position[1] + target.height/2 + 20)
                self.pointer.setFrame(x = 2)
                self.pointer.draw()
            self.commandWheel.render(visibility)
            
    #renders the active highlight and damage
    def renderBattle(self, visibility):
        actor = self.activeActor
            
        #eyecandy highlight for who is currently attacking
        pos = (actor.getSprite().position[0], actor.getSprite().position[1] - actor.getSprite().height/2)
        self.activeHighlight.setPosition(pos[0], pos[1])
        self.activeHighlight.setScale(actor.getSprite().width, 16, True)
        self.activeHighlight.draw()
            
      
        if actor.target != None and self.engageHud:
            self.engageHud.draw()
            
        if self.additionHUD:
            print "drawing addition"
            self.additionHUD.draw()
            return
            
        if actor.target != None and self.displayDelay < 100:
            pos = actor.target.getSprite().position    
            #draws the damage on screen
            bounce = lambda t:(-.017*t**2 + .0134*t + pos[1])+50
            y = bounce(self.displayDelay-25)
            if self.displayDelay > 50:
                color = (1,1,1, (250 - self.displayDelay)/250.0)
            else:
                color = (1,1,1,1)
            self.engine.drawText(self.text, actor.damage, position = (pos[0], y), color = color)

        
    #renders the spiffy intro animation
    def renderIntro(self, visibility):
        if self.introDelay > 450:
            zoom = 100*(1.0+3*(500.0-self.introDelay)/50.0)
        elif self.introDelay > 150:
            zoom = 400
        elif self.introDelay > 100:
            zoom = 100*(4.0-3.0*(150.0-self.introDelay)/50.0)
        else:
            zoom = 100
                
        if self.introDelay > 350:
            pos = self.party[len(self.party)/2].getSprite().position
            if self.introDelay > 450:
                pos = (self.engine.w/2 + (pos[0]-self.engine.w/2)*((500.0-self.introDelay)/50.0),
                        self.engine.h/2 + (pos[1]-self.engine.h/2)*((500.0-self.introDelay)/50.0))
                    
        elif self.introDelay > 250 and self.introDelay < 350:
            aPos = self.party[len(self.party)/2].getSprite().position
            bPos = self.formation[len(self.formation)/2].getSprite().position 
            pos = (aPos[0]-(aPos[0]-bPos[0])*(1.0-abs(self.introDelay-250.0)/100.0),
                    aPos[1]-(aPos[1]-bPos[1])*(1.0-abs(self.introDelay-250.0)/100.0))
        elif self.introDelay > 100:
            pos = self.formation[len(self.formation)/2].getSprite().position
            if self.introDelay < 150:
                pos = (self.engine.w/2 - (self.engine.w/2-pos[0])*(abs(self.introDelay-100.0)/50.0),
                        self.engine.h/2 - (self.engine.h/2-pos[1])*(abs(self.introDelay-100.0)/50.0))
            
        if self.introDelay > 100:
            self.camera.focus(pos[0], pos[1], zoom)
        else:
            self.camera.resetFocus()
            
        if self.introDelay > 0 and self.introDelay < 100:
            alpha = 1.0
            if self.introDelay < 20:
                alpha = self.introDelay/20.0
            self.engine.drawText(self.bigText, self.engine.formation.name, (self.engine.w/2, self.engine.h/2 + 30),
                                    color = (1,1,1,alpha)) 
            difficulty = self.engine.formation.getDifficulty(self.party)
            if difficulty > 0:
                for i in range(difficulty):
                    pos = (self.engine.w/2 - (self.diffStar.width/2 + 10)*(difficulty-1) + (self.diffStar.width + 10) * i,
                            self.engine.h/2 - 30)
                    self.engine.drawImage(self.diffStar, position = pos)
        self.introDelay -= 2
        
    def render(self, visibility):
        self.background.draw()
        
        for i, member in enumerate(self.party):
            sprite = member.getSprite()
            sprite.setPosition(self.engine.w*.8 - 20*i, self.engine.h*.4 + 65*i)
            if self.introDelay < 450 and self.introDelay > 400:
                alpha = (450.0-self.introDelay)/50.0
            elif self.introDelay >= 450:
                alpha = 0.0
            else:
                alpha = 1.0
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
            self.renderHUDS(visibility)
            if not self.battling:
                self.renderInterface(visibility)
            else:
                self.renderBattle(visibility)
        else:
            self.renderIntro(visibility)
    
    #show the victory screen
    def victory(self):
        self.victoryPanel = VictoryPanel(self, self.totalTurns)
        
    def end(self):
        if self.engine.town:
            self.engine.viewport.changeScene("Town")
        else:
            self.engine.viewport.changeScene("Maplist")
