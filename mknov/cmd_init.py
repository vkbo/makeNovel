"""makeNovel Init Command

makeNovel – Init Command
========================
Initialise a new project

File History:
Created:   2018-03-04 [0.1.0]

"""

import logging
import getopt
import mknov   as mn

from os import path, getcwd, pardir

from mknov.config import Config

logger = logging.getLogger(__name__)

def initProject(sysArgs):
    
    logger.info("Initialising new makeNovel project")
    
    # Valid Input Options
    shortOpt = "hne"
    longOpt  = [
        "help",
        "new",
        "empty",
    ]
    
    helpMsg = (
        "novelWriter Init Module\n"
        "\n"
        "Usage:\n"
        " -h, --help   Print this message.\n"
        " -n, --new    Create a new project with a set of basic project files (default).\n"
        " -e, --empty  Create an empty project.\n"
    ).format(
        version   = mn.__version__,
        status    = mn.__status__,
        copyright = mn.__copyright__
    )
    
    # Check config
    mnConf = Config()
    if mnConf.findConfig():
        logger.error("Project folder already exists.")
        return False
    
    # Parse Options
    try:
        inOpts, inArgs = getopt.getopt(sysArgs,shortOpt,longOpt)
    except getopt.GetoptError:
        print(helpMsg)
        exit(2)
    
    # Parse Input
    for inOpt, inArg in inOpts:
        if inOpt in ("-h","--help"):
            print(helpMsg)
            exit()
        elif inOpt in ("-n","--new"):
            pass
        elif inOpt in ("-e","--empty"):
            mnConf.setConfig()
            mnConf.saveConfig()
    
    return True
