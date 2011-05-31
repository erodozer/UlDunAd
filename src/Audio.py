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

enabled = True

#an object for sound effects
# do not use this to play music
# use BGMObj for that
class SoundObj:
    def __init__(self, path, loop = 0):
        
        filePath = os.path.join("..", "data", "audio", "sound", path)

        #sound object must be wav or it will not work!
        if os.path.splitext(filePath)[1].lower() != ".wav":
            return

        #new sound object
        self.audio = pygame.mixer.Sound(filePath)
        self.volume = 10                	    #volume of the object
        self.loop = loop               		    #how many times it will loop (default = once)
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
        if enabled:
            self.audio.play(self.loop)

    #stops the audio
    def stop(self):
        self.audio.stop()

#an object for background music
class BGMObj:
    def __init__(self, AudioFile, volume = 10, queue = False):
        #the music file
        audiopath = os.path.join("..", "data", "audio", "music", AudioFile)

        self.volume = 10            #volume of the song (0-10 scale)
        self.loop = -1              #how many times it will loop (default = forever)

        if not enabled:
            return
        
        #checks if the file exists and if it does then it should play it
        if os.path.exists(os.path.join(audiopath)):
            if queue == True:
                pygame.mixer.music.queue(audiopath)
            else:
                pygame.mixer.music.fadeout(100)
                pygame.mixer.music.load(audiopath)
                pygame.mixer.music.play(self.loop)
        else:
            return
  
    #changes how many times the song will loop
    def setLoop(loop = -1):
        self.loop = loop

    #plays the music
    def play(self):
        if enabled:
            pygame.mixer.music.play(self.loop)

    #stops the music
    def stop(self):
        pygame.mixer.music.stop()

    #fades the music out and stops it
    #   @time       time, in milliseconds, it takes to fade the music out
    def fadeToStop(time = 100):
        pygame.mixer.music.fadeout(time)
        pygame.mixer.music.stop()

    #change the volume
    #   @volume     volume of the music, value between 0 - 10
    def setVolume(self, volume):
        pygame.mixer.music.set_volume(int(volume)/10.0)

