# _*_ coding: UTF-8 _*_
###################################################################
## this module stores the different vehicles and their data
###################################################################

class VehicleData(object):
    '''
    '''
    def __init__(self):
        self.vehicles = {}
        self.vehicles = {
                        "standard":{#name of the vehicle
                                "model_path":"data/models/vehicle01",#path to the model
                                "model_scale":(1,1,1),#scale of the model
                                "mass_box":((1000,1,1,1),)#allocation of the mass from the vehicle
                                
                                },
                                
                                }
        
    # ---------------------------------------------------------
        
    def getData(self, name):
        '''
        returns all data of the choosen vehicle
        '''
        return self.vehicles["standard"]
        
    # ---------------------------------------------------------
    
    def getVehicles(self):
        '''
        returns all available vehicles between the player can choose
        '''
        pass
        
    # ---------------------------------------------------------