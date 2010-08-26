from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
 

class RageTracks(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()

        #load the models
        
        #environment
        self.environ = self.loader.loadModel("data/models/egg/Plane")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(1, 1, 1)
        self.environ.setPos(0, 0, 0)
        
        #racer
        self.glider = self.loader.loadModel("data/models/egg/gleiter_A")
        # Reparent the model to render.
        self.glider.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.glider.setScale(1, 1, 1)
        self.glider.setPos(0, 0, 1)
        
        base.camera.reparentTo(self.glider)
        base.camera.setPos(0,-30,10)
        base.camera.lookAt(self.glider)
        #Initialise the Ode world
        world = OdeWorld()
        world.setGravity(0, 0, -9.81)
         

    def physicsTask(task):
      # Step the simulation and set the new positions
      world.quickStep(globalClock.getDt())
      return task.cont

game = RageTracks() 
game.run()