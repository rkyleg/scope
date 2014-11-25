import outline

def addDock(parent):
    dock = outline.Outline(parent)
    parent.evnt.editorAdded.connect(dock.addOutline)
    parent.evnt.editorTabChanged.connect(dock.editorTabChanged)
    dock.title = 'Outline'
    dock.location = 'left'
    return dock