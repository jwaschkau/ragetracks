from math import sqrt, ceil

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

 
class SplitScreen(object):
    '''
    '''    
    def __init__(self, player_count = 1):
        '''
        '''
        self.player_count = player_count

        # Add all SplitScreen parts for the count of players
        print self.getRegions(player_count)
##        self.cameras = self.createNCamera(self.createNCameras(self.playerCount))

    # -----------------------------------------------------------------
    
    def addScreen(self):
        '''
        '''
        return self.createCamera((0,1,1,0))
    
    # -----------------------------------------------------------------
        
    def todel(self):
        #Change the Size of a Display Region
        #self.cameras[0].node().getDisplayRegion(0).setDimensions(0, 0, 0, 0)
        
        #Del one Camera 
        #self.cameras[0].removeNode()
        pass
    
    # -----------------------------------------------------------------
        
    def oneMorePlayer(player):
        players.append(player) #Every Player must have a Camera created with CreateOneCamera
        reRegion()
    
    # -----------------------------------------------------------------
       
    def oneLessPlayer(player):
        for i in range(0 , len(self.players), 1):
            if self.players[i].getNumber() == player.getNumber():
                self.players[i].kill()
                del self.players[i]
        reRegion()

    # -----------------------------------------------------------------

    def refreshScreens(self, players):
        regions = self.getRegions(len(players))
        for i in range(0 , len(players), 1):
            players[i].getCamera().node().getDisplayRegion().setDimensions(displayRegions[i])
            #JEDEM PLAYER EIENE neue REGION zuweise
            
    # -----------------------------------------------------------------

    def createCamera(self,region):
        '''
        Create one Camera for a new Player
        '''
        camera=base.makeCamera(base.win,displayRegion=region)
        camera.node().getLens().setAspectRatio(3.0/4.0)
        camera.node().getLens().setFov(45) #optional.
        camera.setPos(0,-8,3) #set its position.
        return camera

    # -----------------------------------------------------------------
    
    def createCameras(self, count):
        '''
        Generates a count of cameras and deletes all old ones before generating new ones
        '''
        # delete the old cameras
        del self.cameras
        self.cameras = []
        
        # calculate, which regions are nessecary
        regions = self.getRegions(count)
        # add the cameras
        for region in regions:
            self.cameras.append(self.createCamera(region))
    
    # -----------------------------------------------------------------

    def getRegions(self, count):
        '''
        Calculates the window size and position for a count of n screens
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
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
       
if __name__ == "__main__":
#Only for Test 
    splitter = SplitScreen(2)
