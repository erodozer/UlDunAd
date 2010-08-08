'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View import *

import Input

class MainMenu(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.text       = FontObj(self.engine.data.defaultFont)
        self.commands   = ["New Game", "Continue", "Exit"]
        self.buttons    = [ImgObj(self.engine.data.defaultButton, True, frameY = 2)
                           for n in range(len(self.commands))]
        self.background = ImgObj(Texture("title.png"))
        
        self.window     = WinObj(Texture("window.png"), 300, 128)
        self.size       = 0
        
        self.music = BGMObj("test.mp3")
        
    def run(self):
        if (Scene.objInput in self.buttons):
            Scene.objInput.setFrame(y = 2)
            if Scene.objInput == self.buttons[0]:
                self.engine.viewport.changeScene("CreateFamily")
        else:
            for b in self.buttons:
                b.setFrame(y = 1)
            
        for key, char in Input.getKeyPresses():
            if key == K_SPACE:
                if self.size < 4:
                    self.size += 1
                else:
                    self.size = 0
                print self.size
            
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))        
        for i, button in enumerate(self.buttons):
            self.engine.drawImage(button, position = (w*.18, h*(.5 - .1*i)),
                                  color = (.5,1.0,1.0,.2))

            self.text.setText(self.commands[i]) 
            self.text.setPosition(w*.18, h*(.5-.1*i))
            self.text.scaleHeight(36.0)
            self.text.draw()
            
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
        self.window.draw()

