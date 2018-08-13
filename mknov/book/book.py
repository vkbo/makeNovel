# -*- coding: utf-8 -*
"""makeNovel Book Class

makeNovel – Book Class
=======================
The Book class holds all the data contained in the novel files

File History:
Created: 2018-03-15 [0.1.0]

"""

import mknov as mn

from os         import path

from .error     import ErrHandler, ErrCodes
from .parser    import Parser
from .chapter   import Chapter
from .scene     import Scene
from .character import Character

class Book():

    theParser  = None
    masterFile = None

    def __init__(self, masterFile):

        if not path.isfile(masterFile):
            mn.OUT.errMsg("File not found: %s" % masterFile)

        self.masterFile     = masterFile
        self.theMaster      = Parser(masterFile)
        self.isMaster       = False

        # Book Meta
        self.bookTitle      = ""
        self.bookAuthor     = []
        self.bookStatus     = ""

        # Book Content
        self.bookChapters   = []
        self.bookScenes     = []
        self.bookCharacters = []

        # Book Parsing Data
        self.currChapter    = None
        self.currCharacter  = None

        self.cmdStack       = []

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
            # print("'{command}' '{target}' '{data}' '{type}'".format(**theCmd))

            #
            # Master
            #
            if theCmd["command"] == "@master":
                self.isMaster = True

            #
            # ADD Command
            #
            elif theCmd["command"] == "@add":

                # Add New Character
                if theCmd["target"] == "character":
                    newID        = self.validData(theCmd,Parser.TYP_VAR)
                    newCharacter = Character(newID)
                    self.bookCharacters.append(newCharacter)
                    self.currCharacter = len(self.bookCharacters) - 1
                    mn.OUT.infMsg(" > Added character: %s" % newID)

                # Add New Chapter
                elif theCmd["target"] in Chapter.MAP_TYPE.keys():
                    newID      = self.validData(theCmd,Parser.TYP_VAR)
                    newChapter = Chapter(newID)
                    self.bookChapters.append(newChapter)
                    self.currChapter = len(self.bookChapters) - 1
                    mn.OUT.infMsg(" > Added chapter: %s" % newID)

                # Add New Scene
                elif theCmd["target"] == "scene":
                    if self.hasChapter(theCmd):
                        newFile  = self.validData(theCmd,Parser.TYP_STR)
                        newScene = Scene(newFile)
                        self.bookScenes.append(newScene)
                        newIndex = len(self.bookScenes) - 1
                        self.bookChapters[self.currChapter].addScene(newIndex)
                        mn.OUT.infMsg("   > Added scene file: \"%s\"" % newFile)

                # If Reached, Error
                else:
                    mn.OUT.errMsg("{raw}".format(**theCmd))
                    mn.OUT.errMsg("Unknown command target \"{target}\"".format(**theCmd))
                    ErrHandler.terminateExec(ErrCodes.ERR_COMMAND)

            #
            # SET Command
            #
            elif theCmd["command"] == "@set":

                # Book Meta
                if theCmd["target"] == "book.title":
                    self.bookTitle = self.validData(theCmd,Parser.TYP_STR)
                    self.setMessage("book title",0,theCmd)
                elif theCmd["target"] == "book.author":
                    newAuthor = self.validData(theCmd,Parser.TYP_STR)
                    self.bookAuthor.append(newAuthor)
                    self.setMessage("book authore",0,theCmd)
                elif theCmd["target"] == "book.status":
                    self.bookStatus = self.validData(theCmd,Parser.TYP_STR)
                    self.setMessage("book status",0,theCmd)

                # Character Meta
                elif theCmd["target"] == "character.name":
                    if self.hasCharacter(theCmd):
                        self.bookCharacters[self.currCharacter].setName(theCmd)
                        self.setMessage("character name",1,theCmd)
                elif theCmd["target"] == "character.status":
                    if self.hasCharacter(theCmd):
                        self.bookCharacters[self.currCharacter].setStatus(theCmd)
                        self.setMessage("character status",1,theCmd)
                elif theCmd["target"] == "character.importance":
                    if self.hasCharacter(theCmd):
                        self.bookCharacters[self.currCharacter].setImportance(theCmd)
                        self.setMessage("character importance",1,theCmd)

                # Chapter Meta
                elif theCmd["target"] == "chapter.title":
                    if self.hasChapter(theCmd):
                        self.bookChapters[self.currChapter].setTitle(theCmd)
                        self.setMessage("chapter title",1,theCmd)
                elif theCmd["target"] == "chapter.type":
                    if self.hasChapter(theCmd):
                        self.bookChapters[self.currChapter].setType(theCmd)
                        self.setMessage("chapter type",1,theCmd)
                elif theCmd["target"] == "chapter.numbered":
                    if self.hasChapter(theCmd):
                        self.bookChapters[self.currChapter].setNumbered(theCmd)
                        self.setMessage("chapter numbered",1,theCmd)

                # If Reached, Error
                else:
                    mn.OUT.errMsg("{raw}".format(**theCmd))
                    mn.OUT.errMsg("Unknown command target \"{target}\"".format(**theCmd))
                    ErrHandler.terminateExec(ErrCodes.ERR_COMMAND)

            #
            # Unknown Command
            #
            else:
                mn.OUT.errMsg("{raw}".format(**theCmd))
                mn.OUT.errMsg("Unknown command \"{command}\"".format(**theCmd))
                ErrHandler.terminateExec(ErrCodes.ERR_COMMAND)

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

    def setMessage(self, theTarget, theLevel, theCmd):
        sWrap = ""
        if theCmd["type"] == Parser.TYP_STR: sWrap = "\""
        mn.OUT.infMsg(" %s> Set %s to: %s%s%s" % (
            "  "*theLevel,
            theTarget,
            sWrap,
            theCmd["data"],
            sWrap
        ))
        return

    def validData(self, theCmd, theType):

        if theCmd["type"] == theType:
            return theCmd["data"]

        mn.OUT.errMsg("{raw}".format(**theCmd))
        mn.OUT.errMsg("Wrong data type for %s, expected %s, got %s in %s:%d" % (
            theCmd["target"],
            Parser.REV_TYPE[theType],
            Parser.REV_TYPE[theCmd["type"]],
            self.theMaster.inFile,
            theCmd["line"]
        ))
        ErrHandler.terminateExec(ErrCodes.ERR_DATATYPE)

        return ""

    def hasCharacter(self, theCmd):
        if self.currCharacter is None:
            mn.OUT.errMsg("{raw}".format(**theCmd))
            mn.OUT.errMsg("No character has been added yet.")
            ErrHandler.terminateExec(ErrCodes.ERR_SETBFADD)
            return False
        return True

    def hasChapter(self, theCmd):
        if self.currChapter is None:
            mn.OUT.errMsg("{raw}".format(**theCmd))
            mn.OUT.errMsg("No chapter has been added yet.")
            ErrHandler.terminateExec(ErrCodes.ERR_SETBFADD)
            return False
        return True

# End Class Book
