import pygame, pygame.image
from pygame.locals import *

#object that has been cached
class CacheElement(object):
    def __init__(self,content):
        self.content = content      #content of the element
        self.accessed()             #gets the time of creation

    #calls the engine's clock to determine last time the element was used
    def accessed(self):
        self.lastUse = pygame.time.get_ticks()

#caching system from FoFiX's font system, implemented to hopefully improve performance
class Cache(object):
    def __init__(self,maxCount=256):
        self.elements = {}
        self.maxCount = maxCount        #maximum number of elements

    def get(self,key):
        e = self.elements[key]
        e.accessed()                    #updates the element's last use time
        return e.content

    def add(self,key,element):
        self.elements[key] = CacheElement(element)
        
        #if the number of elements exceeds the maximum amount,
        #the key(s) that has(have) the longest time since its last use
        #are removed
        if len(self.elements) > self.maxCount:
            keys = self.elements.keys()
            keys.sort(key=lambda e:-self.elements[e].lastUse)
            for k in keys[self.maxCount:]:
                del self.elements[k]
