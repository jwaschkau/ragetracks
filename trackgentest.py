
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
        self.accept("tab",self.onTab)
        self.startGame()
        self.cam_on = True
        # -----------------------------------------------------------------

    # -----------------------------------------------------------------
    
    def onSpace(self, evt=None):
        '''
        '''
        if self.trackmesh2.getParent() == render:
            self.trackmesh.reparentTo(render)
            self.trackmesh2.detachNode()
        else:
            self.trackmesh.detachNode()
            self.trackmesh2.reparentTo(render)
##        base.toggleWireframe()
        

    # -----------------------------------------------------------------

    def startGame(self):
        '''
        Start the game
        '''
        #Create the Track
        
        self.track = trackgen3d.Track3d(1000, 800, 600, 200, 5)
        
        self.trackmesh = NodePath(self.track.createRoadMesh())
        tex = loader.loadTexture('data/textures/street.png')
        self.trackmesh.setTexture(tex)
        
        self.trackmesh2 = NodePath(self.track.createUninterpolatedRoadMesh())
        self.trackmesh2.setTexture(tex)
        #nodePath.setTwoSided(True)

        self.trackmesh.reparentTo(render)
        
        #LICHT
        self.plight = PointLight('kkkplight')
        self.plight.setColor(VBase4(21, 0, 0, 1))
        self.plnp = NodePath(self.plight)
        self.plnp.reparentTo(render)
        self.plnp.setPos(0,0,2000)
        self.plnp.node().setAttenuation(Point3(0,0,1))
        self.plnp.setScale(.5,.5,.5)
        
        

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
##        nodePath2 = self.render.attachNewNode(self.track.createBorderLeftMesh())
##        tex2 = loader.loadTexture('data/textures/border.png')
##        nodePath2.setTexture(tex2)
##        
##        nodePath3 = self.render.attachNewNode(self.track.createBorderRightMesh())
##        tex2 = loader.loadTexture('data/textures/border.png')
##        nodePath3.setTexture(tex2)
        ring = loader.loadModel("data/models/ring.egg")
        ring.setScale(24)
        ring.setZ(-25)
        ring.setY(100)
        ring.setTransparency(TransparencyAttrib.MAlpha) 
        ring.reparentTo(render)
        
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.8, 0.8, 0.8, 1))
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
    
    def onTab(self):
        '''
        '''
        if self.cam_on:
            base.disableMouse()
            base.camera.setPos(-293.807, 91.2993, 3984.4)
            base.camera.setHpr(-76.0078, -85.4581, -71.7315)

            #base.camera.setPos(39.3053, -376.205, -3939.89)
            #base.camera.setHpr(5.33686, -82.7432, 8.26239)

            #print base.camera.getPos(), base.camera.getHpr()
            self.cam_on = False
        else:
            base.enableMouse()
            self.cam_on = True

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()




