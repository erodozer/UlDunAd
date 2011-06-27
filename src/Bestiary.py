
import os

from Config import Configuration

class Bestiary:
    def __init__(self, family):
        
        self.family = family        #save data for the bestiary
        
        path = os.path.join("..", "data", "actors", "enemies")
        enemies = os.listdir(path)
        enemies.sort()
        
        path = os.path.join("..", "data", "actors", "families", family.name, "bestiary.ini")
        if not os.path.exists(path):
            Configuration(path).save()
            self.catalog = Configuration(path)
            self.catalog.bestiary.__setattr__(enemies[0], 0)
            self.catalog.save()
       
        self.catalog = Configuration(path)
        
        self.beasts = []
        for beast in enemies:
            try:
                self.beasts.append([beast, self.catalog.bestiary.__getattr__(beast, int)])
            except:
                self.catalog.bestiary.__setattr__(beast, 0)
                self.catalog.save()
                self.catalog = Configuration(path)
                self.beasts.append([beast, self.catalog.bestiary.__getattr__(beast, int)])
                
              
    def __str__(self):
        str = ""
        for i, beast in enumerate(self.beasts):
            str += "%03i: %-16s%02i\n" % (i+1, beast[0], beast[1])
        return str
