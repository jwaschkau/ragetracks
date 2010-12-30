# -*- coding: utf-8 -*-

import trackgen3d
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
import wx
import wx.lib.agw.floatspin as FS

ID_PREVIEW = wx.NewId()
ID_SAVE = wx.NewId()
ID_OPEN = wx.NewId()
ID_NEW = wx.NewId()
ID_MODE = wx.NewId()

MODE_ROAD = False
MODE_BORDER = True

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Editor(wx.Frame):
    '''
    '''
    def __init__(self):
        wx.Frame.__init__(self, None, title="Road Shape Editor", size=wx.Size(800,480))
        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D)
        self.canvas = Canvas(self.splitter)
        self.panel = wx.Panel(self.splitter, style=wx.BORDER_SUNKEN)
        self.splitter.SplitVertically(self.canvas, self.panel, -200)
        
        wx.StaticText(self.panel, -1, "Title:", wx.Point(10,10))
        wx.StaticText(self.panel, -1, "Author:", wx.Point(10,60))
        self.title = wx.TextCtrl(self.panel, -1, "Road Part", wx.Point(15,30), wx.Size(150,23))
        self.author = wx.TextCtrl(self.panel, -1, "RageTracks Team", wx.Point(15,80), wx.Size(150,23))
        
        self.mirrored = wx.CheckBox(self.panel, -1, " mirrored", wx.Point(15, 130))
        self.mode = wx.CheckBox(self.panel, ID_MODE, " Border Mode", wx.Point(15, 150))
        
        ##wx.Button(self.panel, ID_PREVIEW, "Preview", wx.Point(20,180), wx.Size(150,23))
        
        wx.Button(self.panel, ID_NEW, "New", wx.Point(20,230), wx.Size(150,23))
        wx.Button(self.panel, ID_OPEN, "Open", wx.Point(20,260), wx.Size(150,23))
        wx.Button(self.panel, ID_SAVE, "Save", wx.Point(20,290), wx.Size(150,23))
        
        self.Bind(wx.EVT_BUTTON, self.onNew, id=ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.onOpen, id=ID_OPEN)
        self.Bind(wx.EVT_BUTTON, self.onSave, id=ID_SAVE)
        self.Bind(wx.EVT_CHECKBOX, self.onCheck)
        
    # -----------------------------------------------------------------    
    
    def onCheck(self, evt):
        '''
        '''
        if evt.GetId() == ID_MODE:
            self.canvas.mode = not self.canvas.mode
        else:
            if self.mirrored.GetValue():
                self.canvas.road.mirrored = True
                self.canvas.road.mirrorPoints()
            else:
                self.canvas.road.mirrored = False
                self.canvas.road.demirrorPoints()
            self.canvas.Refresh()
    
    # -----------------------------------------------------------------    
    
    def onNew(self, evt):
        '''
        '''
        self.canvas.road = trackgen3d.StreetData(mirrored=False)
        self.canvas.Refresh()
        
        self.title.SetValue("Road Part")
        self.author.SetValue("RageTracks Team")
        self.mirrored.SetValue(False)
        
    # -----------------------------------------------------------------    
    
    def onOpen(self, evt):
        '''
        '''
        dlg = wx.FileDialog(self, "open a shape", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:

##            try:
            success = True
            
            self.canvas.road.readFile(dlg.GetPath())

            self.title.SetValue(self.canvas.road.name)
            self.author.SetValue(self.canvas.road.author)
            self.mirrored.SetValue(self.canvas.road.mirrored)

            self.canvas.Refresh()
            
##            except:
##                success = False
##            
##            if not success:
##                msg = wx.MessageDialog(self, "There was an error while reading file", "Open File", style = wx.OK | wx.ICON_ERROR)
##                self.onNew(None)
##            
##                msg.ShowModal()
##                msg.Destroy()
        dlg.Destroy()
        
    # -----------------------------------------------------------------    
    
    def onSave(self, evt):
        '''
        '''
        dlg = wx.FileDialog(self, "save the current shape", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            self.canvas.road.name = self.title.GetValue()
            self.canvas.road.author = self.author.GetValue()
            self.canvas.road.mirrored = self.mirrored.GetValue()
            
            if path[:-4] != ".xml":
                path += ".xml"
            
            try:
                self.canvas.road.writeFile(dlg.GetPath())
                success = True
            except:
                success = False
            
            if success:
                msg = wx.MessageDialog(self, "File saved successfully!", "Save File", style = wx.OK | wx.ICON_INFORMATION)
            else:
                msg = wx.MessageDialog(self, "There was an error while saving file", "Save File", style = wx.OK | wx.ICON_ERROR)
            
            msg.ShowModal()
            msg.Destroy()
        dlg.Destroy()
        
    # ----------------------------------------------------------------- 

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Canvas(wx.Window):
    '''
    '''
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.road = trackgen3d.StreetData(mirrored=False)
        self.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)        
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_RIGHT_UP, self.onAddPoint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onZoom)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        
        self.active_point = None
        self.mode = MODE_ROAD
        
        self.max_value= 50
    
    # -----------------------------------------------------------------
    
    def onPaint(self, evt):
        '''
        '''
        dc = wx.PaintDC(self)
        w,h = dc.GetSizeTuple()
        
        dc.SetPen(wx.Pen(wx.Colour(120,120,120), 1))

        for i in xrange(1, self.max_value+1):
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
        
        # draw road
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))
        
        last = None
        for i in self.road:
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
        evt.Skip()
    
    # draw border
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        dc.SetBrush(wx.Brush(wx.Colour(0,0,255)))
        
        last = None

        for i in self.road.border_l:
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
        w,h = self.GetClientSizeTuple()
        x,y = evt.GetPositionTuple()
        x,y = self.getLogicalPosition(x,y,w,h)

        if self.mode == MODE_ROAD:
            self.road.addPoint(x,y)
        else:
            self.road.border_l.addPoint(x,y)
        self.Refresh()
        evt.Skip()
        
    # -----------------------------------------------------------------

    def hitPoint(self, x,y):
        '''
        '''
        w,h = self.GetClientSizeTuple()
        
        if self.mode == MODE_ROAD:
            for point in self.road:
                px, py = self.getRasterPosition(point.getX(), point.getY(), w,h)
                rect = wx.Rect(px-4,py-4,8,8)
                if rect.Contains(wx.Point(x,y)):
                    return point
        else:
            for point in self.road.border_l:
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

    def onDoubleClick(self, evt):
        '''
        '''
        # check if there is a poit under the click
        x,y = evt.GetPositionTuple() 
        point = self.hitPoint(x,y)
        if point:
            dlg = PointDialog(self,point.getX(), point.getY())
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.getValue()
                point[0] = data[0]
                point[1] = data[1]
                self.Refresh()
            dlg.Destroy()
        evt.Skip()
    
    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class PointDialog(wx.Dialog):
    '''
    '''
    def __init__(self, parent, x, y):
        '''
        '''
        wx.Dialog.__init__(self, parent, size=wx.Size(140,120))
        
        wx.StaticText(self, -1, "x", wx.Point(10,10))
        wx.StaticText(self, -1, "y", wx.Point(10,35))
        self.x = FS.FloatSpin(self, -1, pos= wx.Point(25,10), min_val=-100, max_val=100, increment=0.01, value=x, agwStyle=FS.FS_LEFT)
        self.y = FS.FloatSpin(self, -1, pos= wx.Point(25,35), min_val=-100, max_val=100, increment=0.01, value=y, agwStyle=FS.FS_LEFT)
        wx.Button(self, wx.ID_OK, "Ok", wx.Point(10,60), wx.Size(110,23))
    
    # -----------------------------------------------------------------
        
    def getValue(self):
        '''
        '''
        return self.x.GetValue(), self.y.GetValue()
        
    # -----------------------------------------------------------------
    
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Preview(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        self.road = trackgen3d.StreetData()
        
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