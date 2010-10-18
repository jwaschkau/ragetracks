# -*- coding: utf-8 -*-
###################################################################
## this module contains the camera of one player
###################################################################
from pandac.PandaModules import Vec3, NodePath #Load all PandaModules
from direct.directnotify.DirectNotify import DirectNotify

class PlayerCam(object):
    '''
    '''
    def __init__(self, camera):
        '''
        '''
        self._notify = DirectNotify().newCategory("PlayerCam")
        self._notify.info("New PlayerCam-Object created: %s" %(self))
        self._position = Vec3(0,-20,5)
        self._camera = camera
        self._vehicle_direction = Vec3(0,0,0) #the direction the object is moving
        self._nodepath = None
        self._distance = 0.7
        self._cam_node = NodePath()
        
    
    # ---------------------------------------------------------
    def followVehicle(self, direction, nodepath = None):
        '''
        Let the camera follow the node path.
        '''
        self._nodepath = nodepath
        self._vehicle_direction = direction
        
    # ---------------------------------------------------------
    def updateCam(self):
        '''
        Needs to get executed every frame that gets displayed on the screen
        '''
        if self._nodepath != None:
            x,y,z = self._nodepath.getX(),self._nodepath.getY(),self._nodepath.getZ()
            self._camera.setPos((self._nodepath.getQuat().xform(Vec3(0,-10,4))+self._nodepath.getPos()-(self._vehicle_direction*0.2)))
            self._camera.lookAt(x,y,z)
            self._camera.setR(self._nodepath.getR())
        else:
            pass
        
    # ---------------------------------------------------------
    
    def getCamera(self):
        return self._camera


    def setCamera(self, value):
        self._camera = value

    camera = property(fget = getCamera, fset = setCamera)
        
    
    
if __name__ == "__main__":
    import main