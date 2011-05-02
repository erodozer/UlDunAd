import os, sys
from PyQt4 import QtGui, QtCore

#from Item import Item
from itemDialog import *	

#Main Editor window
class Editor(QtGui.QWidget):

	def __init__(self):
		super(Editor, self).__init__()
        
		self.elements = []
		self.initUI()
        
    #initializes the main interface
	def initUI(self):
		self.setWindowTitle('UlDunAd Editor')
		self.setFixedSize(640,480)
		self.center()
		
		self.tabs = QtGui.QTabBar(self)
		self.tabs.resize(self.width(), 22)
		tabs = ["Item", "Enemy", "Formation"]
		for i, tab in enumerate(tabs):
			self.tabs.insertTab(i, tab)
			
		#displays the list of elements							
		self.itemListLabel = QtGui.QLabel(self)
		self.itemListLabel.move(10, 28)
		self.itemList = QtGui.QListWidget(self)
		self.itemList.addItems(self.elements)
		self.itemList.resize(150, self.height() - 150)
		self.itemList.move(self.itemListLabel.x(), self.itemListLabel.y() + self.itemListLabel.height()/2 + 10)

		#add new element button
		newButton = QtGui.QPushButton("New", self)
		newButton.move(10, self.height() - newButton.height() - 35)
		
		#add save element button
		saveButton = QtGui.QPushButton("Save", self)
		saveButton.move(self.width() - saveButton.width() - 10, self.height() - saveButton.height() - 35)
				
		#different dialog displays
		self.dialogs = [ItemDialog(self), None, None]
		self.activeDialog = self.dialogs[0]
		
		self.changeSection(0)
		
		self.connect(self.tabs, QtCore.SIGNAL('stateChanged(int)'), self.changeSection)
		self.connect(newButton, QtCore.SIGNAL('clicked()'), self.activeDialog.new)
		self.connect(saveButton, QtCore.SIGNAL('clicked()'), self.save)
		self.connect(self.itemList, QtCore.SIGNAL('itemChanged()'), self.switch)	
		
	#centers the window on screen
	def center(self):
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
      
    #changes the active dialog  
	def changeSection(self, value):
		for i in range(len(self.dialogs)):
			try:
				if i == value:
					self.dialogs[i].show()
				else:
					self.dialogs[i].hide()
			except:
				continue
		self.activeDialog = self.dialogs[value]
		self.activeDialog.move(0, 24)
	
	def switch(self, value):
		self.activeDialog.switch(value)
		
	def save(self):
		self.activeDialog.save()
		self.itemList.clear()
		self.activeDialog.update()
			
if __name__ == '__main__':
  
	app = QtGui.QApplication(sys.argv)
	ed = Editor()
	ed.show()
	app.exec_()
