
class Item:
    pass
class Spell:
    pass

#Creating an attack isn't as hard as one would think it would be.
#Most of the attack code is handled in the battle scene.  All you
#need to do is create an .ini with the attack name and insert the
#combo and how much time the user is alotted to perform the move.

class Attack:
    def __init__(self, name):
        attackini = Configuration(os.path.join("data", "attacks", name + ".ini")).job

        self.combo = attackini.__getattr__("combo").split()    
                                            #the buttons in the order that need to be pressed

        self.time  = attackini.__getattr__("time", int, 300.0) 
                                            #how much time you have to perform the combo, in milliseconds
                                            #default is 300 ms

        self.dam   = attackini.__getattr__("damage", int, 100.0)
                                            #a strength percentage multiplier that is applied
                                            #upon successfully performing the attack
