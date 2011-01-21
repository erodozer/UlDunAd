'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from numpy import float32, array

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import WorldScenes

import Input

#basic template of what a scene may contain
class Scene:
    #creation of the scene takes place in here
    # All images, sounds, fonts, and scene specific variables
    # should be initialized here, not later in the process or 
    # as local variables, it should be done HERE!!!
    def __init__(self):
        pass

    #if an image is clicked this should determine what should happen
    def buttonClicked(self, image):
        pass
        
    #if a key is pressed, what happens is controlled in this method
    def keyPressed(self, key, char):
        pass
        
    #anything that is 3d should be rendered in this method
    def render3D(self):
        pass

    #anything that is 2d should be rendered during this process
    def render(self, visibility):
        pass

    #anything involving actions between the user 
    # and the game should happen in here
    def run(self):
        pass
        
#here's a little test scene to show how a scene may function
# it draws 5 awesome smilies, where only the one in the middle 
# reacts to being clicked
class TestScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        Texture(self, "textTex", "test.png")
        self.image  = ImgObj(self.textTex, True)
        self.image2 = ImgObj(self.textTex, True)
        
    def buttonPressed(self, image):
        if image == self.image2:
            print 1
    
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h
        
        positions = [(w/2,h), 
                     (w,h/2), 
                     (w/2,0),
                     (0,h/2),
                     (w/2,h/2)]
        
        for i in range(len(positions) - 1):
            self.engine.drawImage(self.image, position = positions[i])
        self.engine.drawImage(self.image2, position = position[-1])
        
#this is the main viewport/engine
#it handles the mouse input, the opengl window
#and which scenes are being rendered.
class Viewport:
    def __init__(self, engine, resolution):
        self.engine = engine                    #the game engine and main values
        self.resolution = resolution            #width and height of the viewport
        self.camera = Camera(resolution)        #viewport's opengl camera
        self.scenes = []                        #scenes to render
        self.visibility = []                    #visibility of the scenes
        self.inputObjects = []                  #list of images that can be clicked
        self.input = False                      #is the viewport in its mouse input cycle
        
        self.transitionTime = 512.0             #time it takes to transition between scenes (milliseconds)
        
        #creates an OpenGL Viewport
        glViewport(0, 0, resolution[0], resolution[1])

    #changes the topmost scene (the one that is being rendered) with a new one
    def changeScene(self, scene):
        if scene not in self.scenes:
            Input.resetKeyPresses()
            self.scenes.pop(-1)
            self.visibility.pop(-1)
            scene = WorldScenes.create(self.engine, scene)
            self.scenes.append(scene)
            self.visibility.append(0.0)
            self.hasTransitioned = True

    #removes the passed scene
    def popScene(self, scene):
        if scene in self.scenes:
            Input.resetKeyPresses()
            self.visibility.pop(self.scenes.index(scene))
            self.scenes.remove(scene)

    #adds the passed scene
    def addScene(self, scene):
        Input.resetKeyPresses()
        scene = WorldScenes.create(self.engine, scene)
        self.scenes.append(scene)
        self.visibility.append(0.0)
    
    #checks to see where the position of the mouse is over 
    #an object and if that object has been clicked
    def detect(self, scene):
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        glDisable(GL_LIGHTING)

        for key, char in Input.getKeyPresses():
            scene.keyPressed(key, char)

        if Input.clicks:
            #print Input.clicks
            for press in Input.clicks:
                for image in self.inputObjects:
                    if image.getCollision(press):
             #           print "image clicked!", image
                        scene.buttonClicked(image)
                        break
    
    #renders a scene fully textured
    def render(self, scene, visibility):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_FOG)
        glEnable(GL_LIGHTING)

        glScalef(self.resolution[0]/800.0,self.resolution[1]/600.0, 1.0)

        scene.render(visibility)

    def run(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.scenes:
            #ticks/rate of change in time
            t = float(self.engine.clock.get_time()) / self.transitionTime

            #all scenes should be rendered but not checked for input
            for i, scene in enumerate(self.scenes):
                topmost = bool(scene == self.scenes[-1])#is the scene the topmost scene
                visibility = self.visibility[i] = min(1.0, self.visibility[i] + t)
                
                if topmost:
                    scene.run()                         #any calculations of interactions are processed from the
                                                        # previous loop before anything new is rendered

                scene.render3D()                        #for anything in the scene that might need perspective

                try:
                    self.camera.setOrthoProjection()    #changes projection so the hud/menus can be drawn
                    self.render(scene, visibility)      #renders anything to the scene that is 2D
                    pygame.display.flip()               #switches back buffer to the front
                    if topmost:                         #only should the topmost scene be checked for input
                        self.detect(scene)              #checks to see if any object on the back buffer has been clicked
                finally:
                    self.camera.resetProjection()       #resets the projection to have perspective

        #clears the clickable images at the end of each frame
        self.imageObjects = []

