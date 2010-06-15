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
        self.buttons    = [ImgObj(self.buttonTex, True),
		            	  ImgObj(self.buttonTex, True),
		            	  ImgObj(self.buttonTex, True),
	            		  ImgObj(self.buttonTex, True),
			              ImgObj(self.buttonTex, True)]
        self.background = ImgObj(Texture("bg.png"))

        self.music = BGMObj("test.mp3")
        
    def run(self):
        if (Scene.objInput in self.buttons):
            self.buttons[self.buttons.index(Scene.objInput)].setRect((0,0,1,.5))
            #self.engine.viewport.changeScene(MainMenu(self.engine))
        else:
            for b in self.buttons:
                b.setRect((0,.5,1,1))
            
            
    def render(self):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))        
        for i, button in enumerate(self.buttons):
            self.engine.drawImage(button, position = (w*.18, h*(.1 + .1*i)))
            self.text.setPosition(w/2, h/2)
            self.text.setText("awesome")
            self.text.draw()

