# -*- coding: utf-8 -*
"""makeNovel Init

makeNovel – MakeNovel Class
===========================
MakeNovel main class
Wraps the input file and parses it

File History:
Created: 2017-09-22 [0.1.0]

"""

import re
import logging
import makenovel

from os import path

logger = logging.getLogger(path.basename(__file__))

class MakeNovel():

    def __init__(self, inputFile):

        self.inFile    = inputFile
        self.rawBuffer = []
        self.incFiles  = []
        self.lineNo    = []
        self.cmdStack  = []

        logger.input("Master file is %s" % inputFile)

        # Add root file to file stack
        self.incFiles.append(inputFile)
        self.lineNo.append(0)
        
        logger.info("Reading master file ...")
        self.readFile(0)

        logger.info("Parsing buffer ...")
        self.parseBuffer()

        return

    def readFile(self, fileID):

        with open(self.incFiles[fileID], mode="rt") as inFile:

            fileName = self.incFiles[fileID]
            fileLine = 0

            logger.debug("File %d.BOF: Reading %s" % (fileID,fileName))

            for readLine in inFile:
                fileLine += 1
                readLine  = re.sub(r"\#.*?\n","",readLine).strip()
                if readLine == "":
                    continue
                elif readLine[0:4] == "@INC":
                    nextFile = readLine[4:].strip()
                    if path.isfile(nextFile):
                        logger.input("Including %s in %s line %d" % (nextFile,fileName,fileLine))
                        if nextFile in self.incFiles:
                            logger.warn("Already included %s, ignoring" % nextFile)
                        else:
                            self.incFiles.append(nextFile)
                            nextID = len(self.incFiles) - 1
                            logger.debug("File %d.%3d: %s" % (fileID,fileLine,readLine))
                            self.readFile(nextID)
                    else:
                        logger.error("File not found %s in %s line %d, aborting" % (nextFile,fileName,fileLine))
                        exit(2)
                else:
                    self.rawBuffer.append({0:fileID,1:fileLine,2:readLine})
                    self.cmdStack.append({0:"NUL",1:"NONE",2:"NONE",3:""})
                    logger.debug("File %d.%3d: %s" % (fileID,fileLine,readLine))

        logger.debug("File %d.EOF: Closing %s" % (fileID,fileName))

        return

    def parseBuffer(self):

        for n in range(len(self.rawBuffer)):

            rawFile = self.rawBuffer[n][0]
            rawLine = self.rawBuffer[n][1]
            rawText = self.rawBuffer[n][2]
            rawName = self.incFiles[rawFile]

            lineSearch = re.search("^[A-Za-z0-9\s_]+",rawText)
            if lineSearch:

                lineKey = rawText[0:lineSearch.end()].strip().upper()
                if len(rawText) > lineSearch.end():
                    lineOp  = rawText[lineSearch.end()]
                    lineVal = rawText[lineSearch.end()+1:].strip()
                else:
                    lineOp  = "¤" # Just some operator not in use
                    lineVal = ""

                if lineOp == "=":
                    self.checkVariable(n,lineKey,lineVal)
                elif lineOp == ":":
                    self.checkFunction(n,lineKey,lineVal)
                elif lineOp == "¤":
                    self.checkCommand(n,lineKey)
                else:
                    logger.error("Unknown operator %s in %s line %d, aborting" % (lineOp,rawName,rawLine))
                    exit(2)

            else:
                logger.error("Unexpected input in %s line %d, aborting" % (rawName,rawLine))
                exit(2)

        return

    def checkVariable(self,saveIdx,checkKey,checkVal):

        fileID   = self.rawBuffer[saveIdx][0]
        fileName = self.incFiles[fileID]
        fileLine = self.rawBuffer[saveIdx][0]

        self.cmdStack[saveIdx][0] = "VAL"
        self.cmdStack[saveIdx][1] = ""
        self.cmdStack[saveIdx][2] = checkKey
        self.cmdStack[saveIdx][3] = checkVal

        logger.debug("File %d.%3d: VALUE '%s' = '%s'" % (fileID,fileLine,checkKey,checkVal))

        return

    def checkFunction(self,saveIdx,checkKey,checkVal):

        fileID   = self.rawBuffer[saveIdx][0]
        fileName = self.incFiles[fileID]
        fileLine = self.rawBuffer[saveIdx][0]

        validFunctions = {
            "SET" : ["TITLE","AUTHOR","FORMAT"],
            "ADD" : ["PROLOGUE","CHAPTER","SCENE"],
        }
        isValid = False
        for valType in validFunctions.keys():
            nChars = len(valType)
            if len(checkKey) < nChars: continue
            if checkKey[0:nChars+1] == valType+" ":
                funType   = valType
                chkTarget = checkKey[nChars+1:].strip()
                if chkTarget in validFunctions[valType]:
                    funTarget = chkTarget
                    funValue  = checkVal.split(";")
                    isValid   = True

        if isValid:
            self.cmdStack[saveIdx][0] = "FUN"
            self.cmdStack[saveIdx][1] = funType
            self.cmdStack[saveIdx][2] = funTarget
            self.cmdStack[saveIdx][3] = funValue
            logger.debug("File %d.%3d: FUN '%s': '%s'" % (fileID,fileLine,checkKey,checkVal))
        else:
            logger.error("Unknown function call '%s' in %s line %d, aborting" % (checkKey,fileName,fileLine))
            exit(2)

        return

    def checkCommand(self,saveIdx,checkKey):

        fileID   = self.rawBuffer[saveIdx][0]
        fileName = self.incFiles[fileID]
        fileLine = self.rawBuffer[saveIdx][0]

        validCommands = ["SEPARATOR"]

        if checkKey in validCommands:
            self.cmdStack[saveIdx][0] = "CMD"
            self.cmdStack[saveIdx][1] = ""
            self.cmdStack[saveIdx][2] = checkKey
            self.cmdStack[saveIdx][3] = ""
            logger.debug("File %d.%3d: CMD '%s'" % (fileID,fileLine,checkKey))
        else:
            logger.error("Unknown command '%s' in %s line %d, aborting" % (checkKey,fileName,fileLine))
            exit(2)

        return

# End Class MakeNovel
