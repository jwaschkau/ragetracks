# -*- coding: utf-8 -*-
#Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
#Date: 7/25/2005

import direct.directbase.DirectStart
from panda3d.core import Filename,Buffer,Shader
from panda3d.core import PandaNode,NodePath
from panda3d.core import ColorBlendAttrib
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import TextNode,Point3,Vec4
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import sys,os


#This function is responsible for setting up the two blur filters.
#It just makes a temp Buffer, puts a screen aligned card, and then sets
#the appropiate shader to do all the work. Gaussian blurs are decomposable
#into a two-pass algorithm which is faster than the equivalent one-pass
#algorithm, so we do it in two passes. The full explanation (for math buffs)
#can be found in the article above

def makeFilterBuffer(srcbuffer, name, sort, prog):
    blurBuffer=base.win.makeTextureBuffer(name, 512, 512)
    blurBuffer.setSort(sort)
    blurBuffer.setClearColor(Vec4(1,0,0,1))
    blurCamera=base.makeCamera2d(blurBuffer)
    blurScene=NodePath("new Scene")
    blurCamera.node().setScene(blurScene)
    shader = loader.loadShader(prog)
    card = srcbuffer.getTextureCard()
    card.reparentTo(blurScene)
    card.setShader(shader)
    return blurBuffer

class GlowDemo(DirectObject):
    def __init__(self):
        #base.disableMouse()
        base.setBackgroundColor(0,0,0)
        camera.setPos(0,-50,0)

        # Check video card capabilities.

        if (base.win.getGsg().getSupportsBasicShaders() == 0):
            raise StandardError("Glow Filter: Video driver reports that shaders are not supported.")
            #return

        #create the shader that will determime what parts of the scene will glow
        glowShader=loader.loadShader("data/shaders/glowShader.sha")

        # load our model
        self.tron=Actor()
        self.tron.loadModel("data/models/vehicles/vehicle02")
        #self.tron.loadAnims({"running":"models/tron_anim"})
        self.tron.reparentTo(render)
        
        
        # load our model
        self.tron2=Actor()
        self.tron2.loadModel("data/models/vehicles/vehicle01")
        #self.tron.loadAnims({"running":"models/tron_anim"})
        self.tron2.reparentTo(render)
        self.tron2.setX(5)

##        #put some lighting on the tron model
##        dlight = DirectionalLight('dlight')
##        alight = AmbientLight('alight')
##        dlnp = render.attachNewNode(dlight)
##        alnp = render.attachNewNode(alight)
##        dlight.setColor(Vec4(1.0, 1.0, 1.0, 1))
##        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
##        dlnp.setHpr(0, -60, 0)
##        render.setLight(dlnp)
##        render.setLight(alnp)

        # create the glow buffer. This buffer renders like a normal scene,
        # except that only the glowing materials should show up nonblack.
        glowBuffer=base.win.makeTextureBuffer("Glow scene", 512, 512)
        glowBuffer.setSort(-3)
        glowBuffer.setClearColor(Vec4(0,0,0,1))

        # We have to attach a camera to the glow buffer. The glow camera
        # must have the same frustum as the main camera. As long as the aspect
        # ratios match, the rest will take care of itself.
        glowCamera=base.makeCamera(glowBuffer, lens=base.cam.node().getLens())

        # Tell the glow camera to use the glow shader
        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setShader(glowShader)
        glowCamera.node().setInitialState(tempnode.getState())

        # set up the pipeline: from glow scene to blur x to blur y to main window.
        blurXBuffer=makeFilterBuffer(glowBuffer,  "Blur X", -2, "data/shaders/XBlurShader.sha")
        blurYBuffer=makeFilterBuffer(blurXBuffer, "Blur Y", -1, "data/shaders/YBlurShader.sha")
        self.finalcard = blurYBuffer.getTextureCard()
        self.finalcard.reparentTo(render2d)
        self.finalcard.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))

        self.glowOn=True;

t=GlowDemo()

run()

