from . import pygit

title = 'Git'
location = 'bottom'

def addPlugin(parent):
    plugin = pygit.PyGit(parent)
    # parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    # parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
    # parent.evnt.close.connect(plugin.killAll)
##    plugin.title = 'Output'
##    plugin.location = 'bottom'
    return plugin