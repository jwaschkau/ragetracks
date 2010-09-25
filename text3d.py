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
        self._position = pos
        self._hpr = hpr
        self._color = color
        self._spacing = spacing
        self._spacing_count = 0
        self._font = loader.loadModel("data/models/3dfont/letters")
        self._node = render.attachNewNode("3DText")
        self._node.setTwoSided(True)
        self._node.reparentTo(render)
        self._node.setColor(self._color)
        self._node.setHpr(self._hpr)
        self._node.hide()

        for letter in self._string:
            letter3d = self._font.find("*/%s"%(letter))
            placeholder = self._node.attachNewNode("letter")
            placeholder.setPos(self._spacing_count,0,0)
            letter3d.instanceTo(placeholder)
            self._spacing_count += self._spacing
        
        
        
    # -----------------------------------------------------------------
    def setString(self, string):
        self._node.stash()
        self._spacing_count = 0
        self._string = string
        
        self._node = render.attachNewNode("3DText")
        self._node.setTwoSided(True)
        self._node.reparentTo(render)
        self._node.setColor(self._color)
        self._node.setHpr(self._hpr)
        self._node.hide()

        for letter in self._string:
            letter3d = self.font.find("*/%s"%(letter))
            placeholder = self._node.attachNewNode("letter")
            placeholder.setPos(self._spacing_count,0,0)
            letter3d.instanceTo(placeholder)
            self._spacing_count += self._spacing
        
    def getString(self):
        return self._string
        
    string = property(fget = getString, fset = setString)
    
    # ----------------------------------------------------------------- 
    
    def showText(self):
        self._node.show()
    
    # -----------------------------------------------------------------    
    def hideText(self):
        self._node.hide()
    
    # ----------------------------------------------------------------- 
    def __del__(self):
        self._node.stash()
    
if __name__ == "__main__":
    import main