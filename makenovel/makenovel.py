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
        
        with open(inputFile, mode="rt") as inFile:
            
            for tmpLine in inFile:
                
                lineNo += 1

                # Strip comments and whitespaces
                tmpLine = re.sub(r"\#.*?\n","",tmpLine).strip()
                if tmpLine == "": continue

                # Find first occurence of operator
                varOp = tmpLine.find("=")
                funOp = tmpLine.find(":")
                
                nMatch = 0
                
                if varOp > 0:
                    isVar   = True
                    nMatch += 1
                else:
                    isVar   = False

                if funOp > 0:
                    isFun   = True
                    nMatch += 1
                else:
                    isFun   = False
                
                print(tmpLine)
                print(nMatch)
                print(varOp)
                print(funOp)
        
        return
    