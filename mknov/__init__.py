# -*- coding: utf-8 -*
"""makeNovel Init

makeNovel – Init
================
Application initialisation

File History:
Created:   2017-09-22 [0.1.0]
Rewritten: 2018-03-04 [0.1.0] Split up into sub commands

"""

import logging

from os import path, remove, rename

from .config import Config
from .output import Output

from .cmd_init import initProject
from .cmd_make import makeProject

__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2018"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "code@vkbo.net"
__status__     = "Development"
__url__        = "https://github.com/vkbo/makeNovel"

# Initiating logging
logger = logging.getLogger(__name__)

# Create config object
OUT  = Output()

#
# Main program
#

def main(sysArgs):
    
    #
    # Logging
    #
    
    # Defaults
    debugLevel = logging.DEBUG
    debugStr   = "%(levelname)-8s  %(message)s"
    timeStr    = "[%(asctime)s] "
    logFile    = ""
    toFile     = False
    toStd      = True
    showTime   = False
    
    # Read logging settings
    mnConf = Config()
    if mnConf.findConfig():
        pass
        
    # Set Logging
    if showTime:
        debugStr = timeStr+debugStr
    logFmt = logging.Formatter(fmt=debugStr,datefmt="%Y-%m-%d %H:%M:%S")
    
    if not logFile == "" and toFile:
        if path.isfile(logFile+".bak"):
            remove(logFile+".bak")
        if path.isfile(logFile):
            rename(logFile,logFile+".bak")
        
        fHandle = logging.FileHandler(logFile)
        fHandle.setLevel(debugLevel)
        fHandle.setFormatter(logFmt)
        logger.addHandler(fHandle)
    
    if toStd:
        cHandle = logging.StreamHandler()
        cHandle.setLevel(debugLevel)
        cHandle.setFormatter(logFmt)
        logger.addHandler(cHandle)
    
    logger.setLevel(debugLevel)
    
    #
    # Parse Iinput and Call Submodules
    #
    
    helpMsg = (
        "mknovel {version} ({status})\n"
        "{copyright}\n"
        "\n"
        "List of Commands:\n"
        "  init      Sets up a new project.\n"
        "  make      Make the novel file tree into various output formats.\n"
        "  build     Build various outputs like story timeline, etc.\n"
        "  analyse   Prints a list of statistics like word count, etc.\n"
        "  config    Set various configuration options.\n"
        "  backup    Create a backup of the novel project.\n"
        "  version   Print program version.\n"
        "  help      Print this help message, or for any of the above commands.\n"
        "\n"
        "For more details on each command, type mknovel help [command]."
    ).format(
        version   = __version__,
        status    = __status__,
        copyright = __copyright__
    )
    
    if len(sysArgs) == 0:
        print(helpMsg)
        exit(2)
    
    theCmd  = sysArgs[0]  # The command called
    theArgs = sysArgs[1:] # The args to pass on to the command class
    
    if theCmd == "init":
        return initProject(theArgs)
    elif theCmd == "make":
        return makeProject(theArgs)
    elif theCmd == "build":
        print("Command not implemented yet")
        return True
    elif theCmd == "analyse":
        print("Command not implemented yet")
        return True
    elif theCmd == "config":
        print("Command not implemented yet")
        return True
    elif theCmd == "backup":
        print("Command not implemented yet")
        return True
    elif theCmd == "version":
        print("mknovel {version} ({status})".format(version = __version__, status = __status__))
        return True
    else:
        print(helpMsg)
        return True
    
    return False
