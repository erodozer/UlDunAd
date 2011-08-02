'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

#system design based on Ian Mallett's glLib for pygame

#an opengl camera object
#it starts out with a view with perspective, 
#but you can make it orthographic with one call
class Camera:
    def __init__(self,pos,center,upvec=[0,1,0]):
        #camera's values
        self.pos = pos                  #current position
        self.center = center            #current center
        self.upvec = upvec              #current up vector
        
        #values to which the camera wants to obtain
        self.targetpos = pos            #new position
        self.targetcenter = center      #new center
        self.targetupvec = upvec        #new up vector
        
        
        self.adjustRate = 0.1           #speed at which the camera will transition into 
                                        # it's target values
        
    #sets the camera's target position
    def setTargetPos(self, tP):
        self.target = tP
        
    #sets the camera's target center
    def setTargetCenter(self,tC):
        self.targetcenter = tC
        
    #sets the camera's target up vector
    def set_target_up_vector(self,new_target_up_vector):
        self.targetupvec = new_target_up_vector
       
    #adjusts the change rate of the camera
    def setAdjustRate(self,value):
        self.adjust = value
       
    #updates the camera's values
    def update(self):
        #gets differences
        diff = lambda i, n: [i[x] - n[x] for x in range(3)]  
        
        pos_diff = diff(self.pos, self.targetpos)
        cen_diff = diff(self.center, self.targetcenter)
        upv_diff = diff(self.upvec, self.targetupvec)
              
        #gets the adjusted values
        adjust = lambda i, diff: [i[x]-(diff[x]*self.adjustRate) for x in range(3)]
        
        self.pos = adjust(self.pos, pos_diff)
        self.center = adjust(self.center, cen_diff)
        self.upvec = adjust(self.upvec, upv_diff)
       
        self.setCamera()
        
    #sets up the camera to show what it's looking at
    def setCamera(self):
        gluLookAt(self.pos[0],self.pos[1],self.pos[2],
                  self.center[0],self.center[1],self.center[2],
                  self.upvec[0],self.upvec[1],self.upvec[2])


        
