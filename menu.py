# -*- coding: utf-8 -*-
###################################################################
## this module represents the menu
###################################################################

from panda3d.core import NodePath
from pandac.PandaModules import *
import time
import sys
from direct.directnotify.DirectNotify import DirectNotify
import trackgen3d
import glob
import settings

COUNTDOWN_START = 1

FONT = 'data/fonts/Orbitron/TTF/orbitron-black.ttf'
class MainMenu(object):

    def __init__(self, newGame, device, devices):
        self._notify = DirectNotify().newCategory("Menu")
        self._notify.info("New Menu-Object created: %s" %(self))
        self.device = device #The keybord
        self.devices = devices #For Wii
        
        time.sleep(1)               #Bad Hack to make sure that the Key isn't pressed.
        self.device.boost = False   #Bad Hack to make sure that the Key isn't .setColor(self.colorA)pressed.
        
        self.newGame = newGame
        self.track = []

        #Wiimotes
        self.wiimoteX = []
                
        #Font
        self.font = DynamicTextFont(FONT)
        self.font.setRenderMode(TextFont.RMSolid)
        
        self.CONF_PATH = "user/config.ini"
        self._conf = settings.Settings()
        self._conf.loadSettings(self.CONF_PATH)
        
        taskMgr.add(self.input, 'input')
    
    # -----------------------------------------------------------------

    def initNode(self):
        '''
        Create a clear menu
        '''
        self.camera = None
        self.selected = 0
        self.options = []
        self.optionsModells = []
        self.menuNode = NodePath("menuNode")
        self.menuNode.reparentTo(render)
        self.menuNode.setPos(-4.5,15,3)
        self.menuNode.setH(40)
        
        self.colorA = Vec4(1,1,0,0)
        self.colorB = Vec4(0,1,1,0)
        
        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(10, 10, 10, 1))
        plnp = self.menuNode.attachNewNode(plight)
        plnp.setPos(-10, -800, 20)
        self.menuNode.setLight(plnp)

    def menuMain(self):
        '''
        The content for the main menu
        '''
        self.initNode()
        self.addOption(_("New Game"), self.newGame)
        self.addOption(_("Options"), self.option)
        self.addOption(_("Wiimote"), self.addWii)
        self.addOption(_("Credits"), self.newGame)
        self.addOption(_("Exit"), self.exit)
        
        self.road = loader.loadModel("data/models/road01.egg")
        self.road.reparentTo(self.menuNode)
        self.road.setPos(26,20,-7)
        self.road.setHpr(-50,10,30)
        #self.text = Text3D(_("NewGame"))
        self.showMenu()
    
    # -----------------------------------------------------------------
    
    def menuOption(self):
        '''
        The content for the option menu
        '''
        self.initNode()
        self.addOption(_("Resolution"), self.newGame)
        self.addOption(_("Full Screen"), self.fullscreen)
        self.addOption(_("Shader"), self.newGame)
        self.addOption(_("Back"), self.backToMain)
        self.showMenu()

    # -----------------------------------------------------------------
    
    def option(self):
        '''
        Start a option menu
        '''
        self.menuOption()
        taskMgr.doMethodLater(0.5, self.input, 'input')
        
    # -----------------------------------------------------------------
    
    def backToMain(self):
        '''
        Start a main menu
        '''
        self.menuMain()
        taskMgr.doMethodLater(0.5, self.input, 'input')

    # -----------------------------------------------------------------
    
    def exit(self):
        '''
        Save the config
        And Exit the Game
        '''
        self._conf.saveSettings(self.CONF_PATH)
        sys.exit()

    # -----------------------------------------------------------------
    
    def addWii(self):
        self.devices.wiis.getWiimotes()
#        try:
#            print 'Put Wiimote in discoverable mode now (press 1+2)...'
#            wiimote = cwiid.Wiimote()
#            self.wiimoteX.append(wiimote)
#            print "Wii", len(self.wiimoteX)
#        except:
#            pass
        self.backToMain()
        
    def fullscreen(self):
        '''
        Witch between Fullscreen and window mode
        '''
        self._conf.fullscreen = not self._conf.fullscreen
        wp = WindowProperties()
        wp.setFullscreen(self._conf.fullscreen)
        wp.setOrigin(0,0)
        wp.setSize(int(base.pipe.getDisplayWidth()),int(base.pipe.getDisplayHeight()))
        base.win.requestProperties(wp)
        self.option()
        ##TODO Save the config????

    # -----------------------------------------------------------------
    
    def input(self, task):
        '''
        Getting the keys from all devices
        '''
        #self._notify.debug( self.device.directions )
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
        Add one option to the menu Node
        '''
        text = TextNode(name)
        text.setFont(self.font)
        text.setText(name)
        self.options.append((name, function))
        self.optionsModells.append(NodePath("test").attachNewNode(text)) #setPos fehlt
        self.optionsModells[-1].setColor(self.colorA)
        self.optionsModells[-1].setPos(0, 0, -len(self.optionsModells))
        self.menuNode.attachNewNode(text)

    # -----------------------------------------------------------------

    def hideMenu(self):
        '''
        Remove the aktiv menu Node
        '''
        self.menuNode.removeNode()
        
        self.camera.node().setActive(False)

    # -----------------------------------------------------------------
    
    def showMenu(self):
        '''
        Show the menu Node
        '''
        if len(self.optionsModells) == 0:
            return
        self.optionsModells[self.selected].setColor(self.colorB)
        
        #Create a camera if there is none
        if self.camera is None: 
            self.camera = base.makeCamera(base.win)
        else:
            self.camera.node().setActive(True)

    # -----------------------------------------------------------------

    def selectNext(self):
        '''
        Bring out the next menu option
        '''
        old = self.selected
        self.selected += 1
        if self.selected == len(self.options):
            self.selected = 0
        
        self.optionsModells[old].setColor(self.colorA)
        self.optionsModells[self.selected].setColor(self.colorB)
        

    # -----------------------------------------------------------------

    def selectPrev(self):
        '''
        Bring out the previous menu option
        '''
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
        
        self.wii = []
        
        #StartScreen Node
        self.startNode = NodePath("StartNode")
        self.startNode.reparentTo(render)
        self.startNode.setPos(-5,15,3)

        #Headline model
        headline = loader.loadModel("data/models/logo.egg")
        headline.setX(4.7)
        headline.setY(-4)
        headline.setZ(-2)
        headline.setP(90)
        headline.reparentTo(self.startNode)
        
        #Press any key text
        presskey = TextNode("PressAnyKey")
        presskey.setFont(self.font)
        presskey.setText(_("Press any key!!"))
        textNodePath = NodePath("PressAnyNode")
        textNodePath.attachNewNode(presskey)
        textNodePath.setPos(0,10,-9.5)
        textNodePath.reparentTo(self.startNode)
        
        #Show the start screen 
        self.startNode.show()
        
        #LICHT
        plight = PointLight('plight')
        plight.setColor(VBase4(10, 10, 10, 1))
        plnp = self.startNode.attachNewNode(plight)
        plnp.setPos(20, -800, 30)
        self.startNode.setLight(plnp)
        
        #Camera
        self.camera = base.makeCamera(base.win)
        
        self._notify.info("StarScreen initialized")
        
    # -----------------------------------------------------------------
    
    def fetchAnyKey(self, task):
        '''
        Return the first device with the first key stroke
        '''
        for i in xrange(len(self._devices.devices)):
            if self._devices.devices[i].boost:
                #Kill Camera
                self.camera.node().setActive(False)
                #Kill Node
                self.startNode.removeNode()
                
                #Start the menu
                self.menu = MainMenu(self.newGame, self._devices.devices[i], self._devices)
                self.menu.menuMain()
                return task.done
        return task.cont



        # -----------------------------------------------------------------

    def newGame(self):
        '''
        The select vehicle screen
        '''
        base.enableParticles()
        self.countdown = COUNTDOWN_START #the countdown, when its over the game can be started
        self._notify.info("Initializing new game")
        #GlobPattern if we need a Panda Class
        self.vehicle_list = glob.glob("data/models/vehicles/*.egg")
        for index in range(len(self.vehicle_list)):
            self.vehicle_list[index] = Filename.fromOsSpecific(self.vehicle_list[index]).getFullpath()
        self._notify.debug("Vehicle list: %s" %(self.vehicle_list))
        self.platform = loader.loadModel("data/models/platform.egg")
        
        #Loading-Text that gets displayed when loading a model
        text = TextNode("Loading")
        text.setFont(self.font)
        text.setText(_("Loading..."))
        text.setAlign(TextProperties.ACenter)
        self.loading = NodePath("LoadingNode")
        self.loading.attachNewNode(text)
        self.loading.setPos(0,0,2)
        
        #The countdown, its possible to start the game when its 0
        text = TextNode("Countdown")
        text.setFont(self.font)
        text.setAlign(TextProperties.ACenter)
        text.setText(_(str(COUNTDOWN_START)))
        self.countdown_node = NodePath("Countdown")
        self.countdown_node.attachNewNode(text)
        self.countdown_node.setPos(0,0,4)
        
        #PreLoad the description that gets displayed when loading a model
        text = TextNode("name")
        text.setFont(self.font)
        text.setText(_("Loading..."))
        text.setAlign(TextProperties.ACenter)
        self.attributes = NodePath("AttributeNode")
        self.attributes.attachNewNode(text)
        
        self.unusedDevices = self._devices.devices[:]
        taskMgr.add(self.collectPlayer, "collectPlayer")
        #taskMgr.add(self.collectWii, "collectWii")
        self.screens = []
        taskMgr.add(self.selectVehicle, "selectVehicle")
        
        self.color_red = Vec4(1,0,0,0)
        self.color_green = Vec4(0,1,0,0)
        
        self._notify.info("New game initialized")
        
    # -----------------------------------------------------------------
        
    def selectVehicle(self, task):
        '''
        The vehicle select and rotate task
        '''
        #Set the countdown and hide, if > 3
        self.countdown -= globalClock.getDt()
        if self.countdown <=0:
            self.countdown_node.getChild(0).node().setText(_("Go"))
            self.countdown_node.setColor(self.color_green)
        elif self.countdown <=3: 
            self.countdown_node.getChild(0).node().setText(str(int(round((self.countdown+0.5)))))
            self.countdown_node.setColor(self.color_red)           
            self.countdown_node.show()
        else: self.countdown_node.hide()
        
        heading = self.loading.getH() -(30 * globalClock.getDt())
        self.loading.setH(heading)
        for player in self._players:
            if player.vehicle.model != None:
                player.vehicle.model.setH(heading)
                
            if self.player_buttonpressed[self._players.index(player)] < task.time and not player.vehicle.model_loading:
                if player.device.directions[0] < -0.8:
                    self.countdown = COUNTDOWN_START
                    self.player_buttonpressed[self._players.index(player)] = task.time + self.KEY_DELAY
                    index = self.vehicle_list.index("data/models/vehicles/%s" %(player.vehicle.model.getName()))-1
                    self._notify.debug("Previous vehicle selected: %s" %(index))
                    player.vehicle.model_loading = True
                    player.vehicle.model.hide()
                    player.camera.camera.getParent().find("AttributeNode").hide()#Hide the attributes
                    self.loading.instanceTo(player.camera.camera.getParent())
                    loader.loadModel(self.vehicle_list[index], callback = player.setVehicle)
                if player.device.directions[0] > 0.8:
                    self.countdown = COUNTDOWN_START
                    self.player_buttonpressed[self._players.index(player)] = task.time + self.KEY_DELAY
                    index = self.vehicle_list.index("data/models/vehicles/%s" %(player.vehicle.model.getName()))+1
                    self._notify.debug("Next vehicle selected: %s" %(index))
                    if index >= len(self.vehicle_list): index = 0
                    player.vehicle.model_loading = True
                    player.vehicle.model.hide()
                    player.camera.camera.getParent().find("AttributeNode").hide()#Hide the attributes
                    self.loading.instanceTo(player.camera.camera.getParent())
                    loader.loadModel(self.vehicle_list[index], callback = player.setVehicle)
        return task.cont
    
    # -----------------------------------------------------------------

    def collectWii(self, task):
        '''
        Collect wiimotes task
        '''
        try:
            print 'Put Wiimote in discoverable mode now (press 1+2)...'
            wiimote = cwiid.Wiimote()
            self.wiimoteX.append(wiimote)
            print len(self.wiimoteX)
        except:
            pass
        return task.cont
        
    # -----------------------------------------------------------------
     
    def collectPlayer(self, task):
        '''
        Wait until all players are ready
        '''
        if len(self._players) > 0 and self.player_buttonpressed[0] < task.time:
            if self._players[0].device.boost and self.countdown <= 0:
                loading = False
                for player in self._players: 
                    if player.vehicle.model_loading: 
                        loading = True
                        break
                self._notify.debug("Loading vehicle: %s" %(loading))
                if not loading:
                    taskMgr.remove("selectVehicle")
                    self.track =  trackgen3d.Track3d(1000, 1800, 1600, 1200, len(self._players))
                    self.streetPath = render.attachNewNode(self.track.createRoadMesh())
                    self.borderleftPath = render.attachNewNode(self.track.createBorderLeftMesh())
                    self.borderrightPath = render.attachNewNode(self.track.createBorderRightMesh())
                    ##self.borderPath = render.attachNewNode(self.track.createBorderMesh())
                    roadtex = loader.loadTexture('data/textures/street.png')
                    bordertex = loader.loadTexture('data/textures/border.png')
                    self.streetPath.setTexture(roadtex)
                    self.borderleftPath.setTexture(bordertex)
                    self.borderrightPath.setTexture(bordertex)

                    #self.streetPath = loader.loadModel('data/models/Street.egg')
                    ##self.streetPath = loader.loadModel('data/models/Street.egg')
                    #tex = loader.loadTexture('data/models/StreetTex.png')
                    #self.nodePath.setTexture(tex)
                    
                    self._parent.startGame(self.streetPath, self.track.trackpoints)
                    return task.done

        for device in self.unusedDevices:
                if device.boost:
                    self.countdown = COUNTDOWN_START
                    self.player_buttonpressed.append(0)
                    self._parent.addPlayer(device)
                    
                    #Set the PlayerCam to the Vehicle select menu Node        
                    vehicleSelectNode = NodePath("VehicleSelectNode")
                    self._players[-1].camera.camera.reparentTo(vehicleSelectNode)
                    
                    #Light, that casts shadows
                    plight = Spotlight('plight')
                    plight.setColor(VBase4(10.0, 10.0, 10.0, 1))
                    if (base.win.getGsg().getSupportsBasicShaders() != 0):
                        pass
                        ##plight.setShadowCaster(True, 2048, 2048)#enable shadows for this light ##TODO wegen Linux
                        
                    #Light
                    plight.getLens().setFov(80)
                    plnp = vehicleSelectNode.attachNewNode(plight)
                    plnp.setPos(2, -10, 10)
                    plnp.lookAt(0,0,0)
                    vehicleSelectNode.setLight(plnp)
##                    vehicleSelectNode.setShaderAuto()#enable autoshader so we can use shadows
                    
                    #Light
                    ambilight = AmbientLight('ambilight')
                    ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
                    vehicleSelectNode.setLight(vehicleSelectNode.attachNewNode(ambilight))
                    self.platform.instanceTo(vehicleSelectNode) #Load the platform
                    
                    #instance shown text
                    self.countdown_node.instanceTo(vehicleSelectNode) #Instance the Countdown
                    self.loading.instanceTo(vehicleSelectNode) #Show the Loading-Text
                    self.attributes.copyTo(vehicleSelectNode).hide()
                    self._players[-1].vehicle.model_loading = True
                    
                    #start loading the model
                    loader.loadModel(self.vehicle_list[0], callback = self._players[-1].setVehicle)
                    self._notify.debug("Loading initial vehicle: %s" %(self.vehicle_list[0]))
                    self.unusedDevices.remove(device) 
                    self.player_buttonpressed[-1] = task.time + self.KEY_DELAY

        for player in self._players:
            if self.player_buttonpressed[self._players.index(player)] < task.time:
                if player.device.use_item:
                    self.countdown = COUNTDOWN_START
                    self._notify.debug("Removing player: %s" %(player))
                    self.unusedDevices.append(player.device)
                    self.player_buttonpressed.pop(self._players.index(player))
                    self._parent.removePlayer(player) 
        return task.cont

    # -----------------------------------------------------------------

if __name__ == "__main__":
    import main
