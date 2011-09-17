
from Texture import Texture
from ImgObj  import *
from FontObj import FontObj

class ButtonObj(ImgObj):
    
    def __init__(self, text, style = None, fontStyle = None):
        
        if style:
            if isinstance(style, Texture):
                self.texture = style
            else:
                self.texture = Texture(style)
        else:
            self.texture = Texture("button.png")
            
        if fontStyle:
            self.font = fontStyle
        else:
            self.font = FontObj("default.ttf", 16)
        self.font.setText(text)
            
        #attributes
        self.scale       = (1.0, 1.0)               #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.angle       = 0                        #angle which the image is drawn
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.frameSize   = (1.0,.5)
                                                    #the size of each cell when divided into frames
        self.rect        = (0.0,0.0,self.frameSize[0],self.frameSize[1])
        self.alignment  = CENTER                   #alignment of the vertices for placement
        self.pixelSize   = (self.texture.pixelSize[0],
                            self.texture.pixelSize[1]/2.0)   
        self.width, self.height = self.pixelSize    #the width and height after transformations
                                                    # are taken into account

        self.bounds  = (0.0, 1.0, 0.0, 1.0)         #the bounds of the picture
        self.tBounds = []

        ImgObj.clickableObjs.append(self)
            
        self.createArrays()
        self.frames = [1, 2]
        self.currentFrame = [0,0]
        
        self.active = False                         #is the button active
        
        self.alignment = CENTER                     #alignment for the button
        self.textAlignment = CENTER                 #alignment for the font
        
    def setText(self, text):
        self.font.setText(text)
        
    def setActive(self, active):
        self.active = active
        self.setFrame(y = active+1)
        
    def setAlignment(self, align = None, textalign = None):
        if align:
            super(ButtonObj, self).setAlignment(self, align)
        if textalign:
            self.font.setAlignment(textalign)
        
    def draw(self):
        
        super(ButtonObj, self).draw()
        if self.font.alignment == LEFT:
            self.font.setPosition(self.position[0] - self.width/2 + 4, self.position[1])
        elif self.font.alignment == RIGHT:
            self.font.setPosition(self.position[0] + self.width/2 - 4, self.position[1])
        else:
            self.font.setPosition(self.position[0], self.position[1])
            
        self.font.draw()
        
        
