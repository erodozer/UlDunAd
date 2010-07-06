
class SelectFamily(Scene):
    def __init__(self, engine):
        self.engine     = engine
        self.families   = self.engine.listPath(path = os.path.join("data", "actors", "families"))

        self.background = Texture("select_background.png")
        
        self.hlTex      = Texture("select_highlight.png")
        self.highlight  = [ImgObj(self.htTex, boundable = True, frameY = 2) for n in len(self.families)]
        #self.slider     = ImgObj(Texture("slider.png"))
        self.slide_b    = [ImgObj(Texture("slider_buttons.png"), boundable = True, frameY = 2),
                           ImgObj(Texture("slider_buttons.png"), boundable = True, frameY = 2)]
        self.button     = Texture("button.png")
        self.selectwin  = Texture("window_selected.png")

        self.pos        = 0
        self.newpos     = 0
        self.slideUP    = False
        self.slideDOWN  = False

        self.listlength = self.engine.h*(self.htTex.pixelSize[1]/2*len(self.highlight))
        
        self.selected   = None

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
            continue

        if self.slideDOWN:
            if self.pos < self.newPos:
                self.pos += 1
            else:
                self.pos = self.newPos
                self.slideDOWN = False
            continue

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
    def render(self):
        w, h = self.engine.w, self.engine.h

        self.engine.draw(self.background, scale = (w, h)

        if self.selected:
            self.engine.draw(self.selectwin, position = (w/2, h*.9), scale = (w, h*.2))
            
        for f, i in enumerate(self.highlight):
            frame = 1
            if f == self.selected:
                frame = 2
            self.engine.draw(f, position = (w/2, self.pos + self.listlength/len(self.hightlight)*i), frameY = frame)
            

        self.engine.draw(self.slide_b[0], position = (w*.9, h*.1), frameY = 1)
        self.engine.draw(self.slide_b[1], position = (w*.9, h*.9), frameY = 2) 

        
