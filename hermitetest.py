# -*- coding: utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
import wx

ID_PREVIEW = wx.NewId()
ID_SAVE = wx.NewId()
ID_OPEN = wx.NewId()
ID_NEW = wx.NewId()
ID_MODE = wx.NewId()

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Editor(wx.Frame):
    '''
    '''
    def __init__(self):
        wx.Frame.__init__(self, None, title="HermiteTest", size=wx.Size(800,480))
        self.canvas = Canvas(self)

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Canvas(wx.Window):
    '''
    '''
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.points = []
        self.curvepoints = []
        self.SetBackgroundColour(wx.Colour(255,255,255))

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.onAddPoint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onZoom)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_MOTION, self.onMotion)

        self.active_point = None

        self.max_value= 50

        self.points = [Vec2(-10,-20), Vec2(0,20), Vec2(10,-20)]

        self.actualizePoints()

    # -----------------------------------------------------------------

    def actualizePoints(self):
        '''
        '''
        self.curve = HermiteCurve()
        self.curvepoints = []
        for point in self.points:
            #HCCUT, #HCFREE , #HCG1, #HCSMOOTH
            self.curve.appendCv(HCSMOOTH, point[0],point[1], 0)

        for i in range(len(self.points)-1):
        #i = 1
            vec1 = self.points[i+1]-self.points[i-1]
            vec2 = self.points[i+1]-self.points[i-1]
            self.curve.setCvIn(i, Vec3(vec1[0],vec1[1], 0))
            self.curve.setCvOut(i, Vec3(vec2[0],vec2[1], 0))

        point = Vec3(0,0,0)

        length = self.curve.getMaxT()
        resolution = 100
        xres = length/resolution
        for i in range(0,resolution):
            self.curve.getPoint(i*xres, point)
            self.curvepoints.append(Vec3(point))

    # -----------------------------------------------------------------

    def onPaint(self, evt):
        '''
        '''
        dc = wx.PaintDC(self)
        w,h = dc.GetSizeTuple()

        # draw grid
        dc.SetPen(wx.Pen(wx.Colour(220,220,220), 1))

        for i in range(1, self.max_value+1):
            x,y = self.getRasterPosition(i,i,w,h)
            dc.DrawLine(x, 0, x, h-1)
            dc.DrawLine(0, y, w-1, y)
            x,y = self.getRasterPosition(-i,-i,w,h)
            dc.DrawLine(x, 0, x, h-1)
            dc.DrawLine(0, y, w-1, y)

        dc.SetPen(wx.Pen(wx.Colour(0,100,0), 2))
        dc.DrawLine(w/2,0, w/2,h-1)
        dc.SetPen(wx.Pen(wx.Colour(200,0,0), 2))
        dc.DrawLine(0,h/2, w-1,h/2)

        # draw points
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))

        last = None
        for i in self.points:
            x = i.getX()
            y = i.getY()
            x,y = self.getRasterPosition(x,y,w,h)

            if last != None:
                lx = last.getX()
                ly = last.getY()
                lx,ly = self.getRasterPosition(lx,ly,w,h)
                dc.DrawLine(lx,ly,x,y)

            dc.DrawRectangle(x-4,y-4,8,8)
            last = i

        # draw curve
        dc.SetPen(wx.Pen(wx.Colour(255,0,0)))

        last = None
        for i in self.curvepoints:
            x = i.getX()
            y = i.getY()
            x,y = self.getRasterPosition(x,y,w,h)

            if last != None:
                lx = last.getX()
                ly = last.getY()
                lx,ly = self.getRasterPosition(lx,ly,w,h)
                dc.DrawLine(lx,ly,x,y)
            last = i
        evt.Skip()

    # -----------------------------------------------------------------

    def getRasterPosition(self, x, y, w, h):
        '''
        '''
        max = self.max_value*2.0
        if x > 0:
            x = (w/max)*x+(w/2)
        else:
            x = (w/2)-((w/max)*-x)

        if y > 0:
            y = (h/2)-((h/max)*y)
        else:
            y = ((h/max)*-y)+(h/2)

        return int(x),int(y)

    # -----------------------------------------------------------------

    def getLogicalPosition(self, x, y, w, h):
        '''
        '''
        max = self.max_value*2.0
        if x > w/2:
            x = (x-(w/2))/(w/max)
        else:
            x = -self.max_value+(x/(w/max))

        if y > 0:
            y = ((h/2)-y)/(h/max)
        else:
            y = -((y-(h/2))/(h/max))

        return x,y

    # -----------------------------------------------------------------

    def onSize(self, evt):
        '''
        '''
        self.Refresh()
        evt.Skip()

    # -----------------------------------------------------------------

    def onZoom(self, evt):
        '''
        '''
        val = evt.GetWheelRotation()
        if val < 0 and self.max_value < 80:
            self.max_value += 1
        if val > 0 and self.max_value > 10:
            self.max_value -= 1
        self.Refresh()
        evt.Skip()

    # -----------------------------------------------------------------

    def onAddPoint(self, evt):
        '''
        '''
        pass
##        w,h = self.GetClientSizeTuple()
##        x,y = evt.GetPositionTuple()
##        x,y = self.getLogicalPosition(x,y,w,h)
##
##        if self.mode == MODE_ROAD:
##            self.road.addPoint(x,y)
##        else:
##            self.road.border_l.addPoint(x,y)
##        self.Refresh()
##        evt.Skip()

    # -----------------------------------------------------------------

    def hitPoint(self, x,y):
        '''
        '''
        w,h = self.GetClientSizeTuple()


        for point in self.points:
            px, py = self.getRasterPosition(point.getX(), point.getY(), w,h)
            rect = wx.Rect(px-4,py-4,8,8)
            if rect.Contains(wx.Point(x,y)):
                return point

        return None

    # -----------------------------------------------------------------

    def onLeftDown(self, evt):
        '''
        '''
        # check if there is a poit under the click
        x,y = evt.GetPositionTuple()
        self.active_point = self.hitPoint(x,y)

        evt.Skip()

    # -----------------------------------------------------------------

    def onLeftUp(self, evt):
        '''
        '''
        self.active_point = None
        self.actualizePoints()
        self.Refresh()
        evt.Skip()

    # -----------------------------------------------------------------

    def onMotion(self, evt):
        '''
        '''
        if self.active_point:
            w,h = self.GetClientSizeTuple()
            x,y = evt.GetPositionTuple()
            x,y = self.getLogicalPosition(x,y,w,h)

            self.active_point.setX(x)
            self.active_point.setY(y)
            self.Refresh()

        evt.Skip()

    # -----------------------------------------------------------------


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