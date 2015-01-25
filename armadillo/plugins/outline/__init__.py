from . import outline

def addPlugin(parent):
    plugin = outline.Outline(parent)
    parent.evnt.editorAdded.connect(plugin.addOutline)
    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
    plugin.title = 'Outline'
    plugin.location = 'left'
    return plugin