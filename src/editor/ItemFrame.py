import os
import wx
from Item import *
from Data import listpath

#Tab controlling the creation of new items
class ItemFrame(wx.Panel):
    def __init__(self, parent):
        super(ItemFrame, self).__init__(parent, style = wx.EXPAND)
        
        self.item = None
        self.InitUI()
        self.Show()
    
    def loadItem(self, name):
        ini = Configuration(os.path.join("..", "data", "items", i, "item.ini"))
        #detecting what type of item it is
        if ini.parser.has_section("weapon"):
            item = Weapon(i)
        elif ini.parser.has_section("armor"):
            item = Armor(i)
        elif ini.parser.has_section("loot"):
            item = Loot(i)
        elif ini.parser.has_section("usuable"):
            item = Usable(i)
        else:
            item = Item(i)  
                  
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

        self.Bind(wx.EVT_LISTBOX, self.refreshItem, id=self.list.GetId())
        
        #name
        wx.StaticText(self, -1, "Name: ", pos = (180, 16))
        self.nameBox = wx.TextCtrl(self, -1, "", pos = (230, 10), size = (210, 28))
        
        #worth
        wx.StaticText(self, -1, "Worth: ", pos = (470, 16))
        self.worthWheel = wx.SpinCtrl(self, -1, '', pos = (520, 10), size = (100, 28))

        self.showEquip(None)
        
    #show equipment interface
    def showEquip(self, event = None):
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
        
    #show loot interface
    def showLoot(self, event):
        pass
        
    #hide loot interface
    def hideLoot(self):
        pass
     
    #update the list of items
    def updateList(self):
        self.list.clear()
        for i, item in enumaerate(listPath(os.path.join("data", "items"), "item.ini", "folderDeepSearch")):
            self.list.add("%03i: %s" % (i, item))
     
    #update the interface with the currently selected item
    def refreshItem(self):
        self.list.GetSelection()
        
 
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

class ProjectilePanel(wx.Panel):
    def __init__(self, parent):
        super(ProjectilePanel, self).__init__(parent, pos = (180, 258), size = (130, 60))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, '', (0, 0), size = (120, 50))
        self.projectCheck = wx.CheckBox(self, 6, 'Projectile', (10, 16), size = (100, 28))

        self.Bind(wx.EVT_CHECKBOX, self.GetParent().showWeaponSpecials, id=self.projectCheck.GetId())
           
    def GetValue(self):
        return self.projectCheck.GetValue()
        
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
        
    def SetValues(self, itemini):
        pass
    
class ComboPanel(wx.Panel):
    def __init__(self, parent):
        super(ComboPanel, self).__init__(parent, pos = (368, 146), size = (250,110))
        
        self.InitUI()

    def InitUI(self):
                
        wx.StaticBox(self, -1, "Combo Attack", (0, 0), size = (240, 100))
                
        #attack input buttons
        for i in range(7):
            setattr(self, "attack%i" % (i+1), wx.Button(self, -1, "%i" % (i+1), (10 + 32*i, 20), size = (28, 28)))
        #timer amount
        wx.StaticText(self, -1, "Time: ", pos = (50, 64))
        self.time = wx.SpinCtrl(self, -1, '', pos = (90, 58), size = (100, 28))

    def Clear(self):
        self.time.SetValue(0)
        
    def SetValues(self, itemini):
        pass
        
