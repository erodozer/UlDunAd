
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
	pass
	
class Attack(Command):
    def execute(self):
	hit = (self.parent.proficiency*2) - self.parent.target.evd >= self.parent.target.evd*1.5
        
	if hit:
	    self.parent.damage = self.parent.str - (self.parent.target.defn * 1.368295)
	    self.parent.damage = max(0, int(self.damage))
	else:
            self.parent.damage = "Miss"
        
class Cast(Command):
    def __init__(self, actor):
	self.parent = actor
	self.animation = self.parent.command.animation
	
    def execute(self):
        self.parent.damage = (self.mag + self.command.damage) - (self.parent.target.res * 1.368295)
            
class ComboAttack(Command):
    def execute(self):
        hit = self.parent.comboComplete
        if hit:
	    self.parent.damage = (self.str*1.25 - (self.target.defn * 1.368295))*len(self.equipment[self.hand].attack)
        else:
            self.parent.damage = "Miss"
        
class Defend(Command):
    def __init__(self, actor):
	super(Defend, self).__init__(actor)
	
    def execute(self):
	self.parent.defn *= 2.5
	
    def reset(self):
	self.parent.defn /= 2.5
	
class Boost(Command):
    def __init__(self, actor):
	super(Boost, self).__init__(actor)
	
    def execute(self):
	self.parent.defn *= 2.5
	
    def reset(self):
	self.parent.fp = self.parent.maxFP
	self.parent.defn *= 2
        	
