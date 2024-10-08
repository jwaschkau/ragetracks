# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from panda3d.core import * #Load all PandaModules
import os.path
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self, *args):
        '''
        '''
        ShowBase.__init__(self)

        base.setBackgroundColor(0,0,0)

        self.mdl = self.loader.loadModel("data/models/vehicles/vehicle01.egg")
        self.mdl.reparentTo(render)

        #Add the Skybox
        self.skybox = self.loader.loadModel("data/models/skybox.egg")
        t = Texture()
        #t.load(PNMImage("../skybox/skybox_tronic.png"))
        t.load(PNMImage("../skybox/test.png"))
        self.skybox.setTexture(t)
        self.skybox.setBin("background", 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setDepthTest(0)
        self.skybox.setLightOff()
        self.skybox.setScale(10000)
        self.skybox.reparentTo(render)
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()