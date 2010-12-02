
# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
import trackgen3d

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        #loadPrcFileData("", "want-pstats 1\n pstats-host 127.0.0.1\n pstats-tasks 1\n task-timer-verbose 1")
        #loadPrcFileData("", "pstatshost 192.168.220.121")
        ShowBase.__init__(self)
        
        #PStatClient.connect() #activate to start performance measuring with pstats
        base.setFrameRateMeter(True) #Show the Framerate
        #base.toggleWireframe()
        self.accept("space",self.onSpace)
        self.startGame()
        # -----------------------------------------------------------------

    # -----------------------------------------------------------------
    
    def onSpace(self, evt=None):
        '''
        '''
        base.toggleWireframe()
        

    # -----------------------------------------------------------------

    def startGame(self):
        '''
        Start the game
        '''
        #Create the Track
        
        self.track = trackgen3d.Track3d(100, 800, 600, 200, 5)
        nodePath = self.render.attachNewNode(self.track.createMesh())
        tex = loader.loadTexture('data/textures/street.png')
        nodePath.setTexture(tex)
        #nodePath.setTwoSided(True)
        
    
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()




