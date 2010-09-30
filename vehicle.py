# -*- coding: utf-8 -*-
###################################################################
## this module represents one vehicle a player can control
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from wiregeom import WireGeom
from collisionray import CollisionRay

class Vehicle(object):
    '''
    '''
    def __init__(self, ode_world, ode_space, name = "standard"):
        '''
        '''

        self._ode_world = ode_world
        self._ode_space = ode_space
        self._model = None
        self._physics_model = None
        self._physics_mass = None
        self._collision_model = None
        self._speed = 0.0 #the actual speed of the vehicle (forward direction)
        self._direction = Vec3(0,0,0) #the direction the car is heading
        self._boost_strength = 0.0 #the boost propertys of the vehicle
        self._control_strength = 0.0 #impact on the steering behaviour
        self._grip_strength = 0.0 #impact on the steering behaviour
        self._hit_ground = False
        
        self.setVehicle(name) #set the initial vehicle
        
    # ---------------------------------------------------------
    
    def setVehicle(self, name):
        '''
        Choose what vehicle the player has chosen. This method initializes all data of this vehicle
        '''
        self._boost_strength = 100.0
        self._control_strength = 0.1
        self._grip_strength = 2
        
        self._model = loader.loadModel("data/models/vehicle01")
        self._model.reparentTo(render)
        self._model.setPos(0,0,10)
        self._model.setHpr(0,0,0)
        
        #Initialize the physics-simulation for the vehicle
        self._physics_model = OdeBody(self._ode_world)
        self._physics_model.setPosition(self._model.getPos(render))
        self._physics_model.setQuaternion(self._model.getQuat(render))        
        
        #Initialize the mass of the vehicle
        physics_mass = OdeMass()
        physics_mass.setBox(400,1,1,1)
        self._physics_model.setMass(physics_mass)
        
        #Initialize the collision-model of the vehicle
        ##for use with blender models
        ##self.collision_model = OdeTriMeshGeom(self.ode_space, OdeTriMeshData(self.model, True))
        self._collision_model = OdeBoxGeom(self._ode_space, 4,8,4)
        self._collision_model.setBody(self._physics_model)
        self._collision_model.setCollideBits(1)
        self._collision_model.setCategoryBits(0)

        #Add collision-rays for the floating effect
        self._front_left = CollisionRay(Vec3(-2,4,-1), Vec3(0,0,-1), self._ode_space, parent = self._collision_model, length = 5.0)
        self._front_right = CollisionRay(Vec3(2,4,-1), Vec3(0,0,-1), self._ode_space, parent = self._collision_model, length = 5.0)
        self._back_left= CollisionRay(Vec3(-2,-4,-1), Vec3(0,0,-1), self._ode_space, parent = self._collision_model, length = 5.0)
        self._back_right = CollisionRay(Vec3(2,-4,-1), Vec3(0,0,-1), self._ode_space, parent = self._collision_model, length = 5.0)
           
    # ---------------------------------------------------------
    
    def setPos(self, x, y, z):
        '''
        '''
        self._model.setPos(x,y,z)
        
    def getPos(self):
        '''
        '''
        return self._model.setPos(x,y,z)
        
    position = property(fget = getPos, fset = setPos)
        
    # ---------------------------------------------------------
    
    def setModel(self, model):
        '''
        '''
        self._model = model
        
    def getModel(self):
        '''
        '''
        return self._model
        
    model = property(fget = getModel, fset = setModel)
        
    # ---------------------------------------------------------
    
    def setCollisionModel(self, model):
        '''
        '''
        self._collision_model = model
        
    def getCollisionModel(self):
        '''
        '''
        return self._collision_model
        
    collision_model = property(fget = getCollisionModel, fset = setCollisionModel)
        
    # ---------------------------------------------------------
    
    def setPhysicsModel(self, model):
        '''
        '''
        self._physics_model = model
        
    def getPhysicsModel(self):
        '''
        '''
        return self._physics_model
        
    physics_model = property(fget = getPhysicsModel, fset = setPhysicsModel)
        
    # ---------------------------------------------------------
    
    def setBoost(self):
        '''
        Boosts the vehicle by indicated strength
        '''
        if self._hit_ground:
            direction = self._collision_model.getQuaternion().xform(Vec3(0,1,0))
            self._physics_model.addForce(direction*self._boost_strength)
    
    # ---------------------------------------------------------
        
    def setDirection(self, dir):
        '''
        Boosts the vehicle by indicated strength
        '''
        rel_direction = self._collision_model.getQuaternion().xform(Vec3(dir[1],0,dir[0]))
        rel_position = self._collision_model.getQuaternion().xform(Vec3(5,0,0))
        #force = Vec3(rel_direction[0]*self.direction[0]*self._control_strength*self.speed,rel_direction[1]*self.direction[1]*self._control_strength*self.speed,rel_direction[2]*self.direction[2]*self._control_strength*self.speed)
        self._physics_model.addTorque(-rel_direction+self._direction*self._control_strength)
    
    def getDirection(self):
        return self._direction
        
    direction = property(fget = getDirection, fset = setDirection)        
        
    # ---------------------------------------------------------
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        #refresh variables
        linear_velocity = self._physics_model.getLinearVel()
        direction = self._collision_model.getQuaternion().xform(Vec3(0,1,0)) 
        
        #This needs to be done, so we dont create a new object but only change the existing one. else the camera wont update
        self.direction[0], self.direction[1],self.direction[2] = direction[0],direction[1],direction[2]
        
        xy_direction = self.collision_model.getQuaternion().xform(Vec3(1,1,0)) 
        self._speed = Vec3(linear_velocity[0]*xy_direction[0],linear_velocity[1]*xy_direction[1],linear_velocity[2]*xy_direction[2]).length()
        
        #calculate delayed velocity changes
        linear_velocity.normalize()
        self._direction.normalize()
        self._physics_model.addForce(self._direction*(self._speed*self._grip_strength))#+linear_velocity)
        self._physics_model.addForce(-linear_velocity*(self._speed*self._grip_strength))#+linear_velocity)
        
        #refresh the positions of the collisionrays
        self._front_left.doStep()
        self._front_right.doStep()
        self._back_left.doStep()
        self._back_right.doStep()
        
    
    # ---------------------------------------------------------
    
    def getCollisionRays(self):
        return (self._front_left.getRay(), self._front_right.getRay(), self._back_left.getRay() ,self._back_right.getRay())#
    
    collision_rays = property(fget = getCollisionRays)    
    
    # ----------------------------------------------------------------- 
        
    def getHitGround(self):
        return self._hit_ground
        
    def setHitGround(self, value):
        if type(value) != bool:
            raise TypeError("Type should be %s not %s"% (bool,type(value)))
        self._hit_ground = value
    
    hit_ground= property(fget = getHitGround, fset = setHitGround)
    
    # ----------------------------------------------------------------- 
    
    def __del__(self):
        pass
    
if __name__ == "__main__":
    import main