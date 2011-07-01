from sysobj import *
from OpenGL.GL import glPushMatrix, glPopMatrix, glScalef

from PIL import Image, ImageDraw

import math

#this is the hud that displays the character information
#it's not one big window, instead it is 1-3 little windows
#arranged to save space in an efficent manner when more or
#less characters are present in your party
class BattleHUDCharacter:
    def __init__(self, character, position = (0,0), scale = 1.0):
        self.character = character

        self.x, self.y = position
        
        scenepath = os.path.join("scenes", "battlesystem")
        
        self.setPosition(self.x, self.y)
    
        self.scale = scale
        
        self.drawing = ImgObj(Texture(os.path.join(scenepath, "circle.png")))
        
        #these determine the size of the PIL pie-slice
        self.centerX   = self.drawing.width/2
        self.centerY   = self.drawing.height/2
        self.inRadius  = 0
        self.outRadius = self.drawing.width/2
    
        self.hpMeter = self.generateCircle(self.drawing)
        self.fpMeter = self.generateCircle(self.drawing)
        
        self.face = self.character.sprites['face']
        
    #generates all the images needed for the circle
    def generateCircle(self, base):
        drawnOverlays = {}
        baseFillImageSize = base.pixelSize
        for degrees in range(0, 361, 5):
            image = Image.open(base.texture.path)
            mask = Image.new('RGBA', baseFillImageSize)
            overlay = Image.new('RGBA', baseFillImageSize)
            draw = ImageDraw.Draw(mask)
            draw.pieslice((self.centerX-self.outRadius, self.centerY-self.outRadius,
                     self.centerX+self.outRadius, self.centerY+self.outRadius),
                     -90, degrees-90, outline=(255,255,255,255), fill=(255,255,255,255))
            draw.ellipse((self.centerX-self.inRadius, self.centerY-self.inRadius,
                    self.centerX+self.inRadius, self.centerY+self.inRadius),
                    outline=(0, 0, 0, 0), fill=(0, 0, 0, 0))
            r,g,b,a = mask.split()
            overlay.paste(image, mask=a)
            dispOverlay = ImgObj(Texture(surface = overlay))
            drawnOverlays[degrees] = dispOverlay
        return drawnOverlays
        
    def update(self):
        pass
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        
        s = self.scale
        
        self.face.setPosition(self.x, self.y-(15*s))
        self.face.setScale(140*s, 70*s, inPixels = True)
        self.face.setRect((0.0,0.5,1.0,1.0))
        self.face.draw()
        
        self.drawing.setPosition(self.x, self.y)
        self.drawing.setScale(150*s,150*s,inPixels = True)
        self.drawing.setColor((0,0,0,1.0))
        self.drawing.draw()
        
        degrees = lambda ratio: int(180*ratio) - (int(180*ratio) % 5)
        
        circle = self.hpMeter[degrees(self.character.currentHP/float(self.character.hp))]
        circle.setPosition(self.x, self.y)
        circle.setScale(-150*s, 150*s, inPixels = True)
        circle.setColor((0,1.0,0,1.0))
        circle.setAngle(-45)
        circle.draw()

        circle = self.fpMeter[degrees(self.character.fp/float(self.character.maxFP))]
        circle.setPosition(self.x, self.y)
        circle.setScale(150*s, 150*s, inPixels = True)
        circle.setColor((1.0,1.0,0,1.0))
        circle.setAngle(45)
        circle.draw()
        
        self.face.setPosition(self.x, self.y+(55*s))
        self.face.setScale(140*s, 70*s, inPixels = True)
        self.face.setRect((0.0,0.0,1.0,0.5))
        self.face.draw()
        
