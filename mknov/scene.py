# -*- coding: utf-8 -*
"""makeNovel Scene Class

makeNovel – Scene Class
========================
This class holds the individual scene files

File History:
Created: 2017-09-23 [0.1.0]

"""

import re
import logging
import mknov

from os import path

logger = logging.getLogger(__name__)

class Scene():
    
    def __init__(self,inPath,inFile,inFormat=""):
        
        self.fileName   = ""
        self.fileFormat = ""
        self.fileExists = False
        
        pathOpt1 = path.join(inPath,inFile)
        pathOpt2 = path.join(inPath,inFile+"."+inFormat)
        
        if path.isfile(pathOpt1):
            logger.input("Opening scene file %s" % pathOpt1)
            fileName, fileExt = path.splitext(pathOpt1)
            self.filePath   = pathOpt1
            self.fileFormat = fileExt
            self.fileExists = True
        elif path.isfile(pathOpt2):
            logger.debug("Found file %s as %s" % (inFile,pathOpt2))
            fileName, fileExt = path.splitext(pathOpt2)
            self.fileName   = pathOpt2
            self.fileFormat = fileExt
            self.fileExists = True
        else:
            logger.warning("Scene file not found %s, skipping" % inFile)
        
        return

# End Class Scene
