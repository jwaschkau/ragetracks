# _*_ coding: UTF-8 _*_
##############################################################
## this module contains a class for generating racing tracks
##############################################################

import random
import bitmap24
import nurbstest
import copy
from panda3d.core import *

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------


'''
- es gibt 4 Quadranten
- es wird eine Reihenfolge festgelegt, in welcher Reihenfolge die übrigen Quadranten durchfahren werden.
- in jedem Quadranten gibt es 4 "Major-Points", die den groben Streckenverlauf festlegen.
* zwischen den "Major-Points" werden "Minor-Points" interpoliert, die Kurven glätten und zusätzliche Details festlegen.
* Bei Überschneidungen wird eine der beiden Strecken nach oben oder unten verschoben
* seitliche Neigung der Strecke wird festgelegt (besonders in Kurven)
* Tiles werden entlang der Strecke platziert (Straßenstücke, Tunnel usw.)
* Environment (Skybox, fliegende Deko, Wolkenkratzer usw.) wird geladen
'''

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
        self.__points = []

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


        # Die einzelnen Quadranten mit den Major-Points füllen
        for i in range(4):
            q1.append((random.randint(q1_size[0][0], q1_size[1][0]), random.randint(q1_size[0][1], q1_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q2.append((random.randint(q2_size[0][0], q2_size[1][0]), random.randint(q2_size[0][1], q2_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q3.append((random.randint(q3_size[0][0], q3_size[1][0]), random.randint(q3_size[0][1], q3_size[1][1]), random.randint(0, self.__size[2])))

        for i in range(4):
            q4.append((random.randint(q4_size[0][0], q4_size[1][0]), random.randint(q4_size[0][1], q4_size[1][1]), random.randint(0, self.__size[2])))


        # Zufällige Reihenfolge der Quadranten festlegen
        points=[q1,q2,q3,q4]
        random.shuffle(points)

        # Die einzelnen Quadranten in zufälliger Reihenfolge in die Map einfügen
        self.__points.extend(points[0])
        self.__points.extend(points[1])
        self.__points.extend(points[2])
        self.__points.extend(points[3])


        # ================= TEST ================
        # === Strecke in Bitmap visualisieren ===
        # =======================================
        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)

        last = None
        for i in(self.__points):

            if last == None:
                last = i
                continue

            if i[2] != 0:
                rgb = int((i[2] / 255.0)*200)

            bmp.drawLine(last[0], last[1], i[0], i[1], (rgb,rgb,rgb) )

            last = i

        bmp.drawLine(self.__points[0][0], self.__points[0][1], self.__points[-1][0], self.__points[-1][1])
        bmp.drawDigit(0, self.__points[0][0], self.__points[0][1], (255,0,0))

        bmp.writeBitmap("test1.bmp")
        # =======================================




        ####
        #### INTERPOLATION DURCH NURBS


        curve = nurbstest.getNurbs(self.__points)

        # ================= TEST ================
        # === Strecke in Bitmap visualisieren ===
        # =======================================
        bmp = bitmap24.Bitmap24("", self.__size[0]+1, self.__size[1]+1)

        last = None

        point = Vec3(0,0,0)

        for i in xrange(0,1000):
            curve.getPoint(i*.1, point)

            if last == None:
                last = copy.deepcopy(point)
                continue

            if point.getZ() != 0:
                rgb = int((point.getZ() / 255.0)*200)

            bmp.drawLine(last.getX(), last.getY(), point.getX(), point.getY(), (rgb,rgb,rgb) )

            last = copy.deepcopy(point)

        #bmp.drawLine(self.__points[0][0], self.__points[0][1], self.__points[-1][0], self.__points[-1][1])
        bmp.drawDigit(0, self.__points[0][0], self.__points[0][1], (255,0,0))

        bmp.writeBitmap("test2.bmp")


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

m = Track(800,600)
m.generateTrack()
