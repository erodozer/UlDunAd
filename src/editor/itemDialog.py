import os, sys
from PyQt4 import QtGui, QtCore

#searches path for files with filetype or folder
def listPath(path, value = "ini", flag = None, exclude = None):
    items = []
    searchpath = os.path.join("..", "..", "data", path)
    #retrieve just the file names
    if flag == "filename":
            items = [n.rsplit("/",1)[1].replace("." + value, "") for n in glob.glob(os.path.join(searchpath, "*." + value))]
    #returns a list of the folders in the path
    elif flag == "folder":
            items = os.listdir(searchpath)
    #returns a list of the folders in the path that contain the searched file
    elif flag == "folderDeepSearch":
            items = [n for n in os.listdir(searchpath) if os.path.isfile(os.path.join(searchpath, n, value))]
    #retrieve the entire filename, extension included
    else:
            items = [n.rsplit("/",1)[1] for n in glob.glob(os.path.join(searchpath, "*." + value))]
    #removes this file from list
    if exclude:
            items.remove(exclude)

    return items

#shows the item editor
class ItemDialog(QtGui.QWidget):
    def __init__(self, parent):
            super(ItemDialog, self).__init__(parent)

            self.parent = parent
            self.resize(parent.width(), parent.height())
            self.updateList()

            self.selectedItem = None				#currently selected item
            self.items = ["%03i: %s" % (i, name) for i, name in enumerate(self.parent.elements)]
                                                                                            #this is the list of items this install of UlDunAd
                                                                                            # currently has in its data directory
            self.initUI()
            self.setEnabled(True)

    #creates the interface
    def initUI(self):

            #displays name of the items
            nameLabel = QtGui.QLabel(self)
            nameLabel.setText("Name:")
            nameLabel.move(self.parent.itemList.x() + self.parent.itemList.width() + 10, 24)
            name = QtGui.QLineEdit(self)
            name.resize(150, 20)
            name.move(nameLabel.x() + nameLabel.width()/2 + 2, nameLabel.y())

            #displays cost of the items
            worthLabel = QtGui.QLabel(self)
            worthLabel.setText("Worth:")
            worthLabel.move(name.x() + name.width() + 10, nameLabel.y())
            worth = QtGui.QLineEdit(self)
            worth.resize(50, 20)
            worth.move(worthLabel.x() + worthLabel.width()/2 + 2, worthLabel.y())

            #item type switch
            itemType = QtGui.QButtonGroup(self)
            usable = QtGui.QRadioButton("Usable", self)
            usable.move(name.x(), nameLabel.y() + nameLabel.height())
            usable.toggle()
            equipable = QtGui.QRadioButton("Equipable", self)
            equipable.move(usable.x() + usable.width() + 20, usable.y())
            itemType.addButton(usable)
            itemType.addButton(equipable)

            usableProperties = UsableItemWidget(self.parent, self.selectedItem)

            #changes which properties to show
            def switchShow(button):
                    if button == usable:
                            usableProperties.show()
                    else:
                            usableProperties.hide()

            #connects the buttons and list as input accepting objects
            self.connect(itemType, QtCore.SIGNAL('clicked()'), switchShow)

    def show(self):
            self.parent.itemListLabel.setText("Items")

    def new(self):
            pass

    #saves the current edited item values and updates the item list
    def saveItem(self):
            pass

    #updates the current item being displayed
    def updateList(self):
            self.parent.elements = ["%03i: %s" % (i, n) for i, n in enumerate(listPath(path = os.path.join("items"), value = "item.ini", flag = "folderDeepSearch"))]
            self.parent.itemList.addItems(self.parent.elements)

    def switch(self, value):
            self.selectedItem = Item(self.parent.elements[i])

    #shows properties of equipment
    def showEquip(self):

            #item type switch
            equipType = QtGui.QButtonGroup(self)
            weapon = QtGui.QRadioButton("Weapon", self)
            weapon.move(160, 140)
            armor = QtGui.QRadioButton("Armor", self)
            armor.move(weapon.x() + weapon.width() + 10, weapon.y())
            accessory = QtGui.QRadioButton("Accessory", self)
            accessory.move(armor.x() + armor.width() + 10, armor.y())
            equipType.addButton(weapon)
            equipType.addButton(armor)
            equipType.addButton(accessory)

            #shows the weapon properties
            def showWeapon():
                    pass
            #shows the armor properties
            def showArmor():
                    pass
            #shows the accessory properties
            def showAccessory():
                    pass

            #changes which properties to show
            def switchShow(button):
                    if button == usable:
                            self.showWeapon()
                    if button == armor:
                            self.showArmor()
                    else:
                            self.showAccessory()

            self.connect(itemType, QtCore.SIGNAL('clicked()'), switchShow)

#Usable item properties are displayed in this little sub window
class UsableItemWidget(QtGui.QWidget):
    def __init__(self, parent, item):
            super(UsableItemWidget, self).__init__(parent)

            self.item = item
            self.initUI()

    #creates the layout of objects in the widget
    def initUI(self):

            #displays hp affectiveness of the item
            self.hpLabel = QtGui.QLabel(self)
            self.hpLabel.setText("HP:")
            self.hpLabel.move(200, 140)
            self.hp = QtGui.QLineEdit("0", self)
            self.hp.resize(50, 20)
            self.hp.move(self.hpLabel.x() + self.hpLabel.width()/2 + 2, self.hpLabel.y())
            self.hp.setAlignment(QtCore.Qt.AlignRight)
            self.hpPercentage = QtGui.QCheckBox("%", self)
            self.hpPercentage.move(self.hp.x() + self.hp.width() + 5, self.hp.y())

            #displays mp affectiveness of the item
            self.mpLabel = QtGui.QLabel(self)
            self.mpLabel.setText("MP:")
            self.mpLabel.move(200, self.hpLabel.y() + self.hpLabel.height()/2 + 10)
            self.mp = QtGui.QLineEdit("0", self)
            self.mp.resize(50, 20)
            self.mp.move(self.mpLabel.x() + self.mpLabel.width()/2 + 2, self.mpLabel.y())
            self.mp.setAlignment(QtCore.Qt.AlignRight)
            self.mpPercentage = QtGui.QCheckBox("%", self)
            self.mpPercentage.move(self.hpPercentage.x(), self.mp.y())

            self.connect(self.mpPercentage, QtCore.SIGNAL('clicked()'), self.hide)
            print "connected"

    def new(self):
            pass

    def hide(self):
            self.hpLabel.hide()
            self.hp.hide()
            self.hpPercentage.hide()
            self.mpLabel.hide()
            self.mp.hide()
            self.mpPercentage.hide()
            self.setEnabled(False)

    def show(self):
            self.hpLabel.show()
            self.hp.show()
            self.hpPercentage.show()
            self.mpLabel.show()
            self.mp.show()
            self.mpPercentage.show()
            self.setEnabled(True)

    #returns all the properties from the various fields in the widget
    def getProperties(self):
            return self.hp.getState()
