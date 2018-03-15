"""makeNovel Make Command

makeNovel – Make Command
========================
Main function for the make command

File History:
Created:   2018-03-06 [0.1.0]

"""

import logging
import getopt
import mknov   as mn

from os import path, getcwd, pardir

from mknov.config import Config

logger = logging.getLogger(__name__)

def makeProject(sysArgs):
    
    logger.info("Running make project")
    
    # Valid Input Options
    shortOpt = "ho:"
    longOpt  = [
        "help",
        "output=",
    ]
    
    helpMsg = (
        "novelWriter Make Module\n"
        "\n"
        "Usage:\n"
        " -h, --help    Print this message.\n"
        " -o, --output  Output format [pdf,html,fodt].\n"
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
