'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
from Actor  import *

import string
import Input

class CreateCharacter(Scene):
    def __init__(self, engine):
        self.engine = engine

        self.background = ImgObj(Texture("creation_background.png"))
        self.window = ImgObj(Texture("creation_window.png"))
        buttonTex = Texture("button.png")
        self.button = self.engine.loadImage(buttonTex, boundable = True, frameY = 2)
        self.font   = FontObj("default.ttf")

        self.classes = ["Easy", "Normal", "Hard"]

        #family info
        self.name = []          #name of the family
        self.diffselected = 1   #the difficulty selected (match up number with position in difficulty array
                                # (1 = default, Normal difficulty)

        self.fadeIn     = True  #are the windows transitioning in or out

        self.error = False      #was an error thrown
        self.step = 0           #step 0 = naming, step 1 = choose difficulty

        Input.resetKeyPresses()

    def run(self):
        for key, char in Input.getKeyPresses():
            #name is a maximum of 13 letters
            if len(self.name) < 13:
                if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                    self.name.append(char)
                if len(self.name) > 0:  #can not have the first character be a blank
                    if key == K_SPACE:
                        self.name.append(" ")

            #can only delete letters if there are some to delete
            if len(self.name) > 0:
                if key == K_BACKSPACE:
                    self.name.pop(-1)


        self.button.setFrame(y = 1)
        if Scene.objInput == self.button:
            self.button.setFrame(y = 2)
            self.next()
        for i, button in enumerate(self.diffButton):
            button.setFrame(y = 1)
            if Scene.objInput == button:
                button.setFrame(y = 2)
                self.diffselected = i
                self.next()
            

    def next(self):
        if self.step == 0 and not self.name:
            self.error = True
        else:
            self.step += 1

    def renderNaming(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.engine.drawImage(self.window, position = (w/2, h/2 - h*(.1*(1-visibility))), 
                              color = (1.0,1.0,1.0,visibility))

        if visibility >= 1.0:
            self.engine.drawText(self.font, "Enter a name", (w*.5, h*.6))
            name = string.join(self.name, '')
            self.engine.drawText(self.font, name, (w*.5, h*.5))

            if name:
                self.engine.drawImage(self.button, position = (w/2, h*.4))
                self.engine.drawText(self.font, "Next", (w*.5, h*.4))

    def renderDifficulty(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.engine.drawImage(self.window, position = (w/2, h/2 - h*(.1*(1-visibility))), 
                              color = (1.0,1.0,1.0,visibility))


        if visibility >= 1.0:
            self.engine.drawText(self.font, "Select the difficulty", (w*.5, h*.6))
            for i, diff in enumerate(self.difficulty):
                self.engine.drawImage(self.diffButton[i], position = (w*.5, h*.54-h*(.07*i)))
                self.engine.drawText(self.font, diff, (w*.5, h*.54-h*(.07*i)))

    def create(self):
        name = string.join(self.name, '')
        family = Family(None)
        family.create(name, self.diffselected)
        self.engine.family = Family(name)
        self.engine.viewport.changeScene("MainMenu")
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.engine.drawImage(self.background, scale = (w,h))

        if self.step == 0:
            self.renderNaming(visibility)
        elif self.step == 1:
            self.renderDifficulty(visibility)
        else:
            self.create()

        if self.error:
            self.engine.showError("You must enter a name")


        