

#skills are a main part of battle
#Passive skills are skills that effect the character at all times
#   these are usually weapon proficiency buffs or stat buffs dependent
#   on their class
#Active skills are skills that can be used in battle like healing
#   or attack magic.
class Skill:
    def __init__(self, job, lvl = 0):
        pass

#increases one's sword proficency
class SwordMastery(Skill):
    def __init__(self, job, lvl = 0):
        
        self.job = job
        
        self.name = "Sword Mastery"
        self.level = lvl
        
        #adds .5 level to the sword proficiency of the job for every level it goes up
        self.job.swordProf += 50.0*self.level
        
        self.active = False #the skill is passive
        
#a skill that can be used in battle that inflicts fire damage on the target
class Fire(Skill):
    def __init__(self, job, lvl = 0):
        self.job = job
        self.name = "Fire"
        self.level = lvl
        
        self.damage = 50 + (5*lvl)
        
        self.active = True
        
#increases one's evasion
class Hiding(Skill):
    def __init__(self, job, lvl = 0):
        
        self.job = job
        
        self.name = "Hiding"
        self.level = lvl
        
        #adds .5 level to the sword proficiency of the job for every level it goes up
        self.job.evd += 3.0*self.level
        
        self.active = False #the skill is passive
        
        
        
