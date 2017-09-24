# -*- coding: utf-8 -*
"""makeNovel Scene Class

makeNovel – Scene Class
========================
This class holds the individual scene files

File History:
Created: 2017-09-23 [0.1.0]

"""

import re
import logging
import mknov

from os import path
#import xml.etree.ElementTree as etree

logger = logging.getLogger(__name__)

class Scene():
    
    def __init__(self,inPath,inFile,inFormat=""):
        
        self.fileName   = ""
        self.fileFormat = ""
        self.fileExists = False
        self.Paragraphs = []
        
        pathOpt1 = path.join(inPath,inFile)
        pathOpt2 = path.join(inPath,inFile+"."+inFormat)
        
        if path.isfile(pathOpt1):
            logger.input("Opening scene file %s" % pathOpt1)
            fileName, fileExt = path.splitext(pathOpt1)
            self.filePath     = pathOpt1
            self.fileExists   = True
        elif path.isfile(pathOpt2):
            logger.debug("Found file %s as %s" % (inFile,pathOpt2))
            fileName, fileExt = path.splitext(pathOpt2)
            self.fileName     = pathOpt2
            self.fileExists   = True
        else:
            logger.warning("Scene file not found %s, skipping" % inFile)
        
        if not self.fileExists: return

        if fileExt in (".txt",".text"):
            self.fileFormat = "TXT"
            self.readText()
        elif fileExt in (".fodt"):
            self.fileFormat = "FODT"
            self.readFodt()
        elif fileExt in (".htm",".html"):
            self.fileFormat = "HTM"
            self.readHtml()
        else:
            logger.error("Unsupported file format '%s' for %s" % (self.fileFormat,self.fileName))
        
        return
    
    def readText(self):
        
        if not self.fileExists: return
        
        parBuffer = ""
        nPar      = 0
        with open(self.fileName,mode="rt") as inFile:
            for readLine in inFile:
                readLine = readLine.strip()
                if readLine == "":
                    self.Paragraphs.append(parBuffer)
                    parBuffer = ""
                    nPar     += 1
                else:
                    parBuffer += readLine+" "
            if not parBuffer == "":
                self.Paragraphs.append(parBuffer)
                nPar += 1

        logger.debug("Read %d paragraphs" % nPar)
        
        return True

    def readFodt(self):
        
        if not self.fileExists: return
        
        parBuffer = ""
        inPar     = False
        nStart    = 0
        nStop     = 0
        with open(self.fileName,mode="rt") as inFile:
            for readLine in inFile:
                readLine = readLine.strip()
                if readLine[0:8] == "<text:p ":
                    parBuffer = ""
                    inPar     = True
                    nStart   += 1
                if inPar: parBuffer += readLine+" "
                if readLine[-9:] == "</text:p>":
                    self.Paragraphs.append(parBuffer)
                    parBuffer = ""
                    inPar     = False
                    nStop    += 1
        
        if not nStart == nStop:
            logger.warning("Parser found %d open and %d close tags in scene file" % (nStart,nStop))
        else:
            logger.debug("Read %d paragraphs" % nStart)
        
        return True

    def readHtml(self):
        
        if not self.fileExists: return
        
        parBuffer = ""
        inPar     = False
        nStart    = 0
        nStop     = 0
        with open(self.fileName,mode="rt") as inFile:
            for readLine in inFile:
                readLine = readLine.strip()
                if readLine[0:2] == "<p":
                    parBuffer = ""
                    inPar     = True
                    nStart   += 1
                if inPar: parBuffer += readLine+" "
                if readLine[-4:] == "</p>":
                    self.Paragraphs.append(parBuffer)
                    parBuffer = ""
                    inPar     = False
                    nStop    += 1
        
        if not nStart == nStop:
            logger.warning("Parser found %d open and %d close tags in scene file" % (nStart,nStop))
        else:
            logger.debug("Read %d paragraphs" % nStart)
        
        return True

# End Class Scene
