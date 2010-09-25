# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *


class Text3D(object):
    '''
    Creates a 3D-Object out of a string
    '''
    def __init__(self, string, pos = Vec3(0,0,0), hpr = Vec3(0,0,0)):
        '''
        '''
        self.string = string
        self.position = pos
        self.hpr = hpr
        self.letters = loader.loadModel("data/models/3dfont/letters")
        self.node = render.attachNewNode("3DText")
        self.node.reparentTo(render)
        #self.node.setColor("red")
        self.node.hide()

        #self.letters.ls()
        for letter in self.string:
            letter3d = self.letters.find("a")
            print letter3d
            #letter3d.reparentTo(self.node)
        
        
        
    # -----------------------------------------------------------------
    def setText(self, string):
        self.string = string
    
    ##funktioniert aus irgendeinem grund noch nicht
    #string = property(fset = setText)
    
    # ----------------------------------------------------------------- 
    
    def showText(self):
        self.node.show()
    
    # -----------------------------------------------------------------    
    def hideText(self):
        self.node.hide()
    
    # -----------------------------------------------------------------   
    
if __name__ == "__main__":
    import main