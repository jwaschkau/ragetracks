# -*- coding: utf-8 -*-
#Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
#Date: 7/25/2005

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters


class GlowDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setBackgroundColor(0,0,0)
        #render.setShaderAuto()
        
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambilight))
        
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.8, intensity=4.0, size="big")
        
        
##        self.glowSize=4
        
##        ts = TextureStage('ts')
##        ts.setMode(TextureStage.MGlow)
        
        self.tron = loader.loadModel("data/models/vehicles/vehicle01")
        self.tron.reparentTo(render)
        

        self.tron2 = loader.loadModel("data/models/vehicles/vehicle02")
        self.tron2.reparentTo(render)
        self.tron2.setX(5)
        

        self.tron3 = loader.loadModel("data/models/vehicles/vehicle03")
        self.tron3.reparentTo(render)
        self.tron3.setX(-5)
        

t=GlowDemo()

run()

