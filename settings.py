# -*- coding: utf-8 -*-
##############################################################
## this module contains a class to save and load the
## application's settings and configuration
##############################################################

from configobj import ConfigObj
from direct.directnotify.DirectNotify import DirectNotify

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class Settings(object):
    '''
    This class represents a joystick and holds the pygame data
    '''
    def __init__(self):
        '''
        this class is able to load and save the application's settings
        '''
        self._notify = DirectNotify().newCategory("Settings")
        self._notify.info("New Settings-Object created: %s" %(self))
        self.width = 800
        self.height = 600

        self.fullscreen = False
        self._input_settings = {"keyboard" : {},
                                "joysticks" : {}
                                }

    # ---------------------------------------------------------

    def saveSettings(self, filename):
        '''
        '''
        config = ConfigObj()
        config.filename = filename

        config["application"] = {}
        #config["application"]["resolution"] = "%dx%d"%(self.width, self.height)
        config["application"]["resolution"] = [str(self.width), str(self.height)]
        config["application"]["fullscreen"] = str(int(self.fullscreen))

        config["joysticks"] = {}

        config.write()


    # ---------------------------------------------------------

    def loadSettings(self, filename):
        '''
        '''
        config = ConfigObj(filename)
        #
        self.width = int(config["application"]["resolution"][0])
        self.height = int(config["application"]["resolution"][1])
        self.fullscreen = bool(int(config["application"]["fullscreen"]))

        self._input_settings = {"joysticks": config["joysticks"],
                                "keyboard": config["keyboard"]
                                }

    # ---------------------------------------------------------

    def getInputSettings(self):
        '''
        '''
        return self._input_settings

    # ---------------------------------------------------------



# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------






if __name__ == "__main__":
    settings = Settings()
    #settings.saveSettings("user/config.ini")
    settings.loadSettings("user/config.ini")
    print settings.fullscreen
    print settings.width, settings.height
