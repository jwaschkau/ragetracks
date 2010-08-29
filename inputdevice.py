# _*_ coding: UTF-8 _*_
###########################################################
## this module holds the keyboard and joystick devices
###########################################################

from panda3d.core import *
import pygame
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

        # if this is a Joystick, look if there are Settings for Joysticks with this name
        if type(self.device) == joystickdevice.JoystickDevice:
            if self.device.getName() in settings["joysticks"]:
                self.settings = settings["joysticks"][self.device.getName()]
            else:
                self.settings = {}
                self._setStandardSettings()

        # Keyboard settings are always available
        else:
            #self.settings = settings["keyboard"]
            self.settings = {}
            self.settings["boost"]      = "space"
            self.settings["use_item"]   = "lalt"
            self.settings["up"]         = "arrow_up"
            self.settings["down"]       = "arrow_down"
            self.settings["left"]       = "arrow_left"
            self.settings["right"]      = "arrow_right"


            self.device.keys[self.settings["up"]] = False
            self.device.keys[self.settings["down"]] = False
            self.device.keys[self.settings["left"]] = False
            self.device.keys[self.settings["right"]] = False
            self.device.keys[self.settings["boost"]] = False
            self.device.keys[self.settings["use_item"]] = False

    # ---------------------------------------------------------

    def _setStandardSettings(self):
        '''
        if the input device is a joystick and no settings are available, this method analyzes the
        kind of the Joystick and tries to find a senseful configuration
        '''
        # if we have at least two axes, the player is controlled by them
        if self.device.getAxisCount() >= 2:
            self.settings["directions"] = ("AXIS", 0)
        # if there is only one or less axes we have to use the cooliehat
        elif self.device.getHatCount() >= 1:
            self.settings["directions"] = ("HAT", 0)
        # if there isn't a hat either, the device can't be used
        else:
            raise StandardError("the Joystick device has no useable axes or hats")

        # if four or more buttons are available, use the buttons for breakting and accelerating, too
        if self.device.getButtonCount() >= 4:
            self.settings["boost"]       = ("BUTTON", 0)
            self.settings["use_item"]    = ("BUTTON", 2)
            self.settings["accelerator"] = ("BUTTON", 1)
            self.settings["brake"]       = ("BUTTON", 3)

        # if only two or three buttons and two axes are available, use the y-axis for breakting and accelerating
        elif self.device.getButtonCount() >= 2 and self.device.getAxisCount() >= 2:
            self.settings["boost"]       = ("BUTTON", 0)
            self.settings["use_item"]    = ("BUTTON", 1)
            self.settings["accelerator"] = ("AXIS", 0)
            self.settings["brake"]       = ("AXIS", 0)

        # if only two or three buttons and a hat is available, use the y-axis of it for breakting and accelerating
        elif self.device.getButtonCount() >= 2 and self.device.getHatCount() >= 1:
            self.settings["boost"]       = ("BUTTON", 0)
            self.settings["use_item"]    = ("BUTTON", 1)
            self.settings["accelerator"] = ("HAT", 0)
            self.settings["brake"]       = ("HAT", 0)

        # if the Joystick has less than 2 Buttons or less than 4 and no at or axes, it can't be used
        else:
            raise StandardError("the Joystick device has not enough buttons")

    # ---------------------------------------------------------

    def getSettings(self):
        '''
        @return: (dict) returns the settings of the device
        '''
        return self.settings

    # ---------------------------------------------------------

    def noticeAction(self):
        '''
        '''
        if type(self.device) == joystickdevice.JoystickDevice:
            ## first get the direction:
            # from axis
            if self.settings["directions"][0] == "AXIS":
                self.directions[0] = self.device.axes[self.settings["directions"][1]]
            # or from cooliehat
            elif self.settings["directions"][0] == "HAT":
                self.directions[0] = self.device.hats[self.settings["directions"][1]]


            # then get the acceleration
            # from buttons
            if self.settings["accelerator"][0] == self.settings["brake"][0] == "BUTTON":
                value = 0
                if self.device.buttons[self.settings["accelerator"][1]]:
                    value += 1
                if self.device.buttons[self.settings["brake"][1]]:
                    value -= 1
                self.directions[1] = value
            # from axis
            elif self.settings["accelerator"][0] == self.settings["brake"][0] == "AXIS":
                self.directions[1] = -self.device.axes[self.settings["accelerator"][1]]
            # or from cooliehat
            elif self.settings["accelerator"][0] == self.settings["brake"][0] == "HAT":
                self.directions[1] = self.device.hats[self.settings["accelerator"][1]]


            # then get boost and item button values
            self.boost = self.device.buttons[self.settings["boost"][1]]
            self.use_item = self.device.buttons[self.settings["use_item"][1]]
        else:
            acceleration = 0
            direction = 0
            if self.device.keys[self.settings["up"]]:
                acceleration += 1
            if self.device.keys[self.settings["down"]]:
                acceleration -= 1

            if self.device.keys[self.settings["left"]]:
                direction -= 1
            if self.device.keys[self.settings["right"]]:
                direction += 1

            self.directions[0] = direction
            self.directions[1] = acceleration

            self.boost = self.device.keys[self.settings["boost"]]
            self.use_item = self.device.keys[self.settings["use_item"]]

            print self.directions, " - boost:", self.boost, " - use_item:", self.use_item
            #print self.device.keys[self.settings["up"]]

    # ---------------------------------------------------------

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class InputDevices(object):
    '''
    '''
    def __init__(self, settings):
        '''
        @param keyboard: = (KeyboardDevice) keyboard
        @param joysticks: = (JoystickDevices) joysicks
        '''

        self.keyboard = keyboarddevice.KeyboardDevice()
        self.joysticks = joystickdevice.JoystickDevices()

        self.devices = [InputDevice(self.keyboard, settings)]

        for joystick in self.joysticks.getJoysticks():
            self.devices.append(InputDevice(joystick, settings))

    # ---------------------------------------------------------

    def fetchEvents(self, task):
        '''
        '''
        self.joysticks.fetchEvents()

        for device in self.devices:
            device.noticeAction()

        return task.cont

    # ---------------------------------------------------------



if __name__ == "__main__":

    from direct.showbase.ShowBase import ShowBase
    sb = ShowBase()

    import time
    import settings

    conf = settings.Settings()
    conf.loadSettings("user/config.ini")

    # init pygame and its joystick module
    pygame.init()
    pygame.joystick.init()

    i = InputDevices(conf.getInputSettings())

    taskMgr.add(i.fetchEvents, "fetchEvents")
    run()

    pygame.joystick.quit()
    pygame.quit()
