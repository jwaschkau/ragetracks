# _*_ coding: UTF-8 _*_
###########################################################
## this module holds the keyboard and joystick devices
###########################################################

import keyboarddevice
import joystickdevice

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class InputDevice(object):
    '''
    '''
    def __init__(self, device, settings):
        '''
        '''
        self.device = device
        self.directions = [0,0]  # x and y movement
        self.boost = False       # Button for boosting
        self.use_item = False    # Button for using items

        if self.device.getName() in settings:
            pass
        else:
            self.settings = {"directions":  None,
                             "boost":       None,
                             "use_item":    None,
                             "accelerator": None,
                             "brake":       None}

        self._initFunctions()

    # ---------------------------------------------------------

    def _initFunctions(self):
        '''
        '''

        # settings should be loaded here

        # if the input device is a joystick
        if type(self.device) == joystickdevice.JoystickDevice:

            # if we have at least two axes, the player is controlled by them
            if self.device.getAxisCount() >= 2:
                self.settings["directions"] = ("AXES", 0,1)
            # if there is only one or less axes we have to use the cooliehat
            elif self.device.getHatCount() >= 1:
                self.settings["directions"] = ("HAT", 0)
            # if there isn't a hat either, the device can't be used
            else:
                raise StandardError("the Joystick Device has no useable axes or hats")

            if self.device.getButtonCount() >= 4:
                self.settings["boost"]       = 0
                self.settings["use_item"]    = 2
                self.settings["accelerator"] = ("BUTTON", 1)
                self.settings["brake"]       = ("BUTTON", 3)
            #elif self.device.getButtonCount() >= 2:
            #    self.settings["boost"]       = 0
            #    self.settings["use_item"]    = 2

        # if the input device is the keyboard
        elif type(self.device) == keyboarddevice.KeyboardDevice:
            pass

    # ---------------------------------------------------------

    def noticeAction(self):
        '''
        '''
        print self.directions, " - boost:", self.boost, " - use_item:", self.use_item

    # ---------------------------------------------------------

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class InputDevices(object):
    '''
    '''
    def __init__(self, keyboard, joysticks, settings):
        '''
        @param keyboard: = (KeyboardDevice) keyboard
        @param joysticks: = (JoystickDevices) joysicks
        '''
        self.id = 0
        self.keyboard = keyboard
        self.joysticks = joysticks

        self.devices = []

        for joystick in self.joysticks.getJoysticks():
            self.devices.append(InputDevice(joystick))

    # ---------------------------------------------------------

    def fetchEvents(self):
        '''
        '''
        self.keyboard.fetchEvents()
        self.joysticks.fetchEvents()

        for device in self.devices:
            device.noticeAction()

    # ---------------------------------------------------------



if __name__ == "__main__":


    import time
    import settings

    conf = settings.Settings()
    conf.loadSettings("user/config.ini")

    i = InputDevices(keyboarddevice.KeyboardDevice(), joystickdevice.JoystickDevices(), conf["joysticks"])

    while True:
        i.fetchEvents()
        time.sleep(1)
