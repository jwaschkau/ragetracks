# _*_ coding: UTF-8 _*_
## TEST MODULE FOR AN INTERPOLATED CURVE
## AUTHOR: CARSTEN PFEFFER
import wx

import math

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Vector3(object):
    '''
    '''
    def __init__(self, x, y, z):
        '''
        @param x: (int) or (float) x coordinate of the vector
        @param y: (int) or (float) y coordinate of the vector
        @param z: (int) or (float) z coordinate of the vector
        '''
        if type(x) != int and type(x) != float:
            raise TypeError("x has to be of type int or float!")

        if type(y) != int and type(y) != float:
            raise TypeError("y has to be of type int or float!")

        if type(z) != int and type(z) != float:
            raise TypeError("z has to be of type int or float!")

        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

    # -----------------------------------------------------------------

    def getNormalized(self):
        '''
        '''
        return self / len(self)

    # -----------------------------------------------------------------

    def __str__(self):
        '''
        @return: (str) sting representation of the Vector "Vector3(x, y, z)"
        '''
        return "Vector3(%f, %f, %f)" % (self._x, self._y, self._z)

    # -----------------------------------------------------------------

    def __add__(self, other):
        '''
        @param other: (Vector3) the vector which should be added to self
        @return: (Vector3) the returning vector of self+other
        '''
        if type(other) != Vector3:
            raise TypeError("a Vector3 can only be added to another Vector3")
        return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)

    # -----------------------------------------------------------------

    def __sub__(self, other):
        '''
        @param other: (Vector3) the vector which should be subtracted from self
        @return: (Vector3) the returning vector of self-other
        '''
        if type(other) != Vector3 and type(other):
            raise TypeError("a Vector3 can only be subtracted by another Vector3")
        return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)

    # -----------------------------------------------------------------

    def __mul__(self, other):
        '''
        @param other: (int) or (float) the scalar with which self should be multiplicated
        @return: (Vector3) the returning vector of self*other
        '''
        if type(other) != int and type(other) != float:
            raise TypeError("a Vector3 can only be multiplicated with a scalar (int or float)")
        return Vector3(self.x*other, self.y*other, self.z*other)

    # -----------------------------------------------------------------

    def __div__(self, other):
        '''
        @param other: (int) or (float) the scalar through which self should be divided
        @return: (Vector3) the returning vector of self/other
        '''
        if type(other) != int and type(other) != float:
            raise TypeError("a Vector3 can only be divided through a scalar (int or float)")
        return Vector3(self.x/other, self.y/other, self.z/other)

    # -----------------------------------------------------------------

    def __getitem__(self, index):
        '''
        @param index: (int) index to a coordinate; 0 means x, 1 means y and 2 means z
        @return: (float) item x, y or z
        '''
        if type(index) != int:
            raise TypeError("index has to be of type int")
        if index > 2 or index < 0:
            raise IndexError("index has to be in range(0,3)")

        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            return self._z

    # -----------------------------------------------------------------

    def __len__(self):
        '''
        @return: (float) returns the length of the vector
        '''
        return math.sqrt((self._x**2)+(self._y**2)+(self._z**2))

    # -----------------------------------------------------------------

    def getLength(self):
        '''
        @return: (float) returns the length of the vector
        '''
        return self.__len__()

    # -----------------------------------------------------------------

    def getX(self):
        '''
        @return: (float) x coordinate of the vector
        '''
        return self._x

    # -----------------------------------------------------------------

    def setX(self, x):
        '''
        @param x: (int) or (float) x coordinate of the vector
        '''
        if type(x) != int and type(x) != float:
            raise TypeError("x has to be of type int or float!")
        self._x = float(x)

    # -----------------------------------------------------------------

    def getY(self):
        '''
        @return: (float) y coordinate of the vector
        '''
        return self._y

    # -----------------------------------------------------------------

    def setY(self, y):
        '''
        @param x: (int) or (float) x coordinate of the vector
        '''
        if type(y) != int and type(y) != float:
            raise TypeError("y has to be of type int or float!")
        self._y = float(y)

    # -----------------------------------------------------------------

    def getZ(self):
        '''
        @return: (float) z coordinate of the vector
        '''
        return self._z

    # -----------------------------------------------------------------

    def setZ(self, z):
        '''
        @param z: (int) or (float) z coordinate of the vector
        '''
        if type(z) != int and type(z) != float:
            raise TypeError("z has to be of type int or float!")
        self._z = float(z)

    # -----------------------------------------------------------------

    x = property(getX, setX)
    y = property(getY, setY)
    z = property(getZ, setZ)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class TangentPoint(Vector3):
    '''
    '''
    def __init__(self, x, y, z, in_t=None, out_t=None):
        '''
        '''
        Vector3.__init__(self, x,y,z)

        if in_t == None:
            self._in_tangent = Vector3(0,0,0)
        else:
            self.setInTangent(in_t)

        if out_t == None:
            self._out_tangent = Vector3(0,0,0)
        else:
            self.setOutTangent(out_t)

    # -----------------------------------------------------------------

    def __add__(self, other):
        '''
        @param other: (Vector3 or TangentPoint) the vector which should be added to self
        @return: (Vector3) the returning vector of self+other
        '''
        if type(other) != Vector3 and type(other) != TangentPoint:
            raise TypeError("a TangentPoint can only be added to another TangentPoint or Vector3")
        return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)

    # -----------------------------------------------------------------

    def __sub__(self, other):
        '''
        @param other: (Vector3 TangentPoint) the vector which should be subtracted from self
        @return: (Vector3) the returning vector of self-other
        '''
        if type(other) != Vector3 and type(other) != TangentPoint:
            raise TypeError("a Vector3 can only be subtracted by another TangentPoint or Vector3")
        return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)

    # -----------------------------------------------------------------

    def getInTangent(self):
        '''
        @return: (Vector3) the incoming tangent
        '''
        return self._in_tangent

    # -----------------------------------------------------------------

    def setInTangent(self, in_t):
        '''
        sets the incoming tangent
        @param in_t: (Vector3) the incoming tangent
        '''
        if type(in_t) != Vector3:
            raise TypeError("in_tangent has to be of type Vector3")
        self._in_tangent = in_t

    # -----------------------------------------------------------------

    def getOutTangent(self):
        '''
        @return: (Vector3) the outgoing tangent
        '''
        return self._out_tangent

    # -----------------------------------------------------------------

    def setOutTangent(self, out_t):
        '''
        sets the outgoing tangent
        @param out_t: (Vector3) the outgoing tangent
        '''
        if type(out_t) != Vector3:
            raise TypeError("out_tangent has to be of type Vector3")
        self._out_tangent = out_t

    # -----------------------------------------------------------------

    in_tangent = property(getInTangent, setInTangent)
    out_tangent = property(getOutTangent, setOutTangent)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class InterpolationCurve(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        self.points = []

        self.points.append(TangentPoint(200,300,0))
        self.points.append(TangentPoint(300,500,0))
        self.points.append(TangentPoint(900,100,0))
        self.points.append(TangentPoint(500,600,0))
        self.points.append(TangentPoint(360,200,0))

        self.computeTangents()

    # -----------------------------------------------------------------

    def computeTangents(self):
        '''
        '''
        for i in xrange(len(self.points)-1):
            self.points[i].in_tangent = self.points[i-1]-self.points[i+1]
            self.points[i].out_tangent = self.points[i+1]-self.points[i-1]

        self.points[-1].in_tangent = self.points[-2]-self.points[0]
        self.points[-1].out_tangent = self.points[0]-self.points[-2]

    # -----------------------------------------------------------------

    def __len__(self):
        '''
        '''
        length = 0
        for i in xrange(len(self.points)):
            length += len(self.points[i]-self.points[i-1])

        return length

    # -----------------------------------------------------------------

    def getPt(self, percent):
        '''
        '''
        length = self.__len__()     # get the length of the curve
        pos = length/100.0*percent    # calculate the position out of the percentage

        poslen = 0                  # go through the points
        n = None
        for i in xrange(len(self.points)-1):
            poslen += len(self.points[i+1]-self.points[i])

            # if we are in the right segment
            if poslen > pos:
                poslen -= len(self.points[i+1]-self.points[i])
                n = i
                break
            # if we hit exactly the point
            elif poslen == pos:
                return self.points[i]

        if n == None:
            n = -1
            #poslen += len(self.points[0]-self.points[-1])

        ####
        ####

        point1 = self.points[n]
        point2 = self.points[n+1]

        relative_dist = len(point2-point1)
        relative_pos = pos-poslen

        factor = relative_pos/relative_dist

        richtungsvektor = (point1.in_tangent*(1-factor)) + (point2.out_tangent*factor)
        #richtungsvektor = richtungsvektor.getNormalized()
        output_point = point1 + (richtungsvektor*factor)
        print relative_dist, factor
        return output_point


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Editor(wx.Frame):
    '''
    '''
    def __init__(self):
        wx.Frame.__init__(self, None, title="Visualisaton", size=wx.Size(1000,700))
        self.canvas = Canvas(self)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Canvas(wx.Window):
    '''
    '''
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(255,255,255))

        self.curve = InterpolationCurve()

        self.Bind(wx.EVT_PAINT, self.onPaint)

    # -----------------------------------------------------------------

    def drawLines(self, dc):
        '''
        '''
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))

        for i in xrange(len(self.curve.points)):
            x1,y1,z = self.curve.points[i-1]
            x2,y2,z = self.curve.points[i]

            dc.DrawLine(x1,y1, x2,y2)


    # -----------------------------------------------------------------

    def drawTangents(self, dc):
        '''
        '''
        for i in xrange(len(self.curve.points)):
            x1,y1,z = self.curve.points[i-1]
            x2,y2,z = self.curve.points[i]

            tx,ty,z = self.curve.points[i-1].in_tangent
            tx += x1
            ty += y1
            dc.SetPen(wx.Pen(wx.Colour(255,0,0)))
            dc.DrawLine(x1,y1, tx,ty)

            tx,ty,z = self.curve.points[i-1].out_tangent
            tx += x1
            ty += y1
            dc.SetPen(wx.Pen(wx.Colour(0,255,0)))
            dc.DrawLine(x1,y1, tx,ty)


    # -----------------------------------------------------------------

    def drawInterpolated(self, dc):
        '''
        '''
        dc.SetPen(wx.Pen(wx.Colour(0,0,255)))

        for i in xrange(100):
            p1 = self.curve.getPt(i)
            p2 = self.curve.getPt(i+1)

            dc.DrawLine(p1.x,p1.y, p2.x, p2.y)

    # -----------------------------------------------------------------

    def onPaint(self, evt):
        '''
        '''
        dc = wx.PaintDC(self)
        self.drawLines(dc)
        self.drawTangents(dc)
        self.drawInterpolated(dc)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class App(wx.App):
    '''
    '''
    def OnInit(self):
        '''
        '''
        editor = Editor()
        editor.Show()
        return True

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

app = App(False)
app.MainLoop()
