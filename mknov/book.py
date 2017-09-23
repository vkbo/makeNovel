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

from os    import path
from .scene import Scene

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
        
        return
    
    def setTitle(self,bookTitle):
        self.bookTitle = bookTitle[0]
        logger.build("Book title set to '%s'" % bookTitle[0])
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
            "Type"  : "File",
            "Scene" : Scene(inPath,inFile,inFormat),
        }
        self.chapterData[self.chapterIdx]["Scenes"].append(self.sceneIdx)

        return True

# End Class Book
