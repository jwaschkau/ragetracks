# _*_ coding: UTF-8 _*_
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
import menu
import settings
import player
import splitScreen
import vehicledata #holds the data of vehicles


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        base.setFrameRateMeter(True) #Show the Framerate
        
        #Initialize needed variables and objects
        self.players = [] #holds the player objects
        self.vehicledata = vehicledata.VehicleData()
        
        #Initialize Physics (ODE)
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -0.5) 
        
        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        #Initialize the surface-table, it defines how objects interact with each other
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        self.space.setAutoCollideWorld(self.world)##use autocollision?
        
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)

        #Initialize the first player
        self.addPlayer("Tastaturdevice") ##pass the device for the first player (probably the keyboard)

        # try to read the ini-file. If it fails the settings class
        # automatically contains default values
        self.settings = settings.Settings()
        try:
            self.settings.loadSettings("user/config.ini")
        except:
            pass    # so here is nothing to do


        # Add the main menu (though this is only temporary:
        # the menu should me a member-variable, not a local one)
        #m = menu.Menu()
        #m.addOption("NewGame", self.newGame)
        #m.addOption("AddPlayer", self.addPlayer)

        #Start the Game for testing purpose
        self.newGame()

    # -----------------------------------------------------------------

    def addPlayer(self, device):
        '''
        creates a new player object, initializes it and sorts the cameras on the screen
        '''    
        #Create a new player object
        self.players.append(player.Player(len(self.players),self.world, self.space, device, base.makeCamera(base.win,1), self.vehicledata))
        
        #sort the cameras
        #self.splitScreen.reRegion(self.players)
        
    # -----------------------------------------------------------------
    
    def removePlayer(self, number):
        '''
        deletes a player object and sorts the cameras on the screem
        '''
        
        #delete the player
        for player in self.players:
            if player.getNumber() == number:
                self.players.remove(player) ##all objects must be deleted!
                
        #sort the cameras
            
    # -----------------------------------------------------------------
    
    def newGame(self):
        '''
        starts the game or goes to the next menu
        '''
        
        print "bla"
        
        #Load the Map
        self.map = self.loader.loadModel("data/models/Track01")
        self.map.reparentTo(self.render)
        self.map.setScale(10, 10, 10)
        self.map.setPos(0, 0, 0)
        
        #add collision with the map
        #OdeTriMeshGeom(self.space, OdeTriMeshData(self.map, True))
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))

        
        #Load the Players
        ##probably unnecessary because the players are already initialized at this point
        
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))       
        
        #start the gametask
        taskMgr.add(self.gameTask, "gameTask")

        

    # -----------------------------------------------------------------

    def gameTask(self, task):
        '''
        this task runs once per second if the game is running
        '''
        #calculate the physics
        self.space.autoCollide() # Setup the contact joints
        self.world.quickStep(globalClock.getDt())   # Step the simulation and set the new positions
        for player in self.players:                      # set new positions
            player.getVehicle().getModel().setPosQuat(render, player.getVehicle().getPhysicsModel().getPosition(), Quat(player.getVehicle().getPhysicsModel().getQuaternion()))
        self.contactgroup.empty() # Clear the contact joints
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

# this code is only executed if the module is executed and not imported
if __name__ == "__main__":
    game = Game()
    game.run()




