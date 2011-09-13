from sysobj import *
#for list files
import glob

#searches path for files with filetype or folder
def listPath(path, value = "ini", flag = None, exclude = None):
    items = []
    searchpath = os.path.join("..", "data", path)
    #returns a list of the folders in the path
    if flag == "folder":
        items = os.listdir(searchpath)
    else:
        #allow for multiple endings when searching
        for val in value.split("|"):
            #retrieve just the file names
            if flag == "filename":
                item = [n.rsplit("/",1)[1].replace("." + value, "") for n in glob.glob(os.path.join(searchpath, "*." + val))]
            #returns a list of the folders in the path that contain the searched file
            elif flag == "folderDeepSearch":
                item = [n for n in os.listdir(searchpath) if os.path.isfile(os.path.join(searchpath, n, val))]
            #retrieve the entire filename, extension included
            else:
                item = [n.rsplit("/",1)[1] for n in glob.glob(os.path.join(searchpath, "*." + val))]
            for i in item:
                items.append(i)
    #removes this file from list
    if exclude:
        items.remove(exclude)
    
    return items


class Data:
    def __init__(self):
        self.defaultButton = Texture("button.png")
    
        #fonts
        self.defaultFont = "default.ttf"
        self.menuFont = "menu.ttf"

        self.towns = listPath(os.path.join("data", "places", "towns"))
