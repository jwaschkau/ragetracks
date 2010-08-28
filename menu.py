# _*_ coding: UTF-8 _*_
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
        self.selection = 0
        self.options = []

    # -----------------------------------------------------------------

    def addOption(self, name, function):
        '''
        '''
        self.image = OnscreenImage(image = "data/sprites/menu/newGame.png", pos = (0, 0, 0), scale = (.6, 1, .06))
        self.options.append((name, function))

    # -----------------------------------------------------------------

    def hideMenu(self):
        '''
        '''
        self.image.destroy()
        pass
        '''
        '''
        for i in range(len(self.options)):
#            self.images[i].destroy()
            self.texts[i].destroy()

        self.images = []
        self.texts = []

    # -----------------------------------------------------------------

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

    # -----------------------------------------------------------------

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

    # -----------------------------------------------------------------

    def chooseOption(self):
        '''
        '''
        # call the function behind the selected option
        self.options[self.selection][1]()
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

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
