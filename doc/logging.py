# -*- coding: utf-8 -*-
###################################################################
## example program on how to use the logger
###################################################################
from pandac.PandaModules import * 
from direct.directnotify.DirectNotify import DirectNotify

loadPrcFileData("", "default-directnotify-level debug\n notify-level-Game info")
class Logging(object):
    def __init__(self):
        #create a new notify category
        self._notify = DirectNotify().newCategory("CamMovement")
        self._notify.info("Put some informational text here.")
        self._notify.debug("Put some informational text here.")
        self._notify.warning("Put some informational text here.")
        self._notify.error("Put some informational text here.") #raise an exeption