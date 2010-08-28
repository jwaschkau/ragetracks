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
        
        #Initialize needed variables and objects
        self.players = [] #holds the player objects
        self.vehicledata = vehicledata.VehicleData()
        
        #Initialize Physics (ODE)
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81) 
        
        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        ##use autocollision? -->then the collision map must be created

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
        #m.addOption("New Game", self.newGame)

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
        
        #Load the Map
        self.map = self.loader.loadModel("data/models/Track01")
        self.map.reparentTo(self.render)
        self.map.setScale(10, 10, 10)
        self.map.setPos(0, 0, 0)
        
        #Load the Players
        ##probably unnecessary because the players are already initialized at this point
        
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))       
        
        #load physics
        #the following code should be executed in the vehicle-class
        
        #for player in self.players:
        #    player.getVehicle().setPhysicsModel(OdeBody(world))
        #    player.getVehicle().setPhysicsModel().setPosition(self.player.getVehicle().getModel().getPos(render))
        #    player.getVehicle().setPhysicsModel().setQuaternion(self.player.getVehicle().getModel().getQuat(render))
        #    player.getVehicle().setPhysicsMass(OdeMass())
        #    player.getVehicle().getPhysicsMass().setBox(11340, 1, 1, 1)
        #    player.getVehicle().getPhysicsModel().setMass(player.getVehicle().getPhysicsMass())
        
        
        #Initialize Collisions
        #this should be executed in the vehicle-class

        

    # -----------------------------------------------------------------

    def gametask(self, task):
        '''
        this task runs once per second if the game is running
        '''
        #calculate the physics
        self.world.quickStep(globalClock.getDt())   # Step the simulation and set the new positions
        for player in players:                      # set new positions
            player.getVehicle().getModel().setPosQuat(render, player.getVehicle().physicsModel().getPosition(), Quat(player.getVehicle().physicsModel().getQuaternion()))
        return task.cont
    # -----------------------------------------------------------------

    def menutask(self, task):
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




