from math import pi, sin, cos, sqrt, ceil

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)
       
        self.playerCount = 7
        self.cameras = self.createCamera( self.createNCameras(self.playerCount))
           
       
        #self.camera1=self.createCamera((0.0, 0.5, 0,1))
        #self.camera1.reparentTo(self.model1)
        #self.camera1.lookAt(self.model1)
        #self.camera2=self.createCamera((0.5,1.0,0,1))
        #self.camera2.reparentTo(self.model2)
        #self.camera2.lookAt(self.model2)
        base.camNode.setActive(False) #disable default cam
       
       
 
        # Disable the camera trackball controls.
        self.disableMouse()
 
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
 
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
 
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        for i in range(self.playerCount):
            angleDegrees = task.time * (i+1) *2
            angleRadians = angleDegrees * (pi / 180.0)
            self.cameras[i].setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
            self.cameras[i].setHpr(angleDegrees, 0, 0)
        return Task.cont

    def createCamera(self,dispRegion):
        cameras = []
        for i in dispRegion:
            camera=base.makeCamera(base.win,displayRegion=i)
            camera.node().getLens().setAspectRatio(3.0/4.0)
            camera.node().getLens().setFov(45) #optional.
            camera.setPos(0,-8,3) #set its position.
            cameras.append(camera)
        return cameras
   
    def createNCameras(self,camCount):
        list = []
        times = ceil(sqrt(camCount))
        if ((times* times) - times >= camCount):
            print times, times-1
            for y in range(1,times ,1):
                for x in range(1,times+1 ,1):
                    print x, y, times
                    print ((x-1)/times, x/times, (y-1)/(times-1), y/(times-1) )
                    list.append(((x-1)/times, x/times, (y-1)/(times-1), y/(times-1) ))
                   
        else:
            print times, times
            for y in range(1, times+1 ,1):
                for x in range(1, times+1 ,1):
                    print x, y, times
                    print ((x-1)/times, x/times, (y-1)/times, y/times )
                    list.append(((x-1)/times, x/times, (y-1)/times, y/times ))
        print len(list)
        return list   
       
       
 
app = MyApp()
app.run()
