import output

def addPlugin(parent):
    plugin = output.Output(parent)
    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    parent.evnt.close.connect(plugin.killAll)
    plugin.title = 'Output'
    plugin.location = 'bottom'
    return plugin