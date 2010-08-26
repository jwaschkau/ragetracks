from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
 

class RageTracks(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #Initialise the Ode world
        world = OdeWorld()
        world.setGravity(0, 0, -9.81)
         
        # The task for our simulation

    def physicsTask(task):
      # Step the simulation and set the new positions
      world.quickStep(globalClock.getDt())
      return task.cont

game = RageTracks() 
game.run()