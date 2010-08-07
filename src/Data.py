from sysobj import *
#for list files
import glob

def listpath(path, value = ".ini", flag = None):
    items = []
    path = os.path.join("..", path)
    if flag == "filename":
        items = [n.replace(value, "") for n in glob.glob(os.path.join(path, "*." + value))]
    else:
        items = [glob.glob(os.path.join(path, "*." + value))]
        
    return items

class Data:
    def __init__(self):
        self.defaultButton = Texture("button.png")
    
        #fonts
        self.defaultFont = "default.ttf"
        self.menuFont = "menu.ttf"

        self.towns = listpath(os.path.join("data", "places", "towns"))
