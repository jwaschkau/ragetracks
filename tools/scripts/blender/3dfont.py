# -*- coding: utf-8 -*-
###################################################################
## this creates 3dmodels out of printable characters
###################################################################
import Blender
import string
from Blender import Curve, Object, Scene, Text3d

scene = Scene.GetCurrent()
for character in string.printable:
    txt = Text3d.New(character) 
    txt.setText(character)
    txt.setName(character)
    txt.setExtrudeDepth(0.2)
    ob = scene.objects.new(txt) 
    ob.makeDisplayList()        
