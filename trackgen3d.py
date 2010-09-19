# _*_ coding: UTF-8 _*_
##############################################################
## this module contains a class for generating racing tracks
##############################################################

#Input is a Tupel with Tupel of (x,y,z)
#They are the midpoints of the Street

from panda3d.core import * 
from trackgen import Track

class Track3d(object):
    varthickness = []  #Generate the Vector for thickness of the road

    def __init__(self, track_points, street_data):
        '''
        '''
        
        for i in range(len(track_points)-1):
            if i == 0:
                self.varthickness.append(self.calcTheVector(track_points[len(track_points)-1],track_points[i],track_points[i+1]))
                continue
            self.varthickness.append(self.calcTheVector(track_points[i-1],track_points[i],track_points[i+1]))
        self.varthickness.append(self.calcTheVector(track_points[len(track_points)-2],track_points[len(track_points)-1],track_points[0]))
        
        #Normalizing the Vector
        for i in self.varthickness:
            i.normalize()
        #Creating the Vertex
        ##TODO
        #Conect the Vertex
        ##TODO
        #?Show the Mesh
        ##TODO
        ##Debugprint
        print self.varthickness
        #return List
        #return self.varthickness

    def calcTheVector(self, pre, now, past):
        vector1 = (pre[0] - now[0], pre[1] - now[1])
        vector2 = (past[0] - now[0], past[1] - now[1])
        high = pre[2] - past[2]
        return Vec3(((vector1[1] + vector2[1])/2.0),((vector1[0] + vector2[0])/2.0), high)

    def getVarthickness(self):
        return self.varthickness

#Test
tuple1 = ((1.0,2.0,3.0),(3.0,4.0,5.0),(6.0,4.0,2.0),(8.0,3.0,6.0),(4.0,7.0,2.0))
tuple2 = ((-2.0, -3.0, 0.0),(1.0, -5.0, 0.0),(4.0, -4.0, 0.0),(6.0, 0.0, 0.0),(3.0, 4.0, 0.0),(-2.0, 6.0, 0.0),(-7.0, 3.0, 0.0),(-8.0, -2.0, 0.0))
tuple3 = ((10.0,10.0,0.0),(10.0,-10.0,0.0),(-10.0,-10.0,0.0),(-10.0,10.0,0.0))

#Test with real Data
m = Track(800,600)
m.generateTrack()
tuple4 = m.getInterpolatedPoints(100)
print tuple4
streetData = (Vec2(1,1),Vec2(5,1),Vec2(6,2))

Track3d(tuple4, streetData)


