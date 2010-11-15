# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules

# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        loadPrcFileData("", "notify-level-x11display fatal")

        ##This variable gets set to true when a collision-event gets fired and to false every ode-frame
        self.ode_collisiontest = False
        
        base.setFrameRateMeter(True) #Show the Framerate
        self.world = OdeWorld()
        self.deltaTimeAccumulator = 0.0 #this variable is necessary to track the time for the physics
        self.stepSize = 1.0 / 300.0 # This stepSize makes the simulation run at 300 frames per second
        
        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        #Initialize the surface-table, it defines how objects interact with each other
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
        
        self.startGame()

    # -----------------------------------------------------------------

    def startGame(self):
        '''
        Start the game
        '''
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))

        #Create the Plane that the model collides with
        self.plane = OdePlaneGeom(self.space,0,0,1,-5)
        self.plane.setCollideBits(0)
        self.plane.setCategoryBits(1)
        
        self.space.setCollisionEvent("ode-collision")
        base.accept("ode-collision", self.onCollision)
        #Set up a model, that collides with the plane, i use a vector instead because it should always collide
##        self.model = loader.loadModel("panda")
##        self.model.reparentTo(render)
##        self.model.setPos(0,50,2)
##        #Initialize the physics-simulation
##        self.physics_model = OdeBody(self.world)
##        self.physics_model.setPosition(self.model.getPos(render))
##        self.physics_model.setQuaternion(self.model.getQuat(render))        
##        
##        #Initialize the mass
##        physics_mass = OdeMass()
##        physics_mass.setBox(1,1,1,1)
##        self.physics_model.setMass(physics_mass)
##        
##        self.collision_model = OdeBoxGeom(self.space, 1,1,1)
##        self.collision_model.setBody(self.physics_model)
##        self.collision_model.setCollideBits(1)
##        self.collision_model.setCategoryBits(0)

        #Set up a vector that collides with the plane
        self.ray = OdeRayGeom(self.space, 100)
        self.ray.setCollideBits(1)
        self.ray.setCategoryBits(0)
        self.ray.set(Vec3(0,2,50),
                    Vec3(0,0,-1))

        #add the game task
        taskMgr.add(self.gameTask, "gameTask")
        self.world.setGravity(0, 0, -0.81)
    
    # -----------------------------------------------------------------
    
    def onCollision(self, entry):
        '''
        Handles Collision-Events
        '''
        #set the variable true when a collision happens
        self.ode_collisiontest = True
    
    # -----------------------------------------------------------------
    
    def gameTask(self, task):
        '''
        this task runs x-times per second if the game is running
        '''
        #calculate the physics
        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize: # Step the simulation
            self.space.autoCollide() # Setup the contact joints
            self.deltaTimeAccumulator -= self.stepSize # Remove a stepSize from the accumulator until the accumulated time is less than the stepsize
            self.world.quickStep(self.stepSize)
            self.contactgroup.empty() # Clear the contact joints
            ##Here we print the variable that should be True when a collision event is fired
            print self.ode_collisiontest
            #Now we set it False again
            self.ode_collisiontest = False
        
        #set the new position
        #self.model.setPosQuat(render, self.physics_model.getPosition(), Quat(self.physics_model.getQuaternion())) 
        return task.cont
        
    # -----------------------------------------------------------------

game = Game()
game.run()
