'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View import *

class MainMenu(Scene):
    def __init__(self, engine):
        self.engine = engine
        self.text       = FontObj(self.engine.data.defaultFont)
        self.commands   = ["New Game", "Continue", "Exit"]
        self.buttons    = [ImgObj(self.engine.data.defaultButton, True, frameY = 2)
                           for n in range(len(self.commands))]
        self.background = ImgObj(Texture("title.png"))

        self.music = BGMObj("test.mp3")
        
    def run(self):
        if (Scene.objInput in self.buttons):
            Scene.objInput.setFrame(y = 2)
            if Scene.objInput == self.buttons[0]:
                self.engine.viewport.changeScene("CreateFamily")
        else:
            for b in self.buttons:
                b.setFrame(y = 1)
            
            
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))        
        for i, button in enumerate(self.buttons):
            self.engine.drawImage(button, position = (w*.18, h*(.5 - .1*i)),
                                  color = (.5,1.0,1.0,.5))

            self.text.setText(self.commands[i]) 
            self.text.setPosition(w*.18, h*(.5-.1*i))
            self.text.scaleHeight(36.0)
            self.text.draw()

