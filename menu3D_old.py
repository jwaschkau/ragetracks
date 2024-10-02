# -*- coding: utf-8 -*-
###################################################################
## this module contains the menu class, which is used for the main-
## and sub menus
###################################################################

from direct.gui.OnscreenImage import OnscreenImage

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Menu(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        self.menuNode = render.attachNewNode("MenuNode")
        self.selection = 0
        self.options = []
        self.selected = 0
        self.menu = [["newGame", "settings", "cars", "exitGame"],(),(),()]

        for i in range (len(self.menu[0])):
            self.entry = loader.loadModel("data/models/menu/" + self.menu[0][i])
            self.entry.reparentTo(self.menuNode)


        #print self.menuNode.ls()
        print("##############################")
        for child in self.menuNode.getChildren():
            print(child)
        print(self.menuNode.find(self.menu[0][0] + "*"))
        print(render.ls())
        base.camera.setPosition(0,0,0)

    # -----------------------------------------------------------------

    def addOption(self, name, function):
        '''
        '''
        image = OnscreenImage(self.imagesDB[name][0][0],self.imagesDB[name][1], self.imagesDB[name][2])
        imageSelected = OnscreenImage(self.imagesDB[name][0][1],self.imagesDB[name][1], self.imagesDB[name][2])
        self.options.append((name, function, image, imageSelected))

    # -----------------------------------------------------------------

    def hideMenu(self):
        '''
        '''
        self.menuNode.hide()


    # -----------------------------------------------------------------

    def showMenu(self):
        '''
        '''
        self.menuNode.show()

    # -----------------------------------------------------------------

    def selectNext(self):
        '''
        Kopie aus Hasenspiel
        '''
        old = self.selected
        self.selected += 1
        if self.selected == len(self.options):
            self.selected = 0

        if old < len(self.texts):
            self.texts[old].setFg(self.color_deselected)
        if self.selected < len(self.texts):
            self.texts[self.selected].setFg(self.color_selected)

    # -----------------------------------------------------------------

    def selectPrev(self):
        '''
        Kopie aus Hasenspiel
        '''
        old = self.selected
        self.selected -= 1
        if self.selected == -1:
            self.selected = len(self.options)-1

        if old < len(self.texts):
            self.texts[old].setFg(self.color_deselected)
        if self.selected < len(self.texts):
            self.texts[self.selected].setFg(self.color_selected)

    # -----------------------------------------------------------------

    def chooseOption(self):
        '''
        '''
        # call the function behind the selected option
        self.options[self.selection][1]()
        '''
        Kopie aus Hasenspiel
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

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
