# -*- coding: utf-8 -*
"""makeNovel Scene Class

makeNovel – Scene Class
=======================
The Scene class holds all the data contained in a scene file

File History:
Created: 2018-03-18 [0.1.0]

"""

import mknov as mn

from os import path

from mknov.input.parser import Parser
from mknov.error        import ErrHandler, ErrCodes

class Scene():

    def __init__(self, sceneFile):

        foundFile = ""
        if path.isfile(sceneFile):
            foundFile = sceneFile
        elif path.isfile(sceneFile+".nwf"):
            foundFile = sceneFile+".nwf"
        else:
            mn.OUT.errMsg("Scene file not found: %s" % sceneFile)
            ErrHandler.terminateExec(ErrCodes.ERR_FILENOTFOUND)
            return

        self.sceneFile  = ""
        self.theScene   = Parser(foundFile)
        self.sceneTitle = ""

        return

# End Class Scene
