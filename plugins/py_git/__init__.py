import os
from . import py_git

title = 'Git'
location = 'bottom'


def addPlugin(parent):
    plugin = py_git.PyGit(parent)
    # parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    # parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
    # parent.evnt.close.connect(plugin.killAll)
    # plugin.title = 'Output'
    # plugin.location = 'bottom'
    # dir = os.getcwd()
    # print dir
    return plugin
