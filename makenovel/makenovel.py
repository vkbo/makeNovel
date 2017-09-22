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

logger = logging.getLogger(__name__)

class MakeNovel():
    
    File   = None
    Buffer = None
    
    def __init__(self, inputFile):
        
        self.File = inputFile
        self.Buffer = {}
        
        logger.info("Input file selected: %s" % inputFile)
        lineNo = 0
        
        opMap = {
            "=" : "VAL",
            ":" : "FUN",
        }
        
        with open(inputFile, mode="rt") as inFile:
            
            for tmpLine in inFile:
                
                lineNo += 1

                # Strip comments and whitespaces
                tmpLine = re.sub(r"\#.*?\n","",tmpLine).strip()
                if tmpLine == "": continue
                
                print(tmpLine)

                lineSearch = re.search("^[A-Za-z0-9\s]+",tmpLine)
                if lineSearch:
                    lineKey = tmpLine[0:lineSearch.end()].strip().upper()
                    lineOp  = tmpLine[lineSearch.end()]
                    lineVal = tmpLine[lineSearch.end()+1:].strip()
                    
                    self.Buffer[lineNo] = ["NUL","NONE",""]
                    if lineOp == "=":
                        self.Buffer[lineNo][0] = "VAL"
                    elif lineOp == ":":
                        self.Buffer[lineNo][0] = "FUN"
                    else:
                        logger.error("Line %d : Unknown operator %s" % (lineNo,lineOp))

                    self.Buffer[lineNo][1] = lineKey
                    self.Buffer[lineNo][2] = lineVal
                else:
                    logger.error("Line %d : %s" % (lineNo,tmpLine))

        
        return
    