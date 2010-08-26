from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
 

class RageTracks(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)
        #base.disableMouse()
        
        #initialise the lights
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        
        #Initialise the Ode world
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -0.5)
        
        #load the models
        
        #environment
        self.environ = self.loader.loadModel("data/models/Plane")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(10, 10, 10)
        self.environ.setPos(0, 0, 0)
        
        #racer
        self.glider = self.loader.loadModel("data/models/vehicle01")
        # Reparent the model to render.
        self.glider.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.glider.setScale(1, 1, 1)
        self.glider.setPos(0, 0, 50)
        
        self.myBody = OdeBody(self.world)
        self.myBody.setPosition(self.glider.getPos(render))
        self.myBody.setQuaternion(self.glider.getQuat(render))
        self.myMass = OdeMass()
        self.myMass.setBox(11340, 1, 1, 1)
        self.myBody.setMass(self.myMass)
        
        
        #set up the camera
        base.camera.reparentTo(self.glider)
        base.camera.setPos(0,-30,10)
        base.camera.lookAt(self.glider)
        
        #add physics to taskmgr
        taskMgr.add(self.physicsTask, 'physics')       

    def physicsTask(self, task):
        # Step the simulation and set the new positions
        self.world.quickStep(globalClock.getDt())
        
        #set new positions
        self.glider.setPosQuat(render, self.myBody.getPosition(), Quat(self.myBody.getQuaternion()))
        return task.cont

game = RageTracks() 
game.run()