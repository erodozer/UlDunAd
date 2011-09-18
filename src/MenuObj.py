'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
import Input

#creates a little button menu
class MenuObj:
    def __init__(self, scene, commands, position = (0, 0), fontStyle = None,
                 buttonStyle = None, window = None, horizontal = False, sound = "chime.wav"):
    
        self.scene    = scene
        self.engine   = scene.engine    
        self.chime    = SoundObj(sound)
        
        self.commands = commands        #the commands to choose from (are drawn on the buttons)
        self.direction = horizontal     #are the buttons in order vertically or horizontally
                
        #font setting for buttons
        if fontStyle == None:
            fontStyle = self.engine.data.defaultFont
        self.text     = FontObj(fontStyle)

        #which keys select the next or previous button
        if self.direction:
            self.moveKeys = [Input.RtButton, Input.LtButton]
        else:
            self.moveKeys = [Input.DnButton, Input.UpButton]
        
        #the texture used for the buttons and the buttons themselves
        if buttonStyle == None:
            buttonStyle = self.engine.data.defaultButton  
        self.buttons  = [ButtonObj(n, style = buttonStyle) for n in self.commands]
                   
        #where on the screen should the menu be displayed
        #  verticle is positioned from the top
        #  horizontal from the left
        self.position = position
        
        for i, button in enumerate(self.buttons):
            if self.direction:
                pos = [self.position[0] + ((button.width + 5) * i), self.position[1]]
            else:
                pos = [self.position[0], self.position[1] + (-(button.height + 5) * i)]
                
            button.setPosition(pos[0], pos[1])
        
        #window setup
        self.window = None
        if window:
            button = self.buttons[0]
            self.window = WinObj(Texture(window))
            #vertical position is based on center button
            y = self.buttons[len(self.buttons)/2].position[1]
            if len(self.buttons) % 2 == 0:
                y = (y + self.buttons[len(self.buttons)/2 - 1].position[1])/2
            self.window.setPosition(position[0], y)
        
        self.index = 0                  #which button is selected
        
    #arrow keys select which button it is
    #enter/return performs the scene's set action for that button
    def keyPressed(self, key):
        if key == Input.AButton:
            self.scene.select(self.index)
            self.playChime()
            
        if key == self.moveKeys[0]:
            if self.index + 1 < len(self.commands):
                self.index += 1
            else:
                self.index = 0
                
        elif key == self.moveKeys[1]:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.commands) - 1
                
        return None
       
    #plays a chime sound effect 
    def playChime(self):
        try:
            self.chime.play()
        except:
            pass
            
    #button is selected by being clicked
    #if the button is clicked again it performs the scene's action
    #  for that button being clicked
    def buttonClicked(self, image):
        if (image in self.buttons):
            i = self.buttons.index(image)
            if not self.index == i:
                self.index = i
            else:
                self.scene.select(self.index)
                self.chime.play()
                
    #renders the menu
    def render(self, visibility = 1.0):
        
        draw = False
        if not self.window:
            draw = True
        
        if self.window:
            button = self.buttons[0]
            self.window.setDimensions(button.width + 20, (button.height + 20) * len(self.buttons))
            self.window.draw()
            if (self.window.scale[0] >= button.width + 10 and \
                self.window.scale[0] >= (button.height + 10) * len(self.buttons)):
                draw = True
                
        if draw:
            for i, button in enumerate(self.buttons):
                if i == self.index:
                    button.setActive(True)
                else:
                    button.setActive(False)
                button.draw()
        
                
                
