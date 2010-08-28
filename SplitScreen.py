from math import sqrt, ceil
 
class SplitScreen(object):
    '''
    '''    
    def __init__(self, playerCount = 1):
        self.playerCount = playerCount
        print "Players:", self.playerCount
        
    def todel(self):
        
        
        
##      Add all SplitScreen parts for the count of players
        self.cameras = self.createNCamera(self.createNCameras(self.playerCount))
        
        #Change the Size of a Display Region
        #self.cameras[0].node().getDisplayRegion(0).setDimensions(0, 0, 0, 0)
        
        #Del one Camera 
        #self.cameras[0].removeNode()
        
        def oneMorePlayer(player):
            players.append(player) #Every Player must have a Camera created with CreateOneCamera
            reRegion()
       
        def oneLessPlayer(player):
            for i in range(0 , len(self.players), 1):
                if self.players[i].getNumber() == player.getNumber():
                    self.players[i].kill()
                    del self.players[i]
            reRegion()

        def reRegion(players):
            displayRegions = createNCameras(len(players))
            for i in range(0 , len(players), 1):
                players[i].getCamera().node().getDisplayRegion.setDimensions(displayRegions[i])
                #JEDEM PLAYER EIENE neue REGION zuweise
        
        
        #TEST
        self.displayRegions = self.createNCameras(2)
        self.cameras.append(self.createOneCamera((0,0,0,0)))
        #for i in range(2):
        self.cameras[0].node().getDisplayRegion(0).setDimensions(self.displayRegions[0][0], self.displayRegions[0][1], self.displayRegions[0][2], self.displayRegions[0][3])
        self.cameras[1].node().getDisplayRegion(0).setDimensions(self.displayRegions[1][0], self.displayRegions[1][1], self.displayRegions[1][2], self.displayRegions[1][3])
            
    
    '''
    Create n Cameras use only CreateOneCamera n times
    '''
    def createNCamera(self,dispRegion):
        cameras = []
        for i in dispRegion:
            cameras.append(self.createOneCamera(i))
        return cameras
    
    '''
    Create one Camera for a new Player
    '''
    def createOneCamera(self,dispRegion):
        camera=base.makeCamera(base.win,displayRegion=dispRegion)
        camera.node().getLens().setAspectRatio(3.0/4.0)
        camera.node().getLens().setFov(45) #optional.
        camera.setPos(0,-8,3) #set its position.
        return camera

    '''
    Generates the Windows size andposition for a cont of N players
    '''
    def createNCameras(self,camCount):
##        if camCount <= 0:
##            pass
        list = []
        times = ceil(sqrt(camCount))
        if ((times* times) - times >= camCount):
            #print times, times-1 #Debug
            for y in range(int(times-1), 0, -1):
                for x in range(1,int(times+1) ,1):
                    #print x, y, times #Debug
                    #print ((x-1)/times, x/times, (y-1)/(times-1), y/(times-1) ) #Debug
                    list.append(((x-1)/times, x/times, (y-1)/(times-1), y/(times-1) ))
                   
        else:
            #print times, times #Debug
            for y in range(int(times), 0, -1):
                for x in range(1, int(times+1) ,1):
                    #print x, y, times #Debug
                    #print ((x-1)/times, x/times, (y-1)/times, y/times ) #Debug
                    list.append(((x-1)/times, x/times, (y-1)/times, y/times ))
        print "SplitScreenView:",len(list)
        return list   
       
       
#Only for Test 
#app = SplitScreen()
#app.run()
