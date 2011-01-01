

#skills are a main part of battle
#Passive skills are skills that effect the character at all times
#   these are usually weapon proficiency buffs or stat buffs dependent
#   on their class
#Active skills are skills that can be used in battle like healing
#   or attack magic.
class Skill:
    def __init__(self, job, lvl = 0):
        pass
        
class SwordMastery(Skill):
    def __init__(self, job, l = 0):
        
        self.job = job
        
        self.name = "Sword Mastery"
        self.level = l
        
        #adds .5 level to the sword proficiency of the job for every level it goes up
        self.job.swordProf += 50.0*self.level
        
        
        
        
