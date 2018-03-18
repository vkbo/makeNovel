# -*- coding: utf-8 -*
"""makeNovel Error Class

makeNovel – Error Class
=======================
The Error class handles critical errors

File History:
Created: 2018-03-18 [0.1.0]

"""

import mknov as mn

class ErrHandler():
    
    ERR_DATATYPE = 1
    
    def __init__(self):
        return
    
    @staticmethod
    def terminateExec(errType):
        
        if errType == ErrHandler.ERR_DATATYPE:
            mn.OUT.critMsg("A datatype error was encountered","Terminating ...")
        
        exit(1)
        
        return False
    
# End Class ErrHandler
