from Config import Configuration

class Item:
    def __init__(self, name):
        itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).item
        
class Weapon(Item):
    def __init__(self, name):
        self.name = name
        self.type = "unknown"
        self.str  = 0
        
class Armor(Item):
    def __init__(self, name):
        Item.__init__(self, name)
        
        self.defn = itemini.__getattr__("def", int)
        self.spd  = itemini.__getattr__("str", int)
        self.evd  = itemini.__getattr__("evd", int)
        self.mag  = itemini.__getattr__("mag", int)
        self.res  = itemini.__getattr__("res", int)

        
        
