# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect



class App(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        # set 'sky' colour
        base.setBackgroundColor(0.0,0.0,0.2,0)

        # just an environment model
        env = loader.loadModel('environment')
        env.reparentTo(render)
        env.setScale(0.02)
        env.setPos(0,18,-3)


        # parent node to attach the particle effect to
        self.parent = render.attachNewNode('parent')

        self.parent.setPos(-24,13,0)


        # enable particles
        base.enableParticles()

        blowout = ParticleEffect()
        # set the file to read particle effect settings from
        blowout.loadConfig(Filename('data/particles/blowout.ptf'))
        #Sets particles to birth relative to the parent
        blowout.start(self.parent)


        # we will need to change some teexturing settings
        blowtexture = loader.loadTexture("data/textures/blowout_orange.png")
        ts = TextureStage("ts")
        #ts.setMode(TextureStage.MReplace)
        blowout.setTexture(ts, blowtexture, 1)

        taskMgr.add(self.moveParent, "moveParent")


    def moveParent(self,task):
            '''
            '''
            self.parent.setX(self.parent.getX()+(8*globalClock.getDt()))
            return task.cont




App()
run()
