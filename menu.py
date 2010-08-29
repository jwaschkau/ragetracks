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
        self.imagesDB = {#{name:[[unselected, selected],pos,scale]}
        "NewGame":[["data/sprites/menu/newGame.png","data/sprites/menu/newGameSelected.png"],(0,0,0),(.6, 1, .06)]  
        }       
        self.selected = 0

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
        self.options.destroy()
        pass

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
