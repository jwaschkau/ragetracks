# _*_ coding: UTF-8 _*_
###################################################################
## this module contains the data for one player
###################################################################

class Player(object):
    '''
    '''
    def __init__(self, number, vehicle = None, device = None, camera = None):
        '''
        '''
        self.number = number
        self.camera = camera
        self.vehicle = vehicle
        self.device = device #The inputdevice
    
    # ---------------------------------------------------------
    
    def setCamera(self, camera):
        '''
        '''
        self.camrea = camera
        
    # ---------------------------------------------------------
        
    def getCamera(self):
        '''
        '''
        return self.camera
        
    # ---------------------------------------------------------
    
    def setNumber(self):
        '''
        '''
        self.number = number
    
    # ---------------------------------------------------------
        
    def getNumber(self):
        '''
        '''
        return self.number
        
    # ---------------------------------------------------------
    
    def setVehicle(self):
        '''
        '''
        self.vehicle = vehicle
        
    # ---------------------------------------------------------
    
    def getVehicle(self):
        '''
        '''
        return self.vehicle
        
    # ---------------------------------------------------------
    def setDevice(self):
        '''
        '''
        self.device = device
        
    # ---------------------------------------------------------
    
    def getDevice(self):
        '''
        '''
        return self.device
        
    # ---------------------------------------------------------