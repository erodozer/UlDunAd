import Config
import pygame
from pygame.locals import *

#names of different buttons
# this way the names can be changed instead
# of always having the same keys.  By doing
# this it allows for joypad input and key
# input.

buttonA      = None
buttonB      = None
buttonC      = None
buttonD      = None
buttonUP     = None
buttonDOWN   = None
buttonLEFT   = None
buttonRIGHT  = None
buttonOK     = None
buttonCANCEL = None

class Input:
    def setup(self):
        global buttonA, buttonB, buttonC, buttonD
        global buttonUP, buttonDOWN, buttonLEFT, buttonRIGHT
        global buttonOK, buttonCANCEL

        config = Config.Configuration(os.path.join("uldunad.ini")).keys

        buttonA      = eval(config.__getattr__("buttonA"))
        buttonB      = eval(config.__getattr__("buttonB"))
        buttonC      = eval(config.__getattr__("buttonC"))
        buttonD      = eval(config.__getattr__("buttonD"))
        buttonUP     = eval(config.__getattr__("buttonUP"))
        buttonDOWN   = eval(config.__getattr__("buttonDOWN"))
        buttonLEFT   = eval(config.__getattr__("buttonLEFT"))
        buttonRIGHT  = eval(config.__getattr__("buttonRIGHT"))
        buttonOK     = eval(config.__getattr__("buttonOK"))
        buttonCANCEL = eval(config.__getattr__("buttonCANCEL"))

        self.keys = [buttonA, buttonB, buttonC, buttonD, 
                     buttonUP, buttonDOWN, buttonLEFT, buttonRIGHT,
                     buttonOK, buttonCANCEL]

    def getPressed(self):
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.key in self.keys:
                return self.keys[self.keys.index(event.key)]

