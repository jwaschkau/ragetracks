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
        #Load the Players
        #Load the Cameras
        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))
        #Initialize Physics
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




