# _*_ coding: UTF-8 _*_
###################################################################
## this module represents one vehicle a player can control
###################################################################

class Vehicle(object):
    '''
    '''
    def __init__(self, model = None, phys_model = None, phys_mass = None, coll_model = None):
        '''
        '''
        self.model = model
        self.physics_model = phys_model
        self.physics_mass = phys_mass
        self.collision_model = coll_model
    
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