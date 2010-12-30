# -*- coding: utf-8 -*-
##############################################################
## this module contains a class for generating racing tracks
##############################################################

##          TODO                
## - The Curve must pass thrue the Points from genStart

import random
import math
import bitmap24
import copy
from panda3d.core import *
from pandac.PandaModules import *
import xml.dom.minidom as dom
from xml.dom.minidom import Document
from direct.directnotify.DirectNotify import DirectNotify

MIN_Z_DIST = 100
MAX_Z_DIST = 500
MIN_DIST = 90
VEHICLE_DIST = 50
MIN_ANGLE = 40

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class Looping(object):
    '''
    describes a special road part, e.g. a Looping
    '''
    def __init__(self, *args, **kwds):
        '''
        '''
        self.points = []
        self.name = "special street part"
        self._notify = DirectNotify().newCategory("TrackGen")
        
        for arg in args:
            if type(arg) == Vec2:
                self.points.append(arg)
        
        if "filename" in kwds.keys():
            self.readFile(str(kwds["filename"]))
            
        if "name" in kwds.keys():
            self.name = str(kwds["name"])
            
        ##self._notify.info("New Looping-Object created: %s" %(self))
    # -------------------------------------------------------------------------------------

    def addPoint(self, x, y, z):
        '''
        adds a point to the road
        notice: the points are connected in the same order, they're added
        @param x: (float) x-coordinate
        @param y: (float) y-coordinate
        @param z: (float) z-coordinate
        '''
        self.points.append(Vec3(x,y,z))
    
    # -------------------------------------------------------------------------------------

    def __mul__(self, value):
        '''
        '''
        for i in xrange(len(self.points)):
            self.points[i] *= value
        return self
    
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
        
        # read out the points
        points = xml.getElementsByTagName("point")
        pointcount = points.length
        for i in xrange(pointcount):
            point = points.item(i)
            x = float(point.getAttribute("x"))
            y = float(point.getAttribute("y"))
            z = float(point.getAttribute("z"))
            self.points.append(Vec3(x, y, z))
    
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
        xml.setAttribute("author", self.author)
        doc.appendChild(xml)

        # insert the points
        points = doc.createElement("points")
        
        for point in self.points:
            p = doc.createElement("point")
            p.setAttribute("x", str(point.getX()))
            p.setAttribute("y", str(point.getY()))
            p.setAttribute("z", str(point.getZ()))
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
            return "Looping"+str(self.points)
        
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

class Line(object):
    '''
    '''
    def __init__(self, vec1, vec2):
        '''
        '''
        self._vec1 = vec1
        self._vec2 = vec2
    
    # -------------------------------------------------------------------------------------
    
    def getVec1(self):
        '''
        '''
        return self._vec1
        
    # -------------------------------------------------------------------------------------
    
    def setVec1(self, vec1):
        '''
        '''
        if type(vec1) != Vec2 and type(vec1) != Vec3:
            raise TypeError("parameter vec1 has to be of type Vec2 or Vec3")
        
        self._vec1 = vec1
    
    # -------------------------------------------------------------------------------------
    
    def getVec2(self):
        '''
        '''
        return self._vec2
    
    # -------------------------------------------------------------------------------------
    
    def setVec2(self, vec2):
        '''
        '''
        if type(vec2) != Vec2 and type(vec2) != Vec3:
            raise TypeError("parameter vec2 has to be of type Vec2 or Vec3")
        
        self._vec2 = vec2
        
    # -------------------------------------------------------------------------------------
    
    def crossesLine(self, other):
        '''
        '''
        x1 = self.vec1.getX()
        x2 = self.vec2.getX()
        x3 = other.vec1.getX()
        x4 = other.vec2.getX()
        
        y1 = self.vec1.getY()
        y2 = self.vec2.getY()
        y3 = other.vec1.getY()
        y4 = other.vec2.getY()
        
        denominator = ((y4-y3)*(x2-x1))-((x4-x3)*(y2-y1))
        
        if denominator == 0:
            print "StandardError" #raise StandardError()
        else:
            u = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/denominator
            v = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/denominator
            
            if 0 < u < 1 and 0 < v < 1:
                return True
            else:
                return False
        
    # -------------------------------------------------------------------------------------
    
    def getAngle(self, other):
        '''
        '''
        a = (other.vec1-self.vec1).length()
        b = (self.vec2-self.vec1).length()
        c = (other.vec2-other.vec1).length()
        
        value = ((b**2)+(c**2)-(a**2)) / (2*b*c)
        
        # because of floating point precision
        if value > 1:
            value = 1
        
        angle = math.degrees(math.acos( value ))

        return angle
        
    # -------------------------------------------------------------------------------------
    
    vec1 = property(getVec1, setVec1)
    vec2 = property(getVec2, setVec2)
        
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class Track(object):
    '''
    This class represents a Track
    '''
    def __init__(self, size_x, size_y, max_height=2300):
        '''
        the constructor creates an empty track
        @param size_x: (int) maximum x-coordinates
        @param size_y: (int) maximum y-coordinates
        @param max_height: (int) maximum z-coordinates
        '''
        self.setSize(size_x, size_y, max_height)
        self.points = []
        self.curve = None
        self._notify = DirectNotify().newCategory("TrackGen")
        self._notify.info("New Track-Object created: %s" %(self))

    # -------------------------------------------------------------------------------------

    def setSize(self, size_x, size_y, max_height=1000):
        '''
        sets the size of the map. This only works if the map is not generated, yet.
        @param size_x: (int) maximum x-coordinates of the map
        @param size_y: (int) maximum y-coordinates of the map
        @param max_height: (int) maximum z-coordinates of the map
        '''
        # check for the right type
        if type(size_x) != type(size_y) != type(max_height) != int:
            raise TypeError("size_x, size_y and max_height have to be of type 'int'")

        # set the size
        self.size = Vec3(size_x, size_y, max_height)

    # -------------------------------------------------------------------------------------

    def getSize(self):
        '''
        returns the map size
        @return: (size_x, size_y, max_height) - all of type integer
        '''
        return self.size

    # -------------------------------------------------------------------------------------
    def generateTestTrack(self, player_count):
        
        #the track
        #rand = random.randint(1,1)
        rand = 0
        if rand == 0:
            self.trackpoints = [[0,0,0],[0,500,0],[200,500,0],[250,250,0],[300,0,200],[400,-500,0],[0,-500,0],[0,-1,0]]
            scale = 2
            for i in xrange(len(self.trackpoints)):
                self.trackpoints[i][0] *= scale
                self.trackpoints[i][1] *= scale
                self.trackpoints[i][2] *= scale
        elif rand == 1:
            self.trackpoints = [[0,0,0],[0,500,100],[200,700,200],[500,600,250],[300,0,350],[-300,-300,350],[-700,-200,200],[-500,-100,100],[0,-500,-100],[100,-300,0],[0,-1,0]]
        elif rand == 2:
            self.trackpoints = [[0,0,0],[0,500,0],[0,500,100],[0,0,100]]
        elif rand == 3:
            self.trackpoints = [[0,0,0],[0,500,0],[200,500,0],[200,-500,0],[0,-500,0],[0,-1,0]]
        elif rand == 4:
            looping = Looping(filename="data/road/parts/helix01.xml") # load the looping from file
            looping *= 100      # scale it by 100
            self.trackpoints = []
            for point in looping:   # add them to the list
                self.trackpoints.append(point)
        
        self.curve = HermiteCurve()
        
        #make the list with points
        self.points = []
        for point in self.trackpoints:
            self.points.append(Vec3(point[0],point[1],point[2]))
        
        for point in self.points:
            self.curve.appendCv(HCFREE, point[0],point[1], point[2])
            
        for i in xrange(len(self.points)-1):
##            self.curve.setCvIn(i, Vec3(self.points[i+1]-self.points[i-1]))
##            self.curve.setCvOut(i, Vec3(self.points[i+1]-self.points[i-1]))
            self.curve.setCvIn(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
            self.curve.setCvOut(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
    
        last = len(self.points)-1
        self.curve.setCvIn(last, Vec3(self.points[0]-self.points[-2]))
        self.curve.setCvOut(last, Vec3(self.points[0]-self.points[-2]))
         
         
    def generateTrack(self, player_count):
        '''
        '''
        y = player_count*VEHICLE_DIST
        points = []
        
        points = [ Vec3(0,0,0), Vec3(0, VEHICLE_DIST, 0) ]

        mat = Mat3()
        for i in xrange(10):
            vec = points[-1]-points[-2]
            axis = Vec3(random.randint(0,10), random.randint(0,10), random.randint(0,10))
            mat.setRotateMat(random.randint(0,10), axis)
            vec = mat.xform(vec)
            vec *= 2
            print vec
            
            point = points[-1]+vec
            points.append(point)
            
        self.points = points
        self.curve = HermiteCurve()
        
        #HCCUT
        #HCFREE 
        #HCG1
        #HCSMOOTH
        
        for point in self.points:
            self.curve.appendCv(HCFREE, point[0],point[1], point[2])
            
        for i in xrange(len(self.points)-1):
            self.curve.setCvIn(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
            self.curve.setCvOut(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
    
    # -------------------------------------------------------------------------------------

    def getInterpolatedPoints(self, resolution):
        '''
        
        '''
        pointlist = []
        point = Vec3(0,0,0)
        
        length = self.curve.getMaxT()
        
        xres = length/resolution
        for i in xrange(0,resolution):
            self.curve.getPoint(i*xres, point)
##            print point
            pointlist.append(Vec3(point))
            
        return pointlist

    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    import trackgentest
#    import sys
#    if len(sys.argv) > 1:
#        if sys.argv[1] == "3d":
#            import trackgentest
#    else:
#        m = Track(800,600)
#        m.generateTrack(9)
        #a = m.getInterpolatedPoints(200)
    
##    import main




