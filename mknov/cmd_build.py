"""makeNovel Build Command

makeNovel – Build Command
=========================
Main function for the build command

File History:
Created:   2018-03-15 [0.1.0]

"""

import logging
import getopt
import mknov   as mn

from os import path, getcwd, pardir

from mknov.config import Config

logger = logging.getLogger(__name__)

def buildProject(sysArgs):
    
    logger.info("Running build project")
    
    # Valid Input Options
    shortOpt = "hft"
    longOpt  = [
        "help",
        "full",
        "timeline",
    ]
    
    helpMsg = (
        "novelWriter Build Module\n"
        "\n"
        "Usage:\n"
        " -h, --help      Print this message.\n"
        " -f, --full      Build all items.\n"
        " -t, --timeline  Build novel timeline.\n"
    ).format(
        version   = mn.__version__,
        status    = mn.__status__,
        copyright = mn.__copyright__
    )
    
    # Check config
    mnConf = Config()
    
    # Parse Input
    for inOpt, inArg in inOpts:
        if inOpt in ("-h","--help"):
            print(helpMsg)
            return True
        elif inOpt in ("-o","--output"):
            pass
    
    return False
