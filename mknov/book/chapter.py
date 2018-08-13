# -*- coding: utf-8 -*
"""makeNovel Chapter Class

makeNovel – Chapter Class
=========================
The Chapter class holds all the data contained in a chapter

File History:
Created: 2018-03-18 [0.1.0]

"""

import logging
import mknov   as mn

class Chapter():

    TYP_NONE        = 0
    TYP_FRONTMATTER = 1
    TYP_PROLOGUE    = 2
    TYP_CHAPTER     = 3
    TYP_EPILOGUE    = 4
    TYP_BACKMATTER  = 5

    REV_TYPE = [
        "Not Specified",
        "Front Matter",
        "Prologue",
        "Chapter",
        "Epilogue",
        "Back Matter"
    ]

    MAP_TYPE = {
        "frontmatter" : TYP_FRONTMATTER,
        "prologue"    : TYP_PROLOGUE,
        "chapter"     : TYP_CHAPTER,
        "epilogue"    : TYP_EPILOGUE,
        "backmatter"  : TYP_BACKMATTER
    }

    def __init__(self, chID):

        self.chapterID       = chID
        self.chapterTitle    = None
        self.chapterType     = self.TYP_CHAPTER
        self.chapterNumbered = True
        self.chapterCompile  = True
        self.chapterNumber   = None
        self.chapterScenes   = []

        self.numberedSet     = False

        return

    def setTitle(self, theCmd):
        self.chapterTitle = theCmd["data"]
        return True

    def setType(self, theCmd):
        if theCmd["data"].lower() in self.MAP_TYPE.keys():
            self.chapterType = self.MAP_TYPE[theCmd["data"]]
        if self.chapterType == self.TYP_CHAPTER and not self.numberedSet:
            self.chapterNumbered = True
        return True

    def setNumbered(self, theCmd):
        self.chapterNumbered = theCmd["data"]
        self.numberedSet     = True
        return True

    def addScene(self, sceneIndex):
        self.chapterScenes.append(sceneIndex)
        return True

# End Class Chapter
