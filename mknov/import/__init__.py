"""makeNovel Import

makeNovel – Import
==================
Import classes. One per file format.

File History:
Created:   2018-08-12 [0.1.0]

"""

import mknov as mn

from os import path

from .plain import ImportPlain

__all__ = ["ImportPlain","ImportMarkdown","ImportFODT"]

class FileImport:

    fileName = None

    def __init__(self,fileName):

        if path.isfile(fileName):
            self.fileName = fileName
        else:
            mn.OUT.errMsg("File not found: %s " % fileName)

        return

# END class FileImport
