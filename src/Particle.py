from ImgObj import ImgObj
import random
from math import *

class Particle(object):
    def __init__(self, image, start = (.5, .5), pathX = lambda t: t, pathY = lambda t: t, velocity = 1.0, spin = 0, scale = lambda s: .5, life = 300.0):
        self.image = image              #image used for the particle
        self.startPosition = start      #position where the particle starts
        self.path = [pathX, pathY]      #path the particle will travel along
        self.velocity = velocity        #how fast it will travel along the path
        self.spin = spin                #degrees it will spin each frame
        self.scale = scale              #percentage size change each frame
        
        self.life = life                #how long it will be visible (milliseconds)
        self.counter = 0.0              #current time of the animation
        self.t = 0                      #current position in the animation
        self.tick = 1
        #sets the particle to its starting position before it can be drawn
        self.image.setPosition(start[0], start[1])
        
    #resets the position of the particle to the beginning of its path
    # and restarts the counter
    def reset(self, start = None):
        self.counter = 0.0
        self.t = 0
        if not start:
            print "not new start"
            start = self.startPosition
        self.startPosition = start
        self.image.setPosition(start[0], start[1])
       
    #draws the particle
    #  returns false when its life is up, true if it was able to draw
    def draw(self):
        self.counter += self.tick
        if self.counter > self.life:
            return False
        
        self.t += random.randint(0, int(self.velocity*100))/100.0
        self.image.setPosition(self.image.position[0] + self.path[0](self.t), self.image.position[1] + self.path[1](self.t))
        self.image.rotate(self.spin)
        scale = self.scale(self.t)
        self.image.setScale(scale, scale)
        self.image.setColor((1.0,1.0,1.0, 1.0-self.counter/self.life))
        self.image.draw()
        
        return True
        
#a collection of particles
class ParticleSystem(object):
    def __init__(self, particles, clock, start = None):
    
        self.startParticles = particles
        self.clock = clock
        #sets all particles to this position on start
        if start:
            for p in self.startParticles:
                p.reset(start)
        
        self.particles = self.startParticles[:]
        
    def reset(self, start = None):
        self.particles = self.startParticles[:]
        #sets all particles to this position on start
        if start:
            print "new start"
            for p in self.particles:
                p.reset(start)
        
    def draw(self):
        if len(self.particles) == 0:
            return False
        
        tick = self.clock.get_fps()
        for p in self.particles:
            p.tick = tick
            if not p.draw():
                self.particles.remove(p)
        return True
