from . import output

title = 'Output'
location = 'bottom'

def addPlugin(parent):
    plugin = output.Output(parent)
    parent.Events.editorTabChanged.connect(plugin.editorTabChanged)
    parent.Events.editorTabClosed.connect(plugin.editorTabClosed)
    parent.Events.close.connect(plugin.killAll)
##    plugin.title = 'Output'
##    plugin.location = 'bottom'
    return plugin