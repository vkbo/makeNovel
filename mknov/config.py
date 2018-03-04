"""makeNovel Config Class

makeNovel – Config Class
========================
Novel configuration

File History:
Created:   2018-03-04 [0.1.0]

"""

import logging
import mknov   as mn

from os import path, getcwd, pardir

logger = logging.getLogger(__name__)

class Config():
    
    projPath = None
    
    def __init__(self):
        
        self.confDir  = ".mknov"
        self.confFile = "config"
        
        return
    
    def findConfig(self):
        
        # Look for .mknov folder in current dir, and parent dirs
        testPath = getcwd()
        nDirs    = 0
        while self.projPath is None:
            nDirs += 1
            if path.isdir(path.join(testPath,self.confDir)):
                self.projPath = testPath
            else:
                parPath = path.abspath(path.join(testPath,pardir))
                if parPath == testPath or nDirs >= 50:
                    break
                else:
                    testPath = parPath
        
        # If unsuccessful, give up
        if self.projPath is None:
            return False
        
        return True
    
# End Class Config
