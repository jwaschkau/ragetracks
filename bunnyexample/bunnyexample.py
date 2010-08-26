# _*_ coding: UTF-8 _*_
###############################################################
##  Autor: Carsten Pfeffer    ##  Version 0.0                ##
###############################################################
##  Programm: BUNNY                                          ##
###############################################################
##  Datum:  08.02.2010                                       ##
###############################################################


## Kommentar entfernen für Vollbildmodus
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "fullscreen 1 win-size 1024 768")

# ----------------------------------------------------------------- #
# -- Importe

from panda3d.core import *
import direct.directbase.DirectStart                        # startet die Engine
from direct.showbase.DirectObject import DirectObject       # Basisklasse für das Spiel
from pandac.PandaModules import WindowProperties            # Fenstereigenschaften
from direct.actor.Actor import Actor                        # bewegliche Models

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

import pygame

import sys
import gui
import math

import player

STATE_MENU = 0
STATE_GAME = 1


SOUND_MENU_SELECT = loader.loadSfx("data/sfx/menusel.wav")
SOUND_MENU_CLICK1 = loader.loadSfx("data/sfx/menuclick1.wav")
SOUND_MENU_CLICK2 = loader.loadSfx("data/sfx/menuclick2.wav")

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

class Game(DirectObject):
    '''
    '''
    def __init__(self):
        '''
        '''
        self.key_map = {"arrow_left": False, "arrow_right": False, "arrow_up": False, "arrow_down": False, "cam_left": False, "cam_right": False, "jump": False, "joy_jump": False,"shoot": False,"joy_shoot": False, "escape": False, "enter": False, "joy_x": 0, "joy_y": 0, "joy_a": 0, "joy_b": 0}

        self.state = STATE_MENU

        #self.joy_text = OnscreenText("0, 0", pos = (0, 0), scale = (.07, .07), fg=(0,0,0,1))

#        font = DynamicTextFont("data/bunny_game.ttf")
#        self.dialog_image = OnscreenImage(image = "data/gfx/dialog.jpg", pos = (0, 0, -0.65), scale = (1.21, 1, .24))
#        self.dialog_image.setTransparency(TransparencyAttrib.MAlpha)
#        self.dialog_image.setAlphaScale(0.4)
#        self.dialog_name_text = OnscreenText("Boothby:", pos = (-1.19, -.51), scale = (.1, .1), fg=(1,.8,.5,1))
#        self.dialog_name_text.setAlign(TextNode.ALeft)
#        self.dialog_name_text.setFont(font)
#
#        txt = "Hello! Did you see the impact, too? That was a big bang, man.\nAny idea what it could have been? Mabe someone should look for it..."
#
#        self.dialog_text = OnscreenText(txt, pos = (-1.18, -.65), scale = (.07, .07), fg=(1,1,1,1))
#        self.dialog_text.setAlign(TextNode.ALeft)
#        self.dialog_text.setFont(font)

        self.properties = WindowProperties()
        self.properties.setCursorHidden(True)
        self.properties.setTitle("Buny test")
        self.properties.setIconFilename("carrott.ico") #!!
#        self.properties.setFullscreen(True)
#        self.properties.setSize(1280, 1024)
        base.win.requestProperties(self.properties)

        base.win.setClearColor(Vec4(0,0,0,1))

        self.menu = gui.Menu()
        self.menu.addOption("Neues Spiel", self.startGame)
        self.menu.addOption("Spiel laden", None)
        self.menu.addOption("Spiel speichern", None)
        self.menu.addOption("Optionen", None)
        self.menu.addOption("Spiel beenden", self.quitGame)
        #self.menu.selectOption(2)
        self.menu.showMenu()


        self.accept("arrow_up", self.setKey, ["arrow_up", True])
        self.accept("arrow_down", self.setKey, ["arrow_down", True])
        self.accept("arrow_left", self.setKey, ["arrow_left", True])
        self.accept("arrow_right", self.setKey, ["arrow_right", True])
        self.accept("enter", self.setKey, ["enter", True])
        self.accept("space", self.setKey, ["shoot", True])
        self.accept("escape", self.setKey, ["escape", True])
        self.accept("a", self.setKey, ["cam_left", True])
        self.accept("d", self.setKey, ["cam_right", True])
        self.accept("lcontrol", self.setKey, ["jump", True])

        self.accept("arrow_up-up", self.setKey, ["arrow_up", False])
        self.accept("arrow_down-up", self.setKey, ["arrow_down", False])
        self.accept("arrow_left-up", self.setKey, ["arrow_left", False])
        self.accept("arrow_right-up", self.setKey, ["arrow_right", False])
        self.accept("enter-up", self.setKey, ["enter", False])
        self.accept("space-up", self.setKey, ["shoot", False])
        self.accept("escape-up", self.setKey, ["escape", False])
        self.accept("a-up", self.setKey, ["cam_left", False])
        self.accept("d-up", self.setKey, ["cam_right", False])
        self.accept("lcontrol-up", self.setKey, ["jump", False])

        pygame.init()
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
            self.joystick = None

    # ----------------------------------------------------------------- #

    def setKey(self, key, value):
        '''
        '''
        #print "key:",key, value
        if self.state == STATE_MENU:
            if self.key_map[key] == False and value == True:
                if key == "arrow_up":
                    SOUND_MENU_SELECT.play()
                    self.menu.selectPrev()
                if key == "arrow_down":
                    SOUND_MENU_SELECT.play()
                    self.menu.selectNext()
                if key == "enter":
                    SOUND_MENU_CLICK2.play()
                    self.menu.chooseSelectedOption()
                if key == "space":
                    SOUND_MENU_CLICK2.play()
                    self.menu.chooseSelectedOption()
        if key == "escape":
            self.quitGame()


        self.key_map[key] = value

    # ----------------------------------------------------------------- #

    def startGame(self):
        '''
        '''
        base.win.setClearColor(Vec4(.3,0.5,1,1))
        self.menu.hideMenu()
        self.state = STATE_GAME
        self.loadLevel("data/levels/terrain")

    # ----------------------------------------------------------------- #

    def loadLevel(self, filename):
        '''
        '''
        # Level laden
        self.level = loader.loadModel(filename)
        self.level.reparentTo(render)
        self.level.setPos(0,0,0)

        # Startpunkt finden und Spieler laden
        start_point = self.level.find("**/start_point")

        model = start_point.getTag("model") # Das Model ist abhängig von der Variable im Level
        if model == "": # aber defaultmaessig der Hase
            model = "rabbit.egg"

        # Spieler laden
        self.player = player.Player("data/models/"+model)
        self.player.reparentTo(render)


        # Größe und Position setzen
        self.player.setScale(.4)
        self.player.setPos(start_point.getPos())

        base.disableMouse()

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.7, .7, .6, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

        # die Bewegungsfunktion zum Taskmanager hnzufügen
        taskMgr.add(self.movePlayer, "movePlayer")


        ##################
        ## Models laden

        doc = loader.loadModel("data/models/doc_hare.egg")
        doc.reparentTo(render)
        doc.setPos(4,0,1)
        doc.setScale(.4)

    # ----------------------------------------------------------------- #

    def quitGame(self):
        '''
        '''
        pygame.joystick.quit()
        pygame.quit()
        sys.exit()

    # ----------------------------------------------------------------- #

    def foo(self):
        '''
        '''
        print "Hallo Welt"

    # ----------------------------------------------------------------- #

    def movePlayer(self, task):
        '''
        '''
        for e in pygame.event.get(): pass

        if self.joystick != None:
            self.key_map["joy_x"] = self.joystick.get_axis(0)      # x-achse zwischen -1 und 1
            self.key_map["joy_y"] = self.joystick.get_axis(1)      # y-achse zwischen -1 und 1
            self.key_map["joy_a"] = self.joystick.get_axis(3)      # x-achse zwischen -1 und 1


            if abs(self.key_map["joy_x"]) < .1: self.key_map["joy_x"] = 0
            if abs(self.key_map["joy_y"]) < .1: self.key_map["joy_y"] = 0
            if abs(self.key_map["joy_a"]) < .1: self.key_map["joy_a"] = 0

            #txt = "%f, %f"%(self.key_map["joy_x"], self.key_map["joy_y"])
            #self.joy_text.setText(txt)


            if self.joystick.get_button(1):
                self.key_map["joy_jump"] = True
            else:
                self.key_map["joy_jump"] = False

            if self.joystick.get_button(3):
                self.key_map["joy_shoot"] = True
            else:
                self.key_map["joy_shoot"] = False

            self.player.movePlayer(self.key_map)


        return task.cont

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

if __name__ == "__main__":
    print "Starting Carrottinators"
    game = Game()
    run()
