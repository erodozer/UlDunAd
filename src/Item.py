from Config import Configuration
import os
import Input
from sysobj import *

class Item:
    def __init__(self, name):
        if (not name) or name == "None":
            return None
            
        try:
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).item
        except:
            return None
            
        self.name = name
        self.sprite = ImgObj(Texture(os.path.join("items", name, "item.png")))
        
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
        self.str  = itemini.__getattr__("str", int)
        
        #weapons, if available, have the ability to perform special
        #combo attacks where you input the specified keys in the amount of time
        #specified (in milliseconds)
        attack = itemini.__getattr__("combo").split(" ")
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
        self.time = itemini.__getattr__("combotime", int)
        
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

        
        
