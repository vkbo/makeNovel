# -*- coding: utf-8 -*
"""makeNovel Book Class

makeNovel – Book Class
=======================
The Book class holds all the data contained in the novel files

File History:
Created: 2018-03-15 [0.1.0]

"""

import logging
import mknov   as mn

from os import path

from .parser import Parser

logger = logging.getLogger(__name__)

class Book():
    
    theParser  = None
    
    masterFile = None
    
    def __init__(self, masterFile):
        
        if not path.isfile(masterFile):
            mn.OUT.errMsg("File not found: %s" % masterFile)
        
        self.masterFile = masterFile
        
        self.theParser = Parser(masterFile)
        
        return

# End Class Book
