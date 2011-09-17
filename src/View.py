'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
import numpy as np
from numpy import float32, array

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *
import random

import WorldScenes

import Input

#basic template of what a scene may contain
class Scene:
    #creation of the scene takes place in here
    # All images, sounds, fonts, and scene specific variables
    # should be initialized here, not later in the process or 
    # as local variables, it should be done HERE!!!
    def __init__(self, engine):
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
        
#test scene for showing off the particle system
class ParticleTest(Scene):
    def __init__(self, engine):
        self.engine = engine
        scenepath = os.path.join("scenes", "particletest")
        self.particle = [ImgObj(Texture(os.path.join(scenepath, "smoke.png"))),
                         ImgObj(Texture(os.path.join(scenepath, "star.png")))]
        
        self.particleSystem = ParticleSystem(self.particle[0], random.randint(-90, 90), self.engine.clock, (-10, -10))

    #anything that is 2d should be rendered during this process
    def render(self, visibility):
        self.particleSystem.draw()
        if len(Input.clicks) > 0:
            print Input.clicks[-1]
            self.particleSystem.reset(pos = Input.clicks[-1])

#here's a little test scene to show how a scene may function
class TestScene(Scene):
    def __init__(self, engine):
        self.engine = engine
        
        self.font = FontObj("default.ttf", self.engine.currentFPS, size = 15)
        self.font.setPosition(5, self.engine.h-20)
        self.font.setAlignment("left")
        
        scenepath = os.path.join("scenes", "test")
        self.updateRate = 100           #updates the fps clock after this many milliseconds
        self.counter = 0                #update counter
        
        
        #tests drawing of windows
        self.window     = WinObj(Texture(os.path.join(scenepath, "window.png")), 300, 128)
        self.size       = 0
        #titled window with title bar
        self.titleWinEx = TitledWinObj(WinObj(Texture(os.path.join(scenepath, "window2.png"))),
                                       FontObj("default.ttf"),
                                       "Testing",
                                       256, 256,
                                       BarObj(Texture(os.path.join(scenepath, "titlebar.png"))),
                                       )
        self.titleWinEx.setPosition(self.engine.w*.75, self.engine.h/2)
        #without title bar
        self.titleWinEx2 = TitledWinObj(WinObj(Texture(os.path.join(scenepath, "window2.png"))),
                                       FontObj("default.ttf"),
                                       "Testing",
                                       256, 256)
        self.titleWinEx2.setPosition(self.engine.w*.25, self.engine.h/2)
        
        #tests drawing of images, sliding, and spinning
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setPosition(self.engine.w/2, self.engine.h/2)
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.test       = [ImgObj(Texture(os.path.join(scenepath, "test.png"))), 0, 0]
        self.bar        = BarObj(Texture(os.path.join(scenepath, "bar.png")), 128)
        self.bar.setPosition(self.engine.w*.5, self.engine.h*.5)
        
        #animation testing
        self.sprite = ImgObj(Texture(os.path.join(scenepath, "testsprite.png")), frameX = 4)
        self.sprite.setPosition(self.engine.w * .8, self.engine.h * .8)
        #self.sprite.setScale(1.0, 1.0)
        self.spriteSize = 0
        
        #tests camera focus
        self.zoomedIn = False
        
        self.helpButtons = [[Input.AButton, "Zoom in/out"],
                            [Input.BButton, "Change window example scaling"],
                            [Input.CButton, "Scale the sprite"],
                            [Input.DButton, "Slides test image"]]
                    
        self.triangVtx = np.array([[ 0,  1, 0],
                                   [-1, -1, 0],
                                   [ 1, -1, 0]], dtype=np.float32)
        
    def buttonPressed(self, image):
        if image == self.image2:
            print 1
            
    def keyPressed(self, key, char):
        if key == Input.BButton:
            if self.size < 4:
                self.size += 1
            else:
                self.size = 0
            print self.size
        elif key == Input.DButton:
            if self.test[1] < 2:
                self.test[1] += 1
            else:
                self.test[1] = 0
            print self.test[1]
        elif key == Input.CButton:
            if self.spriteSize == 0:
                self.spriteSize = 1
            else:
                self.spriteSize = 0
        elif key == Input.AButton:
            self.zoomedIn = not self.zoomedIn
            if self.zoomedIn:
                self.engine.viewport.camera.focus(self.sprite.position[0], self.sprite.position[1], 200)
            else:
                self.engine.viewport.camera.resetFocus()
        elif key == K_LSHIFT:
            self.test[2] += 45
            print self.test[0].angle
        elif key == K_RSHIFT:
            self.test[2] -= 45
            print self.test[0].angle
        #messing around with the bar
        elif key == K_SPACE:
            if self.bar.scale == 256:
                self.bar.setLength(96)
            else:
                self.bar.setLength(256)
        elif key == Input.LtButton:
            self.bar.setAlignment("left")
        elif key == Input.RtButton:
            self.bar.setAlignment("right")
        elif key == Input.DnButton:
            self.bar.setDirection("up")
        elif key == Input.UpButton:
            self.bar.setDirection("down")
        elif key == K_RETURN:
            self.bar.setDirection("horizontal")
            self.bar.setAlignment("center")
            
    def run(self):
        self.counter += 1
        if self.counter % self.updateRate == 0:
            self.counter = 0
    
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h
        
        self.background.draw()
        
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
      
        self.titleWinEx.draw()
        self.titleWinEx2.draw()
        
        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glColor4f(1,.5,.5,1.0)
        glTranslatef(400,40.0,0)
        glScalef(30.0,30.0,1.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.triangVtx)
        glDrawArrays(GL_TRIANGLES, 0, self.triangVtx.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)
        
#this is the main viewport/engine
#it handles the mouse input, the opengl window
#and which scenes are being rendered.
class Viewport:
    def __init__(self, engine, resolution):
        self.engine = engine                    #the game engine and main values
        self.resolution = resolution            #width and height of the viewport
        self.width, self.height = self.resolution
        self.camera = Camera((0, 0), 100)                  
                                                #viewport's opengl camera
        self.scenes = []                        #scenes to render
        self.addScenes = None
        self.input = False                      #is the viewport in its mouse input cycle
        
        self.transitionTime = 32.0             #time it takes to transition between scenes (milliseconds)
        
        self.fade = 0.0

        #images and text used for displaying the onscreen button help
        self.inputButtons = [ImgObj(Texture("inputButtons.png"), frameY = 5),
                             FontObj("default.ttf", size = 16)]
        self.inputButtons[0].setScale(32,32, inPixels = True)
        
        self.setupViewport()
        
    def setupViewport(self):
        #creates an OpenGL Viewport
        glViewport(0, 0, self.resolution[0], self.resolution[1])

        glEnable (GL_LIGHTING)
        glEnable (GL_LIGHT0)
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glEnable ( GL_COLOR_MATERIAL )
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_ALPHA_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glAlphaFunc(GL_NOTEQUAL,0.0)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_FOG)
        glEnable(GL_LIGHTING)
        
    #creates a projection with perspective
    def setPerspectiveProjection(self):
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glPushMatrix()
        gluPerspective(45, 1.0*self.width/self.height, -500.0, 1000.0)
        
    #creates an orthographic projection
    def setOrthoProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glPushMatrix()                   
        glOrtho(0, self.width, 0, self.height, -500.0, 1000.0)
        glScalef((self.width/800.0), (self.height/600.0), 1.0)
        glTranslatef(-self.camera.focusx, -self.camera.focusy, 1.0)
        glScalef(self.camera.zoom/100.0, self.camera.zoom/100.0, 1.0)
        
    def resetProjection(self):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
              
    #if the scene has a list of buttons and their commands then they can be 
    #rendered to the screen if enabled in the uldunad.ini
    def renderInputHelp(self, scene):
        #only draw the help buttons if they exist
        try:
            if not scene.helpButtons:   #if helpButtons is empty
                return 
        except AttributeError:          #if helpButtons doesn't even exist
            return
            
        #drawing should start in the bottom right corner
        x = self.resolution[0]
        y = 32
        self.inputButtons[1].setAlignment("left")
        
        for help in scene.helpButtons:
            
            #draw the help test
            self.inputButtons[1].setText(help[1])
            x -= self.inputButtons[1].width+10
            self.inputButtons[1].setPosition(x, y)
            self.inputButtons[1].draw()
            
            #draw the corresponding button
            x -= self.inputButtons[0].width/2 + 10
            #directional buttons
            if (help[0] == Input.UpButton or
                help[0] == Input.DnButton or
                help[0] == Input.LtButton or
                help[0] == Input.RtButton):
                self.inputButtons[0].setFrame(y=5)
                if help[0] == Input.UpButton:
                    self.inputButtons[0].setAngle(0)
                elif help[0] == Input.RtButton:
                    self.inputButtons[0].setAngle(90)
                elif help[0] == Input.DnButton:
                    self.inputButtons[0].setAngle(180)
                else:
                    self.inputButtons[0].setAngle(270)
            #letter buttons
            else:
                self.inputButtons[0].setAngle(0)
                if help[0] == Input.AButton:
                    self.inputButtons[0].setFrame(y=1)
                elif help[0] == Input.BButton:
                    self.inputButtons[0].setFrame(y=2)
                elif help[0] == Input.CButton:
                    self.inputButtons[0].setFrame(y=3)
                elif help[0] == Input.DButton:
                    self.inputButtons[0].setFrame(y=4)
            self.inputButtons[0].setPosition(x, y)
            self.inputButtons[0].draw()    
            x -= self.inputButtons[0].width/2 + 10
            
    #changes the topmost scene (the one that is being rendered) with a new one
    def changeScene(self, scene):
        if scene not in self.scenes:
            try:
                Input.resetKeyPresses()
                ImgObj.clickableObjs = []
                if scene == "TestScene":
                    scene = TestScene(self.engine)
                elif scene == "ParticleTest":
                    scene = ParticleTest(self.engine)
                else:
                    scene = WorldScenes.create(self.engine, scene)
                self.addScene = scene
            except ImportError:
                print scene + " has not yet been implemented or does not exist"
        else:
            print scene + " is already present"
            
    #removes the passed scene
    def popScene(self, scene):
        if scene in self.scenes:
            Input.resetKeyPresses()
            self.scenes.remove(scene)
        else:
            print scene + " has not been pushed yet"

    #adds the passed scene
    def pushScene(self, scene):
        try:
            Input.resetKeyPresses()
            ImgObj.clickableObjs = []
            if scene == "TestScene":
                scene = TestScene(self.engine)
            elif scene == "ParticleTest":
                scene = ParticleTest(self.engine)
            else:
                scene = WorldScenes.create(self.engine, scene)
            self.addScene = scene
        except ImportError:
            print scene + " has not yet been implemented or does not exist"
            
    #checks to see where the position of the mouse is over 
    #an object and if that object has been clicked
    def detect(self, scene):
        for key, char in Input.getKeyPresses():
            scene.keyPressed(key, char)

        for press in Input.clicks:
            clickedImages = [image.getCollision(press) for image in ImgObj.clickableObjs]
            try:
                x = clickedImages.index(True)
                scene.buttonClicked(ImgObj.clickableObjs[x])
            except ValueError:
                continue


    #renders a scene fully textured
    def render(self, scene, visibility):
        scene.render(visibility)
        self.renderInputHelp(scene)
        
    def run(self):
        #clears the buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #reset matrix every frame
        glLoadIdentity()
        
        #ticks/rate of change in time
        t = 1.0 / self.transitionTime

        if self.addScene:
            self.fade = min(1.0, self.fade + t)
            if self.fade >= 1.0:
                if self.scenes:
                    self.scenes.pop(-1)
                self.scenes.append(self.addScene)
                self.addScene = None
        else:
            self.fade = max(0.0, self.fade - t)                
                
        #fades the screen
        #glColor4f(1,1,1,1-self.fade)
            
        #all scenes should be rendered but not checked for input
        for i, scene in enumerate(self.scenes):
            topmost = bool(scene == self.scenes[-1]) #is the scene the topmost scene
                    
            if topmost:
                scene.run()                         #any calculations of interactions are processed from the
                                                    # previous loop before anything new is rendered

            try:
                self.setOrthoProjection()           #changes projection so the hud/menus can be drawn
                self.render(scene, 1.0)             #renders anything to the scene that is 2D
                self.resetProjection()
            finally:
                self.setPerspectiveProjection()     #resets the projection to have perspective
                scene.render3D()                    #for anything in the scene that might need perspective
                self.resetProjection()
                
        pygame.display.flip()                       #switches back buffer to the front
            
        if self.scenes:
            #only the topmost scene should be checked for input
            self.detect(self.scenes[-1])            #checks to see if any object on the back buffer has been clicked
            
