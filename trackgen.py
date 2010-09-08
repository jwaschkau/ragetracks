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


MIN_DIST = 20

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
            m = float(y2-y1)/(x2-x1)
        except:
            m = 0
        b = y1-m*x1

        return m,b


    # -------------------------------------------------------------------------------------

    def getZbyXY(self,x,y):
        '''
        '''
        z = self.posvec[2]+(self.dirvec[2]*((float(x)-self.posvec[0])/self.dirvec[0]))
        z2 = self.posvec[2]+(self.dirvec[2]*((float(x)-self.posvec[1])/self.dirvec[1]))
        #try:
        return z
        #except:
        #    return self.posvec[2]+(self.dirvec[2]*((x-self.posvec[1])/(self.dirvec[1])))

    # -------------------------------------------------------------------------------------

    def crossesLine(self, other):
        '''
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


        xa1 = self.posvec[0]
        xa2 = self.posvec2[0]
        ya1 = self.posvec[1]
        ya2 = self.posvec2[1]

        xfits = False
        yfits = False

        # x must be between the first and second x value of one ofthe lines
        if xa1 < x and xa2 > x:
            xfits = True
        elif xa1 > x and xa2 < x:
            xfits = True

        # if x doesn't fit, it doesn't matter, if y fits
        if xfits:
            # y must also be between the first and second y value of one of the lines
            if ya1 < y and ya2 > y:
                yfits = True
            elif ya1 > y and ya2 < y:
                yfits = True
            else:
                yfits = False

            # if y fits, the graphs collide in 2d space and we have to check the 3d distance
            if yfits:
                z1 = self.getZbyXY(x,y)
                z2 = other.getZbyXY(x,y)
#                print z1, z2
                print x,y
                dist = abs(z2-z1)

                #if dist < MIN_DIST:
                #    return True
                #else:
                #    return False
                return False
            else:
                return False

        else:
            return False

#    # -------------------------------------------------------------------------------------
#
#    def crossesLine2D(self, other):
#        '''
#        @return: (bool) returns True if the line self and other have a crossing point in 2d space (x-y)
#        '''
#        m1,b1 = self.get2DLineFunction()
#        m2,b2 = other.get2DLineFunction()
#
#        # if this fails, the lines are parallel
#        try:
#            x = (b2-b1)/(m1-m2)
#            y = m1*x+b1
#        except:
#            return False
#
#
#        xa1 = self.posvec[0]
#        xa2 = self.posvec2[0]
#        ya1 = self.posvec[1]
#        ya2 = self.posvec2[1]
#
#        xfits = False
#        yfits = False
#
#        # x must be between the first and second x value of one ofthe lines
#        if xa1 < x and xa2 > x:
#            xfits = True
#        elif xa1 > x and xa2 < x:
#            xfits = True
#
#        # if x doesn't fit, it doesn't matter, if y fits
#        if xfits:
#            # y must also be between the first and second y value of one of the lines
#            if ya1 < y and ya2 > y:
#                yfits = True
#            elif ya1 > y and ya2 < y:
#                yfits = True
#            else:
#                yfits = False
#
#            # if y fits, the graphs collide in 2d space
#            return yfits
#
#        else:
#            return False
#
#
#    # -------------------------------------------------------------------------------------
#
#    def getDistance(self, other):
#        '''
#        this method returns the distance between this line and the one given
#        by the parameter other
#        @param other: (StraightLine) the other line
#        '''
#        a = self.posvec
#        b = other.getPosVec()
#        n = self.dirvec.cross(other.getDirVec())
#
#        d = (n[0]*a[0])+(n[1]*a[1])+(n[2]*a[2])
#
#        try:
#            return abs((n.dot(b)-d)/(n.length()))
#        except:
#            vec = b-a
#            return vec.length()

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
# -------------------------------------------------------------------------------------
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
    def __init__(self, size_x, size_y, max_height=2300):
        '''
        the constructor creates an empty track
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

    def generatePoints(self):
        '''
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

    # -------------------------------------------------------------------------------------

    def generateTrack(self):
        '''
        generates a random track --> sets the attribute self.curve
        '''
        track_is_ok = False

        # generate new tracks until a track seems to be allright
        while not track_is_ok:
            self.generatePoints()
            max_index = len(self.points)-1
            track_is_ok = True

            # check each line (between two points) for collisions
            for i in xrange(max_index):
                for j in xrange(i+1, max_index-2):
                    line1 = StraightLine(self.points[i], self.points[j])
                    line2 = StraightLine(self.points[j+1], self.points[j+2])
                    # if the lines cross / are too near, we have to generate a new map
                    if line1.crossesLine(line2):
                        track_is_ok = False


        ####
        #### INTERPOLATION DURCH NURBS
        self.curve = nurbstest.getNurbs(self.points)


        # ================= TEST ================
        # === Strecke in Bitmap visualisieren ===
        # =======================================
        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)

        last = None
        for i in(self.points):

            if last == None:
                last = i
                continue

            if i[2] != 0:
                rgb = int((float(i[2])/self.__size[2])*200)

            bmp.drawLine(last[0], last[1], i[0], i[1], (rgb,rgb,rgb) )

            last = i

        bmp.drawLine(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))

        bmp.writeBitmap("test1.bmp")
        # =======================================


        # ================= TEST ================
        # === Strecke in Bitmap visualisieren ===
        # =======================================
        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)

        last = None

        point = Vec3(0,0,0)

        for i in xrange(0,1000):
            self.curve.getPoint(i*.1, point)

            if last == None:
                last = copy.deepcopy(point)
                continue

            if point.getZ() != 0:
                rgb = int((float(point.getZ())/self.__size[2])*200)

            bmp.drawLine(last.getX(), last.getY(), point.getX(), point.getY(), (rgb,rgb,rgb) )

            last = copy.deepcopy(point)

        bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))

        bmp.writeBitmap("test2.bmp")


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

    #l1 = StraightLine(Vec3(1,1,200), Vec3(3,20,200))
    #l2 = StraightLine(Vec3(1,1,300), Vec3(3,3,300))
    #print l1.getAngle(l2)



