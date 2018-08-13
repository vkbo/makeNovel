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

    ERR_MISSINGINFO  = 1
    ERR_DATATYPE     = 2
    ERR_COMMAND      = 3
    ERR_SETBFADD     = 4
    ERR_FILENOTFOUND = 5
    ERR_FILEINVALID  = 6

# End Class ErrCodes

class ErrHandler():

    @staticmethod
    def terminateExec(errType):

        if errType == ErrCodes.ERR_MISSINGINFO:
            mn.OUT.critMsg("Input information missing","Terminating ...")
        elif errType == ErrCodes.ERR_DATATYPE:
            mn.OUT.critMsg("A datatype error was encountered","Terminating ...")
        elif errType == ErrCodes.ERR_COMMAND:
            mn.OUT.critMsg("An unknown command sequence was encountered","Terminating ...")
        elif errType == ErrCodes.ERR_SETBFADD:
            mn.OUT.critMsg("Attempting to set value before adding item","Terminating ...")
        elif errType == ErrCodes.ERR_FILENOTFOUND:
            mn.OUT.critMsg("File not found","Terminating ...")
        elif errType == ErrCodes.ERR_FILEINVALID:
            mn.OUT.critMsg("Invalid file","Terminating ...")
        else:
            mn.OUT.critMsg("An unknown error was encountered","Terminating ...")

        exit(1)

        return False

# End Class ErrHandler
