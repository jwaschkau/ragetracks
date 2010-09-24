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
        
        
        
    # -----------------------------------------------------------------
    
if __name__ == "__main__":
    import main