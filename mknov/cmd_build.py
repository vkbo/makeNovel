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

from mknov.error   import ErrHandler, ErrCodes
from mknov.config  import Config
from mknov.main    import MakeNovel

logger = logging.getLogger(__name__)

def buildProject(sysArgs):

    # Valid Input Options
    shortOpt = "hm:at"
    longOpt  = [
        "help",
        "master=",
        "all",
        "timeline",
    ]

    helpMsg = (
        "makenovel {version} build\n"
        "\n"
        "Usage:\n"
        " -h, --help      Print this message.\n"
        " -m, --master=   Specify the master document. If none is specified,\n"
        "                   the previously used file will be used.\n"
        " -a, --all       Build all items.\n"
        " -t, --timeline  Build novel timeline.\n"
    ).format(
        version   = mn.__version__,
        status    = mn.__status__,
        copyright = mn.__copyright__
    )

    # Default Values
    masterFile    = mn.CFG.masterFile
    buildTimeLine = False

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
            return True
        elif inOpt in ("-m","--master"):
            masterFile = inArg

    #
    # Execute Build
    #

    if masterFile == "":
        mn.OUT.errMsg("No master file specified")
        ErrHandler.terminateExec(ErrCodes.ERR_MISSINGINFO)
        exit(2)

    # Command Header
    mn.OUT.printHeader("This is %s build - version %s" % (
        mn.__appname__,mn.__version__), 72
    )

    # Echo Settings
    mn.OUT.infMsg("Master file: %s" % masterFile)

    theProject = MakeNovel()
    theProject.setMasterFile(masterFile)
    #theBook = Book(masterFile)
    #theBook.buildTree()

    mn.OUT.infMsg("")
    mn.CFG.saveConfig()

    return False
