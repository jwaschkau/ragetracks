from panda3d.core import NodePath
#from pandac.PandaModules import Vec3, Vec4, PointLight #Temp for Testing need VBase4
from pandac.PandaModules import *
import time
import sys
from direct.directnotify.DirectNotify import DirectNotify
import glob
import settings

FONT = 'data/fonts/font.ttf'
class MainMenu(object):

    def __init__(self, newGame, device):
        self._notify = DirectNotify().newCategory("Menu")
        self._notify.info("New Menu-Object created: %s" %(self))
        self.device = device #The keybord
        
        time.sleep(1)               #Bad Hack to make sure that the Key isn't pressed.
        self.device.boost = False   #Bad Hack to make sure that the Key isn't pressed.
        
        self.newGame = newGame
        
        #Font
        self.font = DynamicTextFont(FONT)
        self.font.setRenderMode(TextFont.RMSolid)
        
        taskMgr.add(self.input, 'input')
    
    # -----------------------------------------------------------------

    def initNode(self):
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

    def menuMain(self):
        self.initNode()
        #Fill the options List
        #self.options = []
        #self.optionsModells = []
        #self.selected = 0
        self.addOption(_("New Game"), self.newGame)
        self.addOption(_("Options"), self.option)
        self.addOption(_("Hall Of Fame"), self.newGame)
        self.addOption(_("Credits"), self.newGame)
        self.addOption(_("Exit"), sys.exit)
        #self.text = Text3D(_("NewGame"))
        self.showMenu()
    
    # -----------------------------------------------------------------
    
    def menuOption(self):
        self.initNode()
        #Fill the options List
        #self.options = []
        #self.optionsModells = []
        #self.selected = 0
        self.addOption(_("Resolution"), self.newGame)
        self.addOption(_("Full Screen"), self.fullscreen)
        self.addOption(_("Shader"), self.newGame)
        self.addOption(_("Back"), self.backToMain)
        #self.text = Text3D(_("NewGame"))
        self.showMenu()

    # -----------------------------------------------------------------
    
    def option(self):
        
        self.menuOption()
        taskMgr.doMethodLater(0.5, self.input, 'input')
        
    # -----------------------------------------------------------------
    
    def backToMain(self):
        self.menuMain()
        taskMgr.doMethodLater(0.5, self.input, 'input')

    # -----------------------------------------------------------------
    
    def fullscreen(self):
        conf = settings.Settings()
        conf.loadSettings("user/config.ini")
        conf.fullscreen = not conf.fullscreen
        wp = base.win.getProperties()
        #wp.setFullscreen(True) 
        print type(wp)
        wp.setSize(1200, 1920)
        print "TEST2", wp.getYSize()
        base.win.requestProperties(wp)
        taskMgr.doMethodLater(0.5, self.input, 'input')

    # -----------------------------------------------------------------
    
    def input(self, task):
        #print self.device.directions
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
        text = TextNode(name)
        text.setFont(self.font)
        text.setText(name)
        self.options.append((name, function))
        self.optionsModells.append(NodePath("test").attachNewNode(text)) #setPos fehlt
        self.optionsModells[-1].setColor(self.colorA)
        self.optionsModells[-1].setPos(0, 0, -len(self.optionsModells))
        self.menuNode.attachNewNode(text)
        
        
        #text.setTextColor(0.3, 0.6, 0.1, 1.0)
        #text.setText("Every day in every way I'm getting better and better.")
        #textNodePath = NodePath("test")
        #textNodePath.attachNewNode(text)
        #textNodePath.reparentTo(self.menuNode)
        

    # -----------------------------------------------------------------

    def hideMenu(self):
        '''
        '''
        self.menuNode.removeNode()
        
        self.camera.node().setActive(False)

    # -----------------------------------------------------------------
    
    def showMenu(self):
        '''
        '''
        if len(self.optionsModells) == 0:
            return
        #self.menuNode.show()
        self.optionsModells[self.selected].setColor(self.colorB)
        
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
        
        self.optionsModells[old].setColor(self.colorA)
        self.optionsModells[self.selected].setColor(self.colorB)
        

    # -----------------------------------------------------------------

    def selectPrev(self):
        old = self.selected
        self.selected -= 1
        if self.selected == -1:
            self.selected = len(self.options)-1
        
        self.optionsModells[old].setColor(self.colorA)
        self.optionsModells[self.selected].setColor(self.colorB)

    # -----------------------------------------------------------------

    def chooseOption(self):
        '''
        call the function behind the selected option
        '''
        self.hideMenu()
        self.options[self.selected][1]()

class Menu(object):
    '''
    '''
    def __init__(self, parent):
        
        self._notify = DirectNotify().newCategory("Menu")
        self._notify.info("New Menu-Object created: %s" %(self))
        #Font
        self.font = DynamicTextFont(FONT)
        self.font.setRenderMode(TextFont.RMSolid)
        
        self.KEY_DELAY = 0.15
        self.player_buttonpressed = []
        
        self._parent = parent
        self._players = parent.players
        self._devices = parent.devices
        
        taskMgr.add(self.fetchAnyKey, "fetchAnyKey")
        
    def showStartScreen(self):
        '''
        the first screen with "press any Key"
        the device with the first key press will be the first player
        '''
        self._notify.info("Initializing StartScreen")
        

        
        #StartScreen Node
        self.startNode = NodePath("StartNode")
        self.startNode.reparentTo(render)
        self.startNode.setPos(-5,15,3)
        
        headline = TextNode("RageTracks")
        headline.setFont(self.font)
        headline.setText("RageTracks")
        NodePath("test").attachNewNode(headline)
        self.startNode.attachNewNode(headline)
        
        presskey = TextNode("PressAnyKey")
        presskey.setFont(self.font)
        presskey.setText(_("Press any key!!"))
        textNodePath = NodePath("PressAnyNode")
        textNodePath.attachNewNode(presskey)
        textNodePath.setPos(0,10,-9.5)
        textNodePath.reparentTo(self.startNode)
        
        #self.headline = Text3D("RageTracks")
        #self.headline.reparentTo(self.startNode)
        #self.presskey = Text3D(_("PressAnyKey"), Vec3(0,10,-9.5))
        #self.presskey.reparentTo(self.startNode)
        
        self.startNode.show()
        
        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        plnp = self.startNode.attachNewNode(plight)
        plnp.setPos(0, -10, 0)
        self.startNode.setLight(plnp)
        
        #Cam
        self.camera = base.makeCamera(base.win)
        
        #print self.devices.getCount()
        #print self.settings.getInputSettings()
        self._notify.info("StarScreen initialized")
        
    # -----------------------------------------------------------------
    
    def fetchAnyKey(self, task):
        '''
        Return the first device with the first key stroke
        '''
        for i in xrange(len(self._devices.devices)):
            if self._devices.devices[i].boost == True:
                #Kill Cam
                self.camera.node().setActive(False)
                #Kill Node
                self.startNode.hide()       #Maybe there is a function to delete the Node from memory

                #Start the Game for testing purpose
                #self.menu = Menu(self.newGame, self.players[0].getDevice())    #if one player exist
                self.menu = MainMenu(self.newGame, self._devices.devices[i])         #if no player exist
                self.menu.menuMain()
                return task.done
        return task.cont



        # -----------------------------------------------------------------

    def newGame(self):
        '''
        the new game menu
        '''
        self._notify.info("Initializing new game")
        #GlobPattern if we need a Panda Class
        self.vehicle_list = glob.glob("data/models/vehicles/*.egg")
        for index in range(len(self.vehicle_list)):
            self.vehicle_list[index] = Filename.fromOsSpecific(self.vehicle_list[index]).getFullpath()
        self._notify.debug("Vehicle list: %s" %(self.vehicle_list))
        self.platform = loader.loadModel("data/models/platform.egg")
        self.unusedDevices = self._devices.devices[:]
        taskMgr.add(self.collectPlayer, "collectPlayer")
        self.screens = []
        taskMgr.add(self.selectVehicle, "selectVehicle")
        
        self._notify.info("New game initialized")

    # -----------------------------------------------------------------

    def selectVehicle(self, task):
        for player in self._players:
            if player.vehicle.model != None:
                player.vehicle.model.setH(player.vehicle.model.getH()-(30 * globalClock.getDt()) )
                
            if self.player_buttonpressed[self._players.index(player)] < task.time:
                if player.device.directions[0] < -0.8:
                    self.player_buttonpressed[self._players.index(player)] = task.time + self.KEY_DELAY
                    index = self.vehicle_list.index("data/models/vehicles/%s" %(player.vehicle.model.getName()))-1
                    self._notify.debug("Previous vehicle selected: %s" %(index))
                    loader.loadModel(self.vehicle_list[index], callback = player.setVehicle)
                if player.device.directions[0] > 0.8:
                    self.player_buttonpressed[self._players.index(player)] = task.time + self.KEY_DELAY
                    index = self.vehicle_list.index("data/models/vehicles/%s" %(player.vehicle.model.getName()))+1
                    self._notify.debug("Next vehicle selected: %s" %(index))
                    if index >= len(self.vehicle_list): index = 0
                    loader.loadModel(self.vehicle_list[index], callback = player.setVehicle)
        return task.cont
    
    # -----------------------------------------------------------------

    def collectPlayer(self, task):
        '''
        Wait until all players are ready
        '''
        if len(self._players) > 0 and self.player_buttonpressed[0] < task.time:
            if self._players[0].device.boost:
                taskMgr.remove("selectVehicle")
                self._parent.startGame()
                return task.done

        for device in self.unusedDevices:
                if device.boost:
                    self.player_buttonpressed.append(0)
                    self._parent.addPlayer(device)
                    
                    #Set the PlayerCam to the Vehicle select menu Node        
                    vehicleSelectNode = NodePath("VehicleSelectNode")
                    self._players[-1].camera.camera.reparentTo(vehicleSelectNode)
                    #LICHT
                    plight = PointLight('plight')
                    plight.setColor(VBase4(10.0, 10.0, 10.0, 1))
                    plnp = vehicleSelectNode.attachNewNode(plight)
                    plnp.setPos(-10, -10, 5)
                    vehicleSelectNode.setLight(plnp)
                    
                    ambilight = AmbientLight('ambilight')
                    ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
                    vehicleSelectNode.setLight(vehicleSelectNode.attachNewNode(ambilight))
                    
                    #Load the platform
                    self.platform.instanceTo(vehicleSelectNode)
    
                    loader.loadModel(self.vehicle_list[0], callback = self._players[-1].setVehicle)
                    self._notify.debug("Loading initial vehicle: %s" %(self.vehicle_list[0]))
                    self.unusedDevices.remove(device)
                    self.player_buttonpressed[-1] = task.time + self.KEY_DELAY

        for player in self._players:
            if self.player_buttonpressed[self._players.index(player)] < task.time:
                if player.device.use_item:
                    self._notify.debug("Removing player: %s" %(player))
                    self.unusedDevices.append(player.device)
                    self.player_buttonpressed.pop(self._players.index(player))
                    self._parent.removePlayer(player)
        return task.cont

    # -----------------------------------------------------------------

if __name__ == "__main__":
    import main
