# _*_ coding: UTF-8 _*_
##############################################################
## this module contains a class for generating racing tracks
##############################################################

#Input is a Tupel with Tupel of (x,y,z)
#They are the midpoints of the Street

from panda3d.core import * 
from trackgen import Track
from pandac.PandaModules import GeomVertexFormat, Geom, GeomVertexWriter, GeomTristrips, GeomNode

class Track3d(object):
    varthickness = []  #Generate the Vector for thickness of the road

    #Vertex Vars


    def __init__(self, res, x, y, z = 50):
        '''
        '''
        street_data = (Vec2(1,1),Vec2(5,1),Vec2(6,2))
        
        self.vdata = GeomVertexData('name', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic) 
        self.vertex = GeomVertexWriter(self.vdata, 'vertex')
        self.normal = GeomVertexWriter(self.vdata, 'normal')
        self.color = GeomVertexWriter(self.vdata, 'color')
        self.texcoord = GeomVertexWriter(self.vdata, 'texcoord')
        self.prim = GeomTriangles(Geom.UHStatic)
        
        
        m = Track(x,y, z)
        m.generateTrack()
        track_points = m.getInterpolatedPoints(res)
        print "Imput Centers:", track_points
        
    
        for i in range(len(track_points)-1):
            if i == 0:
                self.varthickness.append(self.calcTheVector(track_points[len(track_points)-1],track_points[i],track_points[i+1]))
                continue
            self.varthickness.append(self.calcTheVector(track_points[i-1],track_points[i],track_points[i+1]))
        self.varthickness.append(self.calcTheVector(track_points[len(track_points)-2],track_points[len(track_points)-1],track_points[0]))
        
        #Normalizing the Vector
        for i in self.varthickness:
            i.normalize()
        #Flip the Street to double sided
        street_data = self.flipToDoubleSided(street_data)
        #Creating the Vertex
        self.creatingVertex(track_points, street_data)
        #Connect the Vertex
        self.connectVertex(len(street_data))
        #?Show the Mesh
        #self.CreateMesh(self.vdata, self.prim)
        ##Debugprint
        print "Thickness Vectors:", self.varthickness
        #return List
        #return self.varthickness

    def calcTheVector(self, pre, now, past):
        vector1 = (pre[0] - now[0], pre[1] - now[1])
        vector2 = (past[0] - now[0], past[1] - now[1])
        high = pre[2] - past[2]
        return Vec3(((vector1[1] + vector2[1])/2.0),((vector1[0] + vector2[0])/2.0), high)

    def getVarthickness(self):
        return self.varthickness
    

    def flipToDoubleSided(self, street_data):
        #Flipps only the x with *-1 to the negativ side
        new_street_data = street_data
        for i in range (len(street_data)):
            new_street_data = new_street_data + (Vec2(((street_data[i][0]*(-1)),(street_data[i][1]))),)
        print "Street Data:", new_street_data
        return new_street_data


    def creatingVertex(self, track_points, street_data):
        #Math: self.varthickness are the midd points
        #for every Street Point create one Vertex by x*varthickness+Center and high+Center
        street_data_length = len(street_data)
        for i in range (len(track_points)):
            for j in range (street_data_length): ###WARUM war hier -2!!!!!!!!!!!!!!
                    self.vertex.addData3f((track_points[i][0] + (self.varthickness[i][0]*street_data[j][0]), track_points[i][1] + (self.varthickness[i][1]*street_data[j][0]), track_points[i][2] + (self.varthickness[i][2]+street_data[j][1])))
                    self.normal.addData3f(0, 0, 1)
                    self.color.addData4f(0, 0, 1, 1)
                    self.texcoord.addData2f(1, 0)
##                track_points[i][0] + (self.varthickness[i][0]*street_data[j][0])   #x
##                track_points[i][1] + (self.varthickness[i][1]*street_data[j][0])   #y
##                track_points[i][2] + (self.varthickness[i][2]+street_data[j][1])   #z

    def connectVertex(self, j):
        #j = len(street_Data)
        print "Vertex:", self.vdata.getNumRows()
        for i in range (self.vdata.getNumRows()-(j+1)): #-j??????  oder +-1
            if (i+1) % j != 0:
                self.prim.addVertex(i)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i+j+1)
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+j)
                self.prim.addVertex(i+j+1)
                self.prim.closePrimitive()
            else:
                print i
        print self.prim



    def createMesh(self):
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
         
        node = GeomNode('name')
        node.addGeom(geom)
         
        #nodePath = self.render.attachNewNode(node)
        return node


if __name__ == "__main__":
    #Test
    tuple1 = ((1.0,2.0,3.0),(3.0,4.0,5.0),(6.0,4.0,2.0),(8.0,3.0,6.0),(4.0,7.0,2.0))
    tuple2 = ((-2.0, -3.0, 0.0),(1.0, -5.0, 0.0),(4.0, -4.0, 0.0),(6.0, 0.0, 0.0),(3.0, 4.0, 0.0),(-2.0, 6.0, 0.0),(-7.0, 3.0, 0.0),(-8.0, -2.0, 0.0))
    tuple3 = ((10.0,10.0,0.0),(10.0,-10.0,0.0),(-10.0,-10.0,0.0),(-10.0,10.0,0.0))



    Track3d(10, 800, 600, 50)


