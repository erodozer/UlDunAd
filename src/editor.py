import wx

from editor.ItemFrame import ItemFrame

class MainWindow(wx.Frame):
  
    def __init__(self):
        super(MainWindow, self).__init__(None, style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, title = 'UlDunAd - Editor', size = (650, 400))
        
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        tabs = wx.Notebook(self, -1)            #create the notebook
        
        itemFrame = ItemFrame(tabs)             #item tab
        enemyFrame = EnemyFrame(tabs)           #enemy tab
        formationFrame = FormationFrame(tabs)   #formation tab
        
        #make the pages
        tabs.AddPage(itemFrame, "Item")
        tabs.AddPage(enemyFrame, "Enemy")
        tabs.AddPage(formationFrame, "Formation")
        
        #tabs need sizer
        sizer = wx.BoxSizer()
        sizer.Add(tabs, -1, wx.EXPAND)
        self.SetSizer(sizer)
        
#tab controlling the creation of new enemies
class EnemyFrame(wx.Panel):
    def __init__(self, parent):
        super(EnemyFrame, self).__init__(parent)
        
        self.InitUI()
        self.Show()
        
    def InitUI(self):
        self.list = wx.ListBox(self, -1, pos = (10, 10), size = (160, 300))
        self.addButton = wx.Button(self, -1, "+", pos = (110, 320), size = (28, 28))
        self.removeButton = wx.Button(self, -1, "-", pos = (142, 320), size = (28, 28))
        
        self.restoreButton = wx.Button(self, -1, "Restore", pos = (380, 320), size = (120, 28))
        self.saveButton = wx.Button(self, -1, "Save", pos = (520, 320), size = (120, 28))

        
#tab controlling the creation of new formations
class FormationFrame(wx.Panel):
    def __init__(self, parent):
        super(FormationFrame, self).__init__(parent)
        
        self.InitUI()
        self.Show()
        
    def InitUI(self):
        self.list = wx.ListBox(self, -1, pos = (10, 10), size = (160, 300))
        self.addButton = wx.Button(self, -1, "+", pos = (110, 320), size = (28, 28))
        self.removeButton = wx.Button(self, -1, "-", pos = (142, 320), size = (28, 28))
        
        self.restoreButton = wx.Button(self, -1, "Restore", pos = (380, 320), size = (120, 28))
        self.saveButton = wx.Button(self, -1, "Save", pos = (520, 320), size = (120, 28))

                    
if __name__ == '__main__':
  
    app = wx.App()
    MainWindow()
    app.MainLoop()

