# -*- coding: utf-8 -*-
###################################################################
## this module contains the camera of one player
###################################################################
from pandac.PandaModules import Vec3, NodePath #Load all PandaModules
from direct.directnotify.DirectNotify import DirectNotify
from pandac.PandaModules import * #Load all PandaModules
import random
import glob

class PlayerCam(object):
    '''
    '''
    def __init__(self, camera):
        '''
        '''
        self._notify = DirectNotify().newCategory("PlayerCam")
        self._notify.info("New PlayerCam-Object created: %s" %(self))
        self.position = Vec3(0,-20,5)
        self.camera = camera
        self.vehicle_direction = Vec3(0,0,0) #the direction the object is moving
        self.nodepath = None
        self.distance = 0.7
        self.cam_node = NodePath()
        self.menuNode = NodePath("MenuNode")
        
        #GlobPattern if we need a Panda Class
        self.vehicle = glob.glob("data/models/*.egg")
    
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
    def camModeMenu(self):
        '''
        Set Cam to menu mode
        '''
        self.camera.reparentTo(self.menuNode)
        
        ####TEMP
        #Font
        self.font = DynamicTextFont('data/fonts/font.ttf')
        self.font.setRenderMode(TextFont.RMSolid)
        
        headline = TextNode("RageTracks")
        headline.setFont(self.font)
        headline.setText(str(random.randint(0, 12)))
        NodePath("test").attachNewNode(headline)
        self.menuNode.attachNewNode(headline)
        
        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        plnp = self.menuNode.attachNewNode(plight)
        plnp.setPos(0, -10, 0)
        self.menuNode.setLight(plnp)
        
        #Load the platform
        m = loader.loadModel("data/models/platform.egg")
        m.reparentTo(self.menuNode)
    
    # ---------------------------------------------------------    
    def camModeGame(self):
        '''
        Set Cam to game mode
        '''
        self.camera.reparentTo(render)
        
    # ---------------------------------------------------------
    
if __name__ == "__main__":
    import main