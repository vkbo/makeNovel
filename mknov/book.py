# -*- coding: utf-8 -*
"""makeNovel Book Class

makeNovel – Book Class
=======================
The Book class holds all the data contained in the novel files

File History:
Created: 2018-03-15 [0.1.0]

"""

import logging
import mknov   as mn

from os import path

from .parser import Parser

logger = logging.getLogger(__name__)

class Book():
    
    theParser  = None
    
    masterFile = None
    
    def __init__(self, masterFile):
        
        self.bookTitle    = ""
        self.bookAuthor   = []
        self.bookStatus   = ""
        
        self.bookChapters = []
        self.bookScenes   = []
        self.bookChars    = []
        
        self.cmdStack     = []
        
        if not path.isfile(masterFile):
            mn.OUT.errMsg("File not found: %s" % masterFile)
        
        self.masterFile = masterFile
        self.theMaster  = Parser(masterFile)
        
        return
    
    def buildTree(self, metaOnly=False):
        
        self.parseMaster()
        
        if len(self.cmdStack) == 0:
            mn.OUT.errMsg("Master file appears to be empty.")
            return False
        
        if not self.cmdStack[0]["command"] == "@master":
            mn.OUT.errMsg("The file does not appear to be a master file.")
            return False
        
        for theCmd in self.cmdStack:
            print("'{command}' '{target}' '{data}' '{type}'".format(**theCmd))
            if theCmd["command"] == "@add":
                if theCmd["target"] == "character":
                    newCharacter = self.validData(theCmd,Parser.TYP_STR)
                    mn.OUT.infMsg(" > Added character: %s" % newCharacter)
            elif theCmd["command"] == "@set":
                if theCmd["target"] == "book.title":
                    self.bookTitle = self.validData(theCmd,Parser.TYP_STR)
                    mn.OUT.infMsg(" > Book title set to: %s" % self.bookTitle)
                elif theCmd["target"] == "book.author":
                    newAuthor = self.validData(theCmd,Parser.TYP_STR)
                    self.bookAuthor.append(newAuthor)
                    mn.OUT.infMsg(" > Added author: %s" % newAuthor)
                elif theCmd["target"] == "book.status":
                    self.bookStatus = self.validData(theCmd,Parser.TYP_STR)
                    mn.OUT.infMsg(" > Book status set to: %s" % self.bookStatus)
        
        return
        
    def parseMaster(self):
        
        for rawIndex in range(self.theMaster.getLines()):
            lineType = self.theMaster.getType(rawIndex)
            
            if lineType == Parser.LN_CMD:
                cmdData = self.theMaster.splitCommand(rawIndex)
                self.cmdStack.append(cmdData)
            elif lineType == Parser.LN_TEXT:
                mn.OUT.wrnMsg("Text entry encountered in master file.")
        
        return
    
    def validData(self,theCmd,theType):
        if theCmd["type"] == theType:
            return theCmd["data"]
            
        mn.OUT.errMsg("Wrong data type %s for book.title, expected %s on line %d in file: %s" % (
            Parser.REV_TYPE[theCmd["type"]],
            Parser.REV_TYPE[theType],
            theCmd["line"],
            self.theMaster.inFile
        ))
        return ""

# End Class Book
