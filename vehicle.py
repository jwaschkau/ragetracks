# _*_ coding: UTF-8 _*_
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
        
        self.setVehicle(name)
        
    # ---------------------------------------------------------
    
    def setVehicle(self, name):
        '''
        Choose what vehicle the player has chosen. This method initializes all data of this vehicle
        '''
        self.model = loader.loadModel("data/models/vehicle01")
        self.model.reparentTo(render)
        self.model.setPos(0,30,10)
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
        self.collision_model = OdeTriMeshGeom(self.ode_space, OdeTriMeshData(self.model, True))
        self.collision_model.setBody(self.physics_model)
        self.collision_model.setCollideBits(1)
        self.collision_model.setCategoryBits(0)

        #Add collision-rays for the floating effect
        self.front_left = CollisionRay(Vec3(-2,4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 10.0)
        self.front_right = CollisionRay(Vec3(2,4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 10.0)
        self.back_left= CollisionRay(Vec3(-2,-4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 10.0)
        self.back_right = CollisionRay(Vec3(2,-4,-1), Vec3(0,0,-1), self.ode_space, parent = self.collision_model, length = 10.0)
      
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
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        self.front_left.doStep()
        self.front_right.doStep()
        self.back_left.doStep()
        self.back_right.doStep()
        
    
    # ---------------------------------------------------------
    def getCollisionRays(self):
        return self.front_left.getRay(), self.front_right.getRay(), self.back_left.getRay() ,self.back_right.getRay()