from text3d import Text3D
from panda3d.core import NodePath
#from pandac.PandaModules import Vec3, Vec4, PointLight #Temp for Testing need VBase4
from pandac.PandaModules import *
import time
import sys

class Menu(object):

    def __init__(self, newGame, device):
        self.device = device #The keybord
        
        time.sleep(1)               #Bad Hack to make sure that the Key isn't pressed.
        self.device.boost = False   #Bad Hack to make sure that the Key isn't pressed.
        
        self.newGame = newGame
        
        self.camera = None
        self.selected = 0
        self.options = []
        self.optionsModells = []
        self.menuNode = NodePath("menuNode")
        self.menuNode.reparentTo(render)
        self.menuNode.setPos(-5,15,3)

        self.colorA = Vec4(1,1,0,0)
        self.colorB = Vec4(0,1,1,0)
        
        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        plnp = self.menuNode.attachNewNode(plight)
        plnp.setPos(0, -10, 0)
        self.menuNode.setLight(plnp)
        
        taskMgr.add(self.imput, 'input')
    
    # -----------------------------------------------------------------

    def menuMain(self):
        #Fill the options List
        self.options = []
        self.optionsModells = []
        self.selected = 0
        self.addOption(_("NewGame"), self.newGame)
        self.addOption(_("Options"), self.option)
        self.addOption(_("Credits"), self.newGame)
        self.addOption(_("HallOfFame"), self.newGame)
        self.addOption(_("Exit"), sys.exit)
        #self.text = Text3D(_("NewGame"))
        self.showMenu()
    
    # -----------------------------------------------------------------
    
    def menuOption(self):
        #Fill the options List
        self.options = []
        self.optionsModells = []
        self.selected = 0
        self.addOption(_("Sceen"), self.newGame)
        self.addOption(_("FullScreen"), self.newGame)
        self.addOption(_("Shader"), self.newGame)
        self.addOption(_("KA"), self.newGame)
        self.addOption(_("back"), self.backToMain)
        #self.text = Text3D(_("NewGame"))
        self.showMenu()

    # -----------------------------------------------------------------
    
    def option(self):
        self.menuOption()
        taskMgr.doMethodLater(0.5, self.imput, 'input')
        
    # -----------------------------------------------------------------
    
    def backToMain(self):
        self.menuMain()
        taskMgr.doMethodLater(0.5, self.imput, 'input')

    # -----------------------------------------------------------------
    
    def imput(self, task):
        print self.device.directions
        if self.device.directions == [1,0]:
            task.delayTime = 0.2
            return task.again
        if self.device.directions == [-1,0]:
            task.delayTime = 0.2
            return task.again
        if self.device.directions == [0,1]:
            task.delayTime = 0.2
            self.selectPrev()
            return task.again
        if self.device.directions == [0,-1]:
            task.delayTime = 0.2
            self.selectNext()
            return task.again
        if self.device.boost == True:
            self.chooseOption()
            return task.done
        return task.cont

    # -----------------------------------------------------------------
    
    def addOption(self, name, function):
        '''
        '''
        self.options.append((name, function))
        self.optionsModells.append(Text3D(_(name), Vec3(0, 0, (len(self.optionsModells))*(-1.5)))) #Think will working too without _ after Text3D
        self.optionsModells[len(self.optionsModells)-1].reparentTo(self.menuNode)
        

    # -----------------------------------------------------------------

    def hideMenu(self):
        '''
        '''
        self.menuNode.hide()
        
        self.camera.node().setActive(False)

    # -----------------------------------------------------------------
    
    def showMenu(self):
        '''
        '''
        if len(self.optionsModells) == 0:
            return
        self.menuNode.show()
        self.optionsModells[self.selected].color = self.colorB
        
        #Cam
        if self.camera is None: 
            self.camera = base.makeCamera(base.win)
            #self.camera.setPos(5,-15,-3)
        else:
            self.camera.node().setActive(True)

    # -----------------------------------------------------------------

    def selectNext(self):
        old = self.selected
        self.selected += 1
        if self.selected == len(self.options):
            self.selected = 0
        
        self.optionsModells[old].color = self.colorA
        self.optionsModells[self.selected].color = self.colorB
        

    # -----------------------------------------------------------------

    def selectPrev(self):
        old = self.selected
        self.selected -= 1
        if self.selected == -1:
            self.selected = len(self.options)-1
        
        self.optionsModells[old].color = self.colorA
        self.optionsModells[self.selected].color = self.colorB

    # -----------------------------------------------------------------

    def chooseOption(self):
        '''
        call the function behind the selected option
        '''
        self.hideMenu()
        self.options[self.selected][1]()

if __name__ == "__main__":
    import main
