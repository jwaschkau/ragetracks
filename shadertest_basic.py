# -*- coding: utf-8 -*-
#Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
#Date: 7/25/2005

import direct.directbase.DirectStart
from panda3d.core import *

from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import sys,os


class GlowDemo(DirectObject):
    def __init__(self):
        base.setBackgroundColor(0,0,0)
        
        #render.setShaderAuto()
        
        self.filters = CommonFilters(base.win, base.cam)
        
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size="big")
        
        
        self.glowSize=1
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MGlow)
        
        self.tron=Actor()
        #self.tron.setShaderAuto()
        self.tron.loadModel("data/models/vehicles/vehicle01")
        self.tron.setTexture(ts, "data/textures/vehicle01_body_glow.png")
        #self.tron.
        
        self.tron.reparentTo(render)
        
        self.tron2=Actor()
        #self.tron.setShaderAuto()
        self.tron2.loadModel("data/models/vehicles/vehicle01")
        
        self.tron2.reparentTo(render)
        self.tron2.setX(5)


t=GlowDemo()

run()

