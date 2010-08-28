from math import pi, sin, cos, sqrt, ceil

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
class SplitScreen(ShowBase):
    '''
    '''
    #def __init__(self):
    #    test()
    
    
    def __init__(self):
        self.playerCount = 16
        
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)
        
        print "Players:", self.playerCount
        
##      Add all SplitScreen parts for the count of players
        self.cameras = self.createNCamera( self.createNCameras(self.playerCount))
       
        #self.camera1=self.createCamera((0.0, 0.5, 0,1))
        #self.camera1.reparentTo(self.model1)
        #self.camera1.lookAt(self.model1)
        
        base.camNode.setActive(False) #disable default cam
       
        # Disable the camera trackball controls.
        self.disableMouse()
        
        # Load the Track.
        self.environ = self.loader.loadModel("data/models/Track01")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(3, 3, 3)
        self.environ.setPos(0, 0, 0)
        
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        
        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")
        
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))
        
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()
        
        #Change the Size of a Display Region
        #self.cameras[0].node().getDisplayRegion(0).setDimensions(0, 0, 0, 0)
        
        #Del one Camera 
        #self.cameras[0].removeNode()
        
        def oneMorePlayer(player):
            players.append(player) #Every Player must have a Camera created with CreateOneCamera
            reRegion()
       
        def oneLessPlayer(player):
            for i in range(0 , len(self.players), 1):
                #vill allen playern eine UUID geben?
                if self.players[i] == player:
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
            
    
    # Define a procedure to spin the camera.
    def spinCameraTask(self, task):
        for i in range(self.playerCount):
            angleDegrees = task.time * (i+1) *2
            angleRadians = angleDegrees * (pi / 180.0)
            self.cameras[i].setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
            self.cameras[i].setHpr(angleDegrees, 0, 0)
        return Task.cont

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
app = SplitScreen()
app.run()
