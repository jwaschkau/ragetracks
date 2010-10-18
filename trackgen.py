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

MIN_Z_DIST = 100
MAX_Z_DIST = 500
MIN_DIST = 90
VEHICLE_DIST = 50
MIN_ANGLE = 40

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
    
    def generateTrack(self, player_count):
        '''
        '''
        points = [ Vec3(0,0,0), Vec3(0, VEHICLE_DIST, 0) ]
        crossings = []
        
        # we define 4 quadrants to ensure that the track does run through the whole map
        quadrants = []
        quadrants.append( (Vec2(0, 0), Vec2(self.size.getX()/2, self.size.getY()/2)) )
        quadrants.append( (Vec2(self.size.getX()/2, self.size.getY()/2), Vec2(self.size.getX(), self.size.getY())) )
        quadrants.append( (Vec2(self.size.getX()/2, 0), Vec2(self.size.getX(), self.size.getY()/2)) )
        quadrants.append( (Vec2(0, self.size.getY()/2), Vec2(self.size.getX()/2, self.size.getY())) )
        random.shuffle(quadrants) # the order of the quadrants is randomly chosen

        # generate points quadrant per quadrant
        for quadrant in quadrants:
            # generate 3 points per quadrant
            for i in xrange(3):
                point_ok = False
                points_not_ok = 0
                
                # as long as the point isn't ok, look for another one
                while not point_ok:
                    # if more than 10 points are thrown away, recalculate the last one                    
                    if points_not_ok > 10:
                        del points[-1]

                    # get a point
                    point = Vec3(random.randint(quadrant[0].getX(), quadrant[1].getX()), random.randint(quadrant[0].getY(), quadrant[1].getY()), 0)
                    
                    # define a line for cheching its angle to the last line and for crossing points with other Lines
                    line = Line(point, points[-1])

                    if line.getAngle(Line(points[-2], points[-1])) > MIN_ANGLE and (point-points[-1]).length() > MIN_DIST: # check for length
                        point_ok = True
                    
                    points_not_ok += 1
                
                # check for intersection 
                ## this seems to work, but not for the last points, which are added after this loop
                for j in xrange(len(points)-1):
                    if line.crossesLine(Line(points[j], points[j+1])):
                        crossings.append( (j, len(points)-1) )
                    
                points.append(point)
                self._notify = DirectNotify().newCategory("SplitScreen")
        self._notify.debug("Crossings: %s" %(crossings))

        points.append(Vec3(0,(((player_count-1)/4)+2)*-VEHICLE_DIST, 0))
        points.append(Vec3(0,-VEHICLE_DIST, 0))
        
        
        # add some height
        for i in xrange(2,len(points)-2):
            points[i][2] = random.randint(points[i-1][2]-MAX_Z_DIST, points[i-1][2]+MAX_Z_DIST)
            
        # adjust the height
        for cross in crossings:
            absdist = abs(points[cross[1]][2] - points[cross[0]][2])
            dist = points[cross[1]][2] - points[cross[0]][2]
            sign = absdist / dist
            if absdist < MIN_Z_DIST:
                points[cross[1]][2] += (MIN_Z_DIST-absdist)*sign
                points[cross[1]+1][2] += (MIN_Z_DIST-absdist)*sign
            
        
        self.points = points
        self.curve = HermiteCurve()
        
        #HCCUT
        #HCFREE 
        #HCG1
        #HCSMOOTH
        
        for point in self.points:
            self.curve.appendCv(HCFREE, point[0],point[1], 0)
            
        for i in xrange(len(self.points)-1):
##            self.curve.setCvIn(i, Vec3(self.points[i+1]-self.points[i-1]))
##            self.curve.setCvOut(i, Vec3(self.points[i+1]-self.points[i-1]))
            self.curve.setCvIn(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
            self.curve.setCvOut(i, Vec3(self.points[i+1]-self.points[i-1])*.5)
    
        last = len(self.points)-1
        self.curve.setCvIn(last, Vec3(self.points[0]-self.points[-2]))
        self.curve.setCvOut(last, Vec3(self.points[0]-self.points[-2]))
        
        
        
        if __name__ == "__main__":
            # ================= TEST ================
            # === Strecke in Bitmap visualisieren ===
            # =======================================
            bmp = bitmap24.Bitmap24("", int(self.size[0]+1), int(self.size[1]+1))

            last = None
            for i in(self.points):
                if last == None:
                    last = i
                    continue

                #if i[2] != 0:
                #    rgb = int((float(i[2])/self.size[2])*200)

                bmp.drawLine(last[0], last[1], i[0], i[1], (0,0,0) )

                last = i
            
            count = 0
            for i in(self.points):
                if count < 10:
                    bmp.drawDigit(count, i[0],i[1],(0,0,255))
                bmp.drawPixel(i[0], i[1], (255,0,0) )
                count += 1

            #bmp.drawLine(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
            bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
            bmp.drawPixel(self.points[-2][0], self.points[-2][1], (0,255,0))
            bmp.writeBitmap("test1.bmp")
            # =======================================
            
            
            
            
            # ================= TEST ================
            # === Strecke in Bitmap visualisieren ===
            # =======================================
            bmp = bitmap24.Bitmap24("", int(self.size[0]+1), int(self.size[1]+1))

            last = None

            resolution = 100
            
            point = Vec3(0,0,0)
            length = self.curve.getMaxT()

            for i in xrange(0,resolution):
                self.curve.getPoint(i*(length/resolution), point)

                if last == None:
                    last = copy.deepcopy(point)
                    continue

                bmp.drawLine(last.getX(), last.getY(), point.getX(), point.getY(), (0,0,0) )
                #bmp.writeBitmap("test/"+str(i)+".bmp")

                last = copy.deepcopy(point)

            bmp.drawDigit(0, self.points[0][0], self.points[0][1], (255,0,0))
            bmp.drawPixel(self.points[-2][0], self.points[-2][1], (0,255,0))

            bmp.writeBitmap("test2.bmp")
    
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
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "3d":
        import trackgentest
    else:
        m = Track(800,600)
        m.generateTrack(9)
        #a = m.getInterpolatedPoints(200)
    
##    import main




