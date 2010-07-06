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
        self.infoFont   = FontObj("default.ttf", size = 16)
        self.info       = ["Family: "]
        self.commands   = ["Create", "Battle", "Menu", "", ""]
        self.buttons    = [ImgObj(self.buttonTex, True, frameY = 2) for n in range(5)]
        self.background = ImgObj(Texture("bg.png"))

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
            self.engine.drawImage(button, position = (w*.18, h*(.5 - .1*i)))

            self.text.setText(self.commands[i]) 
            self.text.setPosition(w*.18, h*(.5-.1*i))
            self.text.scaleHeight(36.0)
            self.text.draw()

        if self.engine.family:
            self.infoFont.setPosition(w*.7, h*.9)
            self.infoFont.setText(self.info[0] + self.engine.family.name)
            self.infoFont.draw()

