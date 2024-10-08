# -*- coding: utf-8 -*-


from panda3d.core import Point3, Vec3

from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Geom, GeomNode, GeomPoints, NodePath, GeomLinestrips

import math

"""
Note that wireprims are wire-like representations of geom, in the same manner as Ogre's debug mode.  I find this the most useful way to represent
ODE geom structures visually, as you can clearly see the orientation versus a more generic wireframe mesh.

These wireprims are rendered as linestrips.  Therefore, only vertices are required and texturing is not supported.  You can use standard render attribute changes such
as setColor in order to change the line's color.  By default it is green.

This class merely returns a NodePath to a GeomNode that is a representation of what is requested.  You can use this outside of ODE geom visualizations, obviously.

Supported are sphere, box, cylinder, capsule (aka capped cylinder), ray, and plane

to use:

sphereNodepath = WireGeom().generate ('sphere', radius=1.0)
boxNodepath = WireGeom().generate ('box', extents=(1, 1, 1))
cylinderNodepath = WireGeom().generate ('cylinder', radius=1.0, length=3.0)
rayNodepath = WireGeom().generate ('ray', length=3.0)
planeNodepath = WireGeom().generate ('plane')

"""
class WireGeom:

  def __init__ (self):
    # GeomNode to hold our individual geoms
    self.gnode = GeomNode ('wirePrim')

    # How many times to subdivide our spheres/cylinders resulting vertices.  Keep low
    # because this is supposed to be an approximate representation
    self.subdiv = 12

  def drawLine (self, start, end):

    # since we're doing line segments, just vertices in our geom
    format = GeomVertexFormat.getV3()

    # build our data structure and get a handle to the vertex column
    vdata = GeomVertexData ('', format, Geom.UHStatic)
    vertices = GeomVertexWriter (vdata, 'vertex')

    # build a linestrip vertex buffer
    lines = GeomLinestrips (Geom.UHStatic)

    vertices.addData3f (start[0], start[1], start[2])
    vertices.addData3f (end[0], end[1], end[2])

    lines.addVertices (0, 1)

    lines.closePrimitive()

    geom = Geom (vdata)
    geom.addPrimitive (lines)
    # Add our primitive to the geomnode
    self.gnode.addGeom (geom)

  def drawCircle (self, radius, axis, offset):

    # since we're doing line segments, just vertices in our geom
    format = GeomVertexFormat.getV3()

    # build our data structure and get a handle to the vertex column
    vdata = GeomVertexData ('', format, Geom.UHStatic)
    vertices = GeomVertexWriter (vdata, 'vertex')

    # build a linestrip vertex buffer
    lines = GeomLinestrips (Geom.UHStatic)

    for i in range (0, self.subdiv):
      angle = i / float(self.subdiv) * 2.0 * math.pi
      ca = math.cos (angle)
      sa = math.sin (angle)
      if axis == "x":
        vertices.addData3f (0, radius * ca, radius * sa + offset)
      if axis == "y":
        vertices.addData3f (radius * ca, 0, radius * sa + offset)
      if axis == "z":
        vertices.addData3f (radius * ca, radius * sa, offset)

    for i in range (1, self.subdiv):
      lines.addVertices(i - 1, i)
    lines.addVertices (self.subdiv - 1, 0)

    lines.closePrimitive()

    geom = Geom (vdata)
    geom.addPrimitive (lines)
    # Add our primitive to the geomnode
    self.gnode.addGeom (geom)

  def drawCapsule (self, radius, length, axis):

    # since we're doing line segments, just vertices in our geom
    format = GeomVertexFormat.getV3()

    # build our data structure and get a handle to the vertex column
    vdata = GeomVertexData ('', format, Geom.UHStatic)
    vertices = GeomVertexWriter (vdata, 'vertex')

    # build a linestrip vertex buffer
    lines = GeomLinestrips (Geom.UHStatic)

    # draw upper dome
    for i in range (0, self.subdiv / 2 + 1):
      angle = i / float(self.subdiv) * 2.0 * math.pi
      ca = math.cos (angle)
      sa = math.sin (angle)
      if axis == "x":
        vertices.addData3f (0, radius * ca, radius * sa + (length / 2))
      if axis == "y":
        vertices.addData3f (radius * ca, 0, radius * sa + (length / 2))

    # draw lower dome
    for i in range (0, self.subdiv / 2 + 1):
      angle = -math.pi + i / float(self.subdiv) * 2.0 * math.pi
      ca = math.cos (angle)
      sa = math.sin (angle)
      if axis == "x":
        vertices.addData3f (0, radius * ca, radius * sa - (length / 2))
      if axis == "y":
        vertices.addData3f (radius * ca, 0, radius * sa - (length / 2))

    for i in range (1, self.subdiv + 1):
      lines.addVertices(i - 1, i)
    lines.addVertices (self.subdiv + 1, 0)

    lines.closePrimitive()

    geom = Geom (vdata)
    geom.addPrimitive (lines)
    # Add our primitive to the geomnode
    self.gnode.addGeom (geom)

  def drawRect (self, width, height, axis):

    # since we're doing line segments, just vertices in our geom
    format = GeomVertexFormat.getV3()

    # build our data structure and get a handle to the vertex column
    vdata = GeomVertexData ('', format, Geom.UHStatic)
    vertices = GeomVertexWriter (vdata, 'vertex')

    # build a linestrip vertex buffer
    lines = GeomLinestrips (Geom.UHStatic)

    # draw a box
    if axis == "x":
      vertices.addData3f (0, -width, -height)
      vertices.addData3f (0, width, -height)
      vertices.addData3f (0, width, height)
      vertices.addData3f (0, -width, height)
    if axis == "y":
      vertices.addData3f (-width, 0, -height)
      vertices.addData3f (width, 0, -height)
      vertices.addData3f (width, 0, height)
      vertices.addData3f (-width, 0, height)
    if axis == "z":
      vertices.addData3f (-width, -height, 0)
      vertices.addData3f (width, -height, 0)
      vertices.addData3f (width, height, 0)
      vertices.addData3f (-width, height, 0)

    for i in range (1, 3):
      lines.addVertices(i - 1, i)
    lines.addVertices (3, 0)

    lines.closePrimitive()

    geom = Geom (vdata)
    geom.addPrimitive (lines)
    # Add our primitive to the geomnode
    self.gnode.addGeom (geom)

  def generate (self, type, radius=1.0, length=1.0, extents=Point3(1, 1, 1)):

    if type == 'sphere':
      # generate a simple sphere
      self.drawCircle (radius, "x", 0)
      self.drawCircle (radius, "y", 0)
      self.drawCircle (radius, "z", 0)

    if type == 'capsule':
      # generate a simple capsule
      self.drawCapsule (radius, length, "x")
      self.drawCapsule (radius, length, "y")
      self.drawCircle (radius, "z", -length / 2)
      self.drawCircle (radius, "z", length / 2)

    if type == 'box':
      # generate a simple box
      self.drawRect (extents[1], extents[2], "x")
      self.drawRect(extents[0], extents[2], "y")
      self.drawRect (extents[0], extents[1], "z")

    if type == 'cylinder':
      # generate a simple cylinder
      self.drawLine ((0, -radius, -length / 2), (0, -radius, length/2))
      self.drawLine ((0, radius, -length / 2), (0, radius, length/2))
      self.drawLine ((-radius, 0, -length / 2), (-radius, 0, length/2))
      self.drawLine ((radius, 0, -length / 2), (radius, 0, length/2))
      self.drawCircle (radius, "z", -length / 2)
      self.drawCircle (radius, "z", length / 2)

    if type == 'ray':
      # generate a ray
      self.drawCircle(length / 10, "x", 0)
      self.drawCircle (length / 10, "z", 0)
      self.drawLine ((0, 0, 0), (0, 0, length))
      self.drawLine ((0, 0, length), (0, -length/10, length*0.9))
      self.drawLine ((0, 0, length), (0, length/10, length*0.9))

    if type == 'plane':
      # generate a plane
      length = 3.0
      self.drawRect(1.0, 1.0, "z")
      self.drawLine ((0, 0, 0), (0, 0, length))
      self.drawLine ((0, 0, length), (0, -length/10, length*0.9))
      self.drawLine((0, 0, length), (0, length/10, length*0.9))

    # rename ourselves to wirePrimBox, etc.
    name = self.gnode.getName()
    self.gnode.setName(name + type.capitalize())

    NP = NodePath (self.gnode)  # Finally, make a nodepath to our geom
    NP.setColor(0.0, 1.0, 0.0)   # Set default color

    return NP


# demonstration code below
if __name__ == "__main__":
    import direct.directbase.DirectStart
    allGeoms = render.attachNewNode ("allWireGeoms")

    plane = WireGeom().generate ('plane')
    plane.setPos (0, 0, 0)
    plane.setHpr (0, 0, 0)
    plane.reparentTo( allGeoms )

    sphere = WireGeom().generate ('sphere', radius=1.0)
    sphere.setPos (0, 3, 1)
    sphere.setHpr (0, 0, 0)
    sphere.reparentTo( allGeoms )

    capsule = WireGeom().generate ('capsule', radius=1.0, length=3.0)
    capsule.setPos (0, 6, 1)
    capsule.setHpr (0, 0, 0)
    capsule.reparentTo( allGeoms )

    box = WireGeom().generate ('box', extents=(1, 1, 1))
    box.setPos (0, 9, 1)
    box.setHpr (0, 0, 0)
    box.reparentTo( allGeoms )

    cylinder = WireGeom().generate ('cylinder', radius=1.0, length=3.0)
    cylinder.setPos (0, -3, 1)
    cylinder.setHpr (0, 0, 0)
    cylinder.reparentTo( allGeoms )

    ray = WireGeom().generate ('ray', length=3.0)
    ray.setPos (0, -6, 1)
    ray.setHpr (0, 0, 0)
    ray.reparentTo( allGeoms )

    allGeoms.reparentTo( base.render )

    # Set the camera position
    base.disableMouse()
    base.camera.setPos(40, 0, 0)
    base.camera.lookAt(0, 0, 0)

    # Spin all of the wireGeoms around so you can see 'em
    i = allGeoms.hprInterval (4.0, Vec3(360, 360, 0))
    i.loop()

    run()