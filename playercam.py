# _*_ coding: UTF-8 _*_
###################################################################
## this module contains the camera of one player
###################################################################
from pandac.PandaModules import Vec3 #Load all PandaModules

class PlayerCam(object):
    '''
    '''
    def __init__(self, camera):
        '''
        '''
        self.position = Vec3(0,-20,5)
        self.camera = camera
        self.nodepath = None
        self.delay = 1
    
    # ---------------------------------------------------------
    def followVehicle(self, nodepath = None):
        '''
        Let the camera follow the node path
        '''
        self.nodepath = nodepath
        self.camera.reparentTo(self.nodepath)
    
    # ---------------------------------------------------------
    def updateTask(self):
        '''
        Needs to get executed every frame that gets displayed on the screen
        '''
        pass
    
    # ---------------------------------------------------------