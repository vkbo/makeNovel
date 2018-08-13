# -*- coding: utf-8 -*
"""makeNovel Config Class

makeNovel – Config Class
========================
Novel configuration

File History:
Created:   2018-03-04 [0.1.0]

"""

import logging
import configparser
import mknov as mn

from os       import path, getcwd, pardir, mkdir
from datetime import datetime

logger = logging.getLogger(__name__)

class Config():

    projPath = None

    def __init__(self):

        self.confDir    = ".mknov"
        self.confFile   = "config"
        self.hasConf    = False

        # Settings
        self.logLevel   = logging.INFO
        self.logFile    = True
        self.logStdOut  = False
        self.masterFile = ""

        # Derived Settings
        self.projName   = ""

        return

    def findConfig(self):
        if path.isfile(path.join(self.confDir,self.confFile)):
            self.hasConf = True
            return True
        else:
            return False

    def loadConfig(self):

        if not self.hasConf:
            return False

        logger.debug("Loading config file")
        conf = configparser.ConfigParser()
        conf.read(path.join(self.confDir,self.confFile))
        
        # Get options
        
        ## Main
        if "Main" in conf:
            if "loglevel" in conf["Main"]:
                self.logLevel  = conf["Main"].getint("loglevel")
            if "logfile" in conf["Main"]:
                self.logFile   = conf["Main"].getboolean("logfile")
            if "logstdout" in conf["Main"]:
                self.logStdOut = conf["Main"].getboolean("logstdout")

        ## Build
        if "Build" in conf:
            if "master" in conf["Build"]:
                self.masterFile = conf["Build"].get("master")

        # Set Derived Settings
        self.projName = self.masterFile[:-4]

        return True

    def saveConfig(self):

        if not path.isdir(self.confDir):
            mkdir(self.confDir)
            logger.debug("Folder created: %s" % self.confDir)

        logger.debug("Saving config file")
        conf = configparser.ConfigParser()

        # Set options

        ## Main
        conf["Main"] = {
            "timestamp" : datetime.now().isoformat(),
            "loglevel"  : self.logLevel,
            "logfile"   : self.boolToStr(self.logFile),
            "logstdout" : self.boolToStr(self.logStdOut),
        }

        ## Build
        conf["Build"] = {
            "master" : self.masterFile,
        }

        # Write config file
        with open(path.join(self.confDir,self.confFile),"w") as confFile:
            conf.write(confFile)

        return True

    @staticmethod
    def boolToStr(theBool):
        if theBool:
            return "yes"
        else:
            return "no"

    def setMasterFile(self, masterFile):
        self.masterFile = masterFile
        self.projName   = masterFile[:-4]
        return

# End Class Config
