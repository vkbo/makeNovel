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

    def __init__(self, chTitle, chType):

        self.chapterName    = chTitle
        self.chapterType    = chType
        self.chapterCompile = True
        self.chapterNumber  = None
        self.chapterScenes  = []

        return

    def addScene(self, sceneIndex):
        self.chapterScenes.append(sceneIndex)
        return True

# End Class Chapter
