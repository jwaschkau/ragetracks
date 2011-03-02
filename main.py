# -*- coding: utf-8 -*-
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from pandac.PandaModules import * #Load all PandaModules
from panda3d.core import loadPrcFileData
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.ParticleInterval import ParticleInterval 
from direct.filter.CommonFilters import CommonFilters
import settings
import inputdevice
import player
import splitscreen
from playercam import PlayerCam
import gettext
import sys
import random
from menu import Menu
from menu import MainMenu
from kdtree import KDTree
import time
import trackgen3d
from vlc import VLC


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self, *args):
        '''
        '''
        #loadPrcFileData("", "fullscreen 0\n win-size 1280 720")
        #loadPrcFileData("", "want-pstats 1\n pstats-host 127.0.0.1\n pstats-tasks 1\n task-timer-verbose 1")
##        loadPrcFileData("", "sync-video #f")
        loadPrcFileData("", "default-directnotify-level debug\n notify-level-x11display fatal\n notify-level-Game debug\n notify-level-Menu debug\n notify-level-Vehicle debug")
        ShowBase.__init__(self)
        ##base.toggleWireframe()
        
        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("New Game-Object created: %s" %(self))
        
        base.setBackgroundColor(0,0,0)
##        base.setFrameRateMeter(True) #Show the Framerate
        base.camNode.setActive(False) #disable default cam
        self.disableMouse() #disable manual camera-control
##        render.setShaderAuto()
        
        #Laps
        self.laps = 3 #the Laps
        self.starttime = 0 #Time the Game starts
        self.winingPlayer = 0

        # load the settings
        self.settings = settings.Settings()
        self.settings.loadSettings("user/config.ini")
        gettext.install("ragetracks", "data/language")#, unicode=True) #installs the system language
        #trans = gettext.translation("ragetracks", "data/language", ["de"]) #installs choosen language
        #trans.install() #usage: print _("Hallo Welt")

        #Fullscreen
        if self.settings.fullscreen:
            wp = WindowProperties()
            wp.setFullscreen(self.settings.fullscreen)
            wp.setOrigin(0,0)
            wp.setTitle("RageTracks")
            wp.setSize(int(base.pipe.getDisplayWidth()),int(base.pipe.getDisplayHeight()))
            base.win.requestProperties(wp)
        
        #enable anti-aliasing
        if self.settings.antialias:
            loadPrcFileData("", "framebuffer-multisample 1\n multisamples 2")
            render.setAntialias(AntialiasAttrib.MMultisample)
        
        #Initialize needed variables and objects
        self.players = [] #holds the player objects
        self.TRACK_GRIP = 0.5
        self.LINEAR_FRICTION = 0.02
        self.ANGULAR_FRICTION = 0.02
        self.splitscreen = splitscreen.SplitScreen(0)

        #Initialize Physics (ODE)
        self.world = OdeWorld()
        self.deltaTimeAccumulator = 0.0 #this variable is necessary to track the time for the physics
        self.stepSize = 1.0 / 100.0 # This stepSize makes the simulation run at 60 frames per second

        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        #Initialize the surface-table, it defines how objects interact with each other
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 100.0, 100.1, 0.9, 0.00001, 0.0, 0.002)
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
        
        # initialize the input devices
        self.devices = inputdevice.InputDevices(self.settings.getInputSettings())

        #render.setShaderAuto()
        startgame = True
        #Start the Game
        for arg in sys.argv:
            if  arg == "--ep":
                startgame = False
                if sys.argv[sys.argv.index(arg)+1] == "startGame":
                        player = self.addPlayer(self.devices.devices[-1])
                        import glob
                        self.vehicle_list = glob.glob("data/models/vehicles/*.egg")
                        #start loading the model

                        base.enableParticles()
                        n = 0
                        if len(sys.argv) >= sys.argv.index(arg)+3:
                            try:
                                n = int(sys.argv[sys.argv.index(arg)+2])
                            except:
                                n = 0
                            if n >= len(self.vehicle_list):
                                n = 0
                        self.players[0].setVehicle(loader.loadModel(self.vehicle_list[n]))
                       
                        taskMgr.add(self.devices.fetchEvents, "fetchEvents")
                        track =  trackgen3d.Track3d(1000, 1800, 1600, 1200, 5)#len(self._players))
                        streetPath = render.attachNewNode(track.createRoadMesh())
                        borderleftPath = render.attachNewNode(track.createBorderLeftMesh())
                        borderrightPath = render.attachNewNode(track.createBorderRightMesh())
                        borderleftcollisionPath = NodePath(track.createBorderLeftCollisionMesh())
                        borderrightcollisionPath = NodePath(track.createBorderRightCollisionMesh())
                        
                        textures = ["tube", "tube2", "street"]
                        tex = textures[random.randint(0, len(textures)-1)]
                        roadtex = loader.loadTexture('data/textures/'+tex+'.png')
                        bordertex = loader.loadTexture('data/textures/border.png')
                        streetPath.setTexture(roadtex)
                        borderleftPath.setTexture(bordertex)
                        borderrightPath.setTexture(bordertex)
                        
                        self.startGame(streetPath,borderleftPath,borderrightPath, track.trackpoints, borderleftcollisionPath, borderrightcollisionPath)
            if  arg == "--PSt":
                PStatClient.connect() #activate to start performance measuring with pstats
            if  arg == "--wire":    
                base.toggleWireframe()
                
        if startgame:   
            myMenu = Menu(self)
            taskMgr.add(self.devices.fetchEvents, "fetchEvents")
            myMenu.showStartScreen()
        
        base.accept("tab-up", self.takeScreenshot)
    
    # -----------------------------------------------------------------

    def takeScreenshot(self):
        '''
        '''
        self.screenshot(source=base.win)

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
    
    def createTrackpointTree(self, trackpoints):
        '''
        Create a tree out of the trackpoints
        '''
        self.track_tupel_list = []
        #Change from Vec3 to tupel
        for point in self.trackpoints:
            self.track_tupel_list.append((point.getX(), point.getY(), point.getZ()))
        self.list4tree = self.track_tupel_list[:]
        return KDTree.construct_from_data(self.list4tree)
            
    
    # -----------------------------------------------------------------

    def startGame(self, track, borderl, borderr, trackpoints, borderlcoll, borderrcoll):
        '''
        Start the game
        '''
        #Create the KDTree for the position determination
        self.trackpoints = trackpoints #The mid points of the street for position calculation
        self.TrackpointTree = self.createTrackpointTree(self.trackpoints) 
        
        
        self._notify = DirectNotify().newCategory("Game")
        self._notify.info("Initializing start game")
        #Initialize needed variables
        self.sparks = []
        
        counter = 0
        for player in self.players:
            player.activateGameCam()
            self.players[counter].vehicle.physics_model.setPosition(0, -20 * counter, 10)
            self.players[counter].vehicle.model.setScale(2)
            self.players[counter].vehicle.model.setH(0)
            self.players[counter].vehicle.model.setP(0)
            self.players[counter].vehicle.model.setR(0)
            self.players[counter].vehicle.physics_model.setQuaternion(self.players[counter].vehicle.model.getQuat(render))
##            print "#####!!!!!####", self.players[counter].vehicle.getBoostStrength()
            self.players[counter].vehicle.setBoostStrength(1000)
            counter+=1
        
        #Add the Skybox
        self.skybox = self.loader.loadModel("data/models/skybox.egg")
        t = Texture()
        boxes = ["space", "city", "ocean"]
        box = boxes[random.randint(0, len(boxes)-1)]
        t.load(PNMImage("data/textures/skybox_"+box+".png"))
        self.skybox.setTexture(t)
        self.skybox.setBin("background", 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setDepthTest(0)
        self.skybox.setLightOff()
        self.skybox.setScale(10000)
        self.skybox.reparentTo(render)
        
        #Create the Track
        self.track = track
        self.track.reparentTo(render)
        
        self.borderl = borderl
        self.borderl.reparentTo(render)
        
        self.borderr = borderr
        self.borderr.reparentTo(render)
        
        self.borderlcoll = borderlcoll
        self.borderrcoll = borderrcoll
##        self.borderlcoll.reparentTo(render)
##        self.borderrcoll.reparentTo(render)
        
##        roadtex = loader.loadTexture('data/textures/street.png')
####        roadtex = loader.loadTexture('data/textures/tube.png')
##        bordertex = loader.loadTexture('data/textures/border.png')
##        self.track.setTexture(roadtex)
##        self.borderl.setTexture(bordertex)
##        self.borderr.setTexture(bordertex)

        # createVLC
        self.vlcs = []
        
        for i in xrange(5):
            vlc = VLC(self.space)
            vlc.reparentTo(render)
            vlc.setPosition(-30+i*10,40,5)
            self.vlcs.append(vlc)
        
        self.rings = []
        y = 100
        for i in xrange(4):
            ring = loader.loadModel("data/models/ring.egg")
            ring.setScale(34)
            #ring.setZ(-15)
            ring.setY(y)
            y += 30
            ring.setTransparency(TransparencyAttrib.MAlpha) 
            ring.setLightOff()
            ring.reparentTo(render)
            self.rings.append(ring)

        taskMgr.add(self.turnRings, "turnRings")
        
        #add collision with the map
        self.groundGeom = OdeTriMeshGeom(self.space, OdeTriMeshData(self.track, True))
        self.groundGeom.setCollideBits(0)
        self.groundGeom.setCategoryBits(1)
        
        self.borderl = OdeTriMeshGeom(self.space, OdeTriMeshData(self.borderlcoll, True))
        self.borderl.setCollideBits(0)
        self.borderl.setCategoryBits(0)
        
        self.borderr = OdeTriMeshGeom(self.space, OdeTriMeshData(self.borderrcoll, True))
        self.borderr.setCollideBits(0)
        self.borderr.setCategoryBits(0)
        
        #Create the Plane that you get hit by if you fall down
        self.plane = OdePlaneGeom(self.space,0,0,1,-250)
        self.plane.setCollideBits(0)
        self.plane.setCategoryBits(4)

        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))
        
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(10.0, 10.0, 10.0, 1))
        if (base.win.getGsg().getSupportsBasicShaders() != 0):
            pass
            ##dlight.setShadowCaster(True, 2048, 2048) #enable shadows for this light ##TODO wegen Linux
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        self.space.setCollisionEvent("ode-collision")
        base.accept("ode-collision", self.onCollision)


        #start the gametask
        self._notify.debug("Starting gameTask")
        taskMgr.add(self.gameTask, "gameTask")
        self._notify.debug("Start Pos Calc")
        self.pos_vehicle = 0
        taskMgr.add(self.calculatePos, "calculatePos")
        taskMgr.add(self.updatePos, "updatePos")
        self.world.setGravity(0, 0, -90.81)
        self._notify.info("Start game initialized")
        #set up the collision event
        
        self.starttime = time.time()

    # -----------------------------------------------------------------

    def onCollision(self, entry):
        '''
        Handles Collision-Events
        '''
        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()
        body1 = entry.getBody1()
        body2 = entry.getBody2()
                     
        for player in self.players:
            
##            if geom1.compareTo(player.vehicle.getFrontRay().getRay()) or geom2.compareTo(player.vehicle.getFrontRay().getRay()):
##                ###slipstream doesnt work but why?
##                #if player.device.boost:
##                player.vehicle.setBoost(player.vehicle.getBoostStrength()*0.2)

            #workaround until panda 1.7.1
            #if the player collides with the ground plane he will get reset to the starting position
            if geom1.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body2) == 0 or geom2.compareTo(self.plane) == 0 and player.vehicle.physics_model.compareTo(body1) == 0:
                player.vehicle.physics_model.setPosition(0,0,20)
                player.vehicle.physics_model.setLinearVel(0,0,0)
                player.vehicle.physics_model.setTorque (0,0,0)
                player.vehicle.physics_model.setRotation(Mat3.rotateMat(0,(Vec3(0,0,1))))
                return
            
            #Decrease energy on collision
            elif player.vehicle.physics_model.compareTo(body1) == 0 or player.vehicle.physics_model.compareTo(body2) == 0:
                player.vehicle.energy -= player.vehicle.physics_model.getLinearVel().length() * 0.1
                player.updateOSD()
    # -----------------------------------------------------------------

    def onRayCollision(self, entry, player):
        '''
        Handles Collision-Events with the street
        '''
        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()
        body1 = entry.getBody1()
        body2 = entry.getBody2()
        ray = player.vehicle.ray.getRay()
        normal = Vec3(entry.getContactGeom(0).getNormal())
        normal.normalize()
        player.vehicle.streetnormal = normal
        player.vehicle.physics_model.setGravityMode(0) #disable gravity if on the track
        mass = player.vehicle.physics_model.getMass().getMagnitude()                    
        force_pos = ray.getPosition()
        contact = entry.getContactPoint(0)
        force_dir = force_pos - contact
        
        linear_velocity = player.vehicle.physics_model.getLinearVel() 
        z_direction = player.vehicle.collision_model.getQuaternion().xform(Vec3(0,0,1)) 
        actual_speed = Vec3(linear_velocity[0]*z_direction[0],linear_velocity[1]*z_direction[1],linear_velocity[2]*z_direction[2])
        
        acceleration = ((ray.getLength()/2)-force_dir.length())*actual_speed.length()*2.5#calculate the direction
        player.vehicle.hit_ground = True
        player.vehicle.collision_model.setCollideBits(6)
        #force_dir.normalize()

        #Change the angle of the vehicle so it matches the street
        upvec = Vec3(player.vehicle.collision_model.getQuaternion().xform(Vec3(0,0,1)))
        player.vehicle.physics_model.addTorque(upvec.cross(normal)*mass*upvec.angleDeg(normal) - player.vehicle.physics_model.getAngularVel() * mass)
        if upvec.cross(normal).length() != 0:
##            rotation = Mat3.rotateMat(upvec.angleDeg(normal),upvec.cross(normal))
##            protation=player.vehicle.physics_model.getRotation()
##            protation*=rotation
##            player.vehicle.collision_model.setRotation(protation)
##            
            upvec = Vec3(player.vehicle.collision_model.getQuaternion().xform(Vec3(0,0,1)))
            player.vehicle.collision_model.setPosition(contact+(upvec*force_dir.length()))
        
        #checks if the vehicle is moving to or away from the road
        if (z_direction + actual_speed).length() < actual_speed.length():goes_up = True
        else: goes_up = False
        
        needs_boost = 0
        #calculates the needed boost based on the actual moving direction
        if goes_up:
            if actual_speed.length() < acceleration:
                needs_boost = acceleration - actual_speed.length()
            else:
                needs_boost = acceleration + actual_speed.length()
        else:
            if - actual_speed.length() < acceleration:
                needs_boost = acceleration + actual_speed.length()
            else:
                needs_boost = acceleration - actual_speed.length()

        #push the vehicle
        if needs_boost > 0:
            force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
            player.vehicle.physics_model.addForce(force_dir*mass)
        
        #pull the vehicle
        elif needs_boost:
            force_dir = Vec3(normal[0]*acceleration,normal[1]*acceleration,normal[2]*acceleration)
            player.vehicle.physics_model.addForce(force_dir*mass)
        return
    # -----------------------------------------------------------------       

    def onFrontRayCollision(self, entry, player): 
        '''
        handles extreme changes in height
        collision with the street the vehicle needs to get lifted
        '''
        normal = entry.getContactGeom(0).getNormal()
        mass = player.vehicle.physics_model.getMass().getMagnitude()
        speed = player.vehicle.speed
        #if speed > 5: speed = 5
        upvec = Vec3(player.vehicle.collision_model.getQuaternion().xform(Vec3(0,0,1)))
        player.vehicle.physics_model.addTorque(upvec.cross(normal)*mass*3*upvec.angleDeg(Vec3(normal)) - player.vehicle.physics_model.getAngularVel() * mass)
    
        # -----------------------------------------------------------------       

    def onBorderCollision(self, entry, player): 
        '''
        handles collisions with the border
        '''
        normal = entry.getContactGeom(0).getNormal()
        #player.vehicle.physics_model.addForce(player.vehicle.speed*player.vehicle.weight)
        #return
        needed_rotation = 90-Vec3(normal).angleDeg(player.vehicle.direction)
        
        rotation = Mat3.rotateMat(needed_rotation,player.vehicle.direction)
        force = rotation.xform(normal)
        
        player.vehicle.physics_model.addTorque(player.vehicle.direction.cross(force)*100- player.vehicle.physics_model.getAngularVel())
        player.vehicle.physics_model.addForce(force*player.vehicle.physics_model.getLinearVel().length()*player.vehicle.weight*50)      
        player.vehicle.physics_model.addForce(-(player.vehicle.physics_model.getLinearVel()*player.vehicle.weight*50))          
        
    # -----------------------------------------------------------------
    
    def onVlcCollision(self, entry, player): 
        '''
        handles collisions with vlcs
        '''
        normal = entry.getContactGeom(0).getNormal()
        #player.vehicle.physics_model.addForce(player.vehicle.speed*player.vehicle.weight)
        #return
        needed_rotation = 90-Vec3(normal).angleDeg(player.vehicle.direction)
        
        rotation = Mat3.rotateMat(needed_rotation,player.vehicle.direction)
        force = rotation.xform(normal)
        
        player.vehicle.physics_model.addTorque(player.vehicle.direction.cross(force)*100- player.vehicle.physics_model.getAngularVel())
        player.vehicle.physics_model.addForce(force*player.vehicle.physics_model.getLinearVel().length()*player.vehicle.weight*50)      
        player.vehicle.physics_model.addForce(-(player.vehicle.physics_model.getLinearVel()*player.vehicle.weight*50))          
        
    # -----------------------------------------------------------------

    def calculatePos(self, task):
        '''
        Appropriate the players position
        '''
        task.delayTime = 0.1    ##TODO set value ca. 0.5
        self.players[self.pos_vehicle].pre_position = self.players[self.pos_vehicle].position
        self.pos_vehicle = (self.pos_vehicle + 1) % len(self.players)
        pos = self.TrackpointTree.query(query_point=(self.players[self.pos_vehicle].getVehicle().getPos()), t=1)
        self.players[self.pos_vehicle].position = self.track_tupel_list.index(pos[0])
        #print (self.players[self.pos_vehicle].position - self.players[self.pos_vehicle].pre_position)

        #updateLaps
        if ((self.players[self.pos_vehicle].position - self.players[self.pos_vehicle].pre_position) <= -800):
            self.players[self.pos_vehicle].lap += 1
            #Check if one Wins
            if (self.players[self.pos_vehicle].lap == self.laps + 1): #+1 because it starts at 1
                print "Player", self.players[self.pos_vehicle].number, "Time:" , time.time() - self.starttime
                self.players[self.pos_vehicle].time = time.time() - self.starttime
                self.winingPlayer += 1
                if self.winingPlayer >= 3 or self.winingPlayer >= len(self.players) :
                    print "Game Finish"
            self._notify.debug(self.players[self.pos_vehicle].lap )
        if ((self.players[self.pos_vehicle].position - self.players[self.pos_vehicle].pre_position) >= 800):
            self.players[self.pos_vehicle].lap -= 1
            #self._notify.debug( self.players[self.pos_vehicle].lap )
        #self._notify.debug( ("Player", self.pos_vehicle,":", self.track_tupel_list.index(pos[0])))
        #self._notify.debug( self.players[self.pos_vehicle].getVehicle().getPos())
        return task.again
    
    # -----------------------------------------------------------------
    
    def updatePos(self, task):
        '''
        Set the rank for each player
        '''
        task.delayTime = 0.1    ##TODO set value ca. 0.5
        positionen = []
        for player in self.players:
            positionen.append(player.position)
        positionen.sort()
        for player in self.players:
            player.rank = positionen.index(player.position)
            #self._notify.debug( ("PlayerRank", player.rank ))
        return task.again
    
    # -----------------------------------------------------------------
    
    def gameTask(self, task):
        '''
        this task runs once per frame if the game is running
        And calculate the physics
        '''
        #self.space.autoCollide() # Setup the contact joints

        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize: # Step the simulation
            for player in self.players:
                player.doStep() #refresh player specific things (rays)
                #get the player input and set the forces
                if player.device.boost:
                    player.vehicle.setBoost()
                else:
                    player.vehicle.stopBlowout()
                    
                if player.device.directions[0] != 0 or player.device.directions[1] != 0:
                    player.vehicle.direction = player.device.directions
                linear_velocity = player.vehicle.physics_model.getLinearVel()
                angular_velocity = player.vehicle.physics_model.getAngularVel()
                mass = player.vehicle.physics_model.getMass().getMagnitude()

                #calculate airresistance to get energy out of the ode-system
                player.vehicle.physics_model.addForce(linear_velocity*-self.LINEAR_FRICTION*mass)
                player.vehicle.physics_model.addTorque(angular_velocity*-self.ANGULAR_FRICTION*mass)
                
                #calculate the ray
                col = OdeUtil.collide(player.vehicle.ray.getRay(), self.groundGeom)
                if not col.isEmpty():
                    self.onRayCollision(col, player)#handles collisions from the ray with the street
                
                col = OdeUtil.collide(player.vehicle.frontray.getRay(), self.groundGeom)
                if not col.isEmpty():
                    self.onFrontRayCollision(col, player)
                
                #Collision with the border    
                col = OdeUtil.collide(player.vehicle.collision_model, self.borderr)
                if not col.isEmpty():
                    self.onBorderCollision(col, player)
                else :
                    col = OdeUtil.collide(player.vehicle.collision_model, self.borderl)
                    if not col.isEmpty():
                        self.onBorderCollision(col, player)
                
                for vlc in self.vlcs:
                    col = OdeUtil.collide(player.vehicle.collision_model, vlc.getGeom())
                    if not col.isEmpty():
                        self.onBorderCollision(col, player)

            self.deltaTimeAccumulator -= self.stepSize # Remove a stepSize from the accumulator until the accumulated time is less than the stepsize
            self.space.autoCollide() # Setup the contact joints
            self.world.quickStep(self.stepSize)
            self.contactgroup.empty() # Clear the contact joints
        for player in self.players: # set new rank
            player.updatePlayer()
        return task.cont
    # -----------------------------------------------------------------
    
    def turnRings(self, task):
        '''
        '''
        speeds = [.2,-.5,.7,-.3]
        for i in xrange(len(self.rings)):
            self.rings[i].setR(self.rings[i].getR()+speeds[i])
        return task.cont

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

game = Game()
game.run()