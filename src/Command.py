
import sysobj
import random
from math import *

from Character import Character

#command objects are specifically for the battle system
class Command(object):
    def __init__(self, actor):
	self.parent = actor		#actor who is performing the command
	self.animation = None		#animation to be displayed upon execution in battle
	self.fpCost = 0
	
    #what happens when the command is executed
    def execute(self):
	pass
    
    #any post execution effects that need to be processed,
    #such as decrementing fp
    def reset(self):
	self.parent.fp -= self.fpCost
	
    #will draw the corresponding animation for the command
    # returning False signifies the animation is done
    # returning True signifies the animation is still running
    def draw(self):
	return self.animation.draw()
	
    #returns a string representation of the command for use in menus
    def __str__(self):
	return "command FP: %i" % self.fpCost
	
class Attack(Command):
    def __init__(self, actor, style = 0):
	super(Attack, self).__init__(actor)
	if isinstance(self.parent, Character):
	    self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	else:
	    self.animation = self.parent.attackAnimation
	    
	self.style = style	#3 different styles of attack
				#  0 - normal
				#  1 - aim, 100% accuracy but weaker
				#  2 - strong, 50% accuracy but 200% stronger
	#special attacks cost more fp
	if self.style is not 0:
	    self.fpCost = 45
	else:
	    self.fpCost = 30
	    
    def execute(self):
	#enemies need to be processed differently attack wise for determining chance of landing the blow
	if isinstance(self.parent, Character):
	    factor = (self.parent.proficiency*2)
	else:
	    factor = random.randint(0, 255)
	    
	if self.style == 1:
	    hit = True
	elif self.style == 2:
	    hit = factor - self.parent.target.evd >= self.parent.target.evd*3
	else:
	    hit = factor - self.parent.target.evd >= self.parent.target.evd*1.5
        
	if hit:
	    damage = self.parent.str - (self.parent.target.defn * 1.368295)
	    if self.style == 1:
		damage /= 1.5
	    elif self.style == 2:
		damage *= 2
	    damage = max(0, int(damage))
	else:
            damage = "Miss"
	self.parent.damage = damage
	
	if isinstance(self.parent.target.command, Defend):
	    if isinstance(self.parent, Character):
		self.animation = self.parent.equipment[self.parent.hand].defendAnimation
	    else:
		self.animation = self.parent.defendAnimation
	else:
	    if isinstance(self.parent, Character):
		self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	    else:
		self.animation = self.parent.attackAnimation
	self.animation.currentFrame = 0
	self.animation.setParent(self.parent.target.getSprite())
	if isinstance(self.parent.target, Character):
	    self.animation.flip = -1
	else:
	    self.animation.flip = 1
	    
    def __str__(self):
	if self.style == 1:
	    name = "Accurate"
	elif self.style == 2:
	    name = "Strong"
	else:
	    name = "Normal"
	return "%s FP: %i" % (name, self.fpCost)	
	    	    
class Cast(Command):
    def __init__(self, actor, skill):
	self.parent = actor
	self.skill = skill
	
    def execute(self):
        self.parent.damage = (self.mag + self.skill.damage) - (self.parent.target.res * 1.368295)

#difference between UseItem and Cast is UseItem's damage is constant
class UseItem(Cast):
    def execute(self):
	self.parent.damage = self.skill.damage
	
class ComboAttack(Command):
    def __init__(self, actor):
	super(ComboAttack, self).__init__(actor)
	self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	self.fpCost = 65
	self.complete = False
	self.weapon = self.parent.equipment[self.parent.hand]
	self.keys = self.weapon.attack				#the list of input keys that need to be hit
	self.timer = self.weapon.time 				#time given to perform the attack
	self.keyIndex = 0
	
    #handle the execution of the combo attack
    def runTimer(self, timer):
	self.timer = max(self.timer - timer, 0)
	if self.timer <= 0:
	    self.complete = False
	    return True
	return False
	
    def runKey(self, key):
	if key == self.keys[self.keyIndex]:
	    self.keyIndex += 1
	else:
	    self.complete = False
	    return True
	
	if self.keyIndex >= len(self.keys):
	    self.complete = True
	    return True
	
	return False
	
    def execute(self):
	if self.complete:
	    damage = (self.parent.str*1.25 - (self.parent.target.defn * 1.368295))*len(self.keys)
	    damage = max(0, int(damage))
	else:
            damage = "Miss"
	self.parent.damage = damage

	if isinstance(self.parent.target.command, Defend):
	    if isinstance(self.parent, Character):
		self.animation = self.parent.equipment[self.parent.hand].defendAnimation
	    else:
		self.animation = self.parent.defendAnimation
	else:
	    if isinstance(self.parent, Character):
		self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	    else:
		self.animation = self.parent.attackAnimation
	self.animation.currentFrame = 0
	self.animation.setParent(self.parent.target.getSprite())
	if isinstance(self.parent.target, Character):
	    self.animation.flip = -1
	else:
	    self.animation.flip = 1
	        
    def __str__(self):
	return "%s FP: %i" % ("Combo", self.fpCost)
	
#when a character defends they gain the normal amount of FP per turn (20%)
#but their def is multiplied by 250%
class Defend(Command):
    def __init__(self, actor):
	super(Defend, self).__init__(actor)
	
    def execute(self):
	self.parent.defn *= 2.5
	
    def reset(self):
	self.parent.defn /= 2.5
	
    def __str__(self):
	return "Defend (Def * 2.5)"
	
#when an actor boosts instead of defends,
#their def is halved but they get full FP the next turn
class Boost(Command):
    def __init__(self, actor):
	super(Boost, self).__init__(actor)
	
    def execute(self):
	self.parent.defn *= .5
	
    def reset(self):
	self.parent.fp = self.parent.maxFP
	self.parent.defn *= 2
	
    def __str__(self):
	return "Boost (Full FP)"
	        	
#Guns and Bows have 4 different firing modes
#Single is default for all
#Guns can have either Double shot or Burst+Auto firing modes
#Bows can also have Double
#since this is heavily dependent on equipment, 
#  only characters should use this command
class Shoot(Command):
    def __init__(self, actor, style = 0):
	super(Shoot, self).__init__(actor)
	
	self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	    
	self.style = style	#4 different styles of attack
				#  0 - single
				#  1 - double, 50% accuracy but 200% stronger
				#  2 - burst, 75% accuracy, 3 hits
				#  3 - auto, 50% accuracy, 5 hits
	
	#because guns have a lot of recoil and bows you have to pull back hard on to fire
	# on average they will use more energy to fight with than close range weapons
	#additionally the different types of firing take more energy
	if self.style == 1:
	    self.fpCost = 50
	elif self.style == 2:
	    self.fpCost = 55
	elif self.style == 3:
	    self.fpCost = 65
	else:
	    self.fpCost = 40
	
    #get the amount of damage dealt per hit
    def getDamage(self):
	factor = (self.parent.proficiency*2)
	if self.style == 1 or self.style == 3:
	    hit = factor - self.parent.target.evd >= self.parent.target.evd*3
	elif self.style == 2:
	    hit = factor - self.parent.target.evd >= self.parent.target.evd*2
	else:
	    hit = factor - self.parent.target.evd >= self.parent.target.evd*1.5
        
	if hit:
	    return self.parent.str - (self.parent.target.defn * 1.368295)
	else:
	    return 0
	    
    def execute(self):
	
	damage = 0
	#double shot
	if self.style == 1:
	    damage += 2*self.getDamage()
	#burst
	elif self.style == 2:
	    for i in range(3):
		damage += self.getDamage()
	#auto
	elif self.style == 3:
	    for i in range(5):
		damage += self.getDamage()
	#single
	else:
	    damage += self.getDamage()
	damage = max(0, int(damage))
	
	self.parent.damage = damage
	
	self.animation = self.parent.equipment[self.parent.hand].attackAnimation
	
	self.animation.currentFrame = 0
	self.animation.setParent(self.parent.target.getSprite())
	if isinstance(self.parent.target, Character):
	    self.animation.flip = -1
	else:
	    self.animation.flip = 1

    def __str__(self):
	if self.style == 1:
	    name = "Double"
	elif self.style == 2:
	    name = "Burst"
	elif self.style == 3:
	    name = "Auto"
	else:
	    name = "Single"
	return "%s FP: %i" % (name, self.fpCost)

class Flee(Command):
    def __init__(self, party, formation):
	self.success = False
	
	self.party = party
	self.formation = formation
	
    #chance of fleeing should be determined by comparing party's stat's to the formations
    #it should be harder to flee when the party is almost dead and easier to flee when the
    #enemies formation is almost vanquished
    def execute(self):
	self.success = (random.randint(self.party.avgSpd, 100) / Formation.getDifficulty(self.formation, self.party.getAlive())) > 50
	
    def __str__(self):
	return "Flee"
