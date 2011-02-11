from Config import Configuration
import os

class Item:
    def __init__(self, name):
        if (not name) or name == "None":
            return None
            
        try:
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).item
        except:
            return None
            
        self.name = name
        
class Weapon(Item):
    def __init__(self, name):
        if not name or name == "None":
            return None
        
        try:
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).weapon
        except:
            None
            
        self.name = name
        self.type = "unknown"
        self.str  = 0
        
class Armor(Item):
    def __init__(self, name):
        if not name or name == "None":
            return None
        
        try:
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).armor
        except:
            return None
            
        self.name = name
        self.defn = itemini.__getattr__("def", int)
        self.spd  = itemini.__getattr__("str", int)
        self.evd  = itemini.__getattr__("evd", int)
        self.mag  = itemini.__getattr__("mag", int)
        self.res  = itemini.__getattr__("res", int)

        
        
