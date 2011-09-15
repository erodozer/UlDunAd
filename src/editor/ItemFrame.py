import os
import wx
from Item import *
from Data import listPath

#Tab controlling the creation of new items
class ItemFrame(wx.Panel):
    def __init__(self, parent):
        super(ItemFrame, self).__init__(parent, style = wx.EXPAND)
        
        self.items = []
        self.item = None
        self.InitUI()
        self.updateList()
        self.Show()
    
    def loadItem(self, name):
        ini = Configuration(os.path.join("..", "data", "items", name, "item.ini"))
        #detecting what type of item it is
        if ini.parser.has_section("weapon"):
            item = Weapon(name)
        elif ini.parser.has_section("armor"):
            item = Armor(name)
        elif ini.parser.has_section("loot"):
            item = Loot(name)
        elif ini.parser.has_section("usable"):
            item = Usable(name)
        else:
            item = Item(name)  
        return item
                  
    def InitUI(self):
        self.itemType = ItemTypePanel(self)
        self.equipType = EquipTypePanel(self)
        self.projectile = ProjectilePanel(self)
        self.weapAttr = WeaponAttrPanel(self)
        self.armrAttr = ArmorAttrPanel(self)
        self.weapSpec = ComboPanel(self)
        self.projSpec = FiringModePanel(self)
        
        self.list = wx.ListBox(self, -1, pos = (10, 10), size = (160, 300))
        self.addButton = wx.Button(self, -1, "+", pos = (110, 320), size = (28, 28))
        self.removeButton = wx.Button(self, -1, "-", pos = (142, 320), size = (28, 28))
        
        self.restoreButton = wx.Button(self, -1, "Restore", pos = (380, 320), size = (120, 28))
        self.saveButton = wx.Button(self, -1, "Save", pos = (520, 320), size = (120, 28))

        self.Bind(wx.EVT_LISTBOX, self.Refresh, id=self.list.GetId())
        self.Bind(wx.EVT_BUTTON, self.Refresh, id=self.restoreButton.GetId())
        self.Bind(wx.EVT_BUTTON, self.Save, id=self.saveButton.GetId())
        self.Bind(wx.EVT_BUTTON, self.newItem, id=self.addButton.GetId())
        self.Bind(wx.EVT_BUTTON, self.removeItem, id=self.removeButton.GetId())
        
        #name
        wx.StaticText(self, -1, "Name: ", pos = (180, 16))
        self.nameBox = wx.TextCtrl(self, -1, "", pos = (230, 10), size = (210, 28))
        
        #worth
        wx.StaticText(self, -1, "Worth: ", pos = (470, 16))
        self.worthWheel = wx.SpinCtrl(self, -1, '', pos = (520, 10), size = (100, 28), max = 99999)

        self.showEquip(None)
        
    def Clear(self):
        self.nameBox.SetValue("")
        self.worthWheel.SetValue(0)
        self.itemType.Clear()
        self.equipType.Clear()
        self.projectile.Clear()
        self.weapAttr.Clear()
        self.armrAttr.Clear()
        self.weapSpec.Clear()
        self.projSpec.Clear()
        self.showEquip(None)
        
    #show equipment interface
    def showEquip(self, event):
        self.equipType.Show()
        if self.equipType.weaponType.GetValue():
            self.showWeapon(None)
        else:
            self.showArmor(None)
            
    #hide equipment interface
    def hideEquip(self):
        self.equipType.Hide()
        self.hideWeapon()
        self.hideArmor()
        self.hideWeaponSpecials()
        
    #show weapon interface
    def showWeapon(self, event):
        self.weapAttr.Show()
        self.projectile.Show()
        self.showWeaponSpecials(self.projectile.GetValue())
        self.hideArmor()
        
    #hide weapon interface
    def hideWeapon(self):
        self.weapAttr.Hide()
        self.projectile.Hide()
        
    #shows weapon specials interface
    def showWeaponSpecials(self, event):
        if isinstance(event, wx.Event):
            #show firing mode
            if event.GetEventObject().GetValue():
                self.projSpec.Show()
                self.weapSpec.Hide()
            #show combo
            else:
                self.projSpec.Hide()
                self.weapSpec.Show()
        else:
            #show firing mode
            if event:
                self.projSpec.Show()
                self.weapSpec.Hide()
            #show combo
            else:
                self.projSpec.Hide()
                self.weapSpec.Show()
       
    #hide weapon specials interface
    def hideWeaponSpecials(self):
        self.projSpec.Hide()
        self.weapSpec.Hide()
        
    #show armor interface
    def showArmor(self, event):
        self.hideWeapon()
        self.hideWeaponSpecials()
        self.armrAttr.Show()
        
    #hide armor interface    
    def hideArmor(self):
        self.armrAttr.Hide()
        
    #show the usable panel, hide the others
    def showUsable(self, event):
        self.hideEquip()
        self.hideLoot()
        
    def hideUsable(self):
        pass
        
    #show loot interface
    def showLoot(self, event):
        self.hideEquip()
        self.hideUsable()
        
    #hide loot interface
    def hideLoot(self):
        pass
     
    #update the list of items
    def updateList(self):
        self.list.Clear()
        if len(self.items) == 0:
            self.items = listPath("items", "item.ini", "folderDeepSearch")
            
        for i, item in enumerate(self.items):
            self.list.Append("%03i: %s" % (i, item))
     
    #start creation for new item
    def newItem(self, event):
        self.item = None
        self.list.SetSelection(-1)
        self.Clear()
        
    #removes the item completely
    def removeItem(self, event):
        if self.item:
            #TODO delete the directory and item from the list
            pass
            
    #update the interface with the currently selected item
    def Refresh(self, event):
        self.item = self.loadItem(self.items[self.list.GetSelection()])
        self.nameBox.SetValue(self.item.name)
        self.worthWheel.SetValue(self.item.buyPrice)
        
        if isinstance(self.item, Loot):
            self.itemType.SetValue(2)
            self.showLoot(None)
        elif isinstance(self.item, Usable) or isinstance(self.item, Food):
            self.itemType.SetValue(1)
            self.showUsable(None)
        else:
            self.itemType.SetValue(0)
            if isinstance(self.item, Weapon):
                self.equipType.SetValue(0)
                self.weapAttr.SetValues([self.item.str, self.item.mag])
                if (self.item.type == "gun" or self.item.type == "bow"):
                    self.projectile.SetValue(True)
                    self.projSpec.SetFiringModes(self.item.firingMode)
                    self.projSpec.SetProjType(self.item.type == "gun")
                else:
                    self.projectile.SetValue(False)
                    self.weapSpec.SetTime(self.item.time)
                    self.weapSpec.SetAttack(self.item.attack)
                    
                self.showWeapon(None)
            else:
                self.equipType.SetValue(1)
                self.showArmor(None)
            self.showEquip(None)

    def Save(self, event):
        name = self.nameBox.GetValue().lower()  #directory names are lower case
        if os.path.exists(os.path.join("..", "data", "items", name)) and not self.item:
            message = wx.MessageDialog(self.GetParent(), "An item with that name already exists", style = wx.OK|wx.CENTRE)
            message.ShowModal()
            message.Destroy()
            return
        elif os.path.exists(os.path.join("..", "data", "items", name)) and self.item:
            message = wx.MessageDialog(self.GetParent(), "An item with that name already exists", style = wx.OK|wx.CENTRE)
            message.ShowModal()
            message.Destroy()
            return
        elif not os.path.exists(os.path.join("..", "data", "items", name)) and self.item:
            os.rename(os.path.join("..", "data", "items", self.item.name.lower()), os.path.join("..", "data", "items", name))
            self.items.remove(self.item.name.lower())
        else:
            os.mkdir(os.path.join("..", "data", "items", name))
        Configuration(os.path.join("..", "data", "items", name, "item.ini")).save()
        itemini = Configuration(os.path.join("..", "data", "items", name, "item.ini"))
        itemini.item.__setattr__("worth", self.worthWheel.GetValue())
        type = self.itemType.GetValue()
        if type == 0:   #equipment
            type = self.equipType.GetValue()
            if type == 0:   #weapon
                #save attributes
                attr = self.weapAttr.GetValues()
                itemini.weapon.__setattr__("str", attr[0])
                itemini.weapon.__setattr__("mag", attr[1])
                if self.projectile.GetValue():
                    if self.projSpec.GetProjType():
                        itemini.weapon.__setattr__("type", "gun")
                    else:
                        itemini.weapon.__setattr__("type", "bow")
                    itemini.weapon.__setattr__("firingmode", "".join("|", self.projSpec.GetFiringModes()))
                else:
                    itemini.weapon.__setattr__("combotimer", self.weapSpec.getTime())
                    itemini.weapon.__setattr__("attack", "".join(" ", self.weapSpec.GetAttack()))
            elif type == 1: #armor
                #save attributes
                attr = self.armrAttr.GetValues()
                itemini.armor.__setattr__("def", attr[0])
                itemini.armor.__setattr__("res", attr[1])
                itemini.armor.__setattr__("spd", attr[2])
                itemini.armor.__setattr__("evd", attr[3])
        elif type == 1: #usable
            itemini.usable.__setattr__("function", "None")
        elif type == 2: #loot
            itemini.loot.__setattr__("worth", self.worthWheel.GetValue())
        itemini.save()
        self.items.append(name)
        self.updateList()
        self.list.SetSelection(len(self.items)-1)
        self.item = self.loadItem(self.items[self.list.GetSelection()])
 
class ItemTypePanel(wx.Panel):
    def __init__(self, parent):
        super(ItemTypePanel, self).__init__(parent, pos = (180, 48), size = (130, 120))
        
        self.InitUI()
        self.Show()

    def InitUI(self):
        #item type box
        wx.StaticBox(self, -1, 'Item Type', (0, 0), size=(120, 110))
        self.equipType = wx.RadioButton(self, -1, 'Equipable', (10, 16), size = (100, 28), style=wx.RB_GROUP)
        self.useType = wx.RadioButton(self, -1, 'Usable', (10, 46), size = (100, 28))
        self.lootType = wx.RadioButton(self, -1, 'Loot', (10, 76), size = (100, 28))

        self.Bind(wx.EVT_RADIOBUTTON, self.GetParent().showEquip, id=self.equipType.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.GetParent().showUsable, id=self.useType.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.GetParent().showLoot, id=self.lootType.GetId())

    def Clear(self):
        self.equipType.SetValue(True)
        
    def GetValue(self):
        if self.equipType.GetValue():
            return 0
        elif self.useType.GetValue():
            return 1
        else:
            return 2
            
    def SetValue(self, val):
        if val == 0:
            self.equipType.SetValue(True)
        elif val == 1:
            self.useType.SetValue(True)
        else:
            self.lootType.SetValue(True)
            
class EquipTypePanel(wx.Panel):
    def __init__(self, parent):
        super(EquipTypePanel, self).__init__(parent, pos = (180, 168), size = (130, 90))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, 'Equipment Type', (0, 0), size=(120, 80))
        self.weaponType = wx.RadioButton(self, -1, 'Weapon', (10, 16), size = (100, 28), style=wx.RB_GROUP)
        self.armorType = wx.RadioButton(self, -1, 'Armor', (10, 46), size = (100, 28))

        self.Bind(wx.EVT_RADIOBUTTON, self.GetParent().showWeapon, id=self.weaponType.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.GetParent().showArmor, id=self.armorType.GetId())

    def Clear(self):
        self.weaponType.SetValue(True)
        
    def SetValue(self, val):
        if val == 0:
            self.weaponType.SetValue(True)
        else:
            self.armorType.SetValue(True)
            
    def GetValue(self, val):
        return int(self.armorType.GetValue())
        
class ProjectilePanel(wx.Panel):
    def __init__(self, parent):
        super(ProjectilePanel, self).__init__(parent, pos = (180, 258), size = (130, 60))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, '', (0, 0), size = (120, 50))
        self.projectCheck = wx.CheckBox(self, 6, 'Projectile', (10, 16), size = (100, 28))

        self.Bind(wx.EVT_CHECKBOX, self.GetParent().showWeaponSpecials, id=self.projectCheck.GetId())
      
    def Clear(self):
        self.projectCheck.SetValue(False)
        
    def GetValue(self):
        return self.projectCheck.GetValue()
        
    def SetValue(self, val):
        self.projectCheck.SetValue(val)
        
class WeaponAttrPanel(wx.Panel):
    def __init__(self, parent):
        super(WeaponAttrPanel, self).__init__(parent, pos = (368, 48), size = (250,80))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, "Attributes", (0, 0), size = (240, 78))
        
        wx.StaticText(self, -1, "Attack Power", (10, 20))
        self.strVal = wx.SpinCtrl(self, -1, '', (120, 16), size = (100, 24)) 

        wx.StaticText(self, -1, "Magic Power", (10, 50))
        self.magVal = wx.SpinCtrl(self, -1, '', (120, 46), size = (100, 24)) 

    def Clear(self):
        self.strVal.SetValue(0)
        self.magVal.SetValue(0)
        
    def SetValues(self, values):
        self.strVal.SetValue(values[0])
        self.magVal.SetValue(values[1])
        
    def GetValues(self):
        return [self.strVal.GetValue(), self.magVal.GetValue()]
        
class ArmorAttrPanel(wx.Panel):
    def __init__(self, parent):
        super(ArmorAttrPanel, self).__init__(parent, pos = (368, 48), size = (250,150))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, "Attributes", (0, 0), size = (240, 140))
        
        wx.StaticText(self, -1, "Defence", (10, 20))
        self.defVal = wx.SpinCtrl(self, -1, '', (120, 16), size = (100, 24)) 

        wx.StaticText(self, -1, "Resistance", (10, 50))
        self.resVal = wx.SpinCtrl(self, -1, '', (120, 46), size = (100, 24)) 

        wx.StaticText(self, -1, "Speed", (10, 80))
        self.spdVal = wx.SpinCtrl(self, -1, '', (120, 76), size = (100, 24)) 

        wx.StaticText(self, -1, "Evasion", (10, 110))
        self.evdVal = wx.SpinCtrl(self, -1, '', (120, 106), size = (100, 24)) 

    def Clear(self):
        self.defVal.SetValue(0)
        self.resVal.SetValue(0)
        self.spdVal.SetValue(0)
        self.evdVal.SetValue(0)
        
    def GetValues(self):
        return [self.defVal.GetValue(), self.resVal.GetValue(), self.spdVal.GetValue(), self.evdVal.GetValue()]
        
    
class FiringModePanel(wx.Panel):
    def __init__(self, parent):
        super(FiringModePanel, self).__init__(parent, pos = (368, 146), size = (250,110))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, "Projectile Firing Mode", (0, 0), size = (240, 110))
        
        self.bowType = wx.RadioButton(self, -1, 'Bow', (10, 16), size = (100, 28), style=wx.RB_GROUP)
        self.gunType = wx.RadioButton(self, -1, 'Gun', (116, 16), size = (100, 28))

        self.Bind(wx.EVT_RADIOBUTTON, self.enableBow, id=self.bowType.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.enableGun, id=self.gunType.GetId())
        
        self.singleCheck = wx.CheckBox(self, 6, 'Single', (10, 46), size = (100, 28))
        self.singleCheck.SetValue(True)
        self.singleCheck.Disable()
        self.doubleCheck = wx.CheckBox(self, 6, 'Double', (10, 76), size = (100, 28))
        self.burstCheck = wx.CheckBox(self, 6, 'Burst', (116, 46), size = (100, 28))
        self.autoCheck = wx.CheckBox(self, 6, 'Auto', (116, 76), size = (100, 28))

        self.enableBow(None)
        
    def enableGun(self, event):
        self.doubleCheck.Disable()
        self.burstCheck.Enable()
        self.autoCheck.Enable()
        
    def enableBow(self, event):
        self.doubleCheck.Enable()
        self.burstCheck.Disable()
        self.autoCheck.Disable()
        
    def Clear(self):
        self.bowType.SetValue(True)
        self.gunType.SetValue(False)
        self.enableBow(None)
        self.doubleCheck.SetValue(False)
        self.burstCheck.SetValue(False)
        self.autoCheck.SetValue(False)
        
    #set the projectile type
    def SetProjType(self, val):
        if val == 0:
            self.bowType.SetValue(True)
            self.enableBow(None)
        else:
            self.gunType.SetValue(True)
            self.enableGun(None)
          
    def GetProjType(self):
        if self.bowType.GetValue():
            return 0
        else:
            return 1
            
    #set the firing modes
    def SetFiringModes(self, values):
        self.doubleCheck.SetValue("double" in values)
        self.burstCheck.SetValue("burst" in values)
        self.autoCheck.SetValue("auto" in values)
        
    def GetFiringModes(self):
        values = []
        if self.doubleCheck.GetValue():
            values.append("double")
        if self.burstCheck.GetValue():    
            values.append("burst")
        if self.autoCheck.GetValue():     
            values.append("auto")
        return values
        
    
class ComboPanel(wx.Panel):
    def __init__(self, parent):
        super(ComboPanel, self).__init__(parent, pos = (368, 146), size = (250,110))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, "Combo Attack", (0, 0), size = (240, 100))
                
        #attack input buttons
        for i in range(7):
            setattr(self, "attack%i" % (i+1), wx.Button(self, -1, "%i" % (i+1), (10 + 32*i, 20), size = (28, 28)))
            self.Bind(wx.EVT_BUTTON, self.GetKey, id = getattr(self, "attack%i" % (i+1)).GetId())
        #timer amount
        wx.StaticText(self, -1, "Time: ", pos = (50, 64))
        self.time = wx.SpinCtrl(self, -1, '', pos = (90, 58), size = (100, 28), min = 0, max = 3000)

    def GetKey(self, event):
        message = ButtonConfig(self, event.GetEventObject())
        message.ShowModal()
        message.Destroy()
        
    def Clear(self):
        self.time.SetValue(0)
        
    def SetTime(self, time):
        self.time.SetValue(time)
        
    def GetTime(self):
        return self.time.GetValue()
        
    def SetAttack(self, values):
        pass
        
    def GetAttack(self):
        values = []
        for i in range(7):
            val = getattr(self, "attack%i" % (i+1)).GetLabel()
            if val in ["A", "B", "C", "D", "Up", "Dn", "Lt", "Rt"]:
                values.append(val)
        return values
        
        
class ButtonConfig(wx.Dialog):
    def __init__(self, parent, button):
        super(ButtonConfig, self).__init__(parent, -1, "Select a Key", size = (260,48))
        
        self.InitUI()
        self.Centre()
        self.SetFocus()
        self.button = button

    def InitUI(self):
        self.buttonA = wx.Button(self, -1, "A", pos = (10,10), size = (28,28))
        self.buttonB = wx.Button(self, -1, "B", pos = (40,10), size = (28,28))
        self.buttonC = wx.Button(self, -1, "C", pos = (70,10), size = (28,28))
        self.buttonD = wx.Button(self, -1, "D", pos = (100,10), size = (28,28))
        self.buttonUp = wx.Button(self, -1, "Up", pos = (130,10), size = (28,28))
        self.buttonDn = wx.Button(self, -1, "Dn", pos = (160,10), size = (28,28))
        self.buttonLt = wx.Button(self, -1, "Lt", pos = (190,10), size = (28,28))
        self.buttonRt = wx.Button(self, -1, "Rt", pos = (220,10), size = (28,28))
        
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonA.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonB.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonC.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonD.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonUp.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonDn.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonLt.GetId())
        self.Bind(wx.EVT_BUTTON, self.GetKey, id = self.buttonRt.GetId())
        
    def GetKey(self, event):
        self.button.SetLabel(event.GetEventObject().GetLabel())
        self.Close()
