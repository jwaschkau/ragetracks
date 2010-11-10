# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from pandac.PandaModules import * #Load all PandaModules
from panda3d.core import loadPrcFileData
import settings
import inputdevice
import player
import splitscreen
import trackgen3d
from playercam import PlayerCam
import gettext
import sys
from menu import Menu
from menu import MainMenu

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self, *args):
        '''
        '''
        
        #loadPrcFileData("", "fullscreen 1\n win-size 1680 1050")
        #loadPrcFileData("", "want-pstats 1\n pstats-host 127.0.0.1\n pstats-tasks 1\n task-timer-verbose 1")
        loadPrcFileData("", "sync-video #f")
        loadPrcFileData("", "default-directnotify-level debug\n notify-level-x11display fatal\n notify-level-Game debug\n notify-level-Menu debug\n notify-level-Vehicle debug")
        ShowBase.__init__(self)
        base.enableParticles()
        
        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("New Game-Object created: %s" %(self))
        
        base.setFrameRateMeter(True) #Show the Framerate
        base.camNode.setActive(False) #disable default cam
        self.disableMouse() #disable manual camera-control
        render.setShaderAuto()

        # load the settings
        self.settings = settings.Settings()
        self.settings.loadSettings("user/config.ini")
        gettext.install("ragetrack", "data/language")#, unicode=True) #installs the system language
        #trans = gettext.translation("ragetrack", "data/language", ["de"]) #installs choosen language
        #trans.install() #usage: print _("Hallo Welt")

        #Fullscreen
        if self.settings.fullscreen:
            wp = WindowProperties()
            wp.setFullscreen(self.settings.fullscreen)
            wp.setOrigin(0,0)
            wp.setSize(int(base.pipe.getDisplayWidth()),int(base.pipe.getDisplayHeight()))
            base.win.requestProperties(wp)
        
        #Initialize needed variables and objects
        self.players = [] #holds the player objects
        self.TRACK_GRIP = 0.5
        self.LINEAR_FRICTION = 0.02
        self.ANGULAR_FRICTION = 0.02
        self.splitscreen = splitscreen.SplitScreen(0)

        #Initialize Physics (ODE)
        self.world = OdeWorld()
##        self.world.setGravity(0, 0, -9.81)
        self.deltaTimeAccumulator = 0.0 #this variable is necessary to track the time for the physics
        self.stepSize = 1.0 / 300.0 # This stepSize makes the simulation run at 60 frames per second

        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        #Initialize the surface-table, it defines how objects interact with each other
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
        
        #set up the collision event
        self.space.setCollisionEvent("ode-collision")
        base.accept("ode-collision", self.onCollision)
        
        # initialize the input devices
        self.devices = inputdevice.InputDevices(self.settings.getInputSettings())

        startgame = True
        #Start the Game
        for arg in sys.argv:
            if  arg == "--ep":
                startgame = False
                if sys.argv[sys.argv.index(arg)+1] == "startGame":
                    for i in xrange(len(self.devices.devices)):
                        #myMenu = Menu(self)
                                           
                        player = self.addPlayer(self.devices.devices[0])
                        import glob
                        self.vehicle_list = glob.glob("data/models/vehicles/*.egg")
                        #start loading the model
                        self.players[0].setVehicle(loader.loadModel(self.vehicle_list[-1]))
                       
                        taskMgr.add(self.devices.fetchEvents, "fetchEvents")
                        
                        self.streetPath = loader.loadModel('data/models/Street.egg')    #Test Street
                        self.startGame(self.streetPath)
            if  arg == "--PSt":
                PStatClient.connect() #activate to start performance measuring with pstats
            if  arg == "--wire":    
                base.toggleWireframe()
        if startgame:   
            myMenu = Menu(self)
            taskMgr.add(self.devices.fetchEvents, "fetchEvents")
            myMenu.showStartScreen()
            

    # -----------------------------------------------------------------

    def addPlayer(self, device):
        '''
        creates a new player object, initializes it and sorts the cameras on the screen
        '''
        self._notify.info("Adding Player, Device: %s" %(device))
        screen = self.splitscreen.addCamera()
        camera = PlayerCam(screen)
        
        #Create a new player object
        self.players.append(player.Player(len(self.players),self.world, self.space, device, camera))
        
        self._notify.info("Player added: %s" %(self.players[-1]))

    # -----------------------------------------------------------------

    def removePlayer(self, player):
        '''
        deletes a player object and sorts the cameras on the screem
        '''
        #delete the cam
        self.splitscreen.removeCamera(player.camera.camera)
        #delete the player
        self.players.remove(player) ##all objects must be deleted!
        self._notify.info("Player removed: %s" %(player))
        
    # -----------------------------------------------------------------

    def startGame(self, track):
        '''
        Start the game
        '''
        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("Initializing start game")
        counter = 0
        for player in self.players:
            player.activateGameCam()
            self.players[counter].vehicle.physics_model.setPosition(0, -5 * counter, 10)
            self.players[counter].vehicle.model.setH(0)
            self.players[counter].vehicle.model.setP(0)
            self.players[counter].vehicle.physics_model.setQuaternion(self.players[counter].vehicle.model.getQuat(render))
            counter+=1
        
        #Create the Track
        self.track = track
        self.track.reparentTo(render)
        
        #add collision with the map
        self.groundGeom = OdeTriMeshGeom(self.space, OdeTriMeshData(self.track, True))
        self.groundGeom.setCollideBits(0)
        self.groundGeom.setCategoryBits(1)
        
        #Create the Plane that you get hit by if you fall down
        self.plane = OdePlaneGeom(self.space,0,0,1,-50)
        self.plane.setCollideBits(0)
        self.plane.setCategoryBits(3)

        self.arrows = loader.loadModel("data/models/arrows.egg")
        self.arrows.reparentTo(render)
        self.arrows.setPos(0,0,0)
        
        self.arrows2 = loader.loadModel("data/models/arrows.egg")
        self.arrows2.reparentTo(render)
        self.arrows2.setPos(0,60,0)

        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))
        
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(10.0, 10.0, 10.0, 1))
        #dlight.setShadowCaster(True, 2048, 2048) #enable shadows for this light
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)

        #start the gametask
        self._notify.debug("Starting gameTask")
        taskMgr.add(self.gameTask, "gameTask")
        self.world.setGravity(0, 0, -9.81)
        self._notify.info("Start game initialized")

    # -----------------------------------------------------------------

    def onCollision(self, entry):
        '''
        Handles Collision-Events
        '''

        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()
        body1 = entry.getBody1()
        body2 = entry.getBody2()

        #Handles the collision-rays from the players
        for player in self.players:
            ray = player.vehicle.ray.getRay()
            #print geom1.compareTo(ray)
            #print geom2.compareTo(ray)
            if geom1 == ray or geom2 == ray:
                normal = entry.getContactGeom(0).getNormal()
                normal.normalize()
                player.vehicle.physics_model.setGravityMode(0) #disable gravity if on the track
                mass = player.vehicle.physics_model.getMass().getMagnitude()                    
                force_pos = ray.getPosition()
                contact = entry.getContactPoint(0)
                force_dir = force_pos - contact
                acceleration = ((ray.getLength()/2)-force_dir.length())*20#calculate the direction
                player.vehicle.hit_ground = True
                
                force_dir.normalize()
                #rigidbody.AddTorque(Vector3.Cross(transform.forward, Vector3.up) - rigidbody.angularVelocity * 0.5f);
                
                #Change the angle of the vehicle so it matches the street
                player.vehicle.physics_model.addTorque(player.vehicle.collision_model.getQuaternion().xform(Vec3(0,0,1)).cross(normal)*mass*20)# - player.vehicle.physics_model.getAngularVel() * 0.5)

                #push the vehicle
                if acceleration > 0:
                    force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
                    player.vehicle.physics_model.addForce(force_dir*mass)
                
                #pull the vehicle
                else:
                    force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
                    player.vehicle.physics_model.addForce(force_dir*mass)
                player.vehicle.physics_model.addForce(normal[0]*player.vehicle.boost_direction[0]*-0.9*mass, normal[1]*player.vehicle.boost_direction[1]*-0.9*mass, normal[2]*player.vehicle.boost_direction[2]*-0.9*mass)
                return
                     
        for player in self.players:
            #workaround until panda 1.7.1
            #if the player collides with the ground plane he will get reset to the starting position   
            if geom1.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body2) == 0:
                player.vehicle.physics_model.setPosition(0,0,20)
                player.vehicle.physics_model.setLinearVel(0,0,0)
                return
            elif geom2.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body1) == 0:
                player.vehicle.physics_model.setPosition(0,0,20)
                player.vehicle.physics_model.setLinearVel(0,0,0)
                #body1.setPosition(0,0,20)
                return
            #Decrease energy on collision
            elif player.vehicle.physics_model.compareTo(body1) == 0 or player.vehicle.physics_model.compareTo(body2) == 0:
                player.vehicle.energy -= 0.1

 # -----------------------------------------------------------------

    def gameTask(self, task):
        '''
        this task runs once per second if the game is running
        '''
        #calculate the physics
        #self.space.autoCollide() # Setup the contact joints

        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize: # Step the simulation
            for player in self.players:
                player.doStep() #refresh player specific things (rays)

                #get the player input and set the forces
                if player.device.boost:
                    player.vehicle.setBoost()
                if player.device.directions[0] != 0 or player.device.directions[1] != 0:
                    player.vehicle.direction = player.device.directions

                linear_velocity = player.vehicle.physics_model.getLinearVel()
                angular_velocity = player.vehicle.physics_model.getAngularVel()
                mass = player.vehicle.physics_model.getMass().getMagnitude()

                #calculate airresistance to get energy out of the ode-system
                player.vehicle.physics_model.addForce(linear_velocity*-self.LINEAR_FRICTION*mass)
                player.vehicle.physics_model.addTorque(angular_velocity*-self.ANGULAR_FRICTION*mass)

            self.space.autoCollide() # Setup the contact joints
            self.deltaTimeAccumulator -= self.stepSize # Remove a stepSize from the accumulator until the accumulated time is less than the stepsize
            self.world.quickStep(self.stepSize)
            self.contactgroup.empty() # Clear the contact joints
            player.vehicle.hit_ground = False

        for player in self.players: # set new positions
            player.updatePlayer()
        return task.cont
    # -----------------------------------------------------------------


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()




