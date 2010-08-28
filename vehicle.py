# _*_ coding: UTF-8 _*_
###################################################################
## this module represents one vehicle a player can control
###################################################################

class Vehicle(object):
    '''
    '''
    def __init__(self, main, vehicledata, name = "standard"):
        '''
        '''
        self.main = main
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
        self.model = self.main.loader.loadModel(vehicle["model_path"])
        self.physics_model = None
        self.physics_mass = None
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