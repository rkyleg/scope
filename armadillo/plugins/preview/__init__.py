from . import preview

def addPlugin(parent):
    plugin = preview.Preview(parent)
##    parent.evnt.editorAdded.connect(plugin.addPreview)
    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
    parent.evnt.editorSaved.connect(plugin.updatePreview)
    plugin.title = 'Preview'
    plugin.location = 'right'
    return plugin