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
from menu import Menu
import time

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        #loadPrcFileData("", "fullscreen 1\n win-size 1920 1200")
        #loadPrcFileData("", "want-pstats 1\n pstats-host 127.0.0.1\n pstats-tasks 1\n task-timer-verbose 1")
        loadPrcFileData("", "default-directnotify-level info")
        ShowBase.__init__(self)

        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("New Game-Object created: %s" %(self))
        
        #PStatClient.connect() #activate to start performance measuring with pstats
        base.setFrameRateMeter(True) #Show the Framerate
        base.camNode.setActive(False) #disable default cam
        self.disableMouse() #disable manual camera-control
        base.toggleWireframe()

        #Font
        self.font = DynamicTextFont('data/fonts/font.ttf')
        self.font.setRenderMode(TextFont.RMSolid)

        # load the settings
        self.settings = settings.Settings()
        self.settings.loadSettings("user/config.ini")
        gettext.install("ragetrack", "data/language")#, unicode=True) #installs the system language
        #trans = gettext.translation("ragetrack", "data/language", ["de"]) #installs choosen language
        #trans.install() #usage: print _("Hallo Welt")

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
        self.stepSize = 1.0 / 90.0 # This stepSize makes the simulation run at 60 frames per second

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

        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        plnp = render.attachNewNode(plight)
        plnp.setPos(100, 100, 0)
        render.setLight(plnp)
        
        # initialize the input devices
        self.devices = inputdevice.InputDevices(self.settings.getInputSettings())
        taskMgr.add(self.devices.fetchEvents, "fetchEvents")
        taskMgr.add(self.fetchAnyKey, "fetchAnyKey")
        
        #Start the Game
        self.showStartScreen()

    # -----------------------------------------------------------------

    def addPlayer(self, device):
        '''
        creates a new player object, initializes it and sorts the cameras on the screen
        '''
        self._notify.info("Adding Player")
        screen = self.splitscreen.addCamera()
        camera = PlayerCam(screen)
        
        #Create a new player object
        self.players.append(player.Player(len(self.players),self.world, self.space, device, camera))
        self._notify.info("Player added")
        self.players[-1].camera.camModeMenu()

    # -----------------------------------------------------------------

    def removePlayer(self, number):
        '''
        deletes a player object and sorts the cameras on the screem
        '''
        self._notify.info("Player removed")
        #delete the player
        for player in self.players:
            if player.getNumber() == number:
                self.players.remove(player) ##all objects must be deleted!

        #sort the cameras
    # -----------------------------------------------------------------

    def showStartScreen(self):
        '''
        the first screen with "press any Key"
        the device with the first key press will be the first player
        '''
        self._notify.info("Initializing StartScreen")

        #StartScreen Node
        self.startNode = NodePath("StartNode")
        self.startNode.reparentTo(render)
        self.startNode.setPos(-5,15,3)

        headline = TextNode("RageTracks")
        headline.setFont(self.font)
        headline.setText("RageTracks")
        NodePath("test").attachNewNode(headline)
        self.startNode.attachNewNode(headline)

        presskey = TextNode("PressAnyKey")
        presskey.setFont(self.font)
        presskey.setText(_("Press any key!!"))
        textNodePath = NodePath("PressAnyNode")
        textNodePath.attachNewNode(presskey)
        textNodePath.setPos(0,10,-9.5)
        textNodePath.reparentTo(self.startNode)

        #self.headline = Text3D("RageTracks")
        #self.headline.reparentTo(self.startNode)
        #self.presskey = Text3D(_("PressAnyKey"), Vec3(0,10,-9.5))
        #self.presskey.reparentTo(self.startNode)

        self.startNode.show()

        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        plnp = self.startNode.attachNewNode(plight)
        plnp.setPos(0, -10, 0)
        self.startNode.setLight(plnp)

        #Cam
        self.camera = base.makeCamera(base.win)

        #print self.devices.getCount()
        #print self.settings.getInputSettings()
        self._notify.info("StarScreen initialized")


    # -----------------------------------------------------------------

    def fetchAnyKey(self, task):
        '''
        Return the first device with the first key stroke
        '''
        for i in xrange(len(self.devices.devices)):
            if self.devices.devices[i].boost == True:
                #Kill Cam
                self.camera.node().setActive(False)
                #Kill Node
                self.startNode.hide()       #Maybe there is a function to delete the Node from memory

                #Start the Game for testing purpose
                #self.menu = Menu(self.newGame, self.players[0].getDevice())    #if one player exist
                self.menu = Menu(self.newGame, self.devices.devices[i])         #if no player exist
                self.menu.menuMain()
                return task.done
        return task.cont



        # -----------------------------------------------------------------

    def newGame(self):
        '''
        the new game menu
        '''
        self._notify.info("Initializing new game")
        self.unusedDevices = self.devices.devices[:]
        self._notify.info("New game initialized")
        taskMgr.add(self.collectPlayer, "collectPlayer")
        
        self.screens = []
        taskMgr.add(self.selectVehicle, "selectVehicle")
        #self.startGame()

    # -----------------------------------------------------------------

    def selectVehicle(self, task):
        for i in self.players:
            pass
            #i.
        return task.cont
    
    # -----------------------------------------------------------------

    def collectPlayer(self, task):
        '''
        Wait until all players are ready
        '''
        if len(self.players) > 0:
            if self.players[0].device.boost:
                for i in self.players:
                    i.camera.camModeGame()
                self.startGame()
                return task.done

        for device in self.unusedDevices:
            if device.boost == True:
                self.addPlayer(device)

                #self.unusedDevices.remove(device)
                task.delayTime = 0.2
                return task.again

        return task.cont

    # -----------------------------------------------------------------

    def startGame(self):
        '''
        Start the game
        '''
        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("Initializing start game")
        #Create the Track
        
        self.track = trackgen3d.Track3d(1000, 800, 600, 200, len(self.players))
        nodePath = self.render.attachNewNode(self.track.createMesh())
        tex = loader.loadTexture('data/textures/street.png')
        nodePath.setTexture(tex)
        nodePath.setTwoSided(True)
        
        #Create the Plane that you get hi by if you fall down
        self.plane = OdePlaneGeom(self.space,0,0,1,-50)
        self.plane.setCollideBits(0)
        self.plane.setCategoryBits(1)

        self.arrows = loader.loadModel("data/models/arrows.egg")
        self.arrows.reparentTo(render)
        self.arrows.setPos(0,0,0)
        
        self.arrows2 = loader.loadModel("data/models/arrows.egg")
        self.arrows2.reparentTo(render)
        self.arrows2.setPos(0,60,0)
        
        #self.addPlayer(self.devices.devices[0])

        #Load the Map
        self.map = self.loader.loadModel("data/models/Track01")
        self.map.reparentTo(self.render)
        self.map.setScale(10, 10, 10)
        self.map.setPos(0, 10, -7)

        #add collision with the map
        groundGeom = OdeTriMeshGeom(self.space, OdeTriMeshData(nodePath, True))
        groundGeom.setCollideBits(0)
        groundGeom.setCategoryBits(3)

        #Load the Players
        ##probably unnecessary because the players are already initialized at this point

        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))

        #start the gametask
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
            for ray in player.vehicle.collision_rays:
                #print geom1.compareTo(ray)
                #print geom2.compareTo(ray)
                if geom1 == ray or geom2 == ray:
                    normal = entry.getContactGeom(0).getNormal()
                    player.vehicle.physics_model.setGravityMode(0) #disable gravity if on the track
                    force_pos = ray.getPosition()
                    contact = entry.getContactPoint(0)
                    force_dir = force_pos - contact
                    acceleration = (ray.getLength()/2-force_dir.length())#calculate the direction
                    mass = player.vehicle.physics_model.getMass().getMagnitude()
                    player.vehicle.hit_ground = True
                    if acceleration > 0:
                        force_dir.normalize()
                        force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
                        player.vehicle.physics_model.addForceAtPos(force_dir*mass, force_pos)
                        #dir = player.vehicle.collision_model.getQuaternion().xform(Vec3(-1,0,0))
                        #force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
                    else:
                        force_dir.normalize()
                        force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
                        player.vehicle.physics_model.addForce(force_dir*mass)
                    #player.vehicle.physics_model.setTorque(player.vehicle.physics_model.getAngularVel()*0.01)
                    #player.vehicle.physics_model.addTorque(player.vehicle.physics_model.getAngularVel()*-1)
                    return

        #workaround until panda 1.7.1
        #if the player collides with the ground plane he will get reset to the starting position        
        for player in self.players:
            if geom1.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body2) == 0:
                player.vehicle.physics_model.setPosition(0,0,20)
                return
            if geom2.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body1) == 0:
                player.vehicle.physics_model.setPosition(0,0,20)
                #body1.setPosition(0,0,20)
                return

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

    def menuTask(self, task):
        '''
        this task runs once per second if we are in game menu
        '''
        pass

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()




