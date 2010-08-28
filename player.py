# _*_ coding: UTF-8 _*_
###################################################################
## this module contains the data for one player
###################################################################
import vehicle
import vehicledata

class Player(object):
    '''
    '''
    def __init__(self, main, number, device = None, camera = None, vehicledata = vehicledata.VehicleData()):
        '''
        '''
        self.main = main
        self.number = number
        self.camera = camera
        self.vehicle = vehicle.Vehicle(self.main, vehicledata) #the properties of the vehicle
        self.device = device #The inputdevice
        
        #Initialize the camera
        self.camera.reparentTo(self.vehicle.getModel())
        self.camera.setPos(0,-30,10)
        self.camera.lookAt(player.vehicle.getModel()) 
    
    # ---------------------------------------------------------
    
    def setCamera(self, camera):
        '''
        '''
        self.camera = camera
        
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