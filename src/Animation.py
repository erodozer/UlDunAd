
from ImgObj import ImgObj
from Texture import Texture

import os

class Animation(object):
    def __init__(self, path):
        file = open(os.path.join("..", "data", path + ".anim"))
                                                    #the file containing the animation sequencing
        
        self.image = None                           #the image file
        self.relation = "parent"                    #relation of the position of the image to another image or the screen
        self.parent = None                          #parent image for positioning, if the animation is set to parent relation
        self.currentFrame = 0                       #the current frame of animation
        self.frames = []                            #the frames of animation
        
        #reads in lines one at a time for the sequence file
        for i, line in enumerate(file):
            #first line designates how many frames are in the image
            if i == 0:  
                self.image = ImgObj(Texture(path + ".png"), frameX = int(line))
            #second line designates relation positioning
            elif i == 1:    
                if line == "screen"
                    self.relation = "screen"
                else:
                    self.relation = "parent"
            #every line after is a bit complex
            #   Animation files allow one to render multiple sprites of the same image 
            #   in different locations at the same time.  Additionally, the number
            #   of frames in the animation is dependent on lines, not how many frames
            #   are set in the image.  Multiple sprites are divided by |.  Each sprite
            #   has 3 properties, 1) frame number, 2) x position, 3) y position
            else:   
                self.frames.append([int(f) for f in l.split(",") for l in line.split("|")])
     
    #sets the parent image which parent relation is associated with
    def setParent(self, image):
        self.parent = image
        
    #will draw the animation sequence to screen
    def draw(self):
        
        if self.currentFrame >= len(self.frames):
            return False
            
        frame = self.frames[self.currentFrame]
        
        #draw the multiple sprites to screen
        #positions are in terms of 0.0-1.0, not pixels
        for sprite in frame:
            self.image.setFrame(x = sprite[0])
            if self.relation == "parent":
                point = (self.parent.position[0] - self.parent.scale[0]/2,
                         self.parent.position[1] - self.parent.scale[1]/2)
                self.image.setPosition(point[0] * sprite[1] * self.parent.scale[0],
                                       point[1] * sprite[2] * self.parent.scale[1])
            else:
                self.image.setPosition(sprite[1], sprite[2])
            self.image.draw()
            
        self.currentFrame += 1
        
        return True
