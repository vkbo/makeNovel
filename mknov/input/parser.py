# -*- coding: utf-8 -*
"""makeNovel Input Parser

makeNovel – Input Parser
========================
Parses the tree of files and holds the raw data of command lines

File History:
Created: 2018-03-15 [0.1.0]

"""

import re
import logging
import mknov as mn

from os import path

logger = logging.getLogger(__name__)

class Parser():
    """
    The Parser class reads all lines of a .nwf file into a raw buffer together with their original
    line numbers. If an include statement is encountered, the file is also loaded into the buffer.
    """

    LN_NONE   = 0
    LN_TEXT   = 1
    LN_CMD    = 2

    TYP_NONE  = 0
    TYP_STR   = 1
    TYP_INT   = 2
    TYP_FLOAT = 3
    TYP_BOOL  = 4
    TYP_OBJ   = 5

    REV_TYPE  = [
        "none",
        "string",
        "integer",
        "float",
        "boolean",
        "object"
    ]

    def __init__(self, rootFile):

        if not path.isfile(rootFile):
            mn.OUT.errMsg("File not found: %s " % rootFile)

        self.rootFile  = rootFile
        self.fileList  = [rootFile]
        self.fileRead  = [False]
        self.rawBuffer = []
        self.rawLineNo = []
        self.rawFileNo = []
        self.filePos   = 0

        self.loadBuffer(0)
        self.dumpBuffer()

        return

    def loadBuffer(self, fileIdx):
        """
        Recursively fill the buffer by opening include files and reading them.
        """

        mn.OUT.infMsg("Parsing file: %s" % self.fileList[fileIdx])
        if self.fileRead[fileIdx]:
            mn.OUT.wrnMsg("Circular or duplicate include calls detected. File has already been read.")
            return

        logger.debug("Opening file: %s" % self.fileList[fileIdx])
        with open(self.fileList[fileIdx], mode="r") as theFile:
            lineNo = 0
            for theLine in theFile:
                lineNo += 1
                theLine = theLine.strip()
                if len(theLine) == 0:
                    # Empty line, skip
                    continue
                if not theLine[0] == "@":
                    # Not a command, skip
                    continue
                if len(theLine) > 10:
                    if theLine[0:8] == "@include":
                        # We have an include, so add it to the list and read it
                        incFile = self.stringVal(theLine[8:].strip())
                        self.fileList.append(incFile)
                        self.fileRead.append(False)
                        self.loadBuffer(len(self.fileList)-1)
                        continue
                self.rawBuffer.append(theLine)
                self.rawLineNo.append(lineNo)
                self.rawFileNo.append(fileIdx)

        # Flag the file as read
        self.fileRead[fileIdx] = True
        logger.debug("Closing file: %s" % self.fileList[fileIdx])

        return

    def dumpBuffer(self):
        with open("parser_buffer.dat", mode="w") as theFile:
            theFile.write("Dump of Parser Buffer\n\n")
            theFile.write("FileList [fileNo: fileName]\n")
            theFile.write("="*80+"\n")
            for fileIdx in range(len(self.fileList)):
                theFile.write("%4d: %s\n" % (fileIdx,self.fileList[fileIdx]))
            theFile.write("\n")
            theFile.write("Buffer [fileNo:lineNo rawBuffer]\n")
            theFile.write("="*80+"\n")
            for nFile,nLine,sBuff in zip(self.rawFileNo,self.rawLineNo,self.rawBuffer):
                theFile.write("%4d:%-6d %s\n" % (nFile,nLine,sBuff))
        return

    def getLines(self):
        return len(self.rawBuffer)

    def getType(self, rawIndex):
        if len(self.rawBuffer[rawIndex]) > 0:
            if self.rawBuffer[rawIndex][0] == "@":
                return self.LN_CMD
            else:
                return self.LN_TEXT
        return self.LN_NONE

    def splitCommand(self, rawIndex):

        theCommand = ""
        theTarget  = ""
        theData    = ""
        theType    = self.TYP_NONE
        theStage   = 0
        isCommand  = False
        isTarget   = False
        isData     = False

        for ch in self.rawBuffer[rawIndex]:

            if ch == "@" and theStage == 0:
                theStage = 1

            if theStage == 1:
                if ch in (" ","\t"):
                    theStage = 2
                else:
                    theCommand += ch
            elif theStage == 2:
                if ch == ":":
                    theStage = 3
                else:
                    theTarget += ch
            elif theStage == 3:
                theData += ch

        theData = theData.strip()
        if len(theData) > 0:
            if   theData.lower() in ("true","yes"):
                theType = self.TYP_BOOL
                theData = True
            elif theData.lower() in ("false","no"):
                theType = self.TYP_BOOL
                theData = False
            elif theData[0] == "\"" or theData[0] == "\'":
                if len(theData) >= 2:
                    if theData[0] == theData[-1]:
                        theType = self.TYP_STR
                        theData = theData[1:-1]
                    else:
                        theData = ""
                        mn.OUT.errMsg("Unknown data entry on line %d in file: %s" % (
                            self.rawLineNo[rawIndex], self.rootFile
                        ))
                else:
                    theData = ""
                    mn.OUT.errMsg("Unknown data entry on line %d in file: %s" % (
                        self.rawLineNo[rawIndex], self.rootFile
                    ))
            elif self.isInt(theData):
                theType = self.TYP_INT
                theData = int(theData)
            elif self.isFloat(theData):
                theType = self.TYP_FLOAT
                theData = float(theData)
            elif self.isObject(theData):
                theType = self.TYP_OBJ
                theData = theData.strip()
            else:
                theData = ""
                mn.OUT.errMsg("Unknown data entry on line %d in file: %s" % (
                    self.rawLineNo[rawIndex], self.rootFile
                ))

        theReturn = {
            "line"    : self.rawLineNo[rawIndex],
            "raw"     : self.rawBuffer[rawIndex],
            "command" : theCommand.strip().lower(),
            "target"  : theTarget.strip().lower(),
            "data"    : theData,
            "type"    : theType
        }

        return theReturn

    def splitInput(self, theData):
        """
        Split a string into comma separated elements, ignoring separators in quotes
        RegEx from: https://stackoverflow.com/questions/2785755/
        """
        RESPLIT = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
        return RESPLIT.split(data)[1::2]

    def stringVal(self, theData):
        if self.isString(theData):
            return theData[1:-1]
        else:
            return None

    def isFloat(self, testVal):
        """
        Checks if a value can be cast to integer or not
        """
        try:
            intVal = float(testVal)
        except ValueError:
            return False
        else:
            return True

    def isInt(self, testVal):
        """
        Checks if a value can be cast to float or not
        """
        try:
            floatVal = float(testVal)
            intVal   = int(testVal)
        except ValueError:
            return False
        else:
            return floatVal == intVal

    def isString(self, testVal):
        """
        Checks if a value is a quoted string
        """
        if len(testVal) < 2:
            return False
        if testVal[0] in ("\"","\'") and testVal[0] == testVal[-1]:
            return True
        return False

    def isObject(self, testVal):
        """
        Checks if a string is a valid object name, that is: starts with a character [a-zA-Z],
        and only contains [a-zA-Z0-9_].
        """
        sFirst = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sValid = sFirst+"0123456789_"
        nChar  = len(testVal)
        if nChar == 0: return False
        if testVal[0] not in sFirst: return False
        for i in range(1,nChar):
            if testVal[i] not in sValid: return False
        return True

# End Class Parser
