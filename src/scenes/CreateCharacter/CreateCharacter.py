'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from sysobj import *
from View   import *
from Character  import *

import string
import Input

import Jobs
from Jobs import *

from CreationMenu import CreationMenu
from StatDistMenu import StatDistMenu

class CreateCharacter(Scene):
    def __init__(self, engine):
        self.engine = engine
        w, h = self.engine.w, self.engine.h
        
        self.name   = []
        self.job    = None
    
        scenepath = os.path.join("scenes", "creation")
        self.background = ImgObj(Texture(os.path.join(scenepath, "background.png")))
        self.background.setScale(self.engine.w, self.engine.h, inPixels = True)
        self.background.setPosition(self.engine.w/2,self.engine.h/2)
        
        self.nameWindow = WinObj(Texture(os.path.join(scenepath, "window.png")),w*.5,h*.15)
        self.nameButton = ImgObj(Texture("ok.png"), boundable = True, frameX = 2)
        
        #the jobs to choose from
        jobpath = os.path.join("..", "data", "actors", "jobs")
        self.jobs = Jobs.jobs
                                                    
        self.jobSelect = 0                          #number of the job selected
        self.job = eval(self.jobs[self.jobSelect]+"()")   
                                                    #the job object
                                                    
        self.selectedSprite = 0                     #the sprite selected for the character
        self.gender = "male"
        self.sprites = self.engine.listPath(os.path.join("actors", self.gender, self.job.name), flag="folder")
        self.sprite = ImgObj(Texture(os.path.join("actors", "jobs", self.job.name, self.sprites[self.selectedSprite], "profile.png")))
        
        #stat point distribution
        self.stats = ["Hit Points", "Strength", "Defense", "Agility", "Evasion", "Force", "Resistance"]
        self.statDistMenu = StatDistMenu(self, scenepath)
        self.distPoints = 20
        self.distAreas = [0 for n in self.stats]
                
        #the main menu for selecting what to do in character creation
        self.menu = CreationMenu(self, scenepath)
        
        self.font = FontObj(self.engine.data.defaultFont)
        
        self.error = False      #was an error thrown
        self.step = -1          #step -1 = basic, step 0 = naming, step 1 = distribute stats

    def getSprites(self):
        self.sprites = self.engine.listPath(os.path.join("actors", self.gender), flag="folder")
        self.sprite = ImgObj(Texture(os.path.join("actors", self.gender, self.sprites[self.selectedSprite], "profile.png")))
        
    def run(self):
        self.job = eval(self.jobs[self.jobSelect]+"()")
        self.exists = os.path.exists(os.path.join("..", "data", "actors", "families", self.engine.family.name, string.join(self.name,'')))
        
    def keyPressed(self, key, char):
        if self.step == -1:
            self.menu.keyPressed(key)
        elif self.step == 0:
            #name is a maximum of 13 letters
            if len(self.name) < 13:
                if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                    self.name.append(char)
                if len(self.name) > 0:  #can not have the first character be a blank
                    if key == K_SPACE:
                        self.name.append(" ")

            if len(self.name) > 0:
                #can only delete letters if there are some to delete
                if key == K_BACKSPACE:
                    self.name.pop(-1)
                if key == K_RETURN and not self.exists:
                    self.menu.name = string.join(self.name, '')
                    self.step = -1
        elif self.step == 1:
            self.statDistMenu.keyPressed(key)
                    

    def select(self, index):
        if self.step == -1:
            if index == 0:
                self.step = 0
            if index == 3:
                self.step = 1
            if index == 4:
                self.create()
       
    def renderNaming(self, visibility):
        w, h = self.engine.w, self.engine.h
        self.nameWindow.setPosition(w*.75, h*.90)
        self.nameWindow.draw()

        if visibility >= 1.0:
            name = string.join(self.name, '')
            self.engine.drawText(self.font, name, (w*.5 + 10, h*.9), alignment="left")

            if name:
                if self.exists:
                    frame = 2
                else:
                    frame = 1
                self.nameButton.setPosition(w*.9, h*.9)
                self.nameButton.setScale(75,75, inPixels = True)
                self.nameButton.setFrame(x = frame)
                self.nameButton.draw()
            
    def create(self):
        name = string.join(self.name, '')
        character = Character(None, None)
        character.create(self.engine.family.name, name, self.job.name, 
                         self.distAreas, self.distPoints, sprite = self.sprites[self.selectedSprite])
        self.engine.family.refresh()
        self.engine.viewport.changeScene("Maplist")
        
    def render(self, visibility):
        w, h = self.engine.w, self.engine.h

        self.background.draw()
        
        if not self.step == 1:
            if len(self.sprites) > 0:
                self.engine.drawImage(self.sprite, position = (w*.75, h*.5))
            self.menu.render()
            
        if self.step == 0:
            self.renderNaming(visibility)
        elif self.step == 1:
            self.statDistMenu.render()
        else:
            self.menu.refresh()

        
