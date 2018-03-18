# -*- coding: utf-8 -*
"""makeNovel Character Class

makeNovel – Character Class
===========================
The Character class holds all the meta data for a character

File History:
Created: 2018-03-18 [0.1.0]

"""

import mknov as mn

class Character():
    
    def __init__(self, chID):
        
        self.charID         = chID
        self.charName       = ""
        self.charStatus     = ""
        self.charImportance = 0
        
        return
    
    def setName(self, theCmd):
        self.charName = theCmd["data"]
        return True
    
    def setStatus(self, theCmd):
        self.charStatus = theCmd["data"]
        return True
    
    def setImportance(self, theCmd):
        self.charImportance = theCmd["data"]
        return True
    
# End Class Character
