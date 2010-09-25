# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *


class Text3D(object):
    '''
    Creates a 3D-Object out of a string
    '''
    def __init__(self, string, pos = Vec3(0,0,0), hpr = Vec3(0,90,0), color = Vec4(255,255,255,255), spacing = 1):
        '''
        '''
        self._string = string
        self.position = pos
        self.hpr = hpr
        self.spacing = spacing
        self.spacing_count = 0
        self.font = loader.loadModel("data/models/3dfont/letters")
        self.node = render.attachNewNode("3DText")
        self.node.setTwoSided(True)
        self.node.reparentTo(render)
        self.node.setColor(color)
        self.node.setHpr(self.hpr)
        self.node.hide()

        for letter in self._string:
            letter3d = self.font.find("*/%s"%(letter))
            placeholder = self.node.attachNewNode("letter")
            placeholder.setPos(self.spacing_count,0,0)
            letter3d.instanceTo(placeholder)
            self.spacing_count += self.spacing
        
        
        
    # -----------------------------------------------------------------
    def setString(self, string):
        self.node.stash()
        self.spacing_count = 0
        self._string = string
        
        self.node = render.attachNewNode("3DText")
        self.node.setTwoSided(True)
        self.node.reparentTo(render)
        self.node.setColor(color)
        self.node.setHpr(self.hpr)
        self.node.hide()

        for letter in self._string:
            letter3d = self.font.find("*/%s"%(letter))
            placeholder = self.node.attachNewNode("letter")
            placeholder.setPos(self.spacing_count,0,0)
            letter3d.instanceTo(placeholder)
            self.spacing_count += self.spacing
        
    def getString(self):
        return self._string
        
    string = property(fget = getString, fset = setString)
    
    # ----------------------------------------------------------------- 
    
    def showText(self):
        self.node.show()
    
    # -----------------------------------------------------------------    
    def hideText(self):
        self.node.hide()
    
    # ----------------------------------------------------------------- 
    def __del__(self):
        self.node.stash()
    
if __name__ == "__main__":
    import main