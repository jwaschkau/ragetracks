# -*- coding: utf-8 -*-
###################################################################
## this creates 3dmodels out of the ascii-characters
###################################################################
import Blender
import string
from Blender import Curve, Object, Scene, Text3d

scene = Scene.GetCurrent()
for character in string.letters:
    txt = Text3d.New(character) 
    txt.setText(character)
    txt.setName(character)
    txt.setExtrudeDepth(0.2)
    ob = scene.objects.new(txt)   # create an object from the obdata in the current scene
    ob.makeDisplayList()        # rebuild the display list for this object
