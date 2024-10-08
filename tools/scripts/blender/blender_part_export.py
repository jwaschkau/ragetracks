#!BPY
# -*- coding: utf-8 -*-

""" Registration info for Blender menus:
Name: 'RageTracks Looping Export'
Blender: 245
Group: 'Export'
Tip: 'Export to RageTracks RoadPart XML.'
"""
__author__ = "Carsten Pfeffer"
__url__ = ("RageTracks homepage, http://www.launchpad.net/ragetracks")
__email__=""
__version__ = "0.1"

__bpydoc__ = """
This is an XML exporter for Blender.<br>
it only exports vertices of the selected object.
"""

import bpy
import Blender


def writeFile(filepath):
    output = file(filepath, 'w')
    scene = bpy.data.scenes.active
    object = scene.objects.active
    mesh = object.getData(mesh=1)

    output.write("<?xml version=\"1.0\" ?>\n<xml name=\""+object.name+"\">\n   <points>\n")

    for vert in mesh.verts:
        output.write("      <point x=\"%f\" y=\"%f\" z=\"%f\"/>\n" % (vert.co.x, vert.co.y, vert.co.z) )

    output.write("   </points>\n</xml>")

    output.close()


Blender.Window.FileSelector(writeFile, "Export Special Road Part")
print("-- RageTracks Exporter stopped --")