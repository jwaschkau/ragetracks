# _*_ coding: UTF-8 _*_
###################################################################
## this module represents one vehicle a player can control
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from wiregeom import WireGeom

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
        self.model.setPos(0,25,0)
        
        #Initialize the physics-simulation for the vehicle
        self.physics_model = OdeBody(self.ode_world)
        self.physics_model.setPosition(self.model.getPos(render))
        self.physics_model.setQuaternion(self.model.getQuat(render))        
        
        #Initialize the mass of the vehicle
        self.physics_mass = OdeMass()
        self.physics_mass.setBox(1000,1,1,1)
        self.physics_model.setMass(self.physics_mass)
        
        #Initialize the collision-model of the vehicle
        self.collision_model = OdeTriMeshGeom(self.ode_space, OdeTriMeshData(self.model, True))
        self.collision_model.setBody(self.physics_model)
        self.collision_model.setCollideBits(BitMask32(0x00000001))
        self.collision_model.setCategoryBits(BitMask32(0x00000001))

##        experimental code for the floating effect and visualization of that        
##        #Add collision-rays for the floating effect
        self.front_left = OdeRayGeom(self.ode_space, 4)
        self.front_left.setCollideBits(BitMask32(0x00000000))
        self.front_left.setCategoryBits(BitMask32(0x00000000))
##        self.front_right = OdeRayGeom(self.ode_space, 4)
##        self.back_left= OdeRayGeom(self.ode_space, 4)
##        self.back_right = OdeRayGeom(self.ode_space, 4)
##        
##        #self.front_left.set(Vec3(position) + Vec3(relative position), Vec3(direction))
        self.front_left.set(self.collision_model.getPosition() + Vec3(1,1,0), Vec3(0,0,-1))
##        self.front_right.set(self.collision_model.getPosition() + Vec3(1,-1,0), Vec3(0,0,-1))
##        self.back_left.set(self.collision_model.getPosition() + Vec3(-1,1,0), Vec3(0,0,-1))
##        self.back_right.set(self.collision_model.getPosition() + Vec3(-1,-1,0), Vec3(0,0,-1))
##        
##        print self.collision_model.getQuaternion().getX()    
##        print self.collision_model.getQuaternion().getY()   
##        print self.collision_model.getQuaternion().getZ()       
##        print self.collision_model.getQuaternion().getUp()      
##        print self.collision_model.getQuaternion().getRight()        
##        print self.collision_model.getQuaternion().getHpr()
##        
        ray = WireGeom().generate ('ray', length=3.0)
        ray.setPos (1 , 1, 0)
        ray.setHpr (self.collision_model.getQuaternion().getHpr()[0] , self.collision_model.getQuaternion().getHpr()[1]  , self.collision_model.getQuaternion().getHpr()[2] )
        ray.reparentTo( self.model )
      
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