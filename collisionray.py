# -*- coding: utf-8 -*-
###################################################################
## this module represents a collision ray
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from wiregeom import WireGeom

class CollisionRay(object):
    '''
    '''
    def __init__(self, position, direction, ode_space, length = 1.0, parent = None ,debug = True, collide_bits = 2, category_bits = 0 ):
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
            self.drawray = WireGeom().generate ('ray', length=length)
            self.drawray.reparentTo(render)

            relative_pos = self.parent.getQuaternion().xform(self.position)
            relative_vec = self.parent.getQuaternion().xform(self.direction)
            self.drawray.setPos (self.parent.getPosition() + relative_pos)
            self.drawray.setHpr (0,180,0)

    # ---------------------------------------------------------

    def doStep(self):
        '''
        Calculates the new position of the ray, relative to the collision-model,
        needs to be executed everytime ode.quickStep gets executed
        '''

        relative_pos = self.parent.getQuaternion().xform(self.position)
        relative_vec = self.parent.getQuaternion().xform(self.direction)
        self.ray.set(self.parent.getPosition() + relative_pos,
                    relative_vec)

        if self.debug:
            self.drawray.setPos (self.parent.getPosition() + relative_pos)
            self.drawray.setHpr(Quat(1.0,relative_vec[0],relative_vec[1],relative_vec[2]).getHpr())
##            self.drawray.setHpr(Quat(Vec4(0,0,relative_vec[2],relative_vec[1])).getHpr())


    # ---------------------------------------------------------

    def getRay(self):
        return self.ray