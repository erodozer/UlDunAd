
import os

from Config import Configuration

_itemMax = 99       #maximum amount of one item the family can hold

class Inventory:
    def __init__(self, family):
        
        self.family = family        #save data for the inventory
        
        #gathers all the different enemy types
        path = os.path.join("..", "data", "items")
        items = os.listdir(path)
        items.sort()
        
        path = os.path.join("..", "data", "actors", "families", family.name, "inventory.ini")
        if not os.path.exists(path):
            Configuration(path).save()
            self.catalog = Configuration(path)
            self.catalog.inventory.__setattr__(items[0], 0)
            self.catalog.save()
       
        self.catalog = Configuration(path)
        
        self.items = {}
        def loadList():
            changeMade = False
            for i in items:
                try:
                    ini = Configuration(os.path.join("..", "data", "items", i, "item.ini"))
                    #detecting what type of item it is
                    if ini.parser.has_section("weapon"):
                        item = Weapon(i)
                    elif ini.parser.has_section("armor"):
                        item = Armor(i)
                    else:
                        item = Item(i)
                    self.items[i] = [item, self.catalog.inventory.__getattr__(i, int)]
                except:
                    self.catalog.inventory.__setattr__(i, 0)
                    self.catalog.save()
                
        loadList()
       
    #adds the amount of said item to the inventory
    # do not use negative numbers to remove item, use removeItem method instead
    def addItem(self, name, amount):
        self.items[name][1] = Math.max(_itemMax, self.items[name][1]+amount)
        
    #removes the amount of said item from the inventory
    def removeItem(self, name, amount):
        self.items[name][1] = Math.max(_itemMax, self.items[name][1]-amount)
        
    #creates string rep of the inventory
    def __str__(self):
        str = ""
        for i, item in enumerate(self.items.keys()):
            str += "%03i: %-16s%02i\n" % (i+1, self.items[item][0].name, self.items[item][1])
        return str
    
    def update(self):
        for item in self.items.keys():
            self.catalog.inventory.__setattr__(item, self.items[item][1])
        self.catalog.save()
        self.catalog = Configuration(path)
