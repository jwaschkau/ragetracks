# _*_ coding: UTF-8 _*_
###################################################################
## this module represents a collision ray
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from wiregeom import WireGeom

class CollisionRay(object):
    '''
    '''
    def __init__(self, position, direction, length = 1, parent = None ,debug = False):
        '''
        '''
        self.parent = parent #the collision_model
        self.position = position #Vec3()
        self.direction = direction #Vec3()
        self.ray = OdeRayGeom(self.ode_space, length)
        self.debug = debug
        
        if self.debug:
            self.ray = WireGeom().generate ('ray', length=length)
            self.ray.setPos (self.position[0] + self.parent.getPosition()[0], 
                            self.position[1]  + self.parent.getPosition()[1], 
                            self.position[2] + self.parent.getPosition()[2])
            self.ray.setHpr (self.parent.getQuaternion().getHpr()[0] , 
                            self.parent.getQuaternion().getHpr()[1]  , 
                            self.parent.getQuaternion().getHpr()[2] )
        
    # ---------------------------------------------------------
    
    def doStep(self):
        '''
        Calculates the new position of the ray, relative to the collision-model, 
        needs to be executed everytime ode.quickStep gets executed
        '''
        self.ray.set(self.parent.getPosition() + self.position, 
                    self.parent.getQuaternion().getRight() + self.direction)
        if self.debug:
            self.ray.setPos (self.position[0] + self.parent.getPosition()[0], 
                            self.position[1]  + self.parent.getPosition()[1], 
                            self.position[2] + self.parent.getPosition()[2])
            self.ray.setHpr (self.parent.getQuaternion().getHpr()[0] , 
                            self.parent.getQuaternion().getHpr()[1]  , 
                            self.parent.getQuaternion().getHpr()[2] )
        
    # ---------------------------------------------------------