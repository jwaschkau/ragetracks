# -*- coding: utf-8 -*-
#Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
#Date: 7/25/2005

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters
import colorsys


class GlowDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setBackgroundColor(0,0,0)
        #render.setShaderAuto()
        
        img = PNMImage("data/textures/vehicle01_body.png")
        for y in xrange(img.getReadYSize()):
            for x in xrange(img.getReadXSize()):
                r, g, b = img.getXel(x,y)
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                h += 0.9
##                print "#", r,g,b
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                img.setXel(x,y,r,g,b)
##                print "-", r,g,b
        img.write("data/textures/vehicle01_body2.png")
        

t=GlowDemo()

run()

##r,g,b = (0.5,0.5,0.2)
##h,s,v = colorsys.rgb_to_hsv(r, g, b)
##print r,g,b
##print h,s,v
##r, g, b = colorsys.hsv_to_rgb(h, s, v)
##print r,g,b

