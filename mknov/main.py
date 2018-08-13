# -*- coding: utf-8 -*
"""makeNovel Project Class

makeNovel – Project Class
=========================
Wrapper for the novel project

File History:
Created:   2018-08-13 [0.1.0]

"""

import logging
import mknov as mn

from os import path

from mknov.error import ErrCodes, ErrHandler

logger = logging.getLogger(__name__)

class MakeNovel():

    def __init__(self):

        self.theBuffer = None

        return

    def setMasterFile(self, masterFile):

        if not path.isfile(masterFile):
            mn.OUT.errMsg("File not found: %s" % masterFile)
            ErrHandler.terminateExec(ErrCodes.ERR_FILENOTFOUND)

        if len(masterFile) < 5:
            mn.OUT.errMsg("Expected a .nwf file")
            ErrHandler.terminateExec(ErrCodes.ERR_FILEINVALID)

        if not masterFile[-4:] == ".nwf":
            mn.OUT.errMsg("Unknown file extension for file: %s" % masterFile)
            ErrHandler.terminateExec(ErrCodes.ERR_FILEINVALID)

        mn.CFG.setMasterFile(masterFile)

        return True

# END Class Project
