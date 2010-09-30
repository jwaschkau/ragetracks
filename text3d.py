# -*- coding: utf-8 -*-
from pandac.PandaModules import *


class Text3D(object):
    '''
    Creates a 3D-Object out of a string
    '''
    def __init__(self, string, pos = Vec3(0,0,0), hpr = Vec3(0,90,0), color = Vec4(1,1,0,0), spacing = 1):
        '''
        '''
        if type(string) != str:
            raise TypeError("Type should be %s not %s"%(str,type(string)))
        if type(pos) != type(Vec3()):
            raise TypeError("Type should be %s not %s"%(type(Vec3()),type(pos)))
        if type(hpr) != type(Vec3()):
            raise TypeError("Type should be %s not %s"%(type(Vec3()),type(hpr)))
        if type(color) != type(Vec4()):
            raise TypeError("Type should be %s not %s"%(type(Vec4()),type(color)))
        if type(spacing) != int:
            raise TypeError("Type should be %s not %s"%(int,type(spacing)))
        
        self._string = string
        self._position = pos
        self._hpr = hpr
        self._color = color
        self._spacing = spacing
        self._spacing_count = 0
        self._font = loader.loadModel("data/models/3dfont/letters")
        self._node = render.attachNewNode("3DText")
        self._node.setTwoSided(True)
        self._node.setColor(self._color)
        self._node.setHpr(self._hpr)

        for letter in self._string:
            letter3d = self._font.find("*/%s"%(letter))
            placeholder = self._node.attachNewNode("letter")
            placeholder.setPos(self._spacing_count,0,0)
            letter3d.instanceTo(placeholder)
            self._spacing_count += self._spacing

    # -----------------------------------------------------------------
    
    def setString(self, string):
        if type(string) != str:
            raise TypeError("Type should be %s not %s"%(str,type(string)))        
        self._node.stash()
        self._spacing_count = 0
        self._string = string
        
        self._node = render.attachNewNode("3DText")
        self._node.setTwoSided(True)
        self._node.setColor(self._color)
        self._node.setHpr(self._hpr)

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
    
    def setPosition(self, pos):
        if type(pos) != type(Vec3()):
            raise TypeError("Type should be %s not %s"%(type(Vec3()),type(pos)))
        self._position = pos
        self._node.setPos(self._position)
        
    def getPosition(self):
        return self._position
        
    position = property(fget = getPosition, fset = setPosition)
    
    # ----------------------------------------------------------------- 
    
    def setHpr(self, hpr):
        if type(hpr) != type(Vec3()):
            raise TypeError("Type should be %s not %s"%(type(Vec3()),type(hpr)))
        self._hpr = hpr
        self._node.setHpr(self._hpr)
        
    def getHpr(self):
        return self._hpr
        
    hpr = property(fget = getHpr, fset = setHpr)
    
    # ----------------------------------------------------------------- 
    
    def setColor(self, color):
        if type(color) != type(Vec4()):
            raise TypeError("Type should be %s not %s"%(type(Vec4()),type(color)))
        self._color = color
        self._node.setColor(self._color)
        
    def getColor(self):
        return self._color
        
    color = property(fget = getColor, fset = setColor)
    
    # ----------------------------------------------------------------- 
    
    def showText(self):
        self._node.show()
    
    # -----------------------------------------------------------------
     
    def hideText(self):
        self._node.hide()
        
    # -----------------------------------------------------------------
     
    def reparentTo(self, nodepath):
        if type(nodepath) != type(NodePath()):
            raise TypeError("Type should be %s not %s"%(type(NodePath()),type(nodepath)))
        self._node.reparentTo(nodepath)
    
    # -----------------------------------------------------------------
    def __del__(self):
        try:self._node.stash()
        except:pass
    
if __name__ == "__main__":
    import main