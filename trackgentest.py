
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
        
        self.track = trackgen3d.Track3d(1000, 800, 600, 200, 5)
        
        nodePath = self.render.attachNewNode(self.track.createRoadMesh())
        tex = loader.loadTexture('data/textures/street.png')
        nodePath.setTexture(tex)
        #nodePath.setTwoSided(True)
        
        #LICHT
        self.plight = PointLight('kkkplight')
        self.plight.setColor(VBase4(21, 0, 0, 1))
        self.plnp = NodePath(self.plight)
        self.plnp.reparentTo(render)
        self.plnp.setPos(0,0,2000)
        self.plnp.node().setAttenuation(Point3(0,0,1))
        self.plnp.setScale(.5,.5,.5)
        
        nodePath.setShaderAuto(True)
        

        #self.plnp.setHpr(0,-90,0)
        #print plight.getAttenuation()
        #plnp.setPos(-10, -800, 20)
        render.setLight(self.plnp)
        
        self.accept("w", self.setA, [100])
        self.accept("s", self.setA, [-10])
        self.accept("e", self.setB, [10])
        self.accept("d", self.setB, [-10])
        self.accept("r", self.setC, [100])
        self.accept("f", self.setC, [-100])
        
        self.accept("z", self.setRotation, [0, 10])
        self.accept("h", self.setRotation, [0, -10])
        self.accept("u", self.setRotation, [1, 10])
        self.accept("j", self.setRotation, [1, -10])
        self.accept("i", self.setRotation, [2, 10])
        self.accept("k", self.setRotation, [2, -10])
        
        self.accept("n", self.setExponent, [-50])
        self.accept("m", self.setExponent, [50])
        
        
        # load our model
        tron = loader.loadModel("data/models/vehicles/vehicle02")
        self.tron = tron
        #self.tron.loadAnims({"running":"models/tron_anim"})
        tron.reparentTo(render)
        tron.setPos(0,0,15)
        tron.setHpr(0,-90,0)
        nodePath2 = self.render.attachNewNode(self.track.createBorderLeftMesh())
        tex2 = loader.loadTexture('data/textures/border.png')
        nodePath2.setTexture(tex2)
        
        nodePath3 = self.render.attachNewNode(self.track.createBorderRightMesh())
        tex2 = loader.loadTexture('data/textures/border.png')
        nodePath3.setTexture(tex2)
        
    
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.1, 0.1, 0.1, 1))
        render.setLight(render.attachNewNode(ambilight))

    # -----------------------------------------------------------------
    
    def setA(self, val):
        '''
        '''
        tpos = self.tron.getPos()
        tpos[0] += val
        self.tron.setPos(tpos)
        pos = self.plnp.getPos()
        pos[0] += val
        print pos
        self.plnp.setPos(pos)
        
    def setB(self, val):
        '''
        '''
        tpos = self.tron.getPos()
        tpos[1] += val
        self.tron.setPos(tpos)
        pos = self.plnp.getPos()
        pos[1] += val
        print pos
        self.plnp.setPos(pos)
        
    def setC(self, val):
        '''
        '''
        tpos = self.tron.getPos()
        tpos[2] += val
        self.tron.setPos(tpos)
        pos = self.plnp.getPos()
        pos[2] += val
        print pos
        self.plnp.setPos(pos)
    
    def setRotation(self, var, val):
        '''
        '''
        hpr = self.plnp.getHpr()
        hpr[var] += val
        print "hpr", hpr
        self.plnp.setHpr(hpr)
    
    def setExponent(self, val):
        '''
        '''
        val = self.plight.getExponent()+val
        print val
        self.plight.setExponent(val)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()




