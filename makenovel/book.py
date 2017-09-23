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

from os import path

logger = logging.getLogger(path.basename(__file__))

class Book():
    
    def __init__(self):
        
        self.bookTitle    = ""
        self.bookSubTitle = ""
        self.bookAuthor   = []
        self.chapters     = {}
        self.scenes       = {}
        
        return
    
    def setTitle(self,bookTitle):
        self.bookTitle = bookTitle[0]
        logger.info("1-Book title set to '%s'" % bookTitle[0])
        logger.warn("2-Book title set to '%s'" % bookTitle[0])
        logger.input("3-Book title set to '%s'" % bookTitle[0])
        logger.build("4-Book title set to '%s'" % bookTitle[0])
        return True
        
    def addAuthor(self,bookAuthor):
        for nextAuthor in bookAuthor:
            self.bookAuthor.append(nextAuthor)
            logger.build("Added author '%s'" % nextAuthor)
        return True

# End Class Book
