# -*- coding: utf-8 -*-
###################################################################
## this module contains the data for one player
###################################################################
import vehicle
from pandac.PandaModules import Vec3,Quat #Load all PandaModules

class Player(object):
    '''
    '''
    def __init__(self, number, ode_world, ode_space, device = None, camera = None):
        '''
        '''
        self.ode_world = ode_world
        self.ode_space = ode_space
        self.number = number
        self.camera = camera
        self.vehicle = vehicle.Vehicle(self.ode_world, self.ode_space) #the properties of the vehicle
        self.device = device #The inputdevice
        
        self.camera.followVehicle(self.vehicle.direction, self.vehicle.getModel())
        #self.camera.setPos(0,-40,5)
        #self.camera.lookAt(self.vehicle.getModel())
        
        #Initialize the camera
        #self.camera.reparentTo(self.vehicle.getModel())
        #self.camera.setPos(0,-30,10)
        #self.camera.lookAt(self.vehicle.getModel()) 
    
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
    
    def destroy(self):
        '''
        destroys all objects of the player-object
        '''
        #Del one Camera 
        self.camera.node().removeNode()
        
    # ---------------------------------------------------------
    
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        self.vehicle.doStep()
        
    
    # ---------------------------------------------------------
    
    def updatePlayer(self):
        '''
        Needs to get executed every Ode-Step
        '''
        self.vehicle.getModel().setPosQuat(render, self.vehicle.getPhysicsModel().getPosition(), Quat(self.vehicle.getPhysicsModel().getQuaternion())) #set new position
        self.vehicle.getPhysicsModel().setGravityMode(1) #enable gravity
        self.camera.updateCam()
        
    
    # ---------------------------------------------------------
    
    if __name__ == "__main__":
        import main