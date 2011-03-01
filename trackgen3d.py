# -*- coding: utf-8 -*-
##############################################################
## this module contains a class for generating racing tracks
##############################################################

from panda3d.core import * 
from trackgen import Track
from pandac.PandaModules import GeomVertexFormat, Geom, GeomVertexWriter, GeomTristrips, GeomNode
import xml.dom.minidom as dom
from xml.dom.minidom import Document
from direct.directnotify.DirectNotify import DirectNotify
import random

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class RoadShape(object):
    '''
    describes the shape of the road e.g. |__/\__|
    '''
    def __init__(self, *args, **kwds):
        '''
        '''
        self.points = []
        self.name = "street part"
        self.author = "Rage Tracks Team"
        self.mirrored = True
        
        self.texcoords = []
        
        for arg in args:
            if type(arg) == Vec2:
                self.points.append(arg)
        
        if "name" in kwds.keys():
            self.name = str(kwds["name"])
        
        if "author" in kwds.keys():
            self.author = str(kwds["author"])
        
        if "mirrored" in kwds.keys():
            self.mirrored = bool(kwds["mirrored"])
        
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()
        self._notify = DirectNotify().newCategory("TrackGen3D")
        self._notify.info("New StreetData-Object created: %s" %(self))
    # -------------------------------------------------------------------------------------

    def addPoint(self, x, y):
        '''
        adds a point to the road
        notice: the points are connected in the same order, they're added
        @param x: (float) x-coordinate
        @param y: (float) y-coordinate
        '''
        self.points.append(Vec2(x,y))
    
    # -------------------------------------------------------------------------------------

    def readFile(self, filename):
        '''
        reads the shape out of a file
        @param filename: (str) the filename
        '''
        self.points = []
        # open file
        xmlfile = dom.parse(filename)
        
        # create the root element
        xml = xmlfile.getElementsByTagName("xml").item(0)
        self.name = xml.getAttribute("name") # read name and author out of root
        self.author = xml.getAttribute("author")
        
        # check if the points should be mirrored
        mirrored = xml.getAttribute("mirrored")
        if mirrored == "False":
            self.mirrored = False
        else:
            self.mirrored = True
        
        # read out the points
        points = xml.getElementsByTagName("points")
        points = points[0].childNodes

        pointcount = points.length

        for i in xrange(pointcount):
            point = points.item(i)
            if point.nodeType == point.ELEMENT_NODE:
                x = float(point.getAttribute("x"))
                y = float(point.getAttribute("y"))
                self.points.append(Vec2(x, y))
        
    
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()
        self.calculateTexcoordinates()
    
    # -------------------------------------------------------------------------------------
    
    def calculateTexcoordinates(self):
        '''
        '''
        tmp = []
        length = 0
        n = 0
        # calculate the texcoords
        for i in xrange(len(self.points)-1):
            n = (self.points[i+1]-self.points[i]).length()
            length += n
            tmp.append(n)
        n = (self.points[0]-self.points[i+1]).length()
        tmp.append(n)
        length += n
        
        n = 0
        self.texcoords.append(n)
        for i in tmp:
            n += i/length
            self.texcoords.append(n)
            
    # -------------------------------------------------------------------------------------
    
    def getTexCoordinates(self):
        '''
        '''
        return self.texcoords
    
    # -------------------------------------------------------------------------------------
    
    def mirrorPoints(self):
        '''
        mirrors the point at y axis
        '''
        pointlist = []
        for point in self.points:
            if point.getX() <= 0:
                pointlist.append(point)
                if point.getX() != 0:
                    pointlist.insert(0,Vec2(point.getX()*-1,point.getY()))
        self.points = pointlist
    
    # -------------------------------------------------------------------------------------
    
    def demirrorPoints(self):
        '''
        mirrors the point at y axis
        '''
        pointlist = []
        for point in self.points:
            if point.getX() <= 0:
                pointlist.append(point)
        self.points = pointlist
    
    # -------------------------------------------------------------------------------------
    
    def writeFile(self, filename):
        '''
        writes the shape into a file
        @param filename: (str) the filename
        '''
        # create the document
        doc = Document()

        # chreate the root element
        xml = doc.createElement("xml")
        
        # the name, author and information if the points are mirrored
        xml.setAttribute("mirrored", str(self.mirrored))
        xml.setAttribute("name", self.name)
        xml.setAttribute("author", self.author)
        doc.appendChild(xml)

        # insert the points
        points = doc.createElement("points")
        
        if self.mirrored:
            self.demirrorPoints()
        
        for point in self.points:
            p = doc.createElement("point")
            p.setAttribute("x", str(point.getX()))
            p.setAttribute("y", str(point.getY()))
            points.appendChild(p)

        xml.appendChild(points)

        # write it into a file
        f = file(filename, "w")
        doc.writexml(f, addindent="   ", newl="\n")
        f.close()
        
        if self.mirrored:
            self.mirrorPoints()
    
        
    # -------------------------------------------------------------------------------------
    
    def __str__(self):
            '''
            returns a string representation e.g. for printing
            '''
            return str(self.points)
        
    # -------------------------------------------------------------------------------------
    
    def __getitem__(self, index):
        '''
        this method is used for indexing like street_data[1]
        '''
        return self.points[index]
    
    # -------------------------------------------------------------------------------------
    
    def __len__(self):
        '''
        returns the count of the points
        '''
        return len(self.points)
    
    # -------------------------------------------------------------------------------------
    
    def getLength(self):
        '''
        returns the count of the points
        '''
        return len(self.points)
    
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class StreetData(RoadShape):
    '''
    '''
    def __init__(self, *args, **kwds):
        RoadShape.__init__(self, *args, **kwds)
        self.border_l = RoadShape()
        self.border_l_coll = RoadShape()
        self.border_r = RoadShape()
        self.border_r_coll = RoadShape()
    
    # -------------------------------------------------------------------------------------
        
    def readFile(self, filename):
        '''
        reads the shape out of a file
        @param filename: (str) the filename
        '''
        self.points = []
        # open file
        xmlfile = dom.parse(filename)
        
        # create the root element
        xml = xmlfile.getElementsByTagName("xml").item(0)
        self.name = xml.getAttribute("name") # read name and author out of root
        self.author = xml.getAttribute("author")
        
        # check if the points should be mirrored
        mirrored = xml.getAttribute("mirrored")
        if mirrored == "False":
            self.mirrored = False
        else:
            self.mirrored = True
        
        # read out the points
        points = xml.getElementsByTagName("points")
        points = points[0].childNodes

        pointcount = points.length

        for i in xrange(pointcount):
            point = points.item(i)
            if point.nodeType == point.ELEMENT_NODE:
                x = float(point.getAttribute("x"))
                y = float(point.getAttribute("y"))
                self.points.append(Vec2(x, y))
    
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()
                
            # read out the border
            border_l = xml.getElementsByTagName("border_l")
            if len(border_l) > 0:
                border_l = border_l[0].childNodes

                border_lcount = border_l.length

                for i in xrange(border_lcount):
                    point = border_l.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_l.points.append(Vec2(x, y))
                        self.border_r.points.insert(0,Vec2(x*-1,y))
            
            #read out the collision model border
            border_l_coll = xml.getElementsByTagName("border_l_coll")
            if len(border_l_coll) > 0:
                border_l_coll = border_l_coll[0].childNodes

                border_l_collcount = border_l_coll.length

                for i in xrange(border_l_collcount):
                    point = border_l_coll.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_l_coll.points.append(Vec2(x, y))
                        self.border_r_coll.points.insert(0,Vec2(x*-1,y))
        else:
            #read out the borders separately
            
            # read out the left border
            border_l = xml.getElementsByTagName("border_l")
            if len(border_l) > 0:
                border_l = border_l[0].childNodes

                border_lcount = border_l.length

                for i in xrange(border_lcount):
                    point = border_l.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_l.points.append(Vec2(x, y))
            # left collision model
            border_l_coll = xml.getElementsByTagName("border_l_coll")
            if len(border_l_coll) > 0:
                border_l_coll = border_l_coll[0].childNodes

                border_l_collcount = border_l_coll.length

                for i in xrange(border_l_collcount):
                    point = border_l_coll.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_l_coll.points.append(Vec2(x, y))
                    
            # read out the right border
            border_r = xml.getElementsByTagName("border_r")
            if len(border_r) > 0:
                border_r = border_r[0].childNodes

                border_rcount = border_r.length

                for i in xrange(border_rcount):
                    point = border_r.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_r.points.append(Vec2(x, y))
            
            # right collision model
            border_r_coll = xml.getElementsByTagName("border_r_coll")
            if len(border_l_coll) > 0:
                border_r_coll = border_r_coll[0].childNodes

                border_r_collcount = border_r_coll.length

                for i in xrange(border_r_collcount):
                    point = border_r_coll.item(i)
                    if point.nodeType == point.ELEMENT_NODE:
                        x = float(point.getAttribute("x"))
                        y = float(point.getAttribute("y"))
                        self.border_r_coll.points.append(Vec2(x, y))
        
        self.calculateTexcoordinates()
        if len(self.border_l) > 0:
            self.border_l.calculateTexcoordinates()
        if len(self.border_r) > 0:
            self.border_r.calculateTexcoordinates()

        if len(self.border_l_coll) > 0:
            self.border_l_coll.calculateTexcoordinates()
        if len(self.border_r_coll) > 0:
            self.border_r_coll.calculateTexcoordinates()
    
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class Track3d(object):
    '''
    Generate the 3d Mesh out of the StreetData and the 2dTrack
    '''
    def __init__(self, res, x, y, z = 200, player_count=1, street_data=""):
        '''
        '''
        self._notify = DirectNotify().newCategory("TrackGen3D")
        self._notify.info("New Track3D-Object created: %s" %(self))
        #street_data = (Vec2(4.0,4.0), Vec2(10.0,10.0), Vec2(10.0,0.0), Vec2(4.0,0.0), Vec2(0.0,-1.0))
        #street_data = StreetData(Vec2(15.0,1.0), Vec2(15.0,-5.0), Vec2(0.0,-5.0), mirrored=True) #, Vec2(15.0,0.0)
        self.street_data = StreetData()
        
##        self.street_data.readFile("data/road/road01.xml")
##        self.street_data.readFile("data/road/tube.xml")
        if street_data == "":
            datas = ["road01", "tube"]
            street_data = datas[random.randint(0, len(datas)-1)]
        self.street_data.readFile("data/road/"+street_data+".xml")
    
        self.streetTextrange = 0.0
        self.track = Track(x, y, z)
        self.track.generateTestTrack(player_count)
##        self.track.generateTrack(player_count)
     
        self.track_points = self.track.getInterpolatedPoints(res)
        self.varthickness = []  #Generate the Vector for thickness of the road
        
        self.generateNormals()
##        for i in range(len(self.track_points)-1):
##            if i == 0:
##                self.varthickness.append(self.calcTheVector(self.track_points[i],self.track_points[i],self.track_points[i+1])) #First
##                continue
##            self.varthickness.append(self.calcTheVector(self.track_points[i-1],self.track_points[i],self.track_points[i+1])) 
##        self.varthickness.append(self.calcTheVector(self.track_points[len(self.track_points)-2],self.track_points[len(self.track_points)-1],self.track_points[len(self.track_points)-1])) #Last
##        
##        #Normalizing the Vector
##        for i in self.varthickness:
##            i.normalize()
##
##        print self.varthickness[-1]
##        print self.varthickness[0]
##        print self.varthickness[1]
##        print self.varthickness[2]
            
        #Spin the last 100 Points a litte bit to Vec3(-1,0,0)
        for i in xrange (-100,1):
            #print self.varthickness[i] * (-i / 100), self.varthickness[i] , ((i* -1) / 100.0), i
            #print ((i* -1) / 100.0), self.varthickness[i], self.varthickness[i] * ((i* -1) / 100.0)
            self.varthickness[i] = self.varthickness[i] * (((i+1) * -1) / 100.0) + Vec3(-1,0,0)
            self.normals[i] = self.normals[i] * (((i+1) * -1) / 100.0) + Vec3(0,0,1)
            
            self.varthickness[i].normalize()
            self.normals[i].normalize()
            #print self.varthickness[i]
            
##        print self.varthickness[-1]
##        print self.varthickness[0]
##        print self.varthickness[1]
##        print self.varthickness[2]    
##        print self.varthickness
##        for i in range(len(self.varthickness)):
##            if self.varthickness[i-1].almostEqual(self.varthickness[i], 0.3):
##                pass
##            else:
##                print "varthickness", self.varthickness[i-1], self.varthickness[i]
        

# -------------------------------------------------------------------------------------

    def resetWriters(self):
        '''
        '''
        self.vdata = GeomVertexData('street', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic) 
        
        self.vertex = GeomVertexWriter(self.vdata, 'vertex')
        self.normal = GeomVertexWriter(self.vdata, 'normal')
        self.color = GeomVertexWriter(self.vdata, 'color')
        self.texcoord = GeomVertexWriter(self.vdata, 'texcoord')
        self.prim = GeomTriangles(Geom.UHStatic)

# -------------------------------------------------------------------------------------

    def calcTheVector(self, pre, now, past):
        vector1 = (pre[0] - now[0], pre[1] - now[1])
        vector2 = (now[0] - past[0], now[1] - past[1]) 
        high = pre[2] - past[2]
        return Vec3(((vector1[1] + vector2[1])/2.0),((vector1[0] + vector2[0])/2.0), high)

# -------------------------------------------------------------------------------------

    def getVarthickness(self):
        return self.varthickness
    
# -------------------------------------------------------------------------------------

    def setTrackPoints(self, track_points):
        '''
        '''
        self.track_points = track_points
        
    def getTrackPoints(self):
        '''
        '''
        return self.track_points
        
    trackpoints = property(fget = getTrackPoints, fset = setTrackPoints)
    
# -------------------------------------------------------------------------------------

    def generateNormals(self):
        '''
        '''
        self.varthickness = []
        self.normals = []
        last_normal = Vec3(0,0,1)
        last_vec = Vec3(0,1,0)
        for i in xrange(len(self.track_points)):
            if i == 0:
                vec = self.track_points[0]-self.track_points[1]
            elif i+1 == len(self.track_points):
                vec = self.track_points[i-1]-self.track_points[0]
            else:
                vec = self.track_points[i-1]-self.track_points[i+1]
                
            
            # calculate here the direction out of the street vector and the last normal
            last_normal.normalize()
            vec.normalize()
            mat = Mat3()

            mat.setRotateMat(-90, last_normal) # turn the direction around the last_normal
            turned_vec = mat.xform(vec)
            
            turned_vec.normalize()
            last_normal = turned_vec.cross(vec) # calculate the new normal
            
            turned_vec.normalize()
            self.varthickness.append(turned_vec)
            self.normals.append(last_normal)

# -------------------------------------------------------------------------------------


    def createVertices(self, track_points = None, street_data = None):
        '''
        '''
        if track_points == None:
            track_points = self.track_points
        if street_data == None:
            street_data = self.street_data
            
        self.resetWriters()
        texcoordinates =[]
        street_data_length = len(street_data)
        
        texcoordinates = street_data.getTexCoordinates()
        
        for i in xrange(len(track_points)):
            turned_vec = self.varthickness[i]  
            last_normal = self.normals[i]          
            j = 0
            for shapedot in street_data:
                # this is like a layer in 3d [Ebenengleichung] 
                # vec = vec + vec*scalar + vec*scalar
                # this is used to transform the 2d-Streetshape to 3d
                point = track_points[i] + (turned_vec*shapedot[0]) + (last_normal*shapedot[1])
                
                self.vertex.addData3f(point[0], point[1], point[2])
                self.normal.addData3f(0, 0, 1) #KA how to calc
                self.streetTextrange += 0.004
                self.texcoord.addData2f(texcoordinates[j], self.streetTextrange)
                j += 1
                
            

# -------------------------------------------------------------------------------------

    def connectVertices(self, street_data):
        #param j = len(street_Data)
        j = len(street_data)
        for i in xrange (self.vdata.getNumRows()-(j)): #-j??????  oder +-1
            if (i+1) % j != 0:
                self.prim.addVertex(i)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i+j+1)
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+j+1)
                self.prim.addVertex(i+j)
                self.prim.closePrimitive()
            else: # close mesh's bottom side
                
                self.prim.addVertex(i+1-j)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i)
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i+j)
                self.prim.closePrimitive()
                
        # close start and end
        k = self.vdata.getNumRows()-j
        for i in xrange (j):
            if (i+1) % j != 0:
                self.prim.addVertex(i)
                self.prim.addVertex(i+k+1)
                self.prim.addVertex(i+1)                
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+k)
                self.prim.addVertex(i+k+1)
                self.prim.closePrimitive()
                
            else: # close mesh's bottom side
                self.prim.addVertex(i)
                self.prim.addVertex(i+k-j+1)
                self.prim.addVertex(i-j+1)                
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+k)
                self.prim.addVertex(i+k-j+1)
                self.prim.closePrimitive()

# -------------------------------------------------------------------------------------

    def createRoadMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices()
        #Connect the Vertex
        self.connectVertices(self.street_data)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('street')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node

    # -------------------------------------------------------------------------------------

    def createUninterpolatedRoadMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices(self.track.getPoints(), self.street_data)
        #Connect the Vertex
        self.connectVertices(self.street_data)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('street')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node

# -------------------------------------------------------------------------------------

    def createBorderLeftMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices(self.track_points, self.street_data.border_l)

        #Connect the Vertex
        self.connectVertices(self.street_data.border_l)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('border_l')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node
    
# -------------------------------------------------------------------------------------

    def createBorderRightMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices(self.track_points, self.street_data.border_r)
        #Connect the Vertex
        self.connectVertices(self.street_data.border_r)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('border_r')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node

# -------------------------------------------------------------------------------------

    def createBorderLeftCollisionMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices(self.track_points, self.street_data.border_l_coll)

        #Connect the Vertex
        self.connectVertices(self.street_data.border_l_coll)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('border_l_coll')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node
    
# -------------------------------------------------------------------------------------

    def createBorderRightCollisionMesh(self):
        '''
        '''
        #Creating the Vertex
        self.createVertices(self.track_points, self.street_data.border_r_coll)
        #Connect the Vertex
        self.connectVertices(self.street_data.border_r_coll)
        
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('border_r_coll')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node
    

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    #import main
    #Track3d(200,800,600)
    #Test
    import trackgentest
##    tuple1 = ((1.0,1.0,0.0),(1.0,4.0,0.0),(1.0,10.0,0.0))
##    tuple2 = ((-2.0, -3.0, 0.0),(1.0, -5.0, 0.0),(4.0, -4.0, 0.0),(6.0, 0.0, 0.0),(3.0, 4.0, 0.0),(-2.0, 6.0, 0.0),(-7.0, 3.0, 0.0),(-8.0, -2.0, 0.0))
##    tuple3 = ((10.0,10.0,0.0),(10.0,-10.0,0.0),(-10.0,-10.0,0.0),(-10.0,10.0,0.0))
##
##
##
##    Track3d(100, 800, 600, 50)


  
