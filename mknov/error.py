# -*- coding: utf-8 -*
"""makeNovel Error Class

makeNovel – Error Class
=======================
The Error class handles critical errors

File History:
Created: 2018-03-18 [0.1.0]

"""

import mknov as mn

class ErrCodes():
    
    ERR_DATATYPE     = 1
    ERR_COMMAND      = 2
    ERR_SETBFADD     = 3
    ERR_FILENOTFOUND = 4
    
# End Class ErrCodes

class ErrHandler():
    
    @staticmethod
    def terminateExec(errType):
        
        if errType == ErrCodes.ERR_DATATYPE:
            mn.OUT.critMsg("A datatype error was encountered","Terminating ...")
        elif errType == ErrCodes.ERR_COMMAND:
            mn.OUT.critMsg("An unknown command sequence was encountered","Terminating ...")
        elif errType == ErrCodes.ERR_SETBFADD:
            mn.OUT.critMsg("Attempting to set value before adding item","Terminating ...")
        elif errType == ErrCodes.ERR_FILENOTFOUND:
            mn.OUT.critMsg("File not found","Terminating ...")
        else:
            mn.OUT.critMsg("An unknown error was encountered","Terminating ...")
        
        exit(1)
        
        return False
    
# End Class ErrHandler
