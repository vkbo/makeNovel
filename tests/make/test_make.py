"""
Unit test of make command
"""

from mknov.cmd_make import makeProject

from os import path, chdir, rmdir, unlink

chdir(path.dirname(__file__))

def test_pdf():
    cleanUp()
    assert True

# Cleanup
def cleanUp():
    pass
