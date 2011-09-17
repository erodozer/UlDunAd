from ImgObj import ImgObj
import random
from math import *

class Particle:
    def __init__(self, startX, startY, angle, lifeSpan = 50):
    
        self.startX = startX
        self.startY = startY
        self.life = lifeSpan
        self.vel = 1.0
        self.angle = angle/30.0
        
        self.reset()
        
    def reset(self, pos = None):
        if pos:
            self.startX = pos[0]
            self.startY = pos[1]

        self.x = self.startX
        self.y = self.startY
        self.time = 0
      
    def move(self):
        self.x = self.startX + (self.angle*self.vel*self.time)
        self.y = self.startY + (-.5*self.time**2+32*self.vel*self.time)
        self.time += 1;
    
#a collection of particles
class ParticleSystem(object):
    def __init__(self, image, particles, clock, start):
    
        self.image = image
        self.clock = clock
        self.p = particles
        self.particles = [Particle(start[0], start[1], random.randint(-90, 90), lifeSpan = random.randint(25, 50)) for i in range(self.p)]
        
    def reset(self, pos = None):
        for p in self.particles:
            p.reset(pos)
            
    def draw(self):
        for p in self.particles:
            if p.time > p.life:
                continue
                
            p.move()
            if p.time > p.life/10.0:
                alpha = (p.life-p.time)/10.0
            else:
                alpha = 1.0
            self.image.setPosition(p.x, p.y)
            self.image.setAngle(p.angle)
            self.image.setColor((1.0,1.0,1.0,alpha))
            self.image.draw()
            
