# -*- coding: utf-8 -*
"""makeNovel Book Class

makeNovel – Book Class
=======================
The Book class is a superclass holding the compiled book
There is a subclass for each specific file format

File History:
Created: 2017-09-23 [0.1.0]

"""

import re
import logging
import mknov

from os       import path, getcwd
from textwrap import dedent
from .scene   import Scene

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookTitle    = ""
        self.bookSubTitle = ""
        self.bookAuthor   = []
        
        self.chapterNames = {"P":"Prologue","C":"Chapter","E":"Epilogue"}
        self.chapterNum   = 0
        self.chapterIdx   = -1
        self.chapterData  = {}
        
        self.sceneIdx     = -1
        self.sceneData    = {}
        self.sceneSepText = "***"
        
        self.parJustify   = False
        
        self.includePath  = path.join(path.dirname(path.abspath(__file__)),"includes")
        
        return
    
    def setValue(self,valName,valData):
        if valName == "Title":
            self.bookTitle = valData[0]
            logger.build("Book title set to '%s'" % valData[0])
        elif valName == "Justify":
            if valData[0].upper() in ("ON","TRUE","1"):
                self.parJustify = True
                logger.build("Paragraph alignment set to justify")
            else:
                self.parJustify = False
        elif valName == "Separator":
            self.sceneSepText = valData[0]
            logger.build("Scene separator text set to '%s'" % self.sceneSepText)
        return True
        
    def addAuthor(self,bookAuthor):
        for nextAuthor in bookAuthor:
            self.bookAuthor.append(nextAuthor)
            logger.build("Added author '%s'" % nextAuthor)
        return True
    
    def addChapter(self,chType,chValues):
        
        if len(chValues) == 1:
            chTitle    = chValues[0]
            chSubTitle = ""
        elif len(chValues) == 2:
            chTitle    = chValues[0]
            chSubTitle = chValues[1]
        else:
            chTitle    = ""
            chSubTitle = ""
            
        if chType in ("P","E"):
            self.chapterIdx += 1
            logger.build("Adding %s" % self.chapterNames[chType])
            self.chapterData[self.chapterIdx] = {
                "Type"     : chType,
                "Number"   : 0,
                "Title"    : chTitle,
                "SubTitle" : chSubTitle,
                "Scenes"   : [],
            }
        elif chType == "C":
            self.chapterIdx += 1
            self.chapterNum += 1
            if chTitle == "":
                logger.build("Adding %s %d with no title" % (self.chapterNames["C"],self.chapterNum))
            else:
                logger.build("Adding %s %d titled '%s'" % (self.chapterNames["C"],self.chapterNum,chTitle))
            self.chapterData[self.chapterIdx] = {
                "Type"     : "C",
                "Number"   : self.chapterNum,
                "Title"    : chTitle,
                "SubTitle" : chSubTitle,
                "Scenes"   : [],
            }
        
        return True

    def addScene(self,inPath,inFile,inFormat):
        
        if self.chapterIdx < 0:
            logger.error("No chapter to add scene '%s' to" % inFile)
            return False
        
        self.sceneIdx += 1
        
        chType = self.chapterData[self.chapterIdx]["Type"]
        chNum  = self.chapterData[self.chapterIdx]["Number"]
        if chType == "P":
            sceneTarget = "Prologue"
        elif chType == "E":
            sceneTarget = "Epilogue"
        else:
            sceneTarget = "Chapter %d" % chNum
        
        logger.build("Adding scene '%s' as SCN%04d to %s" % (inFile,self.sceneIdx,sceneTarget))
        self.sceneData[self.sceneIdx] = {
            "Type" : "File",
            "Data" : Scene(inPath,inFile,inFormat),
        }
        self.chapterData[self.chapterIdx]["Scenes"].append(self.sceneIdx)
        
        return True
    
    def addSepItem(self,sepType,sepData=""):
        
        if self.chapterIdx < 0:
            logger.error("No chapter to add separator item to")
            return False
        
        self.sceneIdx += 1
        
        chType = self.chapterData[self.chapterIdx]["Type"]
        chNum  = self.chapterData[self.chapterIdx]["Number"]
        if chType == "P":
            sceneTarget = "Prologue"
        elif chType == "E":
            sceneTarget = "Epilogue"
        else:
            sceneTarget = "Chapter %d" % chNum

        if sepType == "SepTitle":
            logger.build("Adding separator title '%s' as ELM%04d to %s" % (sepData,self.sceneIdx,sceneTarget))
        elif sepType == "Break":
            logger.build("Adding break as ELM%04d to %s" % (self.sceneIdx,sceneTarget))
        elif sepType == "Separator":
            logger.build("Adding separator as ELM%04d to %s" % (self.sceneIdx,sceneTarget))

        self.sceneData[self.sceneIdx] = {
            "Type" : sepType,
            "Data" : sepData,
        }
        self.chapterData[self.chapterIdx]["Scenes"].append(self.sceneIdx)
        
        return True
    
    def buildFODT(self):
        
        if self.parJustify:
            parAlign = "fo:text-align=\"justify\" style:justify-single-word=\"false\" style:writing-mode=\"page\""
        else:
            parAlign = ""
        
        with open(path.join(self.includePath,"header.fodt"),mode="rt") as headerFile:
            outHeader = headerFile.read()
            outHeader = outHeader.replace("$ALIGN",parAlign)
        
        with open(path.join(self.includePath,"footer.fodt"),mode="rt") as footerFile:
            outFooter = footerFile.read()
        
        outPath = path.join(getcwd(),"novel.fodt")
        with open(outPath,mode="wt") as outFile:
            
            # Write Header
            outFile.write(outHeader)
            
            for ch in range(self.chapterIdx+1):
                chType  = self.chapterData[ch]["Type"]
                chNum   = self.chapterData[ch]["Number"]
                chTitle = self.chapterData[ch]["Title"]
                chName  = self.chapterNames[chType]
                if chType == "C":     chName = "%s %d" % (chName,chNum)
                if not chTitle == "": chName = "%s: %s" % (chName,chTitle)
                # outFile.write("   <text:h text:style-name=\"P1\"/>\n")
                outFile.write("   <text:h text:style-name=\"Chapter\">%s</text:h>\n" % chName)
                for scn in self.chapterData[ch]["Scenes"]:
                    scnType = self.sceneData[scn]["Type"]
                    scnData = self.sceneData[scn]["Data"]
                    if scnType == "File":
                        parNum = 0
                        for parTxt in scnData.Paragraphs:
                            parNum += 1
                            parFODT = self.parToFODT(scnData.fileFormat,parTxt,parNum)
                            outFile.write("   %s\n" % parFODT)
                    elif scnType == "SepTitle":
                        outFile.write("   <text:p text:style-name=\"SepTitle\">%s</text:p>\n" % scnData)
                    elif scnType == "Break":
                        outFile.write("   <text:p text:style-name=\"Normal\"/>\n")
                    elif scnType == "Separator":
                        outFile.write("   <text:p text:style-name=\"Separator\">%s</text:p>\n" % self.sceneSepText)
            
            # Write Footer
            outFile.write(outFooter)
        
        return True

    def buildTXT(self):
        logger.error("TXT output not implemented yet.")
        return False

    def buildHTM(self):
        logger.error("HTM output not implemented yet.")
        return False

    def parToFODT(self, inFormat, inPar, parNum):
        
        if inFormat == "FODT":
            # Same format, nothing to do
            return inPar
        
        if inFormat == "TXT":
            # Remove whitespaces, including tabs
            outPar = inPar.strip()
            
            # Replace any existing < or >
            outPar = outPar.replace("<","&lt;")
            outPar = outPar.replace(">","&gt;")
            
            # Add back initial tab for second or later paragraph
            if parNum > 1: outPar = "\t"+outPar
            
            # Replace other formatting
            outPar = outPar.replace("\t","<text:tab/>")
            
            # Wrap and rerturn
            outPar = "<text:p text:style-name=\"Normal\">%s</text:p>" % outPar
            return outPar
        
        return None

# End Class Book
