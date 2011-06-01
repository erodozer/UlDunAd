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
        self.name = name
         
        if name and not name == "None":
            self.sprite = ImgObj(Texture(os.path.join("items", name, "item.png")))
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).weapon
            self.type = itemini.__getattr__("type")
            self.attackAnimation = ImgObj(Texture(os.path.join("items", name, "attack.png"),
                                          fallback = Texture(os.path.join("animations", "attack.png"))), frameX = 9)
            self.defendAnimation = ImgObj(Texture(os.path.join("items", name, "defend.png"),
                                          fallback = Texture(os.path.join("animations", "defend.png"))), frameX = 10)
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
        else:
            self.sprite = None
            self.attackAnimation = ImgObj(Texture(os.path.join("animations", "attack.png")), frameX = 9)
            self.defendAnimation = ImgObj(Texture(os.path.join("animations", "defend.png")), frameX = 10)
            self.type = "unknown"
            self.str  = 1
            self.attack = []
            self.time = 0
            
        
class Armor(Item):
    def __init__(self, name):
        self.name = name
        
        if name and not name == "None":
            self.sprite = ImgObj(Texture(os.path.join("items", name, "item.png")))
            itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini")).armor
            self.defn = itemini.__getattr__("def", int)
            self.spd  = itemini.__getattr__("str", int)
            self.evd  = itemini.__getattr__("evd", int)
            self.mag  = itemini.__getattr__("mag", int)
            self.res  = itemini.__getattr__("res", int)
        else:
            self.sprite = None
            self.defn = 0
            self.spd  = 0
            self.evd  = 0
            self.mag  = 0
            self.res  = 0
