# -*- coding: utf-8 -*-
###################################################################
## this module contains the data for one player
###################################################################
import vehicle
from pandac.PandaModules import Vec3,Quat #Load all PandaModules
from direct.directnotify.DirectNotify import DirectNotify
from direct.gui.OnscreenText import OnscreenText

class Player(object):
    '''
    '''
    def __init__(self, number, ode_world, ode_space, device = None, camera = None):
        '''
        '''
        self._notify = DirectNotify().newCategory("Player")
        self._notify.info("New Player-Object created: %s" %(self))
        self._ode_world = ode_world
        self._ode_space = ode_space
        self._number = number
        self._camera = camera
        self._vehicle = vehicle.Vehicle(self._ode_world, self._ode_space) #the properties of the vehicle
        self._device = device #The inputdevice
        self._osd_health = OnscreenText(text = "100", pos = ((self._number*0.2)-1,0.9))
    
    # ---------------------------------------------------------
    
    def activateGameCam(self):
        self._camera.followVehicle(self._vehicle.boost_direction, self._vehicle)
        self._camera.camera.reparentTo(render)
        self._vehicle.model.reparentTo(render)
        
    # ---------------------------------------------------------
    
    def setCamera(self, camera):
        '''
        '''
        self._camera = camera
        
    def getCamera(self):
        '''
        '''
        return self._camera
        
    camera = property(fget = getCamera, fset = setCamera)
        
    # ---------------------------------------------------------
    
    def updateOSD(self):
        '''
        update the osd-information
        '''
        self._osd_health.setText(str(round(self._vehicle.energy)))
        
    def recalculateOSD(self):
        '''
        recalculate positions of the osd
        '''
        pass
        
    # ---------------------------------------------------------      
    def setVehicle(self, vehicle):
        '''
        '''
        loading = self.camera.camera.getParent().find("LoadingNode")
        #loading.detachNode()
        if loading: loading.removeNode()
        else: self._notify.warning("Could not remove the loading node")
        vehicle.hide()
        vehicle.reparentTo(self.camera.camera.getParent())
        self._vehicle.setVehicle(vehicle)
        vehicle.show()
        
    def getVehicle(self):
        '''
        '''
        return self._vehicle
        
    vehicle = property(fget = getVehicle, fset = setVehicle)
        
    # ---------------------------------------------------------
    
    def setDevice(self, device):
        '''
        '''
        self._device = device
        
    def getDevice(self):
        '''
        '''
        return self._device
        
    device = property(fget = getDevice, fset = setDevice)
        
    # ---------------------------------------------------------
    
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        self._vehicle.doStep()
        
    
    # ---------------------------------------------------------
    
    def updatePlayer(self):
        '''
        Needs to get executed every Ode-Step
        '''
        self._vehicle.model.setPosQuat(render, self._vehicle.physics_model.getPosition(), Quat(self._vehicle.physics_model.getQuaternion())) #set new position
        self._camera.updateCam()
        
    
    # ---------------------------------------------------------
        
    def __del__(self):
        '''
        destroys all objects of the player-object
        '''
        #Del one Camera 
        self._camera.camera.removeNode()#node()
        self._notify.info("Player-Object deleted: %s" %(self))
        
    # ---------------------------------------------------------
    
    if __name__ == "__main__":
        import main