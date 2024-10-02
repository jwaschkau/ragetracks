# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from math import sqrt, ceil
from direct.directnotify.DirectNotify import DirectNotify
from direct.filter.CommonFilters import CommonFilters

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------


class SplitScreen(object):
    '''
    This class manages multiple display regions and handles adding and removing them from screen.
    '''
    def __init__(self, cam_count=0):
        '''
        @param cam_count: (int) number of cameras which should be added
        '''
        self._notify = DirectNotify().newCategory("SplitScreen")
        self._notify.info("New SplitScreen-Object created: %s" %(self))
        self.regions = []   # the regions the screen is separated into
        self.cameras = []   # the cameras (empty ones are None)
        self.filters = []   # the shader filters applied to each camera
        self.cameraPosPre = [] # the position of the cameras before change
        self.steps = 1
        self.shaders_on = False

        if cam_count > 0:   # add cameras, if needed
            self.addCameras(cam_count)

    # -----------------------------------------------------------------

    def addCamera(self):
        '''
        adds a camera for a new player (or an additional view)
        @return: returns the added camera object
        '''
        self._notify.debug("Creating new camera")
        unused = self.getUnusedRegion()
        # if there is an unused camera slot, use it
        if unused != -1:
            self.setShaderOff()
            self.cameras[unused] = self.createCamera(self.regions[unused])
            self.setShaderOn()
        # if there is no free slot, we have to recalculate the regions
        else:
            self.regions = self.calculateRegions(len(self.regions)+1)      # recalc
            self.cameras.append(self.createCamera(self.regions[unused]))   # add a cam

            # if there are empty slots, they're filled with None
            for i in range(len(self.regions)-len(self.cameras)):
                self.cameras.append(None)
                unused -= 1

            self.refreshCameras()   # rearrange the regions

        # if there was an unused slot, the camera is now in it
        # if not, unused is -1 which points to the last element of the list
        # so unused points always to the newest cam
        self._notify.debug("New regions: %s , New cameras: %s" %(self.regions, self.cameras))
        self._notify.debug("New camera created")
        return self.cameras[unused]

    # -----------------------------------------------------------------

    def removeCamera(self,camera):
        '''
        removes a camera out of the list
        @param camera: (Camera NodePath) camera to remove
        '''
        self._notify.debug("Removing camera: %s" %(camera))
        # get the index of the camera
        i = self.cameras.index(camera)

        self.filters[i].delBloom()  # deactivate the shader
        self.filters.pop(i)         # delete the filter
        self.cameras.pop(i)         # delete the camera
        self.regions.pop(i)         # delete the region

        # delete all empty cameras
        try:
            while True:
                self.cameras.remove(None)
        except: pass
        # delete all empty filters
        try:
            while True:
                self.filters.remove(None)
        except: pass

        # the regions have to be recalculated and the cameras have to be rearranged
        self.regions = self.calculateRegions(len(self.cameras))
        self.refreshCameras()
        self._notify.debug("New regions: %s , New cameras: %s" %(self.regions, self.cameras))

    # -----------------------------------------------------------------

    def addCameras(self, cam_count):
        '''
        adds multiple cameras
        @param cam_count: (int) number of cams to add
        @return: (list) returns all recently added cameras
        '''
        cams = [] # this will be returned

        unused = self.getUnusedRegions() # this stores all unused slots

        # if there are enough unused camera slots, use it
        if len(unused) >= cam_count:
            for i in unused:
                self.cameras[i] = self.createCamera(self.regions[i])        # add the cam
                self.cams.append(self.cameras[i])

        # if there are not enough free slots, we have to recalculate the regions
        else:
            self.regions = self.calculateRegions(len(self.cameras)-len(unused)+cam_count)

            # first fill the unused slots
            for i in unused:
                self.cameras[i] = self.createCamera(self.regions[i])        # add the cam
                self.cams.append(self.cameras[i])

            # then add all other new cams at the end
            for i in range(cam_count-len(unused)):
                cam = self.createCamera(self.regions[i])
                self.cameras.append(cam)                                        # add the cam
                cams.append(cam)

            # if there are empty slots, they're filled with None
            for i in range(len(self.regions)-len(self.cameras)):
                self.cameras.append(None)

            # refresh all cameras
            self.refreshCameras()


        return cams # return all added cams

    # -----------------------------------------------------------------

    def refreshCameras(self):
        '''
        updates the size of all cameras, when the count of the regions has changed
        '''
        taskMgr.remove("AnimateRegion")
        self.cameraPosPre = [] # those are the old positions

        # first deactivate all shaders
        self.setShaderOff()

        # then save all old regions
        for i in range(len(self.cameras)):
            if self.cameras[i] != None:
                # add the old regions to the list
                region = self.cameras[i].node().getDisplayRegion(0)
                self.cameraPosPre.append((region.getLeft(), region.getRight(), region.getBottom(), region.getTop()))
                #update the aspect of the camera
                self.cameras[i].node().getLens().setAspectRatio(((self.regions[i][1]-self.regions[i][0])/(self.regions[i][3]-self.regions[i][2])))
                height =  self.cameras[i].node().getDisplayRegion(0).getPixelHeight()
                width =  self.cameras[i].node().getDisplayRegion(0).getPixelWidth()
                ratio = float(width)/float(height)
                self.cameras[i].node().getLens().setFov(45*ratio)

        # start the animation in a new task
        taskMgr.add(self.animateRegion, "AnimateRegion")

##        #Old Code without animation
##        for i in range(len(self.cameras)):
##            if self.cameras[i] != None:
##                print self.cameras[i].node().getDisplayRegion(0), self.cameras[i].node().getDisplayRegions
##                self.cameras[i].node().getDisplayRegion(0).setDimensions(self.regions[i][0], self.regions[i][1], self.regions[i][2], self.regions[i][3])
##                self._notify.debug("Aspect Ratio: %s:%s" %(self.regions[i][1]-self.regions[i][0],self.regions[i][3]-self.regions[i][2]))
##
##                #self.cameras[i].node().getLens().setFov(45*((self.regions[i][1]-self.regions[i][0])/(self.regions[i][3]-self.regions[i][2])))
##                self.cameras[i].node().getLens().setAspectRatio(((self.regions[i][1]-self.regions[i][0])/(self.regions[i][3]-self.regions[i][2])))
##
##        # reactivate the shaders
##        self.setShaderOn()

    #-----------------------------------------------------------------

    ##TODO Use task.time instead of self.steps (Frames)
    def animateRegion(self, task):
        '''
        animates the subwindows to their new positions and reactivates the shaders after that
        '''
        # if the animation is finished, we set the positions to final values
        if task.time >= self.steps:
            for i in range(len(self.cameraPosPre)):
                self.cameras[i].node().getDisplayRegion(0).setDimensions(self.calTheDiff( self.cameraPosPre[i][0], self.regions[i][0], self.steps), self.calTheDiff( self.cameraPosPre[i][1], self.regions[i][1], self.steps), self.calTheDiff( self.cameraPosPre[i][2], self.regions[i][2], self.steps), self.calTheDiff( self.cameraPosPre[i][3], self.regions[i][3], self.steps))
                self.cameras[i].node().getLens().setAspectRatio(((self.regions[i][1]-self.regions[i][0])/(self.regions[i][3]-self.regions[i][2])))
                height =  self.cameras[i].node().getDisplayRegion(0).getPixelHeight()
                width =  self.cameras[i].node().getDisplayRegion(0).getPixelWidth()
                ratio = float(width)/float(height)
                self.cameras[i].node().getLens().setFov(45*ratio)
            # reactivate the shaders
            self.setShaderOn()
            # end the task
            return task.done

        # animate the screens
        for i in range(len(self.cameraPosPre)):
            self.cameras[i].node().getDisplayRegion(0).setDimensions(self.calTheDiff( self.cameraPosPre[i][0], self.regions[i][0], task.time), self.calTheDiff( self.cameraPosPre[i][1], self.regions[i][1], task.time), self.calTheDiff( self.cameraPosPre[i][2], self.regions[i][2], task.time), self.calTheDiff( self.cameraPosPre[i][3], self.regions[i][3], task.time))
            self.cameras[i].node().getLens().setAspectRatio(((self.regions[i][1]-self.regions[i][0])/(self.regions[i][3]-self.regions[i][2])))
            height =  self.cameras[i].node().getDisplayRegion(0).getPixelHeight()
            width =  self.cameras[i].node().getDisplayRegion(0).getPixelWidth()
            ratio = float(width)/float(height)
            self.cameras[i].node().getLens().setFov(45*ratio)
        # continue the task
        return task.cont


    def calTheDiff(self, alt, neu, tasktime):
        return alt + ((neu - alt) / self.steps ) * tasktime

    #-----------------------------------------------------------------

    def getUnusedRegion(self):
        '''
        looks for an unused region to add a new player into it
        @return: (int) the index of an empty camera region
        '''
        for i in range(len(self.cameras)):
            if self.cameras[i] == None:
                return i
        else:
            return -1

    # -----------------------------------------------------------------

    def getUnusedRegions(self):
        '''
        looks for all unused regions to add a new player into it
        @return: (list) the indices of all empty camera regions
        '''
        unused = []

        for i in range(len(self.cameras)):
            if self.cameras[i] == None:
                unused.append(i)

        return unused

    # -----------------------------------------------------------------

    def createCamera(self,region):
        '''
        Create a camera for a new player
        '''
        camera=base.makeCamera(base.win,displayRegion=region)
        camera.node().getLens().setAspectRatio(((region[1]-region[0])/(region[3]-region[2])))
        height =  camera.node().getDisplayRegion(0).getPixelHeight()
        width =  camera.node().getDisplayRegion(0).getPixelWidth()
        ratio = float(width)/float(height)
        camera.node().getLens().setFov(45*ratio)

        camera.setPos(0,-8,3) #set its position.
        return camera

    # -----------------------------------------------------------------

    def calculateRegions(self, count):
        '''
        Calculates the window size and position for a count of n screens
        @return: (tuple) the display region in panda format (x1,x2,y1,y2) x is left-right, y is bottom-up
        '''
        regions = [] #this list stores the display regions for the several screens

        separations = ceil(sqrt(count)) # how often has the screen to be separated?

        # this is executed if a squarical order isn't senseful
        if ((separations**2) - separations >= count):
            for y in range(int(separations-1), 0, -1):
                for x in range(1,int(separations+1) ,1):
                    regions.append(((x-1)/separations, x/separations, (y-1)/(separations-1), y/(separations-1) ))

        # this is executed if the player count is near a square number e.g. 9 or 16
        else:
            for y in range(int(separations), 0, -1):
                for x in range(1, int(separations+1) ,1):
                    regions.append(((x-1)/separations, x/separations, (y-1)/separations, y/separations ))

        return regions

    # -----------------------------------------------------------------

    def setShaderOn(self):
        '''
        activates all shaders
        '''
        # activate the shaders
        self.filters = []

        for i in range(len(self.cameras)):
            if self.cameras[i] != None:
                self.filters.append(CommonFilters(base.win, self.cameras[i]))
                self.filters[i].setBloom(blend=(0,0,0,1), desat=-0.8, intensity=4.0, size="big")
            else:
                self.filters.append(None)
        self.shaders_on = True

    # -----------------------------------------------------------------

    def setShaderOff(self):
        '''
        deactivates all shaders
        '''
        # deactivate the shaders
        for filters in self.filters:
            if filters != None:
                filters.delBloom()
                del filters
        self.filters = []
        self.shaders_on = False

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

if __name__ == "__main__":
    import main
##    app = ShowBase()
##
##    split = SplitScreen(1)
##    print "initialisation done"
##    split.addCamera()
##    split.addCamera()
##    split.addCamera()
##
##    app.run()