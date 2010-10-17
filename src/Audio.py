'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

import os
import sys

import pygame, pygame.image
from pygame.locals import *

#an object for sound effects
# do not use this to play music
# use BGMObj for that
class SoundObj:
    def __init__(self, path, loop = -1):
        filePath = os.path.join("..", "data", path)

        #sound object must be wav or it will not work!
        if os.path.splittext(filePath)[1].lower() != ".wav":
            return

        #new sound object
        self.audio = pygame.mixer.Sound(filePath)
        self.volume = 10                	    #volume of the object
        self.loop = loop               		    #how many times it will loop (default = forever)
        self.play()                             #by default it will start playing as soon as it is initialized

    #changes the volume of the audio
    def setVol(self, volume):
        self.volume = volume
        self.audio.set_volume(self.volume)

    #changes how many times the song will loop 
    def setLoop(self, loop):
        self.loop = loop

    #plays the audio
    def play(self):
        self.audio.play(self.loop)

    #stops the audio
    def stop(self):
        self.audio.stop()

#an object for background music
class BGMObj:
    def __init__(self, AudioFile, volume = 10, queue = False):
        #the music file
        audiopath = os.path.join("..", "data", AudioFile)

        self.volume = 10            #volume of the song (0-10 scale)
        self.loop = -1              #how many times it will loop (default = forever)

        #checks if the file exists and if it does then it should play it
        if os.path.exists(os.path.join(audiopath)):
            if queue == True:
                pygame.mixer.music.queue(audiopath)
            else:
                pygame.mixer.music.load(audiopath)
                pygame.mixer.music.play(self.loop)
        else:
            return None
  
    #changes how many times the song will loop
    def setLoop(loop = -1):
        self.loop = loop

    #plays the music
    def play(self):
        pygame.mixer.music.play(self.loop)

    #stops the music
    def stop(self):
        pygame.mixer.music.stop()

    #change the volume
    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume/10)
