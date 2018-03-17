# -*- coding: utf-8 -*
"""makeNovel Parser Class

makeNovel – Parser Class
========================
Parses the tree of files and holds the raw data

File History:
Created: 2018-03-15 [0.1.0]

"""

import logging
import mknov   as mn

from os import path

logger = logging.getLogger(__name__)

class Parser():
    
    def __init__(self, inputFile):
        
        if not path.isfile(inputFile):
            mn.OUT.errMsg("File not found %s " % inputFile)
        
        self.inFile    = inputFile
        self.inPath    = ""
        self.rawBuffer = []
        self.incFiles  = []
        self.lineNo    = []
        self.cmdStack  = []
        
        # Add root file to file stack
        self.incFiles.append(inputFile)
        self.lineNo.append(0)
        
        mn.OUT.infMsg("Reading project files into buffer:")
        self.readFile(0)
        
        return
    
    def readFile(self, fileID):
        
        with open(self.incFiles[fileID], mode="r") as inFile:
            
            fileName = self.incFiles[fileID]
            lineNo   = 0
            
            mn.OUT.infMsg("File %d.BOF: Reading %s" % (fileID,fileName))
            
            for readLine in inFile:
                
                lineNo += 1
                
                lineBuffer = ""
                lineType   = None
                isEscape   = False
                
                # Loop through characters
                for ch in readLine:
                    if isEscape:
                        lineBuffer += ch
                        isEscape = False
                    elif ch == "\\":
                        isEscape = True
                    elif ch == "#":
                        break
                    else:
                        lineBuffer += ch
                        
        
        return
    
# End Class Parser
