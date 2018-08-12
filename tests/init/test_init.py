"""
Unit test of init command
"""

from mknov.cmd_init import initProject

from os import path, chdir, rmdir, unlink

chdir(path.dirname(__file__))

def test_empty():
    cleanUp()
    assert initProject(["-e"])
    assert not initProject(["-e"])
    # cleanUp()

# Cleanup
def cleanUp():
    pathConfig = path.join(".mknov","config")
    if path.isfile(pathConfig):
        unlink(pathConfig)

    if path.isdir(".mknov"):
        rmdir(".mknov")
