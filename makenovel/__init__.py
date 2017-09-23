# -*- coding: utf-8 -*
"""makeNovel Init

makeNovel – Init
================
Application initialisation

File History:
Created: 2017-09-22 [0.1.0]

"""

import logging
import getopt

from os         import path
from textwrap   import dedent

from .make import MakeNovel

__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "code@vkbo.net"
__status__     = "Development"
__url__        = "https://github.com/vkbo/makeNovel"

#
# Set up logging
#

# Add custom loglevel
INPUT = 60
BUILD = 70
logging.addLevelName(INPUT,"INPUT")
logging.addLevelName(BUILD,"BUILD")

def logInput(self, message, *args, **kws):
    if self.isEnabledFor(INPUT):
        self._log(INPUT, message, args, **kws) 

def logBuild(self, message, *args, **kws):
    if self.isEnabledFor(BUILD):
        self._log(BUILD, message, args, **kws) 

logging.Logger.input = logInput
logging.Logger.build = logBuild

logger = logging.getLogger(__name__)

#
# Main program
#

def main(sysArgs):
    
    # Valid Input Options
    shortOpt = "i:hd:v"
    longOpt  = [
        "infile=",
        "help",
        "debug=",
        "version",
    ]
    
    helpMsg = dedent("""
        makeNovel v%s
        %s
        
        Usage:
        -i, --infile   Input file.
        -h, --help     Print this message.
        -d, --debug    Debug level. Valid options are DEBUG, INFO, WARN or ERROR.
        -v, --version  Print program version and exit.
        """ % (__version__,__copyright__)
    )
    
    # Defaults
    debugLevel = logging.INFO
    debugStr   = "{levelname:8s}  {message}"
    inputFile  = ""
    
    if len(sysArgs) == 0:
        print(helpMsg)
        exit(2)
    
    # Parse Options
    try:
        inOpts, inArgs = getopt.getopt(sysArgs,shortOpt,longOpt)
    except getopt.GetoptError:
        print(helpMsg)
        exit(2)
    
    for inOpt, inArg in inOpts:
        if inOpt in ("-i","--infile"):
            inputFile = inArg
        elif   inOpt in ("-h","--help"):
            print(helpMsg)
            exit()
        elif inOpt in ("-d", "--debug"):
            if   inArg == "ERROR":
                debugLevel = logging.ERROR
                debugStr   = "{levelname:8s}  {message}"
            elif inArg == "WARN":
                debugLevel = logging.WARN
                debugStr   = "{levelname:8s}  {message}"
            elif inArg == "INFO":
                debugLevel = logging.INFO
                debugStr   = "{levelname:8s}  {message}"
            elif inArg == "DEBUG":
                debugLevel = logging.DEBUG
                debugStr   = "[{name:12s}:{lineno:4d}] {levelname:8s}  {message}"
            else:
                print("Invalid debug level")
                exit(2)
        elif inOpt in ("-v", "--version"):
            print("makeNovel %s Version %s" % (__status__,__version__))
            exit()
    
    # Set Logging
    logFmt  = logging.Formatter(fmt=debugStr,datefmt="%Y-%m-%d %H:%M:%S",style="{")
    cHandle = logging.StreamHandler()
    
    cHandle.setLevel(debugLevel)
    cHandle.setFormatter(logFmt)
    
    logger.setLevel(debugLevel)
    logger.addHandler(cHandle)
    
    if path.isfile(inputFile):
        MN = MakeNovel(inputFile)
        MN.buildBook()
    else:
        logger.error("File not found: %s" % inputFile)
    
    return
