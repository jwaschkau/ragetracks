from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
 

class RageTracks(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        
        #initialise the lights
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        
        #Initialise the Ode world
        world = OdeWorld()
        world.setGravity(0, 0, -9.81)
        
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
        self.glider.setPos(0, 0, 3)
        
        myBody = OdeBody(world)
        myBody.setPosition(self.glider.getPos(render))
        myBody.setQuaternion(self.glider.getQuat(render))
        myMass = OdeMass()
        myMass.setBox(11340, 1, 1, 1)
        myBody.setMass(myMass)
        
        
        #set up the camera
        base.camera.reparentTo(self.glider)
        base.camera.setPos(0,-30,10)
        base.camera.lookAt(self.glider)         

    def physicsTask(task):
      # Step the simulation and set the new positions
      world.quickStep(globalClock.getDt())
      return task.cont

game = RageTracks() 
game.run()