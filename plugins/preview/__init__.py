from . import preview

title = 'Preview'
location = 'right'

def addPlugin(parent):
    plugin = preview.Preview(parent)
##    parent.Events.editorAdded.connect(plugin.addPreview)
    parent.Events.editorTabChanged.connect(plugin.editorTabChanged)
    parent.Events.editorTabClosed.connect(plugin.editorTabClosed)
    parent.Events.editorSaved.connect(plugin.updatePreview)
##    plugin.title = 'Preview'
##    plugin.location = 'right'
    return plugin