# -*- coding: utf-8 -*-
###################################################################
## this module contains the camera of one player
###################################################################
from pandac.PandaModules import Vec3, NodePath #Load all PandaModules

class PlayerCam(object):
    '''
    '''
    def __init__(self, camera):
        '''
        '''
        self.position = Vec3(0,-20,5)
        self.camera = camera
        self.vehicle_direction = Vec3(0,0,0) #the direction the object is moving
        self.nodepath = None
        self.distance = 0.7
        self.cam_node = NodePath()
    
    # ---------------------------------------------------------
    def followVehicle(self, direction, nodepath = None):
        '''
        Let the camera follow the node path.
        '''
        self.nodepath = nodepath
        self.vehicle_direction = direction
        
    # ---------------------------------------------------------
    def updateCam(self):
        '''
        Needs to get executed every frame that gets displayed on the screen
        '''
        if self.nodepath != None:
            x,y,z = self.nodepath.getX(),self.nodepath.getY(),self.nodepath.getZ()
            self.camera.setPos((self.nodepath.getQuat().xform(Vec3(0,-10,4))+self.nodepath.getPos()-(self.vehicle_direction*0.2)))
            self.camera.lookAt(x,y,z)
            self.camera.setR(self.nodepath.getR())
        else:
            pass
    
    # ---------------------------------------------------------
    
if __name__ == "__main__":
    import main