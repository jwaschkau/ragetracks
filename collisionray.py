# -*- coding: utf-8 -*-
###################################################################
## this module represents a collision ray
###################################################################

from panda3d.core import * #Load all PandaModules
from panda3d.ode import *
from wiregeom import WireGeom

class CollisionRay(object):
    '''
    '''
    def __init__(self, position, direction, ode_space, length = 1.0, parent = None, debug = False, collide_bits = 0, category_bits = 0 ):
        '''
        '''
        self.ode_space = ode_space
        self.parent = parent #the collision_model
        self.position = position #Vec3()
        self.direction = direction #Vec3()
        self.ray = OdeRayGeom(self.ode_space, length)
        self.debug = debug

        self.ray.setCollideBits(collide_bits)
        self.ray.setCategoryBits(category_bits)

        if self.debug:
            pass

    # ---------------------------------------------------------

    def doStep(self):
        '''
        Calculates the new position of the ray, relative to the collision-model,
        needs to be executed everytime ode.quickStep gets executed
        '''

        relative_vec = self.parent.getQuaternion().xform(self.direction)
        self.ray.set(self.parent.getPosition(),
                    relative_vec)

        if self.debug:
            pass


    # ---------------------------------------------------------

    def getRay(self):
        return self.ray

    def __del__(self):
        self.ray.disable()
        self.ray.destroy()