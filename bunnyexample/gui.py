# _*_ coding: UTF-8 _*_
###############################################################
##  Autor: Carsten Pfeffer    ##  Version 0.0                ##
###############################################################
##  Programm: BUNNY                                          ##
###############################################################
##  Datum:  08.02.2010                                       ##
###############################################################


# ----------------------------------------------------------------- #
# -- Importe

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from pandac.PandaModules import TransparencyAttrib


#myObject = Directxxxxxx(keyword=value, keyword=value, ...)

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

class Menu():
    '''
    '''
    def __init__(self):
        '''
        '''
        self.options = []
        self.images = []
        self.texts = []

        self.selected = 0

        self.color_deselected = (0,.6,.8,1)
        self.color_selected = (.9,.3,0,1)

    # ----------------------------------------------------------------- #

    def addOption(self, text, function):
        '''
        '''
        self.options.append([text, function])

    # ----------------------------------------------------------------- #

    def showMenu(self):
        '''
        '''
        y = (len(self.options)*.4)*.17
        for option in self.options:
            #image = None
            #image = OnscreenImage(image = "data/gfx/menu/button.png", pos = (0, 0, y), scale = (.6, 1, .06))
            #image.setTransparency(TransparencyAttrib.MAlpha)
            #self.images.append(image)

            text = OnscreenText(text = option[0], pos = (0, y-.02), scale = (.07, .07), fg=self.color_deselected)
            font = DynamicTextFont("data/bunny_game.ttf")
            text.setFont(font)
            self.texts.append(text)

            y -= .17

            self.selectOption(self.selected)

    # ----------------------------------------------------------------- #

    def selectNext(self):
        '''
        '''
        old = self.selected
        self.selected += 1
        if self.selected == len(self.options):
            self.selected = 0

        if old < len(self.texts):
            self.texts[old].setFg(self.color_deselected)
        if self.selected < len(self.texts):
            self.texts[self.selected].setFg(self.color_selected)

    # ----------------------------------------------------------------- #

    def selectPrev(self):
        '''
        '''
        old = self.selected
        self.selected -= 1
        if self.selected == -1:
            self.selected = len(self.options)-1

        if old < len(self.texts):
            self.texts[old].setFg(self.color_deselected)
        if self.selected < len(self.texts):
            self.texts[self.selected].setFg(self.color_selected)

    # ----------------------------------------------------------------- #

    def selectOption(self, i):
        '''
        '''
        i %= len(self.options)
        old = self.selected
        self.selected = i
        if self.selected == -1:
            self.selected = len(self.options)-1

        if self.selected == len(self.options):
            self.selected = 0

        if old < len(self.texts):
            self.texts[old].setFg(self.color_deselected)
        if self.selected < len(self.texts):
            self.texts[self.selected].setFg(self.color_selected)


    # ----------------------------------------------------------------- #

    def hideMenu(self):
        '''
        '''
        for i in range(len(self.options)):
#            self.images[i].destroy()
            self.texts[i].destroy()

        self.images = []
        self.texts = []

    # ----------------------------------------------------------------- #

    def chooseSelectedOption(self):
        '''
        '''
        if callable(self.options[self.selected][1]):
            self.options[self.selected][1]()


    # ----------------------------------------------------------------- #