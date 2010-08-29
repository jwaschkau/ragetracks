# _*_ coding: UTF-8 _*_
##############################################################
## this module wraps around the pygame joystick event handling
## and holds the information about all connected joystick and
## gamepad devices
##############################################################

import generaldevice

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

import pygame

class JoystickDevice(object):
    '''
    This class represents a joystick and holds the pygame data
    '''
    def __init__(self, joystick):
        '''
        @param joystick: the pygame joystick object
        '''
        # the pygame joysick object
        self.joystick = joystick
        self.joystick.init()
        #print self.joystick.get_name()

        # initialize the buttons axes, and cooliehats
        self.buttons = []
        self.axes = []
        self.hats = []

        for i in range(self.joystick.get_numaxes()):
            self.axes.append(0.0)

        for i in range(self.joystick.get_numbuttons()):
            self.buttons.append(False)

        for i in range(self.joystick.get_numhats()):
            self.hats.append((0,0))

    # ---------------------------------------------------------

    def getAxisCount(self):
        '''
        '''
        return len(self.axes)

    # ---------------------------------------------------------

    def getHatCount(self):
        '''
        '''
        return len(self.hats)

    # ---------------------------------------------------------

    def getButtonCount(self):
        '''
        '''
        return len(self.buttons)

    # ---------------------------------------------------------

    def getName(self):
        '''
        '''
        return self.joystick.get_name()

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class JoystickDevices(generaldevice.GeneralDevice):
    '''
    This class holds all connected Joystick and gamepad devices
    '''
    def __init__(self):
        '''
        initializes the joysticks
        '''
        # init pygame and its joystick module
        pygame.init()
        pygame.joystick.init()

        # we need a list for our joysticks
        self.joysticks = []

        # fill the list
        for num in range(pygame.joystick.get_count()):
            self.joysticks.append(JoystickDevice(pygame.joystick.Joystick(num)))

    # ---------------------------------------------------------

    def getJoysticks(self):
        '''
        '''
        return self.joysticks

    # ---------------------------------------------------------

    def getDeviceCount(self):
        '''
        @return: (int) count of the connected joystick devices
        '''
        return len(self.joysticks)

    # ---------------------------------------------------------

    def getJoystick(self, number):
        '''
        @return: (pygame.joystick.Joystick) the Joystick with the given number
        '''
        if number >= len(self.joysticks) or number < 0 or type(number) != int:
            raise IndexError("Joystick Device index out of range")
        return self.joysticks[number]

    # ---------------------------------------------------------

    def fetchEvents(self):
        '''
        this function gets the events from pygame
        '''
        # catch all joystick events from pygame
        for e in pygame.event.get([pygame.JOYAXISMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION]): #pygame.JOYBALLMOTION,
            # cooliehat moved / for gamepads without an analog stick
            if e.type == pygame.JOYHATMOTION:
                self.joysticks[e.joy].buttons[e.hat] = e.value
            # button pressed
            if e.type == pygame.JOYBUTTONDOWN:
                self.joysticks[e.joy].buttons[e.button] = True
            # button released
            if e.type == pygame.JOYBUTTONUP:
                self.joysticks[e.joy].buttons[e.button] = False
            # axis changed
            if e.type == pygame.JOYAXISMOTION:
                self.joysticks[e.joy].axes[e.axis] = e.value

    # ---------------------------------------------------------


if __name__ == "__main__":
    j = JoystickDevices()
    while True:
        j.fetchEvents()


    pygame.joystick.quit()
    pygame.quit()
