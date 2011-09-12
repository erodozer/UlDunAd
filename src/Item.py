from Config import Configuration
import os
import Input
from sysobj import *
from Skill import *

_sellRate = .33     #rate at which items sell by

#basic items template
class Item:
    def __init__(self, name):
          
        self.name = name
        self.sprite = ImgObj(Texture(os.path.join("items", name, "item.png")))
        self.itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini"))
        
        self.buyPrice = self.itemini.item.__getattr__("worth", int, 0)  #value at which the item is bought
        self.sellPrice = self.buyPrice*_sellRate                        #value at which it is sold
        self.description = self.itemini.item.__getattr__("description", str, "")
                                                                        #item description used in shops and menus
   
#weapon item
# weapons have special abilities 
class Weapon(Item):
    def __init__(self, name):
        super(Weapon, self).__init__(name)
        
        self.type = self.itemini.weapon.__getattr__("type")
            
        #weapons can have their own attack and defend animations
        path = os.path.join("items", name, "attack.anim")
        if os.path.exists(path):
            path = os.path.join("items", name, "attack")
        else:
            path = "attack"
        self.attackAnimation = Animation(path)
            
        path = os.path.join("items", name, "defend.anim")
        if os.path.exists(path):
            path = os.path.join("items", name, "defend")
        else:
            path = "defend"
        self.defendAnimation = Animation(path)
            
        self.str  = self.itemini.weapon.__getattr__("str", int)
        
        #bows and guns use a different style of attacks defined in the command.py
        #they can be single, burst, auto for guns and single, double for bows
        if self.type == "gun" or self.type == "bow":
            self.firingMode = self.itemini.weapon.__getattr__("mode").split("|")
        else:
            #weapons, if available, have the ability to perform special
            #combo attacks where you input the specified keys in the amount of time
            #specified (in milliseconds)
            attack = self.itemini.weapon.__getattr__("combo").split(" ")
            self.attack = []
            for key in attack:
                if key == "Up":     self.attack.append(Input.UpButton)
                elif key == "Dn":   self.attack.append(Input.DnButton)
                elif key == "Lt":   self.attack.append(Input.LtButton)
                elif key == "Rt":   self.attack.append(Input.RtButton)
                elif key == "A":    self.attack.append(Input.AButton)
                elif key == "B":    self.attack.append(Input.BButton)
                elif key == "C":    self.attack.append(Input.CButton)
                else:               self.attack.append(Input.DButton)
            self.time = self.itemini.weapon.__getattr__("combotime", int)
        
#armor item
# armor fortifies the character wearing it
class Armor(Item):
    def __init__(self, name):
        super(Armor, self).__init__(name)
        
        self.defn = self.itemini.armor.__getattr__("def", int, 0)
        self.spd  = self.itemini.armor.__getattr__("spd", int, 0)
        self.evd  = self.itemini.armor.__getattr__("evd", int, 0)
        self.mag  = self.itemini.armor.__getattr__("mag", int, 0)
        self.res  = self.itemini.armor.__getattr__("res", int, 0)

#items usable only in battle
class Usable(Item):
    def __init__(self, name):
        super(Usable, self).__init__(name)
        self.function = eval(itemini.usable.__getattr__("function"))
            
#foods can function like usable items but only from the inventory
class Food(Item):
    def __init__(self, name):
        super(Food, self).__init__(name)
        self.function = eval(itemini.food.__getattr__("function"))
            
#loot are items found in dungeons or are drops from specific monsters
#loot selling price is the same as it's worth which is different from 
# generic items where the selling price is 1/3.
# loot can not be bought from stores.
class Loot(Item):
    def __init__(self, name):
        super(Loot, self).__init__(name)
        self.buyPrice = self.itemini.loot.__getattr__("worth")
        self.sellPrice = self.itemini.loot.__getattr__("worth")
        self.description = self.itemini.loot.__getattr__("description")
            
