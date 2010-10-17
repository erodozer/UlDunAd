from sysobj import *
from View   import *
from Actor  import *
from MenuObj import MenuObj

class FamilyMenu(MenuObj):
    def __init__(self, scene, families):
        self.scene = scene
        self.engine = scene.engine
        self.commands = families
        
        fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)
        
        buttonStyle  = Texture("select_highlight.png")
        self.buttons = [ImgObj(buttonStyle, boundable = True, frameY = 2)
                        for n in range(len(self.families))]
                        
        self.position = (20, 10)
        for i, button in enumerate(self.buttons):
            button.setPosition(self.position[0], self.position[1] - (150 * i))
        self.slideRate = 150.0/512.0
        
        self.index = 0
        
    def render(self, visibility):
        
class FamilyList(Scene):
    def __init__(self, engine):
        self.engine     = engine
        self.families   = self.engine.listPath(path = os.path.join("data", "actors", "families"))

        self.background = ImgObj(Texture("select_background.png"))
        
        self.hlTex      = Texture("select_highlight.png")
        self.highlight  = [ImgObj(self.hlTex, boundable = True, frameY = 2)
                           for n in range(len(self.families))]
        #self.slider     = ImgObj(Texture("slider.png"))
        self.slide_b    = [ImgObj(Texture("slider_buttons.png"), boundable = True, frameY = 2),
                           ImgObj(Texture("slider_buttons.png"), boundable = True, frameY = 2)]
        self.selectwin  = ImgObj(Texture("window_selected.png"))

        self.pos        = 0
        self.newpos     = 0
        self.slideUP    = False
        self.slideDOWN  = False

        self.listlength = self.engine.h*(self.hlTex.pixelSize[1]/2*len(self.highlight))
        
        self.selected   = 0

    def buttonClicked(self, image):
        if Scene.objInput == self.slide_b[0]:
            if self.pos > 0:
                self.slideUP = True
                self.newPos = self.pos - 30
                if self.newPos < 0:
                    self.newPos = 0
        elif Scene.objInput == self.slide_b[1]:
            if self.pos < self.listlength:
                self.slideUP = True
                self.newPos = self.pos + 30
                if self.newPos > self.listlength:
                    self.newPos = self.listlength

        elif Scene.objInput in self.highlight:
            self.selected = Scene.objInput
    
    def keyPressed(self, key, char):
        if key == K_DOWN:
            if self.selected < len(self.families):
                self.selected += 1
            else:
                self.selected = 0
                
        if key == K_UP:
            if self.selected > 0:
                self.selected -= 1
            else:
                self.selected = len(self.families) - 1
                 
    def run(self):

        #this will slide the list up or down in a smooth motion
        #when one of the slide buttons is clicked!  Each click
        #will offset the list by 30 px and clicking can only be
        #either up or down.  Input can not be taken while the list
        #is sliding to its new position.

        if self.slideUP:
            if self.pos > self.newPos:
                self.pos -= 1
            else:
                self.pos = self.newPos
                self.slideUP = False

        if self.slideDOWN:
            if self.pos < self.newPos:
                self.pos += 1
            else:
                self.pos = self.newPos
                self.slideDOWN = False

    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w, h))

        self.engine.drawImage(self.selectwin, position = (w/2, h*.9), scale = (w, h*.2))
            
        for f, i in enumerate(self.highlight):
            frame = 1
            if f == self.selected:
                frame = 2
            self.engine.drawImage(f, position = (w/2, self.pos + self.listlength/len(self.highlight)*i), frameY = frame)
            

        self.engine.drawImage(self.slide_b[0], position = (w*.9, h*.1), frameY = 1)
        self.engine.drawImage(self.slide_b[1], position = (w*.9, h*.9), frameY = 2) 

        
