# _*_ coding: UTF-8 _*_
##############################################################
## this module contains a class for generating racing tracks
##############################################################

import random
import math
import bitmap24
import nurbstest
import copy
from panda3d.core import *

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

        m = float(y2-y1)/(x2-x1)
        b = y1-m*x1

        return m,b



    # -------------------------------------------------------------------------------------

    def crossesLine(self, other):
        '''
        '''
        m1,b1 = self.get2DLineFunction()
        m2,b2 = other.get2DLineFunction()

        #
        try:
            x = (b2-b1)/(m1-m2)
            y = m1*x+b1
        except:
            return false


        #xa1 =
        #xa2

        #if



    # -------------------------------------------------------------------------------------

    def getDistance(self, other):
        '''
        this method returns the distance between this line and the one given
        by the parameter other
        @param other: (StraightLine) the other line
        '''
        a = self.posvec
        b = other.getPosVec()
        n = self.dirvec.cross(other.getDirVec())

        d = (n[0]*a[0])+(n[1]*a[1])+(n[2]*a[2])

        return abs((n.dot(b)-d)/(n.length()))

    # -------------------------------------------------------------------------------------

    def getAngle(self, other):
        '''
        this method returns the angle between this line and the given one
        @param other: (StraightLine) the other line
        '''
        a = self.dirvec
        b = other.getDirVec()


        return math.degrees(math.acos(a.dot(b)/(a.length()*b.length())))




# -------------------------------------------------------------------------------------

def getAngle(a, b):
    '''
    '''
    return math.degrees(math.acos(a.dot(b)/(a.length()*b.length())))

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------


class Track(object):
    '''
    This class represents a Track
    '''
    def __init__(self, size_x, size_y, max_height=230):
        '''
        the constructor creates an empty track
        '''
        self.setSize(size_x, size_y, max_height)
        self.points = []
        self.curve = None

    # -------------------------------------------------------------------------------------

    def setSize(self, size_x, size_y, max_height=60):
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
        self.__size = (size_x, size_y, max_height)

    # -------------------------------------------------------------------------------------

    def getSize(self):
        '''
        returns the map size
        @return: (size_x, size_y, max_height) - all of type integer
        '''
        return self.__size

    # -------------------------------------------------------------------------------------

    def getCurve(self):
        '''
        '''
        return self.curve


    # -------------------------------------------------------------------------------------

    def generateTrack(self):
        '''
        generates a random track
        '''
        q1 = [] # Quadranten 1 - 4
        q2 = []
        q3 = []
        q4 = []

        q1_size = ((0, 0),(self.__size[0]/2, self.__size[1]/2)) # Abmessungen vom ersten Quadranten ((x1, y1), (x2, y2))
        q2_size = ((self.__size[0]/2, 0),(self.__size[0], self.__size[1]/2))
        q3_size = ((self.__size[0]/2, self.__size[1]/2),(self.__size[0], self.__size[1]))
        q4_size = ((0, self.__size[1]/2),(self.__size[0]/2, self.__size[1]))


        # Die einzelnen Quadranten mit den Major-Points fuellen
        for i in range(4):
            q1.append((random.randint(q1_size[0][0], q1_size[1][0]), random.randint(q1_size[0][1], q1_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q2.append((random.randint(q2_size[0][0], q2_size[1][0]), random.randint(q2_size[0][1], q2_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q3.append((random.randint(q3_size[0][0], q3_size[1][0]), random.randint(q3_size[0][1], q3_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q4.append((random.randint(q4_size[0][0], q4_size[1][0]), random.randint(q4_size[0][1], q4_size[1][1]), random.randint(0, self.__size[2])))


        # Zufaellige Reihenfolge der Quadranten festlegen
        points=[q1,q2,q3,q4]
        random.shuffle(points)

        # Die einzelnen Quadranten in zufaelliger Reihenfolge in die Map einfuegen
        self.points.extend(points[0])
        self.points.extend(points[1])
        self.points.extend(points[2])
        self.points.extend(points[3])


        ####
        #### INTERPOLATION DURCH NURBS


        self.curve = nurbstest.getNurbs(self.points)


#        # ================= TEST ================
#        # === Strecke in Bitmap visualisieren ===
#        # =======================================
#        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)
#
#        last = None
#        for i in(self.points):
#
#            if last == None:
#                last = i
#                continue
#
#            if i[2] != 0:
#                rgb = int((i[2] / 255.0)*200)
#
#            bmp.drawLine(last[0], last[1], i[0], i[1], (rgb,rgb,rgb) )
#
#            last = i
#
#        bmp.drawLine(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
#        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
#
#        bmp.writeBitmap("test1.bmp")
#        # =======================================
#
#
#        # ================= TEST ================
#        # === Strecke in Bitmap visualisieren ===
#        # =======================================
#        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)
#
#        last = None
#
#        point = Vec3(0,0,0)
#
#        for i in xrange(0,1000):
#            curve.getPoint(i*.1, point)
#
#            if last == None:
#                last = copy.deepcopy(point)
#                continue
#
#            if point.getZ() != 0:
#                rgb = int((point.getZ() / 255.0)*200)
#
#            bmp.drawLine(last.getX(), last.getY(), point.getX(), point.getY(), (rgb,rgb,rgb) )
#
#            last = copy.deepcopy(point)
#
#        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
#
#        bmp.writeBitmap("test2.bmp")


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    p1 = Vec3(1,2,3)
    p2 = Vec3(2,3,4)
    p3 = Vec3(5,4,1)

    a = p2-p1
    b = p3-p2

    print getAngle(a,b)
    #m = Track(800,600)
    #m.generateTrack()
    #l1 = StraightLine(Vec3(0,0,0), Vec3(-0.1,0.2,1))
    #l2 = StraightLine(Vec3(0,0,0), Vec3(1,0,0))

    #print l1.getAngle(l2)



