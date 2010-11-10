# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
from direct.particles.ParticleEffect import ParticleEffect

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
        loadPrcFileData("", "default-directnotify-level debug\n notify-level-x11display fatal")
        
        #PStatClient.connect() #activate to start performance measuring with pstats
        base.setFrameRateMeter(True) #Show the Framerate
        #base.toggleWireframe()
        
        self.startGame()
        # -----------------------------------------------------------------



    # -----------------------------------------------------------------

    def startGame(self):
        '''
        Start the game
        '''
        
        base.enableParticles()
        #self.p = ParticleEffect()
        #self.loadParticleConfig('./data.parcticles/blowout_fire.ptf')
        #Start of the code from steam.ptf
        #self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig('./data/particles/blowout.ptf')        
        #Sets particles to birth relative to the teapot, but to render at toplevel
        self.p.start(render)
        self.p.setPos(0.000, 0.000, 0)
    
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




