# _*_ coding: UTF-8 _*_
###################################################################
## this module represents one vehicle a player can control
###################################################################

from pandac.PandaModules import * #Load all PandaModules

class Vehicle(object):
    '''
    '''
    def __init__(self, vehicledata, ode_world, ode_space, name = "standard"):
        '''
        '''
        self.ode_world = ode_world
        self.ode_space = ode_space
        self.model = None
        self.physics_model = None
        self.physics_mass = None
        self.collision_model = None
        self.vehicledata = vehicledata #holds information about the available vehicles
        
        self.setVehicle(name)
        
    # ---------------------------------------------------------
    
    def setVehicle(self, name):
        '''
        Choose what vehicle the player has chosen. This method initializes all data of this vehicle
        '''
        vehicle = self.vehicledata.getData(name)
        self.model = loader.loadModel(vehicle["model_path"])
        self.model.reparentTo(render)
        
        #Initialize the physics-simulation for the vehicle
        self.physics_model = OdeBody(self.ode_world)
        self.physics_model.setPosition(self.model.getPos(render))
        self.physics_model.setQuaternion(self.model.getQuat(render))        
        
        #Initialize the mass of the vehicle
        self.physics_mass = OdeMass()
        for i in vehicle["mass_box"]:
            self.physics_mass.setBox(i[0], i[1], i[2], i[3])
            self.physics_model.setMass(self.physics_mass)
        
        #Initialize the collision-model of the vehicle
        self.collision_model = None
      
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

    def setPhysicsModel(self, phys_mass):
        '''
        '''
        self.physics_mass = phys_mass
        
    # ---------------------------------------------------------
        
    def getPhysicsModel(self):
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