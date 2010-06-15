'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from numpy import float32, array


#basic template of what a scene may contain
class Scene:
    objInput = None     #this is used as the object holder for input

    #creation of the scene takes place in here
    # All images, sounds, fonts, and scene specific variables
    # should be initialized here, not later in the process or 
    # as local variables, it should be done HERE!!!
    def __init__(self):
        pass

    #anything that is 3d should be rendered in this method
    def render3D(self):
        pass

    #anything that is 2d should be rendered during this process
    def render(self):
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
        
    def run(self):
        if (Scene.objInput == self.image2):
            print 1
            
    def render(self):
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
    def __init__(self, resolution):
        self.resolution = resolution            #width and height of the viewport
        self.camera = Camera(resolution)        #viewport's opengl camera
        self.scenes = []                        #scene's to render
        self.imageObjects = []                  #list of images that can be clicked
        self.input = False                      #is the viewport in its mouse input cycle

        #creates an OpenGL Viewport
        glViewport(0, 0, resolution[0], resolution[1])

    #changes the topmost scene (the one that is being rendered) with a new one
    def changeScene(self, scene):
        if scene not in self.scenes:
            self.scenes.pop(-1)
            self.scenes.append(scene)

    #removes the passed scene
    def popScene(self, scene):
        if scene in self.scenes:
            self.scenes.remove(scene)

    #adds the passed scene
    def addScene(self, scene):
        if scene not in self.scenes:
            self.scenes.append(scene)
    
    #checks to see where the position of the mouse is over 
    #an object and if that object has been clicked
    def detect(self, scene):
        glDisable(GL_TEXTURE_2D);
        glDisable(GL_FOG);
        glDisable(GL_LIGHTING);

        Scene.objInput = None
        scene.render()

        x,y = pygame.mouse.get_pos()
        mouseEvent = pygame.mouse.get_pressed()
        
        if mouseEvent[0] == True:
	    #ONLY DO THIS IF MOUSE CLICKED
            #finds the color of the pixel the cursor is over,
            #if it is over an image it should return the image's color ID
            pixels = glReadPixelsub(x, self.resolution[1] - y, 1, 1, GL_RGB)

            #checks each of the images
            for image in self.imageObjects:
                pick_color = image.pick_color.tolist()

                if (pick_color[0] == pixels[0][0][0] and \
                    pick_color[1] == pixels[0][0][1] and \
                    pick_color[2] == pixels[0][0][2]):
                        #print pick_color
                        Scene.objInput = image

    #renders a scene fully textured
    def render(self, scene):
        glEnable(GL_TEXTURE_2D);
        glEnable(GL_FOG);
        glEnable(GL_LIGHTING);

        scene.render()

    def run(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.input = False                          #tell the scene to reset input at the beginning of each cycle

        if self.scenes:
            scene = self.scenes[-1]                 #only topmost scene should be rendered and updated

            scene.run()                             #any calculations of interactions are processed from the
                                                    # previous loop before anything new is rendered

            scene.render3D()                        #for anything in the scene that might need perspective

            try:
                self.camera.setOrthoProjection()    #changes projection so the hud/menus can be drawn
                self.render(scene)                  #renders anything to the scene that is 2D
                pygame.display.flip()               #switches back buffer to the front
                self.input = True                   #sets it so now images are just drawn in their color ID
                self.detect(scene)                  #checks to see if any object on the back buffer has been clicked
            finally:
                self.camera.resetProjection()       #resets the projection to have perspective

        glFlush()

        #clears the clickable images at the end of each frame
        self.imageObjects = []

