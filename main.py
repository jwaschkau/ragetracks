# _*_ coding: UTF-8 _*_
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
import menu
import settings
import player

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
        for player in self.players:
            player.vehicle.getModel().setScale(1, 1, 1)
            player.vehicle.getModel().setPos(0, 0, 3)
        
        #Load the Cameras
        for player in self.players:
            player.getCamera().reparentTo(player.vehicle.getModel())
            player.getCamera().camera.setPos(0,-30,10)
            player.getCamera().lookAt(player.vehicle.getModel())   
        
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))
        
        #Initialize Physics
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        
        for player in self.players:
            player.getVehicle().setPhysicsModel(OdeBody(world))
            player.getVehicle().setPhysicsModel().setPosition(self.player.getVehicle().getModel().getPos(render))
            player.getVehicle().setPhysicsModel().setQuaternion(self.player.getVehicle().getModel().getQuat(render))
            player.getVehicle().setPhysicsMass(OdeMass())
            player.getVehicle().getPhysicsMass().setBox(11340, 1, 1, 1)
            player.getVehicle().getPhysicsModel().setMass(player.getVehicle().getPhysicsMass())
        
        
        #Initialize Collisions

        

    # -----------------------------------------------------------------

    def gametask(self, task):
        '''
        this task runs once per second if the game is running
        '''
        pass

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




