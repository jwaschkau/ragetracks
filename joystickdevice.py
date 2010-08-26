# _*_ coding: UTF-8 _*_
##############################################################
## this module wraps around the pygame joystick event handling
## and holds the information about all connected joystick and
## gamepad devices
##############################################################

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

import pygame

class Joystick(object):
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

        # initialize the buttons ans axes
        self.buttons = []
        self.axes = []

        for i in range(self.joystick.get_numaxes()):
            self.axes.append(0.0)

        for i in range(self.joystick.get_numbuttons()):
            self.buttons.append(False)

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class JoystickDevice(object):
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
            self.joysticks.append(Joystick(pygame.joystick.Joystick(num)))

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
        for e in pygame.event.get([pygame.JOYAXISMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]): #pygame.JOYBALLMOTION, pygame.JOYHATMOTION,
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
    j = JoystickDevice()
    while True:
        j.fetchEvents()


    pygame.joystick.quit()
    pygame.quit()
