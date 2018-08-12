# -*- coding: utf-8 -*
"""makeNovel Parser Class

makeNovel – Parser Class
========================
Parses the tree of files and holds the raw data

File History:
Created: 2018-03-15 [0.1.0]

"""

import mknov as mn

from os import path

class Parser():

    LN_NONE   = 0
    LN_TEXT   = 1
    LN_CMD    = 2

    TYP_NONE  = 0
    TYP_STR   = 1
    TYP_INT   = 2
    TYP_FLOAT = 3
    TYP_BOOL  = 4

    REV_TYPE  = [
        "none",
        "string",
        "integer",
        "float",
        "boolean"
    ]

    def __init__(self, inputFile):

        if not path.isfile(inputFile):
            mn.OUT.errMsg("File not found %s " % inputFile)

        self.inFile    = inputFile
        self.rawBuffer = []
        self.rawLineNo = []
        self.filePos   = 0

        with open(self.inFile, mode="r") as theFile:

            lineNo = 0

            for theLine in theFile:

                lineNo += 1
                theLine = theLine.strip()

                # Skip comments
                if len(theLine) > 0:
                    if theLine[0] == "#":
                        continue

                self.rawBuffer.append(theLine)
                self.rawLineNo.append(lineNo)

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
                            self.rawLineNo[rawIndex], self.inFile
                        ))
                else:
                    theData = ""
                    mn.OUT.errMsg("Unknown data entry on line %d in file: %s" % (
                        self.rawLineNo[rawIndex], self.inFile
                    ))
            elif self.isInt(theData):
                theType = self.TYP_INT
                theData = int(theData)
            elif self.isFloat(theData):
                theType = self.TYP_FLOAT
                theData = float(theData)
            else:
                theData = ""
                mn.OUT.errMsg("Unknown data entry on line %d in file: %s" % (
                    self.rawLineNo[rawIndex], self.inFile
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

    def isFloat(self, testVal):
        try:
            intVal = float(testVal)
        except ValueError:
            return False
        else:
            return True

    def isInt(self, testVal):
        try:
            floatVal = float(testVal)
            intVal   = int(testVal)
        except ValueError:
            return False
        else:
            return floatVal == intVal

# End Class Parser
