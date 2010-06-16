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
        self.buttonTex  = Texture("button.png")
        self.text       = FontObj("default.ttf")
        self.buttons    = [ImgObj(self.buttonTex, True, frameY = 2) for n in range(5)]
        self.background = ImgObj(Texture("bg.png"))

        self.music = BGMObj("test.mp3")
        
    def run(self):
        if (Scene.objInput in self.buttons):
            Scene.objInput.setFrame(y = 1)
            #self.engine.viewport.changeScene(MainMenu(self.engine))
        else:
            for b in self.buttons:
                b.setFrame(y = 2)
            
            
    def render(self):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))        
        self.text.setPosition(w/2, h/2)
        self.text.setText("awesome")
        #self.text.setScale(200,50)
        self.text.draw()
        for i, button in enumerate(self.buttons):
            self.engine.drawImage(button, position = (w*.18, h*(.1 + .1*i)))

