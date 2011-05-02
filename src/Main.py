#!/usr/bin/python
# -*- coding: utf-8 -*-

# gridlayout1.py

import sys, os
from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        self.setWindowTitle('grid layout')

        grid = QtGui.QGridLayout()
	grid.setSpacing(2)
	startButton = QtGui.QPushButton('Start Game')
	grid.addWidget(startButton, 2, 0, 1, 1)
	editorButton = QtGui.QPushButton('Editor')
	grid.addWidget(editorButton, 3, 0, 1, 1)
	creditsButton = QtGui.QPushButton('Credits')
	grid.addWidget(creditsButton, 4, 0, 1, 1)
	exitButton = QtGui.QPushButton('Exit')
	grid.addWidget(exitButton, 5, 0, 1, 1)

        self.setLayout(grid)
	self.connect(startButton, QtCore.SIGNAL('clicked()'),
            self.runEngine)
	self.connect(editorButton, QtCore.SIGNAL('clicked()'),
            QtGui.qApp, QtCore.SLOT('quit()'))
	self.connect(creditsButton, QtCore.SIGNAL('clicked()'),
            QtGui.qApp, QtCore.SLOT('quit()'))
	self.connect(exitButton, QtCore.SIGNAL('clicked()'),
            QtGui.qApp, QtCore.SLOT('quit()'))

    def runEngine(self):
	self.hide()
	os.system("python engine.py")
	self.show()
	
	
app = QtGui.QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
