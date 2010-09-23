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


MIN_DIST = 30

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------


'''
- es gibt 4 Quadranten
- es wird eine Reihenfolge festgelegt, in welcher Reihenfolge die uebrigen Quadranten durchfahren werden.
- in jedem Quadranten gibt es 4 "Major-Points", die den groben Streckenverlauf festlegen.
* zwischen den "Major-Points" werden "Minor-Points" interpoliert, die Kurven glaetten und zusaetzliche Details festlegen.
* Bei Ueberschneidungen wird eine der beiden Strecken nach oben oder unten verschoben
* seitliche Neigung der Strecke wird festgelegt (besonders in Kurven)
* Tiles werden entlang der Strecke platziert (Strassenstuecke, Tunnel usw.)
* Environment (Skybox, fliegende Deko, Wolkenkratzer usw.) wird geladen
'''
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

def getAngle(a, b):
    '''
    @param a: (Vec3) the first vector
    @param b: (Vec3) the second vector
    @return: (float) the angle between the two vectors a and b
    '''
    return math.degrees(math.acos(a.dot(b)/(a.length()*b.length())))

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class StraightLine(object):
    '''
    This class implements a 3-dimensional straight line (in German: Gerade)
    '''
    def __init__(self, vec1, vec2):
        '''
        @param vec1: (Vec3) the first vector to define the line (not a directional vector, but a positional one)
        @param vec2: (Vec3) the second vector to define the line (not a directional vector, but a positional one)
        the directional vector is computed automatically
        '''

        if type(vec1) == tuple:
            vec1 = Vec3(vec1[0], vec1[1], vec1[2])
        if type(vec2) == tuple:
            vec2 = Vec3(vec2[0], vec2[1], vec2[2])

        if type(vec1) != type(vec2) != Vec3:
            raise TypeError("vec1 and vec2 have to be of type 'Vec3' or 'tuple'")

        self.posvec = vec1
        self.posvec2 = vec2
        self.dirvec = vec2-vec1

    # -------------------------------------------------------------------------------------

    def getPosVec(self):
        '''
        @return: (Vec3) returns the position vector of the line
        '''
        return self.posvec

    # -------------------------------------------------------------------------------------

    def getPosVec2(self):
        '''
        @return: (Vec3) returns the second position vector of the line
        '''
        return self.posvec2

    # -------------------------------------------------------------------------------------

    def getDirVec(self):
        '''
        @return: (Vec3) returns the direction vector of the line
        '''
        return self.dirvec

    # -------------------------------------------------------------------------------------

    def get2DLineFunction(self):
        '''
        @return: (tuple) the mathematical function constants (m, b) [m -> slope, b -> y axis collision]
        '''
        x1 = self.posvec[0]
        y1 = self.posvec[1]

        x2 = self.posvec2[0]
        y2 = self.posvec2[1]

        try:
            m = (y2-y1)/(x2-x1)
        except:
            m = 0

        b = y1-(m*x1)

        return m,b

    # -------------------------------------------------------------------------------------

    def getZbyXY(self,x,y):
        '''
        @param x: (float) / (int) x-value
        @param y: (float) / (int) y-value
        @return: (float) the z-value at the given x and y components
        '''
        try:
            z = self.posvec[2]+(self.dirvec[2]*((float(x)-self.posvec[0])/self.dirvec[0])) # !!! sometimes zero division
        except:
            try:
                z = self.posvec[2]+(self.dirvec[2]*((float(y)-self.posvec[1])/self.dirvec[1])) # !!! sometimes zero division
            except:
                raise StandardError("Sorry, but this error will cause the end of the world")
        return z

    # -------------------------------------------------------------------------------------

    def crossesLine(self, other):
        '''
        @param other: (StaightLine) the other line to check if it crosses this one
        @return: (bool) returns True if the line self and other have a crossing point in 2d space (x-y) and are very near in 3d space
        '''
        m1,b1 = self.get2DLineFunction()
        m2,b2 = other.get2DLineFunction()

        # if this fails, the lines are parallel
        try:
            x = (b2-b1)/(m1-m2)
            y = m1*x+b1
        except:
            return False

        a1x = self.posvec[0]
        a1y = self.posvec[1]
        a2x = self.posvec2[0]
        a2y = self.posvec2[1]

        # if the crossing point is on the lines inside the interval of the two given points
        # it must be also on the other line
        if ( (a1x < x < a2x) or (a1x > x > a2x) ) and ( (a1y < y < a2y) or (a1y > y > a2y) ):

            # calculate the distance between the lines:
            try:
                self_z = self.getZbyXY(x,y)
                other_z = other.getZbyXY(x,y)

                dist = abs(other_z - self_z)
            except:
                return True

            # if the distance is smaller than the minimum distance, we can't use the map
            if dist < MIN_DIST:
                return True
            else:
                return False
        else:
            return False


    # -------------------------------------------------------------------------------------

    def getAngle(self, other):
        '''
        @param other: (StraightLine) the other line to determine the angle to
        @return: (float) the angle between this line and the other one
        '''
        a = self.dirvec
        b = other.getDirVec()


        return getAngle(a, b)


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
        self.size = (size_x, size_y, max_height)

    # -------------------------------------------------------------------------------------

    def getSize(self):
        '''
        returns the map size
        @return: (size_x, size_y, max_height) - all of type integer
        '''
        return self.size

    # -------------------------------------------------------------------------------------

    def getCurve(self):
        '''
        the returned curve is an interpolated one, computed out of the randomly generated Points
        @return: (NurbsCurve) the interpolated curve [a panda class]
        '''
        return self.curve

    # -------------------------------------------------------------------------------------

    def generatePoints(self):
        '''
        this method generates some random points and stores them in a member variable
        -> sets the attribute self.points
        '''
        self.points = []
        # we have make four parts out of our coordinate system, so that every Part has got a piece of road
        q1 = []
        q2 = []
        q3 = []
        q4 = []

        # size of the parts
        q1_size = ((0, 0),(self.size[0]/2, self.size[1]/2))
        q2_size = ((self.size[0]/2, 0),(self.size[0], self.size[1]/2))
        q3_size = ((self.size[0]/2, self.size[1]/2),(self.size[0], self.size[1]))
        q4_size = ((0, self.size[1]/2),(self.size[0]/2, self.size[1]))


        # fill the parts with random points
        for i in range(4):
            q1.append(Vec3(random.randint(q1_size[0][0], q1_size[1][0]), random.randint(q1_size[0][1], q1_size[1][1]), random.randint(0, self.size[2])))

        for i in range(4):
            q2.append(Vec3(random.randint(q2_size[0][0], q2_size[1][0]), random.randint(q2_size[0][1], q2_size[1][1]), random.randint(0, self.size[2])))

        for i in range(4):
            q3.append(Vec3(random.randint(q3_size[0][0], q3_size[1][0]), random.randint(q3_size[0][1], q3_size[1][1]), random.randint(0, self.size[2])))

        for i in range(4):
            q4.append(Vec3(random.randint(q4_size[0][0], q4_size[1][0]), random.randint(q4_size[0][1], q4_size[1][1]), random.randint(0, self.size[2])))


        # the parts are randomly patched together
        points=[q1,q2,q3,q4]
        random.shuffle(points)

        # and stored in a member variable
        self.points.extend(points[0])
        self.points.extend(points[1])
        self.points.extend(points[2])
        self.points.extend(points[3])
        
        dir = self.points[1] - self.points[0]
        dir = dir.normalize()
        self.points.append(self.points[0]+(dir*(-200)))
        self.points.append(Vec3(self.points[0]))

    # -------------------------------------------------------------------------------------

    def generateTrack(self):
        '''
        generates a curve out of the points
        -> sets the attribute self.curve
        '''
        track_is_ok = False

        n = 0

        # generate new tracks until a track seems to be allright
        while not track_is_ok:
            self.generatePoints()
            max_index = len(self.points)-1
            track_is_ok = True

            # check each line (between two points) for collisions
            for i in xrange(max_index):
                if not track_is_ok:
                    break
                for j in xrange(i+1, max_index-2):
                    line1 = StraightLine(self.points[i], self.points[j])
                    line2 = StraightLine(self.points[j+1], self.points[j+2])
                    # if the lines cross / are too near, we have to generate a new map
                    if line1.crossesLine(line2):
                        track_is_ok = False
                        n += 1
                        break
                        #print i
                        
        print "times of street generaton", n


        # INTERPOLATION DURCH NURBS
        self.curve = NurbsCurve()
        for point in self.points:
            self.curve.appendCv(point[0],point[1],point[2])
        self.curve.recompute()
        tangent = Vec3(0,0,0)
        self.curve.getTangent(0, tangent)
        self.curve.adjustPoint(0, self.points[-1][0], self.points[-1][1], self.points[-1][2])
        self.curve.adjustPt(self.curve.getMaxT(), self.points[-1][0], self.points[-1][1], self.points[-1][2], tangent[0], tangent[1], tangent[2])
        self.curve.recompute()
    
    def genStart(self, player):
        print player
        startPos = []
        for i in range(player):
            startPos.append(Vec3(0,(10*i),0))
        startPos.append(Vec3(0,3+(10*(player-1)),0))
        for i in self.points:
            startPos.append(i)
        print startPos
        self.points = startPos

##        # ================= TEST ================
##        # === Strecke in Bitmap visualisieren ===
##        # =======================================
##        bmp = bitmap24.Bitmap24("", self.size[0]+1, self.size[1]+1)
##
##        last = None
##        for i in(self.points):
##
##            if last == None:
##                last = i
##                continue
##
##            if i[2] != 0:
##                rgb = int((float(i[2])/self.size[2])*200)
##
##            bmp.drawLine(last[0], last[1], i[0], i[1], (rgb,rgb,rgb) )
##
##            last = i
##
##        #bmp.drawLine(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
##        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
##        bmp.drawPixel(self.points[-2][0], self.points[-2][1], (0,255,0))
##        bmp.writeBitmap("test1.bmp")
##        # =======================================
##
##
##        # ================= TEST ================
##        # === Strecke in Bitmap visualisieren ===
##        # =======================================
##        bmp = bitmap24.Bitmap24("", self.size[0]+1, self.size[1]+1)
##
##        last = None
##
##        resolution = 100
##        
##        point = Vec3(0,0,0)
##        length = self.curve.getMaxT()
##        print length
##
##        for i in xrange(0,resolution):
##            self.curve.getPoint(i*(length/resolution), point)
##
##            if last == None:
##                last = copy.deepcopy(point)
##                continue
##
##            if point.getZ() != 0:
##                rgb = int((float(point.getZ())/self.size[2])*200)
##
##            bmp.drawLine(last.getX(), last.getY(), point.getX(), point.getY(), (rgb,rgb,rgb) )
##            #bmp.writeBitmap("test/"+str(i)+".bmp")
##
##            last = copy.deepcopy(point)
##
##        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
##        bmp.drawPixel(self.points[-2][0], self.points[-2][1], (0,255,0))
##
##        bmp.writeBitmap("test2.bmp")
        
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
            pointlist.append(Vec3(point))
            
        return pointlist

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
#    p1 = Vec3(1,2,3)
#    p2 = Vec3(2,3,4)
#    p3 = Vec3(5,4,1)
#
#    a = p2-p1
#    b = p3-p2
#
#    print getAngle(a,b)
    m = Track(800,600)
    m.generateTrack()
    a = m.getInterpolatedPoints(200)
    #print a
    #print len(a)

    #l1 = StraightLine(Vec3(1,1,200), Vec3(3,20,200))
    #l2 = StraightLine(Vec3(1,1,300), Vec3(3,3,300))
    #print l1.getAngle(l2)



