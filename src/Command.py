
import sysobj

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
	
class Attack(Command):
    def __init__(self, actor, style = 0):
	super(Attack, self).__init__(actor)
	#self.animation = self.parent.equipment[self.parent.hand].animation
	self.style = style	#3 different styles of attack
				#  0 - normal
				#  1 - aim, 100% accuracy but weaker
				#  2 - strong, 50% accuracy but 200% stronger
	#special attacks cost more fp
	if self.style is not 0:
	    self.fpCost = 45
	    
    def execute(self):
	if self.style == 1:
	    hit = True
	elif self.style == 2:
	    hit = (self.parent.proficiency*2) - self.parent.target.evd >= self.parent.target.evd*3
	else:
	    hit = (self.parent.proficiency*2) - self.parent.target.evd >= self.parent.target.evd*1.5
        
	if hit:
	    damage = self.parent.str - (self.parent.target.defn * 1.368295)
	    if self.style == 1:
		damage /= 1.5
	    elif self.style == 2:
		damage *= 2
	    damage = max(0, int(self.damage))
	else:
            damage = "Miss"
	self.parent.damage = damage
    
class Cast(Command):
    def __init__(self, actor):
	self.parent = actor
	#self.animation = self.parent.command.animation
	
    def execute(self):
        self.parent.damage = (self.mag + self.command.damage) - (self.parent.target.res * 1.368295)
            
class ComboAttack(Command):
    def execute(self):
        hit = self.parent.comboComplete
        if hit:
	    self.parent.damage = (self.str*1.25 - (self.target.defn * 1.368295))*len(self.equipment[self.hand].attack)
        else:
            self.parent.damage = "Miss"
    
#when a character defends they gain the normal amount of FP per turn (20%)
#but their def is multiplied by 250%
class Defend(Command):
    def __init__(self, actor):
	super(Defend, self).__init__(actor)
	
    def execute(self):
	self.parent.defn *= 2.5
	
    def reset(self):
	self.parent.defn /= 2.5
	
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
        	
