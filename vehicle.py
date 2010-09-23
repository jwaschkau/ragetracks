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

        self.ode_world = ode_world
        self.ode_space = ode_space
        self.model = None
        self.physics_model = None
        self.physics_mass = None
        self.collision_model = None
        self.speed = 0.0 #the actual speed of the vehicle (forward direction)
        self.direction = Vec3(0,0,0) #the direction the car is heading
        self.boost_strength = 0.0 #the boost propertys of the vehicle
        self.control_strength = 0.0 #impact on the steering behaviour
        self.grip_strength = 0.0 #impact on the steering behaviour
        
        self.setVehicle(name) #set the initial vehicle
        
    # ---------------------------------------------------------
    
    def setVehicle(self, name):
        '''
        Choose what vehicle the player has chosen. This method initializes all data of this vehicle
        '''
        self.boost_strength = 100.0
        self.control_strength = 0.1
        self.grip_strength = 2
        
        self.model = loader.loadModel("data/models/vehicle01")
        self.model.reparentTo(render)
        self.model.setPos(0,30,100)
        self.model.setHpr(0,0,0)
        
        #Initialize the physics-simulation for the vehicle
        self.physics_model = OdeBody(self.ode_world)
        self.physics_model.setPosition(self.model.getPos(render))
        self.physics_model.setQuaternion(self.model.getQuat(render))        
        
        #Initialize the mass of the vehicle
        self.physics_mass = OdeMass()
        self.physics_mass.setBox(4,1,1,1)
        self.physics_model.setMass(self.physics_mass)
        
        #Initialize the collision-model of the vehicle
        ##for use with blender models
        ##self.collision_model = OdeTriMeshGeom(self.ode_space, OdeTriMeshData(self.model, True))
        self.collision_model = OdeBoxGeom(self.ode_space, 4,8,4)
        self.collision_model.setBody(self.physics_model)
        self.collision_model.setCollideBits(1)
        self.collision_model.setCategoryBits(0)

        #Add collision-rays for the floating effect
        self.front_left = CollisionRay(Vec3(-2,4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 14.0)
        self.front_right = CollisionRay(Vec3(2,4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 14.0)
        self.back_left= CollisionRay(Vec3(-2,-4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 14.0)
        self.back_right = CollisionRay(Vec3(2,-4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 14.0)
      
    # ---------------------------------------------------------
    
    def getVehicle(self):
        '''
        Gives back a dictionary with information about the chosen vehicle
        '''
        pass 
   
    # ---------------------------------------------------------
    
    def setModel(self, model):
        '''
        '''
        self.model = model
        
    # ---------------------------------------------------------
        
    def getModel(self):
        '''
        '''
        return self.model
        
    # ---------------------------------------------------------
    
    def setPhysicsModel(self, phys_model):
        '''
        '''
        self.physics_model = phys_model
        
    # ---------------------------------------------------------
        
    def getPhysicsModel(self):
        '''
        '''
        return self.physics_model
        
    # ---------------------------------------------------------

    def setPhysicsMass(self, phys_mass):
        '''
        '''
        self.physics_mass = phys_mass
        
    # ---------------------------------------------------------
        
    def getPhysicsMass(self):
        '''
        '''
        return self.physics_mass
        
    # ---------------------------------------------------------
    
    def setCollisionModel(self, coll_model):
        '''
        '''
        self.collision_model = coll_model
        
    # ---------------------------------------------------------
        
    def getCollisionModel(self):
        '''
        '''
        return self.collision_model
        
    # ---------------------------------------------------------
    
    def setPos(self, x, y, z):
        '''
        '''
        model.setPos(x,y,z)
        
    # ---------------------------------------------------------
    def setScale(self, x, y, z):
        '''
        '''
        model.setScale(x,y,z)
        
    # ---------------------------------------------------------
    
    def setBoost(self):
        '''
        Boosts the vehicle by indicated strength
        '''
        direction = self.collision_model.getQuaternion().xform(Vec3(0,1,0))
        self.physics_model.addForce(direction*self.boost_strength)
        
    def setDirection(self, dir):
        '''
        Boosts the vehicle by indicated strength
        '''
        rel_direction = self.collision_model.getQuaternion().xform(Vec3(dir[1],0,dir[0]))
        rel_position = self.collision_model.getQuaternion().xform(Vec3(5,0,0))
        #force = Vec3(rel_direction[0]*self.direction[0]*self.control_strength*self.speed,rel_direction[1]*self.direction[1]*self.control_strength*self.speed,rel_direction[2]*self.direction[2]*self.control_strength*self.speed)
        self.physics_model.addTorque(-rel_direction+self.direction*self.control_strength)
        
    # ---------------------------------------------------------
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        #refresh variables
        linear_velocity = self.physics_model.getLinearVel()
        direction = self.collision_model.getQuaternion().xform(Vec3(0,1,0)) 
        
        #This needs to be done, so we dont create a new object but only change the existing one. else the camera wont update
        self.direction[0], self.direction[1],self.direction[2] = direction[0],direction[1],direction[2]
        
        xy_direction = self.collision_model.getQuaternion().xform(Vec3(1,1,0)) 
        self.speed = Vec3(linear_velocity[0]*xy_direction[0],linear_velocity[1]*xy_direction[1],linear_velocity[2]*xy_direction[2]).length()
        
        #calculate delayed velocity changes
        linear_velocity.normalize()
        self.direction.normalize()
        self.physics_model.addForce(self.direction*(self.speed*self.grip_strength))#+linear_velocity)
        self.physics_model.addForce(-linear_velocity*(self.speed*self.grip_strength))#+linear_velocity)
        
        #refresh the positions of the collisionrays
        self.front_left.doStep()
        self.front_right.doStep()
        self.back_left.doStep()
        self.back_right.doStep()
        
    
    # ---------------------------------------------------------
    def getCollisionRays(self):
        return self.front_left.getRay(), self.front_right.getRay(), self.back_left.getRay() ,self.back_right.getRay()
    
if __name__ == "__main__":
    import main