"""makeNovel Output Class

makeNovel – Output Class
========================
Handles output to std ot out file

File History:
Created:   2018-03-04 [0.1.0]

"""

import logging
import mknov   as mn

logger = logging.getLogger(__name__)

class Output():

    def __init__(self):

        return

    def printHeader(self, headString, headLen=72):
        strLen = len(headString)
        strInd = round((headLen-strLen)/2)
        print("")
        print("*"*headLen)
        print(" "*strInd + headString)
        print("*"*headLen)
        print("")
        return True

    def infMsg(self, msgString):
        print(msgString)
        return True

    def errMsg(self, msgString):
        print("Error: %s" % msgString)
        return True

    def wrnMsg(self, msgString):
        print("Warning: %s" % msgString)
        return True

    def dbgMsg(self, msgString):
        print("Debug: %s" % msgString)
        return True

    def critMsg(self, msgString, actionString):
        strLen = len(msgString)
        if strLen < 14:
            strLen = 14
        print("")
        print("*"*(strLen+6))
        print("*  Critical Error"+(" "*(strLen-14))+"  *")
        print("* ="+("="*strLen)+"= *")
        print("*  %s  *" % msgString)
        print("*"*(strLen+6))
        print(actionString)
        print("")

# End Class Output
