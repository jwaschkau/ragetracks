# -*- coding: utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        base.setFrameRateMeter(True) #Show the Framerate
        self.skybox = self.loader.loadModel("data/models/skybox.egg")
        self.skybox.setBin("background", 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setDepthTest(0)
        self.skybox.setLightOff()
        self.skybox.setScale(2000)
        self.skybox.reparentTo(render)



# this code is only executed if the module is executed and not imported
if __name__ == "__main__":
    game = Game()
    game.run()
