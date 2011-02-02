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
        
        self.font = FontObj("default.ttf", self.engine.currentFPS, size = 15)
        self.font.setPosition(5, self.engine.h-20)
        self.font.setAlignment("left")
        
        self.updateRate = 100           #updates the clock after this many milliseconds
        self.counter = 0                #update counter
        
        #tests drawing of windows
        self.window     = WinObj(Texture("window.png"), 300, 128)
        self.size       = 0
        
        #tests drawing of images, sliding, and spinning
        self.test       = [ImgObj(Texture("test.png")), 0, 0]
        self.bar        = BarObj(Texture("bar.png"), 128)
        self.bar.setPosition(self.engine.w*.3, self.engine.h*.1)
        
        #animation testing
        self.sprite = ImgObj(Texture(os.path.join("actors", "sprites", "male", "standing.png")), frameX = 4)
        self.sprite.setPosition(self.engine.w * .8, self.engine.h * .8)
        #self.sprite.setScale(1.0, 1.0)
        self.spriteSize = 0
        
    def buttonPressed(self, image):
        if image == self.image2:
            print 1
            
    def keyPressed(self, key, char):
        if key == K_SPACE:
            if self.size < 4:
                self.size += 1
            else:
                self.size = 0
            print self.size
        elif key == K_z:
            if self.test[1] < 2:
                self.test[1] += 1
            else:
                self.test[1] = 0
            print self.test[1]
        elif key == K_UP:
            self.test[2] += 45
            print self.test[0].angle
        elif key == K_DOWN:
            self.test[2] -= 45
            print self.test[0].angle
        elif key == K_x:
            if self.spriteSize == 0:
                self.spriteSize = 1
            else:
                self.spriteSize = 0
     
    def run(self):
        self.counter += 1
        if self.counter % self.updateRate == 0:
            self.counter = 0
    
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h
        
        positions = [(w/2,h), 
                     (w,h/2), 
                     (w/2,0),
                     (0,h/2),
                     (w/2,h/2)]

        self.window.setPosition(w*.5, h*.5)
        if self.size == 1:
            self.window.setDimensions(500, 320)
        elif self.size == 2:
            self.window.setDimensions(200, 200)
        elif self.size == 3:
            self.window.setDimensions(128, 450)
        elif self.size == 4:
            self.window.setDimensions(700, 500)
        else:
            self.window.setDimensions(300, 128)
        self.window.setColor((1.0,1.0,1.0,.4))
        self.window.draw()
        
        self.test[0].spin(self.test[2])
        
        if self.test[1] == 1:
            self.test[0].slide(w*.8, h*.25)
        elif self.test[1] == 2:
            self.test[0].slide(w*.2, h*.75)
        else:
            self.test[0].slide(w*.5, h*.5)
        self.test[0].draw()

        if self.spriteSize == 0:
            self.sprite.setScale(1.0, 1.0)
        else:
            self.sprite.setScale(3.0, 3.0)
            
        self.engine.drawAnimation(self.sprite, direction = 0, loop = True, reverse = 0)
        
        if self.counter == 0:
            self.font.setText(self.engine.currentFPS)
        self.font.draw()
        
        self.bar.draw()
                
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
        
        self.transitionTime = 16.0             #time it takes to transition between scenes (milliseconds)
        
        self.fade = ImgObj(Texture(surface = pygame.Surface(resolution)))
        self.fade.setPosition(.5, .5)
        #creates an OpenGL Viewport
        glViewport(0, 0, resolution[0], resolution[1])

    #changes the topmost scene (the one that is being rendered) with a new one
    def changeScene(self, scene):
        if scene not in self.scenes:
            Input.resetKeyPresses()
            if scene == "TestScene":
                scene = TestScene(self.engine)
            else:
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
        if scene == "TestScene":
            scene = TestScene(self.engine)
        else:
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
            t = 1.0 / self.transitionTime

            #all scenes should be rendered but not checked for input
            for i, scene in enumerate(self.scenes):
                topmost = bool(i == len(self.scenes)-1)#is the scene the topmost scene
                if not topmost:
                    visibility = self.visibility[i] = max(0.0, self.visibility[i] - t)
                    if visibility <= 0.0:
                        self.scenes.pop(i)
                        self.visibility.pop(i)
                        continue
                else:
                    visibility = self.visibility[i] = min(1.0, self.visibility[i] + t)
                    
                if topmost:
                    scene.run()                         #any calculations of interactions are processed from the
                                                        # previous loop before anything new is rendered

                scene.render3D()                        #for anything in the scene that might need perspective

                try:
                    self.camera.setOrthoProjection()    #changes projection so the hud/menus can be drawn
                    self.render(scene, visibility)      #renders anything to the scene that is 2D
                finally:
                    self.camera.resetProjection()       #resets the projection to have perspective

        
            if len(self.scenes) > 1:
                self.fade.setColor((1,1,1,self.visibility[-2] - self.visibility[-1]))
                self.fade.draw()
                
            pygame.display.flip()               #switches back buffer to the front
            
            #only the topmost scene should be checked for input
            if self.visibility[-1] >= 1.0:      #only detect when the scene is fully visible
                self.detect(self.scenes[-1])    #checks to see if any object on the back buffer has been clicked
                
        #clears the clickable images at the end of each frame
        self.imageObjects = []

