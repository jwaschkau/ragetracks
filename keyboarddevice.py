# _*_ coding: UTF-8 _*_
##############################################################
## this module wraps around the panda keybpard event handling
## and holds the information about all (un-) pressed keys
##############################################################

import generaldevice

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class KeyboardDevice(generaldevice.GeneralDevice):
    '''
    This class holds data about the keyboard
    '''
    def __init__(self):
        '''
        '''
        self.keys = {"esc": False
                    }

    # ---------------------------------------------------------

    def fetchEvents(self):
        '''
        this function gets the events from panda
        '''
        # catch all keyboard events from panda
        pass # should be done here

    # ---------------------------------------------------------


if __name__ == "__main__":
    k = KeyboardDevice()
    while True:
        k.fetchEvents()
